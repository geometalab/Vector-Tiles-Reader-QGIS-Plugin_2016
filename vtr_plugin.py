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