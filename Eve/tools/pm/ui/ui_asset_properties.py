# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_asset_properties.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_asset_properties.ui' applies.
#
# Created: Thu Feb 06 13:35:38 2020
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AssetProperties(object):
    def setupUi(self, AssetProperties):
        AssetProperties.setObjectName("AssetProperties")
        AssetProperties.resize(369, 101)
        self.verticalLayout = QtWidgets.QVBoxLayout(AssetProperties)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutAsset = QtWidgets.QVBoxLayout()
        self.layoutAsset.setObjectName("layoutAsset")
        self.verticalLayout.addLayout(self.layoutAsset)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btnUpdateAsset = QtWidgets.QPushButton(AssetProperties)
        self.btnUpdateAsset.setMinimumSize(QtCore.QSize(0, 45))
        self.btnUpdateAsset.setObjectName("btnUpdateAsset")
        self.verticalLayout.addWidget(self.btnUpdateAsset)
        self.splitter_5 = QtWidgets.QSplitter(AssetProperties)
        self.splitter_5.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_5.setObjectName("splitter_5")
        self.btnCreateHoudiniFile = QtWidgets.QPushButton(self.splitter_5)
        self.btnCreateHoudiniFile.setObjectName("btnCreateHoudiniFile")
        self.btnOpenHoudiniFile = QtWidgets.QPushButton(self.splitter_5)
        self.btnOpenHoudiniFile.setObjectName("btnOpenHoudiniFile")
        self.verticalLayout.addWidget(self.splitter_5)

        self.retranslateUi(AssetProperties)
        QtCore.QMetaObject.connectSlotsByName(AssetProperties)

    def retranslateUi(self, AssetProperties):
        AssetProperties.setWindowTitle(QtWidgets.QApplication.translate("AssetProperties", "Form", None, -1))
        self.btnUpdateAsset.setText(QtWidgets.QApplication.translate("AssetProperties", "Update Asset Data", None, -1))
        self.btnCreateHoudiniFile.setText(QtWidgets.QApplication.translate("AssetProperties", "Create Houdini Scene", None, -1))
        self.btnOpenHoudiniFile.setText(QtWidgets.QApplication.translate("AssetProperties", "Open Houdini Scene", None, -1))

