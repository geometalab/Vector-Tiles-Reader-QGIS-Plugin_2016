# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file Ui_VectorTilesReader.ui
# Created with: PyQt4 UI code generator 4.4.4
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_VectorTilesReader(object):
    def setupUi(self, VectorTilesReader):
        VectorTilesReader.setObjectName("VectorTilesReader")
        VectorTilesReader.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(VectorTilesReader)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(VectorTilesReader)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), VectorTilesReader.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), VectorTilesReader.reject)
        QtCore.QMetaObject.connectSlotsByName(VectorTilesReader)

    def retranslateUi(self, VectorTilesReader):
        VectorTilesReader.setWindowTitle(QtGui.QApplication.translate("VectorTilesReader", "VectorTilesReader", None, QtGui.QApplication.UnicodeUTF8))
