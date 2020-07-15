# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_asset.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_asset.ui' applies.
#
# Created: Fri Jun 12 14:44:19 2020
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Asset(object):
    def setupUi(self, Asset):
        Asset.setObjectName("Asset")
        Asset.resize(367, 274)
        self.shotLayout = QtWidgets.QVBoxLayout(Asset)
        self.shotLayout.setContentsMargins(0, 0, 0, 0)
        self.shotLayout.setObjectName("shotLayout")
        self.splitter_4 = QtWidgets.QSplitter(Asset)
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")
        self.label_5 = QtWidgets.QLabel(self.splitter_4)
        self.label_5.setMinimumSize(QtCore.QSize(120, 0))
        self.label_5.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_5.setObjectName("label_5")
        self.linProjectName = QtWidgets.QLineEdit(self.splitter_4)
        self.linProjectName.setEnabled(False)
        self.linProjectName.setAlignment(QtCore.Qt.AlignCenter)
        self.linProjectName.setObjectName("linProjectName")
        self.shotLayout.addWidget(self.splitter_4)
        self.splitter = QtWidgets.QSplitter(Asset)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setMinimumSize(QtCore.QSize(120, 0))
        self.label.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label.setObjectName("label")
        self.linAssetName = QtWidgets.QLineEdit(self.splitter)
        self.linAssetName.setAlignment(QtCore.Qt.AlignCenter)
        self.linAssetName.setObjectName("linAssetName")
        self.shotLayout.addWidget(self.splitter)
        self.splitter_2 = QtWidgets.QSplitter(Asset)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.label_4 = QtWidgets.QLabel(self.splitter_2)
        self.label_4.setMinimumSize(QtCore.QSize(120, 0))
        self.label_4.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_4.setObjectName("label_4")
        self.comAssetType = QtWidgets.QComboBox(self.splitter_2)
        self.comAssetType.setObjectName("comAssetType")
        self.shotLayout.addWidget(self.splitter_2)
        self.splitter_5 = QtWidgets.QSplitter(Asset)
        self.splitter_5.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_5.setObjectName("splitter_5")
        self.label_6 = QtWidgets.QLabel(self.splitter_5)
        self.label_6.setMinimumSize(QtCore.QSize(120, 0))
        self.label_6.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_6.setObjectName("label_6")
        self.linAssetPublish = QtWidgets.QLineEdit(self.splitter_5)
        self.linAssetPublish.setEnabled(False)
        self.linAssetPublish.setAlignment(QtCore.Qt.AlignCenter)
        self.linAssetPublish.setObjectName("linAssetPublish")
        self.shotLayout.addWidget(self.splitter_5)
        self.pushButton = QtWidgets.QPushButton(Asset)
        self.pushButton.setObjectName("pushButton")
        self.shotLayout.addWidget(self.pushButton)
        self.label_2 = QtWidgets.QLabel(Asset)
        self.label_2.setObjectName("label_2")
        self.shotLayout.addWidget(self.label_2)
        self.txtDescription = QtWidgets.QTextEdit(Asset)
        self.txtDescription.setMaximumSize(QtCore.QSize(16777215, 100))
        self.txtDescription.setObjectName("txtDescription")
        self.shotLayout.addWidget(self.txtDescription)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.shotLayout.addItem(spacerItem)

        self.retranslateUi(Asset)
        QtCore.QMetaObject.connectSlotsByName(Asset)

    def retranslateUi(self, Asset):
        Asset.setWindowTitle(QtWidgets.QApplication.translate("Asset", "Asset", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Asset", "Project Name", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Asset", "Asset Name", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Asset", "Asset Type", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("Asset", "Published Version", None, -1))
        self.pushButton.setText(QtWidgets.QApplication.translate("Asset", "Asset Configuration Manager", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Asset", "Asset Description:", None, -1))

