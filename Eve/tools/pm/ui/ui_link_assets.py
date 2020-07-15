# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_link_assets.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_link_assets.ui' applies.
#
# Created: Thu Feb 06 09:09:33 2020
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LinkAssets(object):
    def setupUi(self, LinkAssets):
        LinkAssets.setObjectName("LinkAssets")
        LinkAssets.resize(241, 358)
        self.verticalLayout = QtWidgets.QVBoxLayout(LinkAssets)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(LinkAssets)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setMaximumSize(QtCore.QSize(85, 16777215))
        self.label.setObjectName("label")
        self.linShotName = QtWidgets.QLineEdit(self.splitter)
        self.linShotName.setEnabled(False)
        self.linShotName.setAlignment(QtCore.Qt.AlignCenter)
        self.linShotName.setObjectName("linShotName")
        self.verticalLayout.addWidget(self.splitter)
        self.listAssets = QtWidgets.QListView(LinkAssets)
        self.listAssets.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listAssets.setObjectName("listAssets")
        self.verticalLayout.addWidget(self.listAssets)
        self.btnLinkAssets = QtWidgets.QPushButton(LinkAssets)
        self.btnLinkAssets.setMinimumSize(QtCore.QSize(0, 40))
        self.btnLinkAssets.setObjectName("btnLinkAssets")
        self.verticalLayout.addWidget(self.btnLinkAssets)

        self.retranslateUi(LinkAssets)
        QtCore.QMetaObject.connectSlotsByName(LinkAssets)

    def retranslateUi(self, LinkAssets):
        LinkAssets.setWindowTitle(QtWidgets.QApplication.translate("LinkAssets", "Link Assets", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("LinkAssets", "Shot Name", None, -1))
        self.btnLinkAssets.setText(QtWidgets.QApplication.translate("LinkAssets", "Link Selected Assets to the Shot", None, -1))

