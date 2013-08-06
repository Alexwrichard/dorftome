# Form implementation (largely) generated from reading ui file 'dwarf.ui'
#
# Created: Sun Jul 28 18:59:29 2013
#      by: pyside-uic 0.2.14 running on PySide 1.2.0

import sys
from xml_parsing import load_dict
import page_builders
from PySide import QtCore, QtGui, QtWebKit

class UI(object):
    def setupUi(self, main_window):

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
        self.centralwidget.setObjectName("centralwidget")
        #Layout setup
        self.grid_layout_2 = QtGui.QGridLayout(self.centralwidget)
        self.grid_layout_2.setObjectName("gridLayout_2")
        self.grid_layout = QtGui.QGridLayout()
        self.grid_layout.setObjectName("gridLayout")

        #Browser

        #self.text_browser = QtGui.QTextBrowser(self.centralwidget)
        self.text_browser = QtWebKit.QWebView(self.centralwidget)
        self.text_browser.setObjectName("textBrowser")
        self.grid_layout.addWidget(self.text_browser, 1, 0, 1, 1)

        #Search bar
        self.search_bar = QtGui.QLineEdit(self.centralwidget)
        self.search_bar.setText("")
        self.search_bar.setObjectName("lineEdit")
        self.grid_layout.addWidget(self.search_bar, 0, 0, 1, 1)

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
        self.menu_file.addAction(self.action_load_xml)
        self.menu_file.addSeparator()
        self.menu_file.addAction(self.action_exit)
        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.text_browser.setHtml(page_builders.build_splash_page())

        self.retranslateUi(main_window)
        self.connectButtons(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QtGui.QApplication.translate("main_window", "main_window", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_file.setTitle(QtGui.QApplication.translate("main_window", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("main_window", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_help.setText(QtGui.QApplication.translate("main_window", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_load_xml.setText(QtGui.QApplication.translate("main_window", "Load XML...", None, QtGui.QApplication.UnicodeUTF8))
        self.action_exit.setText(QtGui.QApplication.translate("main_window", "Exit", None, QtGui.QApplication.UnicodeUTF8))

    def connectButtons(self, main_window):
        QtCore.QObject.connect(self.action_exit, QtCore.SIGNAL('triggered()'), QtCore.QCoreApplication.instance().quit)
        QtCore.QObject.connect(self.action_load_xml, QtCore.SIGNAL('triggered()'), self.file_dialog)

    def file_dialog(self):
        self.file_dialog = QtGui.QFileDialog()
        self.file_dialog.setVisible(True)
        QtCore.QObject.connect(self.file_dialog, QtCore.SIGNAL('accepted()'), self.xml_loaded)

    def xml_loaded(self):
        selected = self.file_dialog.selectedFiles()[0]
        everything = load_dict(selected)
        self.text_browser.setHtml(page_builders.build_hf_page(6666, everything))

app = QtGui.QApplication(sys.argv)
wid = QtGui.QMainWindow()
window = UI()
window.setupUi(wid)
wid.show()
sys.exit(app.exec_())
