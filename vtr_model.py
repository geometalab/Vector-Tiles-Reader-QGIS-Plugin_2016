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

from qgis.gui import *
from qgis.core import *
import qgis.utils
from qgis import *

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

    def mbtiles(self, scale=None, coordinates=None):
        # connect to a mb_tile file and extract the data
        cursor = self.database_cursor
        command = self.database_command
        data = cursor.execute(command)
        self._create_layer()

        for index, row in enumerate(data):
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
                self._json_data[geo_type]["features"].append(data)

    def _load_layer(self, json_src):
        # load the created geojson into qgis
        layer = QgsVectorLayer(json_src, "a name", "ogr")
        QgsMapLayerRegistry.instance().addMapLayer(layer)
        scale = self._canvas.scale()

    def _refresh(self):
        QgsMessageLog.logMessage("refresh")

    @property
    def database_cursor(self):
        # connect to the database and return its corresponding cursor
        con = sqlite3.connect(self.database_source)
        return con.cursor()

    @property
    def database_command(self):
        # create a suitable sql query (TODO)
        zoom = self.current_zoom
        coordinates = self.current_coordinates
        tiles = self.calculate_tile_range(coordinates)
        return "SELECT * FROM tiles WHERE zoom_level = %s limit 5;" % zoom

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

    def calculate_tile_range(self, coordinates):
        # return [min_x, min_y, max_x, max_y] of the viewable qgis display
        tmp = []
        return tmp

    def _build_object(self, data, geometry):
        #  single feature structure
        geo_type = self._geo_type_options[data["type"]]
        feature = {
            "type": "Feature",
            "geometry": {
                "type": geo_type,
                "coordinates": self._mercator_geometry(data["geometry"], data["type"], geometry)
            },
            "properties": data["properties"]
        }
        return feature, geo_type

    def _mercator_geometry(self, coordinates, geo_type, geometry):
        # recursively iterate through all the points and create an array,
        tmp = []
        for index, value in enumerate(coordinates):
            if isinstance(coordinates[index][0], int):
                tmp.append(self._calculate_geometry(coordinates[index], geometry))
            else:
                tmp.append(self._mercator_geometry(coordinates[index], 0, geometry))
        if geo_type == 1:  # point remove the outer barcket.
            return tmp[0]
        if geo_type == 3:  # polygon an additional bracket.
            return [tmp]
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
