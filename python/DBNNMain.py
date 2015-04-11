# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DBNNMain.ui'
#
# Created: Sat Apr 11 08:19:35 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1038, 711)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_3 = QtGui.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.ReadProgressBar = QtGui.QProgressBar(self.widget_3)
        self.ReadProgressBar.setGeometry(QtCore.QRect(7, 20, 831, 23))
        self.ReadProgressBar.setProperty("value", 0)
        self.ReadProgressBar.setObjectName("ReadProgressBar")
        self.StatusLabel = QtGui.QLabel(self.widget_3)
        self.StatusLabel.setGeometry(QtCore.QRect(10, 80, 561, 31))
        self.StatusLabel.setText("")
        self.StatusLabel.setObjectName("StatusLabel")
        self.gridLayout.addWidget(self.widget_3, 1, 0, 1, 2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(19)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.AsteroidBrowser = QtGui.QTextBrowser(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AsteroidBrowser.sizePolicy().hasHeightForWidth())
        self.AsteroidBrowser.setSizePolicy(sizePolicy)
        self.AsteroidBrowser.setObjectName("AsteroidBrowser")
        self.verticalLayout.addWidget(self.AsteroidBrowser)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1038, 26))
        self.menubar.setObjectName("menubar")
        self.menuHello_Sample = QtGui.QMenu(self.menubar)
        self.menuHello_Sample.setObjectName("menuHello_Sample")
        self.menuBrains = QtGui.QMenu(self.menubar)
        self.menuBrains.setObjectName("menuBrains")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionBloop_bloop = QtGui.QAction(MainWindow)
        self.actionBloop_bloop.setObjectName("actionBloop_bloop")
        self.actionBloop2 = QtGui.QAction(MainWindow)
        self.actionBloop2.setObjectName("actionBloop2")
        self.menuHello_Sample.addAction(self.actionBloop_bloop)
        self.menuHello_Sample.addAction(self.actionBloop2)
        self.menubar.addAction(self.menuHello_Sample.menuAction())
        self.menubar.addAction(self.menuBrains.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "DBNN.NASA", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Latest Asteroids", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHello_Sample.setTitle(QtGui.QApplication.translate("MainWindow", "Asteroids", None, QtGui.QApplication.UnicodeUTF8))
        self.menuBrains.setTitle(QtGui.QApplication.translate("MainWindow", "Brains", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBloop_bloop.setText(QtGui.QApplication.translate("MainWindow", "Get Latest", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBloop2.setText(QtGui.QApplication.translate("MainWindow", "bloop2", None, QtGui.QApplication.UnicodeUTF8))

