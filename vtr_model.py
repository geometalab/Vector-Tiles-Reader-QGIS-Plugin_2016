# -*- coding: utf-8 -*-

""" THIS COMMENT MUST NOT REMAIN INTACT

The MIT License (MIT)

Copyright (c) 2015 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

# @author Dijan Helbling

# Handling backend operations.
from qgis.core import *

from contrib.mapbox_vector_tile import Mapzen
from contrib.renderer import *

import json

easting, northing, zoom = 2144, 1434, 12
extent = 4096


class Model:

    _pbf_src = "/home/dijan/.qgis2/python/plugins/vectortilereader/data/12_2144_1434.pbf"
    _txt_src = "/home/dijan/.qgis2/python/plugins/vectortilereader/data/12_2144_1434.geojson"
    _mapzen = None

    def __init__(self, iface):
        self._mapzen = Mapzen()
        self._iface = iface

    def decode_file(self):
        with open(self._pbf_src, "rb") as f:
            data = f.read()
        decoded_data = self._mapzen.decode(data)
        self.geojson(decoded_data)

    def geojson(self, decoded_data):
        temporary_dict = write_to_geojson(decoded_data)
        with open(self._txt_src, "w") as f:
            json.dump(temporary_dict, f)

    def load_layer(self):
        layer = self._iface.addVectorLayer(self._txt_src, "test layer", "ogr")
        if not layer:
            QgsMessageLog.logMessage("Layer failed to load!")


def write_to_geojson(decoded_data):
    temporary_dict = {
        "type": "FeatureCollection",
        "crs": {
            "type": "EPSG",
            "properties": {
                "code": 3785
            }
        },
        "features": []
    }

    for name in decoded_data:
        for index, value in enumerate(decoded_data[name]['features']):
            temporary_dict["features"].append(
                build_object(decoded_data[name]["features"][index])
            )
    return temporary_dict


def build_object(data):
    feature = {
        "type": "Feature",
        "geometry": {
            "type": geometry_type(data),
            "coordinates":
                mercator_geometry(data["geometry"], data["type"])
        },
        "properties": data["properties"]
    }
    return feature


def geometry_type(data):
    options = {
        1: "Point",
        2: "LineString",
        3: "Polygon",
        4: "MultiPoint",
        5: "MultiLineString",
        6: "MultiPolygon"
    }
    return options[data["type"]]


def mercator_geometry(coordinates, type):
    tmp = []
    for index, value in enumerate(coordinates):
        if isinstance(coordinates[index][0], int):
            tmp.append(calculate_geometry(coordinates[index]))
        else:
            tmp.append(mercator_geometry(coordinates[index], 0))
    if type == 1:
        return tmp[0]
    return tmp


def calculate_geometry(coordinates):
    tmp = SphericalMercator().bbox(easting, northing, zoom)
    delta_x = tmp[2] - tmp[0]
    delta_y = tmp[3] - tmp[1]
    merc_easting = int(tmp[0] + delta_x / extent * coordinates[0])
    merc_northing = int(tmp[1] + delta_y / extent * coordinates[1])
    return [merc_easting, merc_northing]
