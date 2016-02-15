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

from PyQt4 import QtCore, QtGui


class UserInterface(object):

    button = None

    def setup(self, vectortilesreader):
        vectortilesreader.setObjectName("VectorTilesReader")
        vectortilesreader.resize(400, 300)
        
        self.button = QtGui.QDialogButtonBox(vectortilesreader)
        self.button.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.button.setOrientation(QtCore.Qt.Horizontal)
        self.button.setStandardButtons(QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok)
        self.button.setObjectName("buttonBox")

        self.retranslate(self, vectortilesreader)
        QtCore.QObject.connect(self.button, QtCore.SIGNAL("accepted()"), vectortilesreader.accept)
        QtCore.QObject.connect(self.button, QtCore.SIGNAL("rejected()"), vectortilesreader.reject)
        QtCore.QMetaObject.connectSlotsByName(vectortilesreader)

    @staticmethod
    def retranslate(self, vectortilesreader):
        vectortilesreader.setWindowTitle(QtGui.QApplication.translate("VectorTilesReader",
                                                                      "VectorTilesReader",
                                                                      None, QtGui.QApplication.UnicodeUTF8))

