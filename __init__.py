# -*- coding: utf-8 -*-

""" THIS COMMENT MUST NOT REMAIN INTACT

GNU GENERAL PUBLIC LICENSE

Copyright (c) 2015 geometalab HSR

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

"""


def name():
    return "vtr"


def description():
    return "reades vector tiles"


def version():
    return "Version 0.0.5"


def qgisMinimumVersion():
    return "2.12"


def qgisMinimumVersion():
    return "2.14"


def classFactory(iface):
    from vtr_plugin import Plugin
    return Plugin(iface)
