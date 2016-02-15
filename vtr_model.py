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

from .contrib.vtr_encoder import VectorTile
from .contrib.vtr_decoder import TileData

# from vtr_dialog import Dialog


class Model:

    _extents = None
    vector_tile = None
    _input = None

    def __init__(self, iface):
        self.iface = iface
        _extents = 4096

    @property
    def vector_data(self):
        return self._input

    @vector_data.setter
    def vector_data(self, vector):
        self._input = vector
        print self.decode(vector)

    def decode(self, tile):
        self.vector_tile = TileData()
        message = self.vector_tile.getMessage(tile)
        return message

    def encode(self, layers):
        self.vector_tile = VectorTile(self._extents)
        if isinstance(layers, list):
            for layer in layers:
                self.vector_tile.addFeatures(layer['features'], layer['name'])
        else:
            self.vector_tile.addFeatures(layers['features'], layers['name'])

        return self.vector_tile.tile.SerializeToString()

