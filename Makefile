#/*************************************************************************************
# geocsveditor
#
# Editable CSV Vector Layer
#							 -------------------
#		begin				: 2016-01-01
#		git sha				: $Format:%H$
#		copyright			: (C) 2016 by geometalab
#		email				: geometalab@gmail.com
# *************************************************************************************/
#
#/*************************************************************************************
# *																		              *
# *    The MIT License (MIT)                                                          *
# *                                                                                   *
# *    Copyright (c) 2015                                                             *
# *                                                                                   *
# *    Permission is hereby granted, free of charge, to any person obtaining a copy   *
# *    of this software and associated documentation files (the "Software"), to deal  *
# *    in the Software without restriction, including without limitation the rights   *
# *    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      *
# *    copies of the Software, and to permit persons to whom the Software is          *
# *    furnished to do so, subject to the following conditions:                       *
# *                                                                                   *
# *    The above copyright notice and this permission notice shall be included in all *
# *    copies or substantial portions of the Software.                                *
# *                                                                                   *
# *    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     *
# *    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       *
# *    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    *
# *    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         *
# *    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  *
# *    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  *
# *    SOFTWARE.			                                                          *
# *																		              *
# *************************************************************************************/

PLUGINNAME = VectorTilesReader

PY_FILES = \
    __init__.py \
    vtr_plugin.py \
    vtr_dialog.py \
    vtr_model.py \

UI_FILES = \
    ui_vtr.py \
    
RESOURCE_FILES = resources.py

default: compile
	
compile: $(UI_FILES) $(RESOURCE_FILES)

%.py : %.qrc
	pyrcc4 -o $@  $<

%.py : %.ui
	pyuic4 -o $@ $<