# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_project.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_project.ui' applies.
#
# Created: Tue Dec 24 12:56:45 2019
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Project(object):
    def setupUi(self, Project):
        Project.setObjectName("Project")
        Project.resize(367, 262)
        self.shotLayout = QtWidgets.QVBoxLayout(Project)
        self.shotLayout.setContentsMargins(0, 0, 0, 0)
        self.shotLayout.setObjectName("shotLayout")
        self.splitter = QtWidgets.QSplitter(Project)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setMinimumSize(QtCore.QSize(120, 0))
        self.label.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label.setObjectName("label")
        self.linProjectName = QtWidgets.QLineEdit(self.splitter)
        self.linProjectName.setAlignment(QtCore.Qt.AlignCenter)
        self.linProjectName.setObjectName("linProjectName")
        self.shotLayout.addWidget(self.splitter)
        self.splitter_2 = QtWidgets.QSplitter(Project)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.label_4 = QtWidgets.QLabel(self.splitter_2)
        self.label_4.setMinimumSize(QtCore.QSize(120, 0))
        self.label_4.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_4.setObjectName("label_4")
        self.linProjectLocation = QtWidgets.QLineEdit(self.splitter_2)
        self.linProjectLocation.setAlignment(QtCore.Qt.AlignCenter)
        self.linProjectLocation.setObjectName("linProjectLocation")
        self.shotLayout.addWidget(self.splitter_2)
        self.splitter_5 = QtWidgets.QSplitter(Project)
        self.splitter_5.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_5.setObjectName("splitter_5")
        self.label_3 = QtWidgets.QLabel(self.splitter_5)
        self.label_3.setMinimumSize(QtCore.QSize(120, 0))
        self.label_3.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_3.setObjectName("label_3")
        self.linHoudini = QtWidgets.QLineEdit(self.splitter_5)
        self.linHoudini.setAlignment(QtCore.Qt.AlignCenter)
        self.linHoudini.setObjectName("linHoudini")
        self.shotLayout.addWidget(self.splitter_5)
        self.splitter_3 = QtWidgets.QSplitter(Project)
        self.splitter_3.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_3.setObjectName("splitter_3")
        self.label_5 = QtWidgets.QLabel(self.splitter_3)
        self.label_5.setMinimumSize(QtCore.QSize(120, 0))
        self.label_5.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_5.setObjectName("label_5")
        self.linProjectWidth = QtWidgets.QLineEdit(self.splitter_3)
        self.linProjectWidth.setAlignment(QtCore.Qt.AlignCenter)
        self.linProjectWidth.setObjectName("linProjectWidth")
        self.linProjectHeight = QtWidgets.QLineEdit(self.splitter_3)
        self.linProjectHeight.setAlignment(QtCore.Qt.AlignCenter)
        self.linProjectHeight.setObjectName("linProjectHeight")
        self.shotLayout.addWidget(self.splitter_3)
        self.label_2 = QtWidgets.QLabel(Project)
        self.label_2.setObjectName("label_2")
        self.shotLayout.addWidget(self.label_2)
        self.txtDescription = QtWidgets.QTextEdit(Project)
        self.txtDescription.setMaximumSize(QtCore.QSize(16777215, 100))
        self.txtDescription.setObjectName("txtDescription")
        self.shotLayout.addWidget(self.txtDescription)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.shotLayout.addItem(spacerItem)

        self.retranslateUi(Project)
        QtCore.QMetaObject.connectSlotsByName(Project)

    def retranslateUi(self, Project):
        Project.setWindowTitle(QtWidgets.QApplication.translate("Project", "Form", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Project", "Project Name", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("Project", "Project Location: ", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Project", "Houdini Build", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("Project", "Project Resolution", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Project", "Project Description:", None, -1))

