# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\256\PROJECTS\NSI\PREP\PIPELINE\.dev\UI\createProject_Warning_01.ui'
#
# Created: Tue Jul 10 13:52:24 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_warning(object):
    def setupUi(self, warning):
        warning.setObjectName("warning")
        warning.resize(362, 65)
        self.verticalLayout = QtGui.QVBoxLayout(warning)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lab_warning = QtGui.QLabel(warning)
        self.lab_warning.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_warning.setObjectName("lab_warning")
        self.verticalLayout.addWidget(self.lab_warning)
        self.splitter = QtGui.QSplitter(warning)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.btn_proceed = QtGui.QPushButton(self.splitter)
        self.btn_proceed.setObjectName("btn_proceed")
        self.btn_cancel = QtGui.QPushButton(self.splitter)
        self.btn_cancel.setObjectName("btn_cancel")
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(warning)
        QtCore.QMetaObject.connectSlotsByName(warning)

    def retranslateUi(self, warning):
        warning.setWindowTitle(QtGui.QApplication.translate("warning", "Warning", None, QtGui.QApplication.UnicodeUTF8))
        self.lab_warning.setText(QtGui.QApplication.translate("warning", "Folder exists!", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_proceed.setText(QtGui.QApplication.translate("warning", "PROCEED", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("warning", "CANCEL", None, QtGui.QApplication.UnicodeUTF8))

