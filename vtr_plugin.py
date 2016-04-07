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

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os

from vtr_dialog import Dialog
from vtr_dialog import Model


class Plugin:
    _dialog = None
    _model = None
    vtr_action = None

    def __init__(self, iface):
        self._iface = iface
        self._model = Model(iface)
        self.settings = QSettings("Vector Tile Reader","vectortilereader")

    def initGui(self):
        vtr_layer_icon = QIcon(':/plugins/vectortilereader/icon.png')
        self.vtr_action = QAction(vtr_layer_icon, "Vector Tile Reader", self._iface.mainWindow())
        self._iface.addToolBarIcon(self.vtr_action)
        self._iface.addPluginToMenu("&Vector Tile Reader", self.vtr_action)
        self._iface.addPluginToVectorMenu("&Vector Tile Reader", self.vtr_action)
        self.vtr_action.triggered.connect(
            lambda: Dialog(self._iface, self.settings).create_dialog())

    def unload(self):
        # Remove the plugin menu item and icon
        self._iface.removeToolBarIcon(self.vtr_action)
        self._iface.removePluginMenu("&Vector Tile Reader", self.vtr_action)
        self._iface.removePluginVectorMenu("&Vector Tile Reader", self.vtr_action)

    def run(self):
        # show the _dialog
        self._dialog.show()
        result = self._dialog.exec_()
        if result == 1:
            directory = os.path.dirname(os.path.abspath(__file__))
            self._model.mbtiles("%s/data/zurich.mbtiles" % directory)