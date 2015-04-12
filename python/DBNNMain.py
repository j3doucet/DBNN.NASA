# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DBNNMain.ui'
#
# Created: Sat Apr 11 20:58:54 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(820, 900)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 17, 802, 821))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtGui.QLabel(self.layoutWidget)
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
        self.widget_3 = QtGui.QWidget(self.layoutWidget)
        self.widget_3.setObjectName("widget_3")
        self.ReadProgressBar = QtGui.QProgressBar(self.widget_3)
        self.ReadProgressBar.setGeometry(QtCore.QRect(7, 650, 781, 23))
        self.ReadProgressBar.setProperty("value", 0)
        self.ReadProgressBar.setObjectName("ReadProgressBar")
        self.StatusLabel = QtGui.QLabel(self.widget_3)
        self.StatusLabel.setGeometry(QtCore.QRect(10, 675, 561, 31))
        self.StatusLabel.setText("")
        self.StatusLabel.setObjectName("StatusLabel")
        self.AsteroidBrowser = QtWebKit.QWebView(self.widget_3)
        self.AsteroidBrowser.setGeometry(QtCore.QRect(10, 0, 791, 600))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AsteroidBrowser.sizePolicy().hasHeightForWidth())
        self.AsteroidBrowser.setSizePolicy(sizePolicy)
        self.AsteroidBrowser.setUrl(QtCore.QUrl("about:blank"))
        self.AsteroidBrowser.setObjectName("AsteroidBrowser")
        self.verticalLayout.addWidget(self.widget_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 26))
        self.menubar.setObjectName("menubar")
        self.Asteroids = QtGui.QMenu(self.menubar)
        self.Asteroids.setObjectName("Asteroids")
        self.menuBrains = QtGui.QMenu(self.menubar)
        self.menuBrains.setObjectName("menuBrains")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionGetAsteroids = QtGui.QAction(MainWindow)
        self.actionGetAsteroids.setObjectName("actionGetAsteroids")
        self.actionBloop2 = QtGui.QAction(MainWindow)
        self.actionBloop2.setObjectName("actionBloop2")
        self.actionLoad_Old_Data = QtGui.QAction(MainWindow)
        self.actionLoad_Old_Data.setObjectName("actionLoad_Old_Data")
        self.Asteroids.addAction(self.actionGetAsteroids)
        self.Asteroids.addAction(self.actionLoad_Old_Data)
        self.menubar.addAction(self.Asteroids.menuAction())
        self.menubar.addAction(self.menuBrains.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "DBNN.NASA", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Latest Asteroids", None, QtGui.QApplication.UnicodeUTF8))
        self.Asteroids.setTitle(QtGui.QApplication.translate("MainWindow", "Asteroids", None, QtGui.QApplication.UnicodeUTF8))
        self.menuBrains.setTitle(QtGui.QApplication.translate("MainWindow", "Brains", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGetAsteroids.setText(QtGui.QApplication.translate("MainWindow", "Get Latest", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBloop2.setText(QtGui.QApplication.translate("MainWindow", "bloop2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_Old_Data.setText(QtGui.QApplication.translate("MainWindow", "Load Old Data", None, QtGui.QApplication.UnicodeUTF8))

from PySide import QtWebKit
