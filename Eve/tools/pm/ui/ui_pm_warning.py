# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_pm_warning.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_pm_warning.ui' applies.
#
# Created: Tue Feb 04 14:38:59 2020
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Warning(object):
    def setupUi(self, Warning):
        Warning.setObjectName("Warning")
        Warning.resize(347, 60)
        self.verticalLayout = QtWidgets.QVBoxLayout(Warning)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labWarning = QtWidgets.QLabel(Warning)
        self.labWarning.setAlignment(QtCore.Qt.AlignCenter)
        self.labWarning.setObjectName("labWarning")
        self.verticalLayout.addWidget(self.labWarning)
        self.buttonBox = QtWidgets.QDialogButtonBox(Warning)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Yes)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Warning)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Warning.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Warning.reject)
        QtCore.QMetaObject.connectSlotsByName(Warning)

    def retranslateUi(self, Warning):
        Warning.setWindowTitle(QtWidgets.QApplication.translate("Warning", "Warning", None, -1))
        self.labWarning.setText(QtWidgets.QApplication.translate("Warning", "TextLabel", None, -1))

