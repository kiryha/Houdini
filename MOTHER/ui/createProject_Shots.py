# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'P:\PROJECTS\NSI\PREP\PIPELINE\.dev\UI\createProject_Shots_01.ui'
#
# Created: Fri Jul 13 16:40:24 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_ShotBuilder(object):
    def setupUi(self, ShotBuilder):
        ShotBuilder.setObjectName("ShotBuilder")
        ShotBuilder.resize(345, 67)
        self.verticalLayout = QtGui.QVBoxLayout(ShotBuilder)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lin_shots = QtGui.QLineEdit(ShotBuilder)
        self.lin_shots.setObjectName("lin_shots")
        self.verticalLayout.addWidget(self.lin_shots)
        self.btn_save = QtGui.QPushButton(ShotBuilder)
        self.btn_save.setObjectName("btn_save")
        self.verticalLayout.addWidget(self.btn_save)

        self.retranslateUi(ShotBuilder)
        QtCore.QMetaObject.connectSlotsByName(ShotBuilder)

    def retranslateUi(self, ShotBuilder):
        ShotBuilder.setWindowTitle(QtGui.QApplication.translate("ShotBuilder", "SHOT builder", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_save.setText(QtGui.QApplication.translate("ShotBuilder", "SAVE", None, QtGui.QApplication.UnicodeUTF8))

