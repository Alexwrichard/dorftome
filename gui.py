# Form implementation (largely) generated from reading ui file 'dwarf.ui'
#
# Created: Sun Jul 28 18:59:29 2013
#      by: pyside-uic 0.2.14 running on PySide 1.2.0

import sys
from xml_parsing import load_dict
import page_builders
from PySide import QtCore, QtGui, QtWebKit
from random import randint

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
        self.grid_layout_2 = QtGui.QGridLayout(self.centralwidget)
        self.grid_layout = QtGui.QGridLayout()

        #Search bar
        self.search_bar = QtGui.QLineEdit(main_window)
        self.search_bar.setText("")
        self.grid_layout.addWidget(self.search_bar, 0, 0, 1, 1)

        #Tabs
        self.tab_widget = QtGui.QTabWidget(main_window)
        #self.grid_layout.addWidget(self.tab_widget, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.tab_widget, 1, 0, 1, 1)

        self.grid_layout_2.addLayout(self.grid_layout, 0, 0, 1, 1)
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

        self.open_in_new_tab('sp0000')

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

    def open_in_current_tab(self, page_link):
        try:
            page_link = page_link.toString()
        except:
            pass
        html = page_builders.dispatch_link(page_link, self.everything)
        if(page_link[:2] == "hf"):
            print(html)
        self.tab_widget.currentWidget().setHtml(html)

    def open_in_new_tab(self, page_link):
        try:
            #If it is a URL object, convert to a string first.
            page_link = page_link.toString()
        except:
            #Otherwise, it's already a string.
            pass

        next_tab = QtWebKit.QWebView(self.tab_widget)
        #Append a new QWebView to the browser array.
        #Set this page's HTML.
        next_tab.setHtml(page_builders.dispatch_link(page_link, self.everything))
        
        self.handle_webview_events(next_tab)
        self.tab_widget.addTab(next_tab, str(randint(0, 10000)))

        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setCurrentWidget(next_tab)

    def handle_webview_events(self, webview):
        #This allows me to handle the links by myself.
        webview.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        #Call this method anytime a link is clicked (for now...)
        webview.linkClicked.connect(self.open_in_current_tab)
        #web view now emits signal PySide.QtGui.QWidget.customContextMenuRequested
        webview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        webview.customContextMenuRequested.connect(self.context_menu_requested)

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

        print(self.hit_url.isEmpty())

    def connect_actions(self, main_window):
        self.action_exit.triggered.connect(QtCore.QCoreApplication.instance().quit)
        self.action_load_xml.triggered.connect(self.on_open_file_dialog)
        self.action_openinnewtab.triggered.connect(self.on_click_openinnewtab)
        self.tab_widget.tabCloseRequested.connect(self.on_close_tab)

    def on_close_tab(self, index):
        if self.tab_widget.count() == 1:
            self.open_in_current_tab('sp0000')
        else:
            self.tab_widget.removeTab(index)

    def on_click_openinnewtab(self):
        self.open_in_new_tab(self.hit_url)

    def on_open_file_dialog(self):
        self.file_dialog = QtGui.QFileDialog()
        self.file_dialog.setVisible(True)
        self.file_dialog.accepted.connect(self.xml_loaded)

    def xml_loaded(self):
        selected = self.file_dialog.selectedFiles()[0]
        self.everything = load_dict(selected)
        self.open_in_current_tab('hf6666')

app = QtGui.QApplication(sys.argv)
wid = QtGui.QMainWindow()
window = UI()
window.setupUi(wid)
wid.show()
sys.exit(app.exec_())
