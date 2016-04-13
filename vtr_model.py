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

import json
import sqlite3
import gzip
import os
import uuid

extent = 4096
geo = []  # 0: zoom, 1: easting, 2: northing


class Model:
    directory = os.path.dirname(os.path.abspath(__file__))
    _tmp = "%s/data/tmp/tmp.txt" % directory
    _tmp2 = "%s/data/tmp/tmp2.txt" % directory
    _mapzen = None
    _geo = []
    geojson_data = {"type": "FeatureCollection", "crs": {"type": "EPSG", "properties": {"code": 3785}}, "features": []}

    def __init__(self, iface, database_source):
        self._mapzen = Mapzen()
        self._iface = iface
        self.database_source = database_source
        self._canvas = iface.mapCanvas()
        self._layer = None

    def mbtiles(self, scale=None, coordinates=None):
        # connect to a mb_tile file and extract the data
        cursor = self.database_cursor
        command = self.database_command
        data = cursor.execute(command)

        for index, row in enumerate(data):
            self._geo = [row[0], row[1], row[2]]

            with open(self._tmp, 'wb') as f:
                f.write(row[3])
            with gzip.open(self._tmp, 'rb') as f:
                file_content = f.read()

            decoded_data = self._decode_file(file_content)
            self._write_features(decoded_data, self._geo)
            os.remove(self._tmp)

        json_src = self.unique_file_name

        with open(json_src, "w") as f:
            json.dump(self.geojson_data, f)

        self._load_layer(json_src)

    def _decode_file(self, data):
        # read the binary data file (pbf) using the library from Mapzen
        return self._mapzen.decode(data)

    def _write_features(self, decoded_data, geometry):
        for name in decoded_data:
            for index, value in enumerate(decoded_data[name]['features']):
                self.geojson_data["features"].append(
                    self._build_object(decoded_data[name]["features"][index], geometry)
                )
        return self.geojson_data

    def _load_layer(self, json_src):
        # load the created geojson into qgis
        self._iface.addVectorLayer(json_src, "a name", "ogr")

    @property
    def database_cursor(self):
        # connect to the database and return its corresponding cursor
        con = sqlite3.connect(self.database_source)
        return con.cursor()

    @property
    def database_command(self):
        # create a suitable sql query (TODO)
        zoom = self.current_zoom
        return "SELECT * FROM tiles WHERE zoom_level = %s LIMIT 5;" % zoom

    @property
    def unique_file_name(self):
        unique_name = uuid.uuid4()
        return "%s/data/tmp/%s.geojson" % (self.directory, unique_name)

    @property
    def current_zoom(self):
        # get the current zoom level in qgis as a string
        zoom = 12
        return zoom

    @property
    def current_coordinates(self):
        # get the current coordinates in qgis
        coordinates = [45, 8]
        return coordinates

    @property
    def calculate_tile_range(self):
        # return [min_x, min_y, max_x, max_y] of the viewable qgis display
        tmp = []
        return tmp

    def _build_object(self, data, geometry):
        #  single feature structure
        feature = {
            "type": "Feature",
            "geometry": {
                "type": self._geometry_type(data),
                "coordinates": self._mercator_geometry(data["geometry"], data["type"], geometry)
            },
            "properties": data["properties"]
        }
        return feature

    def _mercator_geometry(self, coordinates, geo_type, geometry):
        # recursively iterate through all the points and create an array,
        # if it is just a point remove the outer barckets.
        tmp = []
        for index, value in enumerate(coordinates):
            if isinstance(coordinates[index][0], int):
                tmp.append(self._calculate_geometry(coordinates[index], geometry))
            else:
                tmp.append(self._mercator_geometry(coordinates[index], 0, geometry))
        if geo_type == 1:
            return tmp[0]
        return tmp

    @staticmethod
    def _geometry_type(data):
        # get the feature type
        options = {
            1: "Point",
            2: "LineString",
            3: "Polygon",
            4: "MultiPoint",
            5: "MultiLineString",
            6: "MultiPolygon"
        }
        return options[data["type"]]

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
