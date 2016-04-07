# -*- coding: utf-8 -*-

""" THIS COMMENT MUST NOT REMAIN INTACT

GNU GENERAL PUBLIC LICENSE

Copyright (c) 2015 geometalab HSR

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""

# @author Dijan Helbling

# Handling backend operations.
from qgis.core import *

from contrib.mapbox_vector_tile import Mapzen
from contrib.globalmaptiles import *

import json, sqlite3, gzip, os

extent = 4096
geo = []  # 0: zoom, 1: easting, 2: northing


class Model:
    directory = os.path.dirname(os.path.abspath(__file__))
    _json_src = "%s/data/test.geojson" % directory
    _tmp = "%s/data/tmp.txt" % directory
    _mapzen = None
    _geo = [13, 408, 5458]  # if no geometry is given.

    def __init__(self, iface):
        self._mapzen = Mapzen()
        self._iface = iface

    def mbtiles(self, database_source):
        # connect to a mb_tile file and extract the data
        con = sqlite3.connect(database_source)
        c = con.cursor()
        c.execute("SELECT * FROM tiles WHERE zoom_level = 14 LIMIT 1;")

        for index, row in enumerate(c):
            self._geo = [row[0], row[1], row[2]]
            with open(self._tmp, 'wb') as f:
                f.write(row[3])
            with gzip.open(self._tmp, 'rb') as f:
                file_content = f.read()
            self.decode_file(file_content)

    def decode_file(self, data):
        # read the binary data file (pbf) using the library from Mapzen
        decoded_data = self._mapzen.decode(data)
        with open (self._tmp, 'w') as f:
            json.dump(decoded_data, f)
        self.geojson(decoded_data)

    def geojson(self, decoded_data):
        # convert the extracted pbf to a standard geojson
        temporary_dict = write_to_geojson(decoded_data, self._geo)
        with open(self._json_src, "w") as f:
            json.dump(temporary_dict, f)
        self.load_layer()

    def load_layer(self):
        layer_name = "{}_{}_{}".format(self._geo[0], self._geo[2], self._geo[1])
        self._iface.addVectorLayer(self._json_src, layer_name, "ogr")


def write_to_geojson(decoded_data, geometry):
    # given  geojson structure, add Feature step by step
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
                build_object(decoded_data[name]["features"][index], geometry)
            )
    return temporary_dict


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


def mercator_geometry(coordinates, type, geometry):
    # recursively iterate through all the points and create an array,
    # if it is just a point remove the outer barckets.
    tmp = []
    for index, value in enumerate(coordinates):
        if isinstance(coordinates[index][0], int):
            tmp.append(calculate_geometry(coordinates[index], geometry))
        else:
            tmp.append(mercator_geometry(coordinates[index], 0, geometry))
    if type == 1:
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
