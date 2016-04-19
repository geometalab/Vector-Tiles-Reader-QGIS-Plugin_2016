# Vector Tiles Reader QGIS-Plugin

This Python plugin reads Mapbox Vector Tiles (MVT) from a local MBTiles file and loads them into a vector layer that is rendered by QGIS and it's (default) styling.

_>> This is Work in Progress! Expected release as experimental QGIS plugin April/May 2016 <<_

For more information about the Vector Tiles concept and limitations of the plugin see homepage.

Important web links:
* __Homepage__       : http://giswiki.hsr.ch/Vector_Tiles_Reader_QGIS_Plugin
* Issues tracker : https://github.com/geometalab/Vector-Tiles-Reader-QGIS-Plugin/issues
* Code repository: https://github.com/geometalab/Vector-Tiles-Reader-QGIS-Plugin (this webpage)

## License

The Vector Tile Reader plugin is released under the GNU license (see LICENSE)

## Contributors

Vector Tile Reader has been developed by

* Dijan Helbling (first implementation, initial releases)

Acknowledgments:

* Stefan Keller
* Carmelo Schumacher
* Nicola Jordan
* Raphael Das Gupta

## Technical documentation

Name conventions for Vector Tiles Reader QGIS Plugin:

* Official full name : "Vector Tiles Reader" or "Vector Tiles Reader QGIS Plugin"
* Camel Case no space: VectorTilesReader
* Lower Case no space: vector_tiles_reader
* Abbreviated name   : vtr

### Development

How this plugin was developed so far:

* Linux Version??? 
* PyCharm Version??? 
* QGIS Version 2.14???

How this plugin was tested so far

1. Update code in local Plugins directory
2. Start QGIS
3. In plugin, load "zuerich.mbtiles"
4. (goto 1)

NOTE: Better future developing and testing would be with debugger and unit tests... 

### API design
![](data/doc/API.png?raw=true)
