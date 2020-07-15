# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_pm_add_sequence.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_pm_add_sequence.ui' applies.
#
# Created: Wed Feb 05 11:57:12 2020
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AddSequence(object):
    def setupUi(self, AddSequence):
        AddSequence.setObjectName("AddSequence")
        AddSequence.resize(370, 89)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddSequence)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutSequence = QtWidgets.QVBoxLayout()
        self.layoutSequence.setObjectName("layoutSequence")
        self.verticalLayout.addLayout(self.layoutSequence)
        self.btnAddSequence = QtWidgets.QPushButton(AddSequence)
        self.btnAddSequence.setMinimumSize(QtCore.QSize(0, 40))
        self.btnAddSequence.setObjectName("btnAddSequence")
        self.verticalLayout.addWidget(self.btnAddSequence)

        self.retranslateUi(AddSequence)
        QtCore.QMetaObject.connectSlotsByName(AddSequence)

    def retranslateUi(self, AddSequence):
        AddSequence.setWindowTitle(QtWidgets.QApplication.translate("AddSequence", "Add Sequence", None, -1))
        self.btnAddSequence.setText(QtWidgets.QApplication.translate("AddSequence", "Add Sequence", None, -1))

