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

from ui_vtr import VtrDialog
from vtr_model import Model

from qgis.core import QgsProject
from PyQt4.QtGui import QFileDialog, QDesktopServices
from PyQt4.Qt import QApplication
from PyQt4.QtCore import QFileInfo

import os


class Dialog:

    def __init__(self, iface, project_settings):
        self.new_dialog = VtrDialog()
        self.new_dialog.setModal(True)
        self._iface = iface
        self._model = Model(self._iface)
        self._init_connections()
        self._settings = project_settings
        self._browse_open_path = self._default_directory(project_settings)

    def create_dialog(self):
        if self.new_dialog.isVisible():
            self.new_dialog.reject()
        self.new_dialog.helpLabel.setOpenExternalLinks(True)
        self.new_dialog.show()
        result = self.new_dialog.exec_()
        if result == 1:
            directory = os.path.dirname(os.path.abspath(__file__))
            self._model.mbtiles("%s/data/zurich.mbtiles" % directory)

    def _init_connections(self):
        self.new_dialog.acceptButton.clicked.connect(self.new_dialog.accept)
        self.new_dialog.rejectButton.clicked.connect(self.new_dialog.reject)
        self.new_dialog.fileBrowserButton.clicked.connect(self._browse_directory)

    def _browse_directory(self):
        vtr_file_path = QFileDialog.getOpenFileName(
            self.new_dialog,
            QApplication.translate("Dialog", "open mbtile file"),
            self._browse_open_path,
            QApplication.translate("Dialog", "Files (*.mbtiles)")
        )
        if vtr_file_path:
            self._new_default_directory(QFileInfo(vtr_file_path).path())
            self.new_dialog.filePath.setText(vtr_file_path)
        self.new_dialog.activateWindow()

    @staticmethod
    def _default_directory(settings):
        current_directory = settings.value('lastUsedFileOpenDir', '')
        if not current_directory:
            absolute_project_path = QgsProject.instance().readPath("./")
            current_directory = QDesktopServices.storageLocation(QDesktopServices.HomeLocation) \
                if absolute_project_path == "./" \
                else absolute_project_path
        return current_directory

    def _new_default_directory(self, path):
        self._settings.setValue('lastUsedFileOpenDir', path)
