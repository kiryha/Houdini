# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\256\PROJECTS\NSI\PREP\PIPELINE\.dev\UI\createProject_SG_01.ui'
#
# Created: Thu Jul 05 12:02:33 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_SetupShotgun(object):
    def setupUi(self, SetupShotgun):
        SetupShotgun.setObjectName("SetupShotgun")
        SetupShotgun.resize(393, 171)
        self.centralwidget = QtGui.QWidget(SetupShotgun)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_shots = QtGui.QPushButton(self.centralwidget)
        self.btn_shots.setObjectName("btn_shots")
        self.verticalLayout.addWidget(self.btn_shots)
        self.btn_assets = QtGui.QPushButton(self.centralwidget)
        self.btn_assets.setObjectName("btn_assets")
        self.verticalLayout.addWidget(self.btn_assets)
        self.btn_presets = QtGui.QPushButton(self.centralwidget)
        self.btn_presets.setObjectName("btn_presets")
        self.verticalLayout.addWidget(self.btn_presets)
        SetupShotgun.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(SetupShotgun)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 393, 26))
        self.menubar.setObjectName("menubar")
        SetupShotgun.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(SetupShotgun)
        self.statusbar.setObjectName("statusbar")
        SetupShotgun.setStatusBar(self.statusbar)

        self.retranslateUi(SetupShotgun)
        QtCore.QMetaObject.connectSlotsByName(SetupShotgun)

    def retranslateUi(self, SetupShotgun):
        SetupShotgun.setWindowTitle(QtGui.QApplication.translate("SetupShotgun", "Setup Shotgun", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_shots.setText(QtGui.QApplication.translate("SetupShotgun", "SETUP SHOTS", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_assets.setText(QtGui.QApplication.translate("SetupShotgun", "SETUP ASSETS", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_presets.setText(QtGui.QApplication.translate("SetupShotgun", "LOAD PRESETS", None, QtGui.QApplication.UnicodeUTF8))

