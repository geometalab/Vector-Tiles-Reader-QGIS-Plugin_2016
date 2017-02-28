# -*- coding: utf-8 -*-

""" THIS COMMENT MUST NOT REMAIN INTACT

GNU GENERAL PUBLIC LICENSE

Copyright (c) 2017 geometalab HSR

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

class VtrPlugin:
    _dialog = None
    _model = None
    vtr_action = None

    def __init__(self, iface):
        # save reference to the QGIS interface
        self.iface = iface
        self.settings = QSettings("Vector Tile Reader","vectortilereader")

    def initGui(self):
        print "VTR Plugin initGui"
        vtr_layer_icon = QIcon(':/plugins/Vector-Tiles-Reader-QGIS-Plugin/icon.png')
        self.vtr_action = QAction(vtr_layer_icon, "Add Vector Tiles Layer", self.iface.mainWindow())
        self.iface.addToolBarIcon(self.vtr_action)
        self.iface.addPluginToMenu("&Vector Tiles Reader", self.vtr_action)
        self.iface.addPluginToVectorMenu("&Vector Tiles Reader", self.vtr_action)
        # self.vtr_action.triggered.connect(
        #     lambda: Dialog(self.iface, self.settings).create_dialog()
        # )

    def unload(self):
        print "VTR Plugin unload"
        # Remove the plugin menu item and icon
        self.iface.removeToolBarIcon(self.vtr_action)
        self.iface.removePluginMenu("&Vector Tiles Reader", self.vtr_action)
        self.iface.removePluginVectorMenu("&Vector Tiles Reader", self.vtr_action)
