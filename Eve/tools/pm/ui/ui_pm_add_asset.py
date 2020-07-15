# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_pm_add_asset.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_pm_add_asset.ui' applies.
#
# Created: Tue Dec 24 10:19:35 2019
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AddAsset(object):
    def setupUi(self, AddAsset):
        AddAsset.setObjectName("AddAsset")
        AddAsset.resize(370, 89)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddAsset)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutAsset = QtWidgets.QVBoxLayout()
        self.layoutAsset.setObjectName("layoutAsset")
        self.verticalLayout.addLayout(self.layoutAsset)
        self.btnAddAsset = QtWidgets.QPushButton(AddAsset)
        self.btnAddAsset.setMinimumSize(QtCore.QSize(0, 40))
        self.btnAddAsset.setObjectName("btnAddAsset")
        self.verticalLayout.addWidget(self.btnAddAsset)

        self.retranslateUi(AddAsset)
        QtCore.QMetaObject.connectSlotsByName(AddAsset)

    def retranslateUi(self, AddAsset):
        AddAsset.setWindowTitle(QtWidgets.QApplication.translate("AddAsset", "Add Asset", None, -1))
        self.btnAddAsset.setText(QtWidgets.QApplication.translate("AddAsset", "Add Asset", None, -1))

