# -*- coding: utf-8 -*-

""" THIS COMMENT MUST NOT REMAIN INTACT

GNU GENERAL PUBLIC LICENSE

Copyright (c) 2015 geometalab HSR

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

"""

import os

from PyQt4 import QtGui, uic

FORM_CLASS_NEW, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_vtr.ui'))


class VtrDialog(QtGui.QDialog, FORM_CLASS_NEW):
    def __init__(self, parent=None):
        super(VtrDialog, self).__init__(parent)
        self.setupUi(self)
