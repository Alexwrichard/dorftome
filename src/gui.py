# Form implementation (largely) generated from reading ui file 'dwarf.ui'
#
# Created: Sun Jul 28 18:59:29 2013
#      by: pyside-uic 0.2.14 running on PySide 1.2.0

import sys, os
from link_creator import get_name_from_page_id
import page_builders
import xml_parsing
from global_vars import *
from PySide import QtCore, QtGui, QtWebKit
from random import randint

from gui.SearchBar import SearchBar

class UI(object):
    def setupUi(self, main_window):
        #Dictionary has not been loaded yet.
        self.everything = None

        #Main window creation
        main_window.resize(800, 600)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)

        #Central widget that contains all other widgets
        self.centralwidget = QtGui.QWidget(main_window)

        #Layout setup
        self.wrapper_layout = QtGui.QGridLayout(self.centralwidget)
        self.main_layout = QtGui.QGridLayout()
        self.search_bar_layout = QtGui.QGridLayout()
        
        #Back and forward buttons
        back_button_pixmap = QtGui.QPixmap(os.path.join(RESOURCES_DIR, 'arrow_left.png'))
        forward_button_pixmap = QtGui.QPixmap(os.path.join(RESOURCES_DIR, 'arrow_right.png'))
        back_button_icon = QtGui.QIcon(back_button_pixmap)
        forward_button_icon = QtGui.QIcon(forward_button_pixmap)
        
        self.back_button = QtGui.QPushButton(main_window)
        self.forward_button = QtGui.QPushButton(main_window)
        self.back_button.setIcon(back_button_icon)
        self.forward_button.setIcon(forward_button_icon)
        self.back_button.setIconSize(QtCore.QSize(20, 20))
        self.forward_button.setIconSize(QtCore.QSize(20, 20))
        
        self.search_bar_layout.addWidget(self.back_button, 0, 0, 1, 1)
        self.search_bar_layout.addWidget(self.forward_button, 0, 1, 1, 1)
        #page_history will be a list of (int, list)s, where the tuple index
        #corresponds to the tab index (each tab has its own history), and the
        #int in the tuple is the current pointer in the history array for that tab.
        self.page_history = []

        #Search bar
        self.search_bar = SearchBar(main_window, self.open_in_new_tab)
        self.search_bar_layout.addWidget(self.search_bar, 0, 2, 1, 1)

        #Tabs
        self.tab_widget = QtGui.QTabWidget(main_window)
        self.main_layout.addLayout(self.search_bar_layout, 0, 0, 1, 1)
        self.main_layout.addWidget(self.tab_widget, 1, 0, 1, 1)

        self.wrapper_layout.addLayout(self.main_layout, 0, 0, 1, 1)
        main_window.setCentralWidget(self.centralwidget)

        #Menu bar
        self.menubar = QtGui.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 634, 19))
        self.menu_file = QtGui.QMenu(self.menubar)
        self.menuAbout = QtGui.QMenu(self.menubar)
        main_window.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

        #Actions
        self.action_help = QtGui.QAction(main_window)
        self.action_load_xml = QtGui.QAction(main_window)
        self.action_exit = QtGui.QAction(main_window)

        #Menu items
        self.menu_file.addAction(self.action_load_xml)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        #Right click context menu
        self.action_openinnewtab = QtGui.QAction(main_window)

        self.open_in_new_tab('spl0000', "Splash")

        self.set_titles(main_window)
        self.connect_actions(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
    
    def set_titles(self, main_window):
        main_window.setWindowTitle("Dwarf Fortress Legends Reader")
        self.menu_file.setTitle("File")
        self.menuAbout.setTitle("About")
        self.action_help.setText("Help")
        self.action_load_xml.setText("Load XML...")
        self.action_exit.setText("Exit")
        self.action_openinnewtab.setText("Open in new tab")

    def open_in_current_tab_with_history(self, page_link, tab_name = None):
        try:
            page_link = page_link.toString()
        except:
            pass
        #Append the page to the page history
        current_index = self.tab_widget.currentIndex()
        historytuple = self.page_history[current_index]
        #slice off the page history list according to the history pointer, advance the pointer,
        #and add the new page link to the history list.
        new_history_list = historytuple[1][:historytuple[0] + 1]
        new_history_list.append(page_link)
        self.page_history[current_index]=(historytuple[0] + 1, new_history_list)
        self.open_in_current_tab(page_link, tab_name)

    def open_in_current_tab(self, page_link, tab_name = None):
        try:
            page_link = page_link.toString()
        except:
            pass
        html = page_builders.dispatch_link(page_link, self.everything)
        self.tab_widget.currentWidget().setHtml(html)
        
        if tab_name == None:
            tab_name = get_name_from_page_id(page_link, self.everything)
        self.tab_widget.setTabText(self.tab_widget.currentIndex(), tab_name)

    def open_in_new_tab(self, page_link, tab_name):
        try:
            #If it is a URL object, convert to a string first.
            page_link = page_link.toString()
        except:
            #Otherwise, it's already a string.
            pass

        next_tab = QtWebKit.QWebView(self.tab_widget)
        self.handle_webview_events(next_tab)
        #Append a new QWebView to the browser array.
        #Set this page's HTML.
        next_tab.setHtml(page_builders.dispatch_link(page_link, self.everything))
        self.page_history.append((0,[page_link]))
        
        self.tab_widget.addTab(next_tab, tab_name)

        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setCurrentWidget(next_tab)

    def handle_webview_events(self, webview):
        #This allows me to handle the links by myself.
        webview.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        #Call this method anytime a link is clicked (for now...)
        webview.linkClicked.connect(self.open_in_current_tab_with_history)
        #Web view now emits signal PySide.QtGui.QWidget.customContextMenuRequested
        webview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        webview.customContextMenuRequested.connect(self.context_menu_requested)
        websettings = webview.settings()

    #This gets called when the user right-clicks on the web view. A QPoint is passed, which represents
    #the location of the mouse click. We then test the page to see what is at that click location.
    def context_menu_requested(self, pos):
        hit_test = self.tab_widget.currentWidget().page().mainFrame().hitTestContent(pos)
        self.hit_url = hit_test.linkUrl()

        global_pos = self.tab_widget.currentWidget().mapToGlobal(pos)

        self.right_click_menu = QtGui.QMenu(self.tab_widget.currentWidget())
        if not self.hit_url.isEmpty():
            self.right_click_menu.addAction(self.action_openinnewtab)
        self.right_click_menu.popup(global_pos) 

    def connect_actions(self, main_window):
        self.action_exit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.action_load_xml.triggered.connect(self.on_open_file_dialog)
        self.action_openinnewtab.triggered.connect(self.on_click_openinnewtab)
        self.tab_widget.tabCloseRequested.connect(self.on_close_tab)
        self.back_button.pressed.connect(self.on_click_backbutton)
        self.forward_button.pressed.connect(self.on_click_forwardbutton)

    def on_close_tab(self, index):
        self.page_history.pop(self.tab_widget.currentIndex())
        if self.tab_widget.count() == 1:
            self.open_in_current_tab('spl0000', 'Splash')
        else:
            self.tab_widget.removeTab(index)

    def on_click_openinnewtab(self):
        tab_name = get_name_from_page_id(self.hit_url.toString(), self.everything)
        self.open_in_new_tab(self.hit_url, tab_name)
        
    def on_click_backbutton(self):
        current_tuple = self.page_history[self.tab_widget.currentIndex()]
        new_pointer_val = current_tuple[0] - 1
        newtuple = (new_pointer_val, current_tuple[1])
        if(newtuple[0] >= 0):
            self.page_history[self.tab_widget.currentIndex()] = newtuple
            self.open_in_current_tab(newtuple[1][newtuple[0]])
            
    def on_click_forwardbutton(self):
        current_tuple = self.page_history[self.tab_widget.currentIndex()]
        new_pointer_val = current_tuple[0] + 1
        newtuple = (new_pointer_val, current_tuple[1])
        if(newtuple[0] < len(current_tuple[1])):
            self.page_history[self.tab_widget.currentIndex()] = newtuple
            self.open_in_current_tab(newtuple[1][newtuple[0]])

    def on_open_file_dialog(self):
        self.file_dialog = QtGui.QFileDialog()
        self.file_dialog.setVisible(True)
        self.file_dialog.accepted.connect(self.xml_loaded)

    def xml_loaded(self):
        self.page_history = []
        selected = self.file_dialog.selectedFiles()[0]
        
        try:
            self.everything = xml_parsing.load_dict(selected)
        except Exception as e:
            self.everything = None
            
        if self.everything == None:
            new_selected = xml_parsing.handle_invalid_file(selected)
            self.everything = xml_parsing.load_dict(new_selected)
            
        self.page_history.append((-1,[]))
        self.open_in_current_tab_with_history('hif6666')
        self.search_bar.load_name_list(self.everything)

app = QtGui.QApplication(sys.argv)
wid = QtGui.QMainWindow()
window = UI()
window.setupUi(wid)
wid.show()
sys.exit(app.exec_())
