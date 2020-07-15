# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_project_properties.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_project_properties.ui' applies.
#
# Created: Tue Dec 24 13:05:54 2019
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_ProjectProperties(object):
    def setupUi(self, ProjectProperties):
        ProjectProperties.setObjectName("ProjectProperties")
        ProjectProperties.resize(368, 138)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProjectProperties)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layoutProject = QtWidgets.QVBoxLayout()
        self.layoutProject.setObjectName("layoutProject")
        self.verticalLayout.addLayout(self.layoutProject)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btnCreateProject = QtWidgets.QPushButton(ProjectProperties)
        self.btnCreateProject.setMinimumSize(QtCore.QSize(0, 40))
        self.btnCreateProject.setObjectName("btnCreateProject")
        self.verticalLayout.addWidget(self.btnCreateProject)
        self.splitter_7 = QtWidgets.QSplitter(ProjectProperties)
        self.splitter_7.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_7.setObjectName("splitter_7")
        self.btnLaunchHoudini = QtWidgets.QPushButton(self.splitter_7)
        self.btnLaunchHoudini.setObjectName("btnLaunchHoudini")
        self.btnLaunchNuke = QtWidgets.QPushButton(self.splitter_7)
        self.btnLaunchNuke.setObjectName("btnLaunchNuke")
        self.btnOpenFolder = QtWidgets.QPushButton(self.splitter_7)
        self.btnOpenFolder.setObjectName("btnOpenFolder")
        self.verticalLayout.addWidget(self.splitter_7)

        self.retranslateUi(ProjectProperties)
        QtCore.QMetaObject.connectSlotsByName(ProjectProperties)

    def retranslateUi(self, ProjectProperties):
        ProjectProperties.setWindowTitle(QtWidgets.QApplication.translate("ProjectProperties", "Form", None, -1))
        self.btnCreateProject.setText(QtWidgets.QApplication.translate("ProjectProperties", "Create Project", None, -1))
        self.btnLaunchHoudini.setText(QtWidgets.QApplication.translate("ProjectProperties", "Launch Houdini", None, -1))
        self.btnLaunchNuke.setText(QtWidgets.QApplication.translate("ProjectProperties", "Launch Nuke", None, -1))
        self.btnOpenFolder.setText(QtWidgets.QApplication.translate("ProjectProperties", "Open Folder", None, -1))

