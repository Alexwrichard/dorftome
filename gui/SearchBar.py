
from PySide import QtCore, QtGui, QtWebKit
from attribute_getters import *

class SearchBar(QtGui.QLineEdit):
    def __init__(self, main_window):
        QtGui.QLineEdit.__init__(self, "", main_window)
        self.autocomplete = QtGui.QListWidget(self)
        
    def load_name_list(self, everything):
        self.name_list = []
        for hf in everything['historical_figures']:
            name = get_name(hf['id'], 'historical_figures', everything)
            self.name_list.append(name.lower())
        self.name_list.sort()
        
        self.load_autocomplete()
            
    def load_autocomplete(self):
        #self.l.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)
        self.autocomplete.setWindowFlags(QtCore.Qt.ToolTip)
        # | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.autocomplete.move(self.mapToGlobal(QtCore.QPoint(0, self.height())))
        
        self.autocomplete.show()
        #completer = QtGui.QCompleter(self.name_list);
        #completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive);
        #completer.activated.connect(self.activated)
       # self.setCompleter(completer)
        
        #self.lis = 
        self.textChanged.connect(self.textWatcher)
        #self.returnPressed.connect(self.enterWatcher)
        
    #def activated(self, text):
    #    print("Hello " + text)
        
    def textWatcher(self, text):
        if len(text) == 0:
            self.autocomplete.hide()
            return
            
        self.autocomplete.move(self.mapToGlobal(QtCore.QPoint(0, self.height())))
        if not self.autocomplete.isVisible():
            self.autocomplete.show()
            
        text = text.lower()
        
        while self.autocomplete.count() > 0:
            self.autocomplete.takeItem(0)
 
        for name in self.name_list:
           if text in name:
                self.autocomplete.addItem(name)
        
    def enterWatcher(self):
        print(self.text())
        
    def focusOutEvent(self, event):
        self.autocomplete.hide()
        
    def focusInEvent(self, event):
        self.autocomplete.hide()
