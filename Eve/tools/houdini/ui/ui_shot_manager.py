# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\houdini\ui\ui_shot_manager.ui',
# licensing of 'E:\Eve\Eve\tools\houdini\ui\ui_shot_manager.ui' applies.
#
# Created: Mon Jun 15 16:18:03 2020
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ShotManager(object):
    def setupUi(self, ShotManager):
        ShotManager.setObjectName("ShotManager")
        ShotManager.resize(360, 187)
        self.verticalLayout = QtWidgets.QVBoxLayout(ShotManager)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(ShotManager)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label.setObjectName("label")
        self.boxSequence = QtWidgets.QComboBox(self.splitter)
        self.boxSequence.setObjectName("boxSequence")
        self.boxShot = QtWidgets.QComboBox(self.splitter)
        self.boxShot.setObjectName("boxShot")
        self.verticalLayout.addWidget(self.splitter)
        self.splitter_3 = QtWidgets.QSplitter(ShotManager)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.btnCreateRenderScene = QtWidgets.QPushButton(self.splitter_3)
        self.btnCreateRenderScene.setMinimumSize(QtCore.QSize(0, 35))
        self.btnCreateRenderScene.setObjectName("btnCreateRenderScene")
        self.btnOpenRenderScene = QtWidgets.QPushButton(self.splitter_3)
        self.btnOpenRenderScene.setMinimumSize(QtCore.QSize(0, 35))
        self.btnOpenRenderScene.setObjectName("btnOpenRenderScene")
        self.verticalLayout.addWidget(self.splitter_3)
        self.splitter_2 = QtWidgets.QSplitter(ShotManager)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.btnCreateAnimationScene = QtWidgets.QPushButton(self.splitter_2)
        self.btnCreateAnimationScene.setMinimumSize(QtCore.QSize(0, 35))
        self.btnCreateAnimationScene.setObjectName("btnCreateAnimationScene")
        self.btnOpenAnimationScene = QtWidgets.QPushButton(self.splitter_2)
        self.btnOpenAnimationScene.setMinimumSize(QtCore.QSize(0, 35))
        self.btnOpenAnimationScene.setObjectName("btnOpenAnimationScene")
        self.verticalLayout.addWidget(self.splitter_2)
        self.pushButton = QtWidgets.QPushButton(ShotManager)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 45))
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        self.retranslateUi(ShotManager)
        QtCore.QMetaObject.connectSlotsByName(ShotManager)

    def retranslateUi(self, ShotManager):
        ShotManager.setWindowTitle(QtWidgets.QApplication.translate("ShotManager", "Shot Manager", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("ShotManager", "Sequence : Shot", None, -1))
        self.btnCreateRenderScene.setText(QtWidgets.QApplication.translate("ShotManager", "Create Render Scene", None, -1))
        self.btnOpenRenderScene.setText(QtWidgets.QApplication.translate("ShotManager", "Open Render Scene", None, -1))
        self.btnCreateAnimationScene.setText(QtWidgets.QApplication.translate("ShotManager", "Create Animation Scene", None, -1))
        self.btnOpenAnimationScene.setText(QtWidgets.QApplication.translate("ShotManager", "Open Animation Scene", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("ShotManager", "Publish Current Scene", None, -1))

