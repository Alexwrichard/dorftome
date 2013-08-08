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
        main_window.setObjectName("main_window")
        main_window.resize(800, 600)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_window.sizePolicy().hasHeightForWidth())
        main_window.setSizePolicy(sizePolicy)

        #Central widget that contains all other widgets
        self.centralwidget = QtGui.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget") #I honestly have no idea what this means.

        #Layout setup
        self.grid_layout_2 = QtGui.QGridLayout(self.centralwidget)
        self.grid_layout_2.setObjectName("gridLayout_2")
        self.grid_layout = QtGui.QGridLayout()
        self.grid_layout.setObjectName("gridLayout")

        #Search bar
        self.search_bar = QtGui.QLineEdit(main_window)
        self.search_bar.setText("")
        self.search_bar.setObjectName("lineEdit")
        self.grid_layout.addWidget(self.search_bar, 0, 0, 1, 1)

        #Tabs
        self.tab_widget = QtGui.QTabWidget(main_window)
        #self.grid_layout.addWidget(self.tab_widget, 2, 0, 1, 1)
        self.grid_layout.addWidget(self.tab_widget, 1, 0, 1, 1)

        #Browser
        self.tab_count = 0
        self.browsers = [] #An array of browsers. So we can use tabbed browsing.
        self.browsers.append(QtWebKit.QWebView(main_window))
        self.browsers[0].setObjectName("textBrowser")

        self.grid_layout_2.addLayout(self.grid_layout, 0, 0, 1, 1)
        main_window.setCentralWidget(self.centralwidget)

        #Menu bar
        self.menubar = QtGui.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 634, 19))
        self.menubar.setObjectName("menubar")
        self.menu_file = QtGui.QMenu(self.menubar)
        self.menu_file.setObjectName("menuFile")
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        main_window.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        #Actions
        self.action_help = QtGui.QAction(main_window)
        self.action_help.setObjectName("actionHelp")
        self.action_load_xml = QtGui.QAction(main_window)
        self.action_load_xml.setObjectName("actionLoad_XML")
        self.action_exit = QtGui.QAction(main_window)
        self.action_exit.setObjectName("actionExit")

        #Menu items
        self.menu_file.addAction(self.action_load_xml)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.on_new_tab_page_load('sp0000')

        self.retranslateUi(main_window)
        self.connect_actions(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
    
    def on_new_tab_page_load(self, page_link):
        print(page_link)
        try:
            #If it is a URL object, convert to a string first.
            page_link = page_link.toString()
        except:
            #Otherwise, it's already a string.
            pass

        self.tab_count += 1

        #Append a new QWebView to the browser array.
        self.browsers.append(QtWebKit.QWebView(self.tab_widget))
        #Set this page's HTML.
        self.browsers[self.tab_count].setHtml(page_builders.dispatch_link(page_link, self.everything))
        
        self.handle_webview_events(self.browsers[self.tab_count])

        self.tab_widget.addTab(self.browsers[self.tab_count], str(randint(0, 10000)))
        self.tab_widget.setCurrentIndex(self.tab_count)
        self.tab_widget.setCurrentWidget(self.browsers[self.tab_count])

    def handle_webview_events(self, webview):
        #This allows me to handle the links by myself.
        webview.page().setLinkDelegationPolicy(QtWebKit.QWebPage.DelegateAllLinks)
        #Call this method anytime a link is clicked (for now...)
        webview.linkClicked.connect(self.on_new_tab_page_load)
        #web view now emits signal PySide.QtGui.QWidget.customContextMenuRequested
        webview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        webview.customContextMenuRequested.connect(self.context_menu_requested)

    #This gets called when the user right-clicks on the web view. A QPoint is passed, which represents
    #the location of the mouse click. We then test the page to see what is at that click location.
    def context_menu_requested(self, pos):
        hit_test = self.tab_widget.currentWidget().page().mainFrame().hitTestContent(pos)
        hit_url = hit_test.linkUrl()
        print(hit_url.isEmpty())

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QtGui.QApplication.translate("main_window", "main_window", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_file.setTitle(QtGui.QApplication.translate("main_window", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("main_window", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_help.setText(QtGui.QApplication.translate("main_window", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_load_xml.setText(QtGui.QApplication.translate("main_window", "Load XML...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_exit.setText(QtGui.QApplication.translate("main_window", "Exit", None, QtGui.QApplication.UnicodeUTF8))

    def connect_actions(self, main_window):
        QtCore.QObject.connect(self.action_exit, QtCore.SIGNAL('triggered()'), QtCore.QCoreApplication.instance().quit)
        QtCore.QObject.connect(self.action_load_xml, QtCore.SIGNAL('triggered()'), self.file_dialog)

    def file_dialog(self):
        self.file_dialog = QtGui.QFileDialog()
        self.file_dialog.setVisible(True)
        QtCore.QObject.connect(self.file_dialog, QtCore.SIGNAL('accepted()'), self.xml_loaded)

    def xml_loaded(self):
        selected = self.file_dialog.selectedFiles()[0]
        self.everything = load_dict(selected)
        self.on_new_tab_page_load('hf6666')

app = QtGui.QApplication(sys.argv)
wid = QtGui.QMainWindow()
window = UI()
window.setupUi(wid)
wid.show()
sys.exit(app.exec_())
