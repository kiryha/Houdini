# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_project_properties.ui'
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
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QVBoxLayout, QWidget)

class Ui_ProjectProperties(object):
    def setupUi(self, ProjectProperties):
        if not ProjectProperties.objectName():
            ProjectProperties.setObjectName(u"ProjectProperties")
        ProjectProperties.resize(368, 138)
        self.verticalLayout = QVBoxLayout(ProjectProperties)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutProject = QVBoxLayout()
        self.layoutProject.setObjectName(u"layoutProject")

        self.verticalLayout.addLayout(self.layoutProject)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btnCreateProject = QPushButton(ProjectProperties)
        self.btnCreateProject.setObjectName(u"btnCreateProject")
        self.btnCreateProject.setMinimumSize(QSize(0, 40))

        self.verticalLayout.addWidget(self.btnCreateProject)

        self.splitter_7 = QSplitter(ProjectProperties)
        self.splitter_7.setObjectName(u"splitter_7")
        self.splitter_7.setOrientation(Qt.Horizontal)
        self.btnLaunchHoudini = QPushButton(self.splitter_7)
        self.btnLaunchHoudini.setObjectName(u"btnLaunchHoudini")
        self.splitter_7.addWidget(self.btnLaunchHoudini)
        self.btnLaunchNuke = QPushButton(self.splitter_7)
        self.btnLaunchNuke.setObjectName(u"btnLaunchNuke")
        self.splitter_7.addWidget(self.btnLaunchNuke)
        self.btnOpenFolder = QPushButton(self.splitter_7)
        self.btnOpenFolder.setObjectName(u"btnOpenFolder")
        self.splitter_7.addWidget(self.btnOpenFolder)

        self.verticalLayout.addWidget(self.splitter_7)


        self.retranslateUi(ProjectProperties)

        QMetaObject.connectSlotsByName(ProjectProperties)
    # setupUi

    def retranslateUi(self, ProjectProperties):
        ProjectProperties.setWindowTitle(QCoreApplication.translate("ProjectProperties", u"Form", None))
        self.btnCreateProject.setText(QCoreApplication.translate("ProjectProperties", u"Create Project", None))
        self.btnLaunchHoudini.setText(QCoreApplication.translate("ProjectProperties", u"Launch Houdini", None))
        self.btnLaunchNuke.setText(QCoreApplication.translate("ProjectProperties", u"Launch Nuke", None))
        self.btnOpenFolder.setText(QCoreApplication.translate("ProjectProperties", u"Open Folder", None))
    # retranslateUi

