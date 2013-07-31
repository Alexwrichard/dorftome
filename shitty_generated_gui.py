# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dwarf.ui'
#
# Created: Sun Jul 28 18:59:29 2013
#      by: pyside-uic 0.2.14 running on PySide 1.2.0

import sys
from xml_parsing import load_dict
from page_builders import build_hf_page
from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(634, 618)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 634, 19))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionLoad_XML = QtGui.QAction(MainWindow)
        self.actionLoad_XML.setObjectName("actionLoad_XML")
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionLoad_XML)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.textBrowser.setDocument(self.html_text_doc())

        self.retranslateUi(MainWindow)
        self.connectButtons(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_XML.setText(QtGui.QApplication.translate("MainWindow", "Load XML...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))

    def connectButtons(self, MainWindow):
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL('triggered()'), QtCore.QCoreApplication.instance().quit)
        QtCore.QObject.connect(self.actionLoad_XML, QtCore.SIGNAL('triggered()'), self.file_dialog)

    def file_dialog(self):
        self.file_dialog = QtGui.QFileDialog()
        self.file_dialog.setVisible(True)
        QtCore.QObject.connect(self.file_dialog, QtCore.SIGNAL('accepted()'), self.xml_triggered)

    def xml_triggered(self):
        selected = self.file_dialog.selectedFiles()[0]
        everything = load_dict(selected)

        self.textDoc.setHtml(build_hf_page(6666, everything, self.css))

    def html_text_doc(self):
        string = "<html><head>\n" + \
                 "<link rel='stylesheet' type='text/css' href='format.css'>\n" + \
                 "</head><body>\n" + \
                 "<h1 class='page-title'> Welcome! </h1>\n" + \
                 "<hr>\n" + \
                 "<p class='plain-text'>To begin browsing, select File > Load XML and locate the correct file.</p>\n" + \
                 "</body></html>"
        self.css = \
                "body {\
                    background-color:#555555;\
                }\
                p {\
                    font-family:Garamond, serif;\
                    font-size:13px\
                }\
                .hf-name-occurence{\
                    font-family:Helvetica, sans-serif;\
                    font-size:14px\
                }\
                .page-title {\
                    color:#BBBBBB;\
                    font-family:Helvetica, sans-serif;\
                }\
                .page-description {\
                    color:#999999;\
                    font-family:Helvetica, sans-serif;\
                }"
        self.textDoc = QtGui.QTextDocument()
        self.textDoc.addResource(QtGui.QTextDocument.StyleSheetResource, QtCore.QUrl("format.css"), self.css)
        self.textDoc.setHtml(string)
        return self.textDoc

app = QtGui.QApplication(sys.argv)
wid = QtGui.QMainWindow() 
window = Ui_MainWindow()
window.setupUi(wid)
wid.show()
sys.exit(app.exec_())
