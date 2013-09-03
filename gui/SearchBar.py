
from PySide import QtCore, QtGui, QtWebKit
from attribute_getters import *
from link_creator import *
from gui.SearchBar_Worker import *
from multiprocessing import Pool, cpu_count


class SearchBar(QtGui.QLineEdit):

    def __init__(self, main_window, open_fcn):
        QtGui.QLineEdit.__init__(self, "", main_window)
        self.autocomplete = QtGui.QListWidget(self)
        self.worker = SearchBar_Worker()
        
        #create pool with num CPUs minus one
        self.pool_size = cpu_count() - 1
        self.pool = Pool(self.pool_size)
        
        #set the fcn to open links in the main GUI
        self.open_fcn = open_fcn
        
    #kill pool when this object is destroyed
    def __del__(self):
        self.pool.terminate()
        
    def load_name_list(self, everything):
        #need everything for tab creation
        self.everything = everything
        
        self.name_list = []
        for tag in everything.keys():
            if not tag.endswith("_names"):
                continue
                
            #this is mapping from id->name
            #so grab all the names
            for name in everything[tag].values():
                self.name_list.append(name.lower())
               
                
        self.name_list.sort()
       
        self.worker.load_name_list(self.name_list)
        
        self.load_autocomplete()
    
    def load_autocomplete(self):
        #self.l.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.autocomplete.setWindowFlags(QtCore.Qt.ToolTip)
        # | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        
        #annoyingly, list will not stay fixed to text entry
        self.autocomplete.move(self.mapToGlobal(QtCore.QPoint(0, self.height())))
        
        self.autocomplete.show()

        #set watchers
        self.textChanged.connect(self.textWatcher)
        self.autocomplete.itemDoubleClicked.connect(self.clickWatcher)

    def textWatcher(self, text):
        
        if len(text) == 0:
            self.autocomplete.hide()
            return
        
        self.autocomplete.clear()
        
        text = text.lower()
        
        #send commands to search the name array
        for i in range(0, self.pool_size):
            self.pool.apply_async(self.worker.search, args = (text, i, self.pool_size), callback = self.addItem)
        
        #move and make visible
        self.autocomplete.move(self.mapToGlobal(QtCore.QPoint(0, self.height())))
        if not self.autocomplete.isVisible():
            self.autocomplete.show()

    #actually add items to the list
    #this is a bottleneck
    #but the list can't be pickled and sent to
    #the processes, so I don't have a better idea
    def addItem(self, names_found):
        for name in names_found:
            self.autocomplete.addItem(name)
            
    #tell GUI to open page for this name
    def select(self, selected_name):
        self.autocomplete.hide()
        element_link = create_page_id(selected_name, self.everything)
        self.open_fcn(element_link, selected_name)
        
    def clickWatcher(self, item):
        self.select(item.text())
        
    def focusOutEvent(self, event):
        self.autocomplete.hide()
        
    def focusInEvent(self, event):
        self.autocomplete.hide()
        
    def keyPressEvent(self, event):
        
        key = event.key()
        if key == QtCore.Qt.Key_Up or key == QtCore.Qt.Key_Down:
            row = self.autocomplete.currentIndex().row()
            if key == QtCore.Qt.Key_Up:
                row -= 1
            elif key == QtCore.Qt.Key_Down:
                row += 1
                
            row %= self.autocomplete.model().rowCount()
            index = self.autocomplete.model().index(row, 0)
            self.autocomplete.setCurrentIndex(index)
            
        elif key == QtCore.Qt.Key_Escape:
            self.autocomplete.hide()
            
        elif key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Return:
            if self.autocomplete.currentIndex().isValid():
                selected_name = self.autocomplete.currentIndex().data()
                self.select(selected_name)
        else:
            #pass the key event through to parent
            QtGui.QLineEdit.keyPressEvent(self, event)
      
