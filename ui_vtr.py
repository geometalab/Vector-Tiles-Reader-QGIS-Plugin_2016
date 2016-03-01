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

# Form implementation generated from reading ui file 'ui_vtr.ui'
#
# Created: Wed Feb 17 14:22:35 2016
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class UserInterface(object):

    button = None

    def setup(self, VectorTilesReader):
        VectorTilesReader.setObjectName(_fromUtf8("VectorTilesReader"))
        VectorTilesReader.resize(450, 170)
        VectorTilesReader.setMaximumSize(QtCore.QSize(450, 250))
        self.verticalLayoutWidget = QtGui.QWidget(VectorTilesReader)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 411, 82))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_1 = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_1.setFont(font)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.horizontalLayout_2.addWidget(self.label_1)
        self.textEdit = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.textEdit.setMaximumSize(QtCore.QSize(275, 25))
        self.textEdit.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout_2.addWidget(self.textEdit)
        self.toolButton_1 = QtGui.QToolButton(self.verticalLayoutWidget)
        self.toolButton_1.setMaximumSize(QtCore.QSize(75, 25))
        self.toolButton_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toolButton_1.setObjectName(_fromUtf8("toolButton_1"))
        self.horizontalLayout_2.addWidget(self.toolButton_1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.textEdit_2 = QtGui.QTextEdit(self.verticalLayoutWidget)
        self.textEdit_2.setMaximumSize(QtCore.QSize(275, 25))
        self.textEdit_2.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.horizontalLayout.addWidget(self.textEdit_2)
        self.toolButton_2 = QtGui.QToolButton(self.verticalLayoutWidget)
        self.toolButton_2.setMaximumSize(QtCore.QSize(75, 25))
        self.toolButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toolButton_2.setPopupMode(QtGui.QToolButton.InstantPopup)
        self.toolButton_2.setObjectName(_fromUtf8("toolButton_2"))
        self.horizontalLayout.addWidget(self.toolButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.buttonBox = QtGui.QDialogButtonBox(VectorTilesReader)
        self.buttonBox.setGeometry(QtCore.QRect(240, 120, 176, 27))
        self.buttonBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))

        self.retranslateUi(VectorTilesReader)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VectorTilesReader.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VectorTilesReader.reject)
        QtCore.QMetaObject.connectSlotsByName(VectorTilesReader)

    def retranslateUi(self, VectorTilesReader):
        VectorTilesReader.setWindowTitle(_translate("VectorTilesReader", "Dialog", None))
        self.label_1.setText(_translate("VectorTilesReader", "local", None))
        self.toolButton_1.setText(_translate("VectorTilesReader", "browse", None))
        self.label_2.setText(_translate("VectorTilesReader", "URL", None))
        self.toolButton_2.setText(_translate("VectorTilesReader", "browse", None))