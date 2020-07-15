# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_pm_add_project.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_pm_add_project.ui' applies.
#
# Created: Mon Dec 23 15:24:49 2019
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_AddProject(object):
    def setupUi(self, AddProject):
        AddProject.setObjectName("AddProject")
        AddProject.resize(369, 92)
        self.verticalLayout = QtWidgets.QVBoxLayout(AddProject)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutProject = QtWidgets.QVBoxLayout()
        self.layoutProject.setObjectName("layoutProject")
        self.verticalLayout.addLayout(self.layoutProject)
        self.btnAddProject = QtWidgets.QPushButton(AddProject)
        self.btnAddProject.setMinimumSize(QtCore.QSize(0, 40))
        self.btnAddProject.setObjectName("btnAddProject")
        self.verticalLayout.addWidget(self.btnAddProject)

        self.retranslateUi(AddProject)
        QtCore.QMetaObject.connectSlotsByName(AddProject)

    def retranslateUi(self, AddProject):
        AddProject.setWindowTitle(QtWidgets.QApplication.translate("AddProject", "Add Project", None, -1))
        self.btnAddProject.setText(QtWidgets.QApplication.translate("AddProject", "Add Project", None, -1))

