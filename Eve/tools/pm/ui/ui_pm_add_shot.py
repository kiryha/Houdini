# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_pm_add_shot.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_pm_add_shot.ui' applies.
#
# Created: Tue Dec 24 10:46:21 2019
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AddShot(object):
    def setupUi(self, AddShot):
        AddShot.setObjectName("AddShot")
        AddShot.resize(370, 89)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddShot)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutShot = QtWidgets.QVBoxLayout()
        self.layoutShot.setObjectName("layoutShot")
        self.verticalLayout.addLayout(self.layoutShot)
        self.btnAddShot = QtWidgets.QPushButton(AddShot)
        self.btnAddShot.setMinimumSize(QtCore.QSize(0, 40))
        self.btnAddShot.setObjectName("btnAddShot")
        self.verticalLayout.addWidget(self.btnAddShot)

        self.retranslateUi(AddShot)
        QtCore.QMetaObject.connectSlotsByName(AddShot)

    def retranslateUi(self, AddShot):
        AddShot.setWindowTitle(QtWidgets.QApplication.translate("AddShot", "Add Shot", None, -1))
        self.btnAddShot.setText(QtWidgets.QApplication.translate("AddShot", "Add Shot", None, -1))

