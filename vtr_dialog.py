# -*- coding: utf-8 -*-

""" THIS COMMENT MUST NOT REMAIN INTACT

GNU GENERAL PUBLIC LICENSE

Copyright (c) 2015 geometalab HSR

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

"""

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
        self._init_connections()
        self._settings = project_settings
        self._browse_open_path = _default_directory(project_settings)

    def create_dialog(self):
        if self.new_dialog.isVisible():
            self.new_dialog.reject()
        self.new_dialog.helpLabel.setOpenExternalLinks(True)
        self.new_dialog.show()
        result = self.new_dialog.exec_()
        if result == 1:
            file_path = self.new_dialog.filePath.text()
            if not os.path.exists(file_path):
                #  take a default mbtile if non is selected.
                dir_path = os.path.dirname(os.path.abspath(__file__))
                file_path = "%s/data/zurich.mbtiles" % dir_path
            model = Model(self._iface, file_path)
            model.mbtiles()

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

    def _new_default_directory(self, path):
        self._settings.setValue('lastUsedFileOpenDir', path)


def _default_directory(settings):
    current_directory = settings.value('lastUsedFileOpenDir', '')
    if not current_directory:
        absolute_project_path = QgsProject.instance().readPath("./")
        current_directory = QDesktopServices.storageLocation(QDesktopServices.HomeLocation) \
            if absolute_project_path == "./" \
            else absolute_project_path
    return current_directory
