# -*- coding: utf-8 -*-

""" THIS COMMENT MUST NOT REMAIN INTACT

GNU GENERAL PUBLIC LICENSE

Copyright (c) 2015 geometalab HSR

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

"""

from contrib.mapbox_vector_tile import Mapzen
from contrib.globalmaptiles import *

from qgis.core import *

import json
import sqlite3
import gzip
import os
import uuid

extent = 4096


class Model:
    directory = os.path.dirname(os.path.abspath(__file__))
    _tmp = "%s/data/tmp/tmp.txt" % directory
    _tmp2 = "%s/data/tmp/tmp2.txt" % directory
    _geo = []  # 0: zoom, 1: easting, 2: northing
    _geo_type_options = {1: "Point", 2: "LineString", 3: "Polygon"}
    _json_data = {"Point": {}, "LineString": {}, "Polygon": {}}

    def __init__(self, iface, database_source):
        self._iface = iface
        self.database_source = database_source
        self._canvas = iface.mapCanvas()
        self._layer = None
        self._mbtile_id = "name"
        self._counter = 0
        self._bool = True

    def mbtiles(self):
        # connect to a mb_tile file and extract the data
        self._set_metadata()
        self._create_layer()
        cursor = self.database_cursor
        command = self.database_command()

        for sql_query in command:
            data = cursor.execute(sql_query)
            for index, row in enumerate(data):
                if not row:
                    break  # Maybe the tile did not exist in the database.
                self._geo = [row[0], row[1], row[2]]

                with open(self._tmp, 'wb') as f:
                    f.write(row[3])
                with gzip.open(self._tmp, 'rb') as f:
                    file_content = f.read()

                # decode the file using Mapzen's decode library
                decoded_data = Mapzen().decode(file_content)
                self._write_features(decoded_data, self._geo)
                os.remove(self._tmp)

        for value in self._geo_type_options:
            file_src = self.unique_file_name
            with open(file_src, "w") as f:
                json.dump(self._json_data[self._geo_type_options[value]], f)
            self._load_layer(file_src)

    def _create_layer(self):
        for value in self._geo_type_options:
            self._json_data[self._geo_type_options[value]] = {"type": "FeatureCollection", "crs":
                {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::3857"}}, "features": []}

    def _write_features(self, decoded_data, geometry):
        for name in decoded_data:
            for index, value in enumerate(decoded_data[name]['features']):
                data, geo_type = self._build_object(decoded_data[name]["features"][index], geometry)
                if data:
                    self._json_data[geo_type]["features"].append(data)

    def _load_layer(self, json_src):
        # load the created geojson into qgis
        name = self._mbtile_id
        layer = QgsVectorLayer(json_src, name, "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(layer)

    def database_command(self):
        # create a suitable sql query (TODO)
        zoom = self.current_zoom
        coordinates = self.current_coordinates
        tiles = self.calculate_tile_range(coordinates, zoom)
        commands = []
        delta_x = tiles[2] - tiles[0]
        delta_y = tiles[3] - tiles[1]
        x_index, y_index = 0, 0
        while x_index <= delta_x:
            while y_index <= delta_y:
                commands.append(
                   "SELECT * FROM tiles WHERE zoom_level=%s and tile_column=%s and tile_row=%s;"
                   % (zoom, tiles[0] + y_index, tiles[1] + x_index)
                )
                y_index += 1
            x_index += 1
            y_index = 0
        return commands

    def _set_metadata(self):
        cursor = self.database_cursor
        cursor.execute("SELECT * FROM metadata WHERE name='id'")
        self._mbtile_id = cursor.fetchone()[1]

    @property
    def database_cursor(self):
        # connect to the database and return its corresponding cursor
        con = sqlite3.connect(self.database_source)
        return con.cursor()

    @property
    def unique_file_name(self):
        unique_name = uuid.uuid4()
        return "%s/data/tmp/%s.geojson" % (self.directory, unique_name)

    @property
    def current_zoom(self):
        # get the current zoom level in qgis as a string
        scale = self._canvas.scale()
        zoom_index = [591657528, 295828764, 147914382, 73957191, 36978595, 18489298, 9244649, 4622324,
                      2311162, 1155581, 577791, 288895, 144448, 72224, 36112]
        for index, value in enumerate(zoom_index):
            if value < scale:
                return index - 1
        return 14  # if the zoom level extends 14, return a default value of 14

    @property
    def current_coordinates(self):
        # get the current mercator coordinates in qgis
        rectangle = self._canvas.extent()
        x_min = int(rectangle.xMinimum())
        y_min = int(rectangle.yMinimum())
        x_max = int(rectangle.xMaximum())
        y_max = int(rectangle.yMaximum())
        return [x_min, y_min, x_max, y_max]

    @staticmethod
    def calculate_tile_range(coordinates, zoom):
        # return tiles of the displayed map canvas
        # add the an additional tile around it.
        tx_min, ty_min = GlobalMercator().MetersToTile(coordinates[0], coordinates[1], zoom)
        tx_max, ty_max = GlobalMercator().MetersToTile(coordinates[2], coordinates[3], zoom)
        return [tx_min - 1, ty_min - 1, tx_max + 1, ty_max + 1]

    def _build_object(self, data, geometry):
        #  single feature structure
        geo_type = self._geo_type_options[data["type"]]
        coordinates = self._mercator_geometry(data["geometry"], geometry, 0)
        if data["type"] == 2 and self._counter > 0:
            # if there it is a MultiLineString, the counter will be greater than zero. return None
            self._counter = 0
            self._bool = True
            return None, geo_type
        if data["type"] == 1:
            # Due to mercator_geometrys nature, the point will be displayed in a List "[[]]", remove the outer bracket.
            coordinates = coordinates[0]
        if data["type"] == 3 and self._counter == 0:
            # If there is not a polygon in a polygon, one bracket will be missing.
            coordinates = [coordinates]
        feature = {
            "type": "Feature",
            "geometry": {
                "type": geo_type,
                "coordinates": coordinates
            },
            "properties": data["properties"]
        }
        self._counter = 0
        self._bool = True
        return feature, geo_type

    def _mercator_geometry(self, coordinates, geometry, counter):
        # recursively iterate through all the points and create an array,
        tmp = []

        for index, value in enumerate(coordinates):
            if isinstance(coordinates[index][0], int):
                tmp.append(self._calculate_geometry(coordinates[index], geometry))
            else:
                tmp.append(self._mercator_geometry(coordinates[index], geometry, counter + 1))
        if self._bool:
            self._counter = counter
            self._bool = False
        return tmp

    @staticmethod
    def _calculate_geometry(coordinates, geometry):
        # calculate the mercator geometry using external library
        # geometry:: 0: zoom, 1: easting, 2: northing
        tmp = GlobalMercator().TileBounds(geometry[1], geometry[2], geometry[0])
        delta_x = tmp[2] - tmp[0]
        delta_y = tmp[3] - tmp[1]
        merc_easting = int(tmp[0] + delta_x / extent * coordinates[0])
        merc_northing = int(tmp[1] + delta_y / extent * coordinates[1])
        return [merc_easting, merc_northing]
