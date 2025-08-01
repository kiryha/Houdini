# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_project.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QSplitter, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Project(object):
    def setupUi(self, Project):
        if not Project.objectName():
            Project.setObjectName(u"Project")
        Project.resize(367, 262)
        self.shotLayout = QVBoxLayout(Project)
        self.shotLayout.setContentsMargins(0, 0, 0, 0)
        self.shotLayout.setObjectName(u"shotLayout")
        self.splitter = QSplitter(Project)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.label = QLabel(self.splitter)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(120, 0))
        self.label.setMaximumSize(QSize(120, 16777215))
        self.splitter.addWidget(self.label)
        self.linProjectName = QLineEdit(self.splitter)
        self.linProjectName.setObjectName(u"linProjectName")
        self.linProjectName.setAlignment(Qt.AlignCenter)
        self.splitter.addWidget(self.linProjectName)

        self.shotLayout.addWidget(self.splitter)

        self.splitter_2 = QSplitter(Project)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.label_4 = QLabel(self.splitter_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(120, 0))
        self.label_4.setMaximumSize(QSize(120, 16777215))
        self.splitter_2.addWidget(self.label_4)
        self.linProjectLocation = QLineEdit(self.splitter_2)
        self.linProjectLocation.setObjectName(u"linProjectLocation")
        self.linProjectLocation.setAlignment(Qt.AlignCenter)
        self.splitter_2.addWidget(self.linProjectLocation)

        self.shotLayout.addWidget(self.splitter_2)

        self.splitter_5 = QSplitter(Project)
        self.splitter_5.setObjectName(u"splitter_5")
        self.splitter_5.setOrientation(Qt.Horizontal)
        self.label_3 = QLabel(self.splitter_5)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 0))
        self.label_3.setMaximumSize(QSize(120, 16777215))
        self.splitter_5.addWidget(self.label_3)
        self.linHoudini = QLineEdit(self.splitter_5)
        self.linHoudini.setObjectName(u"linHoudini")
        self.linHoudini.setAlignment(Qt.AlignCenter)
        self.splitter_5.addWidget(self.linHoudini)

        self.shotLayout.addWidget(self.splitter_5)

        self.splitter_3 = QSplitter(Project)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.label_5 = QLabel(self.splitter_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(120, 0))
        self.label_5.setMaximumSize(QSize(120, 16777215))
        self.splitter_3.addWidget(self.label_5)
        self.linProjectWidth = QLineEdit(self.splitter_3)
        self.linProjectWidth.setObjectName(u"linProjectWidth")
        self.linProjectWidth.setAlignment(Qt.AlignCenter)
        self.splitter_3.addWidget(self.linProjectWidth)
        self.linProjectHeight = QLineEdit(self.splitter_3)
        self.linProjectHeight.setObjectName(u"linProjectHeight")
        self.linProjectHeight.setAlignment(Qt.AlignCenter)
        self.splitter_3.addWidget(self.linProjectHeight)

        self.shotLayout.addWidget(self.splitter_3)

        self.label_2 = QLabel(Project)
        self.label_2.setObjectName(u"label_2")

        self.shotLayout.addWidget(self.label_2)

        self.txtDescription = QTextEdit(Project)
        self.txtDescription.setObjectName(u"txtDescription")
        self.txtDescription.setMaximumSize(QSize(16777215, 100))

        self.shotLayout.addWidget(self.txtDescription)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.shotLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Project)

        QMetaObject.connectSlotsByName(Project)
    # setupUi

    def retranslateUi(self, Project):
        Project.setWindowTitle(QCoreApplication.translate("Project", u"Form", None))
        self.label.setText(QCoreApplication.translate("Project", u"Project Name", None))
        self.label_4.setText(QCoreApplication.translate("Project", u"Project Location: ", None))
        self.label_3.setText(QCoreApplication.translate("Project", u"Houdini Build", None))
        self.label_5.setText(QCoreApplication.translate("Project", u"Project Resolution", None))
        self.label_2.setText(QCoreApplication.translate("Project", u"Project Description:", None))
    # retranslateUi

