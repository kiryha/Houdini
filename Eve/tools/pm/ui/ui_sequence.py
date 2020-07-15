# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Eve\Eve\tools\pm\ui\ui_sequence.ui',
# licensing of 'E:\Eve\Eve\tools\pm\ui\ui_sequence.ui' applies.
#
# Created: Wed Feb 05 14:00:53 2020
#      by: pyside2-uic  running on PySide2 5.9.0a1.dev1528389443
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Sequence(object):
    def setupUi(self, Sequence):
        Sequence.setObjectName("Sequence")
        Sequence.resize(367, 182)
        self.shotLayout = QtWidgets.QVBoxLayout(Sequence)
        self.shotLayout.setContentsMargins(0, 0, 0, 0)
        self.shotLayout.setObjectName("shotLayout")
        self.splitter_2 = QtWidgets.QSplitter(Sequence)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.label_3 = QtWidgets.QLabel(self.splitter_2)
        self.label_3.setMinimumSize(QtCore.QSize(120, 0))
        self.label_3.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label_3.setObjectName("label_3")
        self.linProjectName = QtWidgets.QLineEdit(self.splitter_2)
        self.linProjectName.setEnabled(False)
        self.linProjectName.setAlignment(QtCore.Qt.AlignCenter)
        self.linProjectName.setObjectName("linProjectName")
        self.shotLayout.addWidget(self.splitter_2)
        self.splitter = QtWidgets.QSplitter(Sequence)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setMinimumSize(QtCore.QSize(120, 0))
        self.label.setMaximumSize(QtCore.QSize(120, 16777215))
        self.label.setObjectName("label")
        self.linSequenceName = QtWidgets.QLineEdit(self.splitter)
        self.linSequenceName.setAlignment(QtCore.Qt.AlignCenter)
        self.linSequenceName.setObjectName("linSequenceName")
        self.shotLayout.addWidget(self.splitter)
        self.label_2 = QtWidgets.QLabel(Sequence)
        self.label_2.setObjectName("label_2")
        self.shotLayout.addWidget(self.label_2)
        self.txtDescription = QtWidgets.QTextEdit(Sequence)
        self.txtDescription.setMaximumSize(QtCore.QSize(16777215, 100))
        self.txtDescription.setObjectName("txtDescription")
        self.shotLayout.addWidget(self.txtDescription)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.shotLayout.addItem(spacerItem)

        self.retranslateUi(Sequence)
        QtCore.QMetaObject.connectSlotsByName(Sequence)

    def retranslateUi(self, Sequence):
        Sequence.setWindowTitle(QtWidgets.QApplication.translate("Sequence", "Sequence", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Sequence", "Project Name", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Sequence", "Sequence Name", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Sequence", "Sequence Description:", None, -1))

