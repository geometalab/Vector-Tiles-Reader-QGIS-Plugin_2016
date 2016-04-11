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
import Canvas

extent = 4096
geo = []  # 0: zoom, 1: easting, 2: northing


class Model:
    directory = os.path.dirname(os.path.abspath(__file__))
    _tmp = "%s/data/tmp/tmp.txt" % directory
    _tmp2 = "%s/data/tmp/tmp2.txt" % directory
    _mapzen = None
    _geo = []
    geojson_data = {
        "type": "FeatureCollection",
        "crs": {
            "type": "EPSG",
            "properties": {
                "code": 3785
            }
        },
        "features": []
    }

    def __init__(self, iface, database_source):
        self._mapzen = Mapzen()
        self._iface = iface
        self.temporary_layer = []
        self.database_source = database_source
        # self._init_connections()
        self.mbtiles()

    # def _init_connections(self):
    #     vector_layer = QgsVectorLayer()
    #     vector_layer.geometryChanged.connect(self._refresh)
    #     vector_layer.screenUpdateRequested.connect(self._refresh)
    #     QgsMapCanvas().scaleChanged.connect(self._refresh)
    #
    # def _refresh(self):
    #     scale = self.canvas.scale()
    #     coordinates = self.canvas.xyCoordinates()
    #     with open(self._tmp2, 'w') as f:
    #         f.write(scale)
    #         f.write(coordinates)
    #     self.mbtiles(scale=scale, coordinates=coordinates)

    def mbtiles(self, scale=None, coordinates=None):
        # connect to a mb_tile file and extract the data
        con = sqlite3.connect(self.database_source)
        c = con.cursor()
        c.execute("SELECT * FROM tiles WHERE zoom_level = 12;")

        for index, row in enumerate(c):
            self._geo = [row[0], row[1], row[2]]

            with open(self._tmp, 'wb') as f:
                f.write(row[3])
            with gzip.open(self._tmp, 'rb') as f:
                file_content = f.read()

            decoded_data = self.decode_file(file_content)
            self.write_features(decoded_data, self._geo)
            os.remove(self._tmp)

        json_src = self.unique_file_name

        with open(json_src, "w") as f:
            json.dump(self.geojson_data, f)

        self.load_layer(json_src)

    def decode_file(self, data):
        # read the binary data file (pbf) using the library from Mapzen
        return self._mapzen.decode(data)

    def write_features(self, decoded_data, geometry):
        for name in decoded_data:
            for index, value in enumerate(decoded_data[name]['features']):
                self.geojson_data["features"].append(
                    build_object(decoded_data[name]["features"][index], geometry)
                )
        return self.geojson_data

    def load_layer(self, json_src):
        self._iface.addVectorLayer(json_src, "a name", "ogr")

    @property
    def unique_file_name(self):
        unique_name = uuid.uuid4()
        return "%s/data/tmp/%s.geojson" % (self.directory, unique_name)


# def zoom_level():
#     scale = QgsMapCanvas().scale()
#     scale_index = [500000000, 250000000, 150000000, 70000000, 35000000, 15000000, 10000000,
#                    4000000, 2000000, 1000000, 500000, 250000, 150000, 70000, 35000]
#     index = 0
#     while index < len(scale_index) and scale < scale_index[index]:
#         index += 1
#     return index


def build_object(data, geometry):
    #  single feature structure
    feature = {
        "type": "Feature",
        "geometry": {
            "type": geometry_type(data),
            "coordinates": mercator_geometry(data["geometry"], data["type"], geometry)
        },
        "properties": data["properties"]
    }
    return feature


def geometry_type(data):
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


def mercator_geometry(coordinates, geo_type, geometry):
    # recursively iterate through all the points and create an array,
    # if it is just a point remove the outer barckets.
    tmp = []
    for index, value in enumerate(coordinates):
        if isinstance(coordinates[index][0], int):
            tmp.append(calculate_geometry(coordinates[index], geometry))
        else:
            tmp.append(mercator_geometry(coordinates[index], 0, geometry))
    if geo_type == 1:
        return tmp[0]
    return tmp


def calculate_geometry(coordinates, geometry):
    # calculate the mercator geometry using external library
    # geometry:: 0: zoom, 1: easting, 2: northing
    tmp = GlobalMercator().TileBounds(geometry[1], geometry[2], geometry[0])
    delta_x = tmp[2] - tmp[0]
    delta_y = tmp[3] - tmp[1]
    merc_easting = int(tmp[0] + delta_x / extent * coordinates[0])
    merc_northing = int(tmp[1] + delta_y / extent * coordinates[1])
    return [merc_easting, merc_northing]
