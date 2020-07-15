# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_shot_properties.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_shot_properties.ui' applies.
#
# Created: Wed Feb 05 11:10:46 2020
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ShotProperties(object):
    def setupUi(self, ShotProperties):
        ShotProperties.setObjectName("ShotProperties")
        ShotProperties.resize(370, 193)
        self.verticalLayout = QtWidgets.QVBoxLayout(ShotProperties)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutShot = QtWidgets.QVBoxLayout()
        self.layoutShot.setObjectName("layoutShot")
        self.verticalLayout.addLayout(self.layoutShot)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btnUpdateShot = QtWidgets.QPushButton(ShotProperties)
        self.btnUpdateShot.setMinimumSize(QtCore.QSize(0, 45))
        self.btnUpdateShot.setObjectName("btnUpdateShot")
        self.verticalLayout.addWidget(self.btnUpdateShot)
        self.splitter_6 = QtWidgets.QSplitter(ShotProperties)
        self.splitter_6.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_6.setObjectName("splitter_6")
        self.btnCreateShot = QtWidgets.QPushButton(self.splitter_6)
        self.btnCreateShot.setObjectName("btnCreateShot")
        self.btnOpenShot = QtWidgets.QPushButton(self.splitter_6)
        self.btnOpenShot.setObjectName("btnOpenShot")
        self.verticalLayout.addWidget(self.splitter_6)
        self.splitter_7 = QtWidgets.QSplitter(ShotProperties)
        self.splitter_7.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_7.setObjectName("splitter_7")
        self.btnCreateShotAnim = QtWidgets.QPushButton(self.splitter_7)
        self.btnCreateShotAnim.setObjectName("btnCreateShotAnim")
        self.btnOpenShotAnim = QtWidgets.QPushButton(self.splitter_7)
        self.btnOpenShotAnim.setObjectName("btnOpenShotAnim")
        self.verticalLayout.addWidget(self.splitter_7)

        self.retranslateUi(ShotProperties)
        QtCore.QMetaObject.connectSlotsByName(ShotProperties)

    def retranslateUi(self, ShotProperties):
        ShotProperties.setWindowTitle(QtWidgets.QApplication.translate("ShotProperties", "Form", None, -1))
        self.btnUpdateShot.setText(QtWidgets.QApplication.translate("ShotProperties", "Update Shot Data", None, -1))
        self.btnCreateShot.setText(QtWidgets.QApplication.translate("ShotProperties", "Create Render Scene", None, -1))
        self.btnOpenShot.setText(QtWidgets.QApplication.translate("ShotProperties", "Open Render Scene", None, -1))
        self.btnCreateShotAnim.setText(QtWidgets.QApplication.translate("ShotProperties", "Create Animation Scene", None, -1))
        self.btnOpenShotAnim.setText(QtWidgets.QApplication.translate("ShotProperties", "Open Animation Scene", None, -1))

