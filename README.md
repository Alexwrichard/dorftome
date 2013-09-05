df-legends-reader
=================

A browser that allows you to view Dwarf Fortress legends exports in an efficient and fluid manner.

##Current Features
* Tabbed browsing
* Hyperlinks between elements
* Fast search
    + Currently performs a search of all elements with names (regions/sites/historical figures) with partial matching
    + This is almost instant for a 12 MB file, and takes less than 5 seconds for the 266 MB file

##Future Goals

* Keyboard-only navigation?
* Giving the user a good idea of the relationships between historical figures
    + Eventually, a graph (vertices+edges) that shows this visually
* Visually appealing
   + Clean, elegant light fonts against a dark background
   + User customizable styles
* Easy reading of Legends and connections between characters and their world

###Dependencies
* lxml
* qt4
* qtwebkit (Install this before building PySide, or else it will build successfully without QtWebKit support.)
* pyside
* python3

####Ubuntu packages
* python3-lxml
* qt4-default
* python3-pyside

####Arch packages
* python-lxml
* qt4
* qtwebkit
* python-pyside (from the Arch User Repository)
