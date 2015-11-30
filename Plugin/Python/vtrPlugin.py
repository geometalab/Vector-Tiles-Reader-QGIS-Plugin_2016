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

import PyQt4
import qgis

# import controller
# import model

#import os.path

# The following three lines are used for remote debugging.
# The File Path should point to your pysrc directory in the LiClipse installation folder.
#import sys;
#sys.path.append(r"C:\Program Files\Brainwy\LiClipse 2.4.0\plugins\org.python.pydev_4.4.0.201510052047\pysrc")
#import pydevd

class Plugin:
    pydevd.settrace()
    _iface = None
    _onProjectLoad = None
    
    
    def __init__(self, iface):
        self._iface = iface        
        self._pluginDir = os.path.dirname(__file__)
        self._qSettings = QSettings()

# Translator
        #locale = QSettings().value('locale/userLocale')[0:2]
        #locale_path = os.path.join(self._pluginDir,'i18n','arcgiscon_{}.qm'.format(locale))
        #if os.path.exists(locale_path):
        #    self.translator = QTranslator()
        #    self.translator.load(locale_path)
        #   if qVersion() > '4.3.3':
        #       QCoreApplication.installTranslator(self.translator)
        
        NotificationHandler.configureIface(iface)
        self._iface.projectRead.connect(self._onProjectLoad)        
        #self._updateService = EsriUpdateService.createService(iface)
        #self._updateService.finished.connect(self._updateServiceFinished)      
        
        self._newController = ArcGisConNewController(iface)
        self._refreshController = ArcGisConRefreshController(iface)
    
    def initGUI(self):
        