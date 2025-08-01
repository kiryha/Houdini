# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_pm_main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QListView,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_ProjectManager(object):
    def setupUi(self, ProjectManager):
        if not ProjectManager.objectName():
            ProjectManager.setObjectName(u"ProjectManager")
        ProjectManager.resize(1013, 939)
        self.actionEveDocs = QAction(ProjectManager)
        self.actionEveDocs.setObjectName(u"actionEveDocs")
        self.actionSettings = QAction(ProjectManager)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionCreateDatabase = QAction(ProjectManager)
        self.actionCreateDatabase.setObjectName(u"actionCreateDatabase")
        self.centralwidget = QWidget(ProjectManager)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.boxProjects = QGroupBox(self.centralwidget)
        self.boxProjects.setObjectName(u"boxProjects")
        self.boxProjects.setEnabled(True)
        self.boxProjects.setMaximumSize(QSize(150, 16777215))
        self.boxProjects.setFlat(True)
        self.verticalLayout = QVBoxLayout(self.boxProjects)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.listProjects = QListView(self.boxProjects)
        self.listProjects.setObjectName(u"listProjects")

        self.verticalLayout.addWidget(self.listProjects)

        self.splitter = QSplitter(self.boxProjects)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.btnAddProject = QPushButton(self.splitter)
        self.btnAddProject.setObjectName(u"btnAddProject")
        self.splitter.addWidget(self.btnAddProject)
        self.btnDelProject = QPushButton(self.splitter)
        self.btnDelProject.setObjectName(u"btnDelProject")
        self.splitter.addWidget(self.btnDelProject)

        self.verticalLayout.addWidget(self.splitter)


        self.horizontalLayout.addWidget(self.boxProjects)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMaximumSize(QSize(150, 16777215))
        self.groupBox.setFlat(True)
        self.verticalLayout_4 = QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.listAssets = QListView(self.groupBox)
        self.listAssets.setObjectName(u"listAssets")

        self.verticalLayout_4.addWidget(self.listAssets)

        self.splitter_2 = QSplitter(self.groupBox)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Horizontal)
        self.btnAddAsset = QPushButton(self.splitter_2)
        self.btnAddAsset.setObjectName(u"btnAddAsset")
        self.splitter_2.addWidget(self.btnAddAsset)
        self.btnDelAsset = QPushButton(self.splitter_2)
        self.btnDelAsset.setObjectName(u"btnDelAsset")
        self.splitter_2.addWidget(self.btnDelAsset)

        self.verticalLayout_4.addWidget(self.splitter_2)


        self.horizontalLayout.addWidget(self.groupBox)

        self.boxASS = QGroupBox(self.centralwidget)
        self.boxASS.setObjectName(u"boxASS")
        self.boxASS.setMaximumSize(QSize(150, 16777215))
        self.boxASS.setFlat(True)
        self.verticalLayout_2 = QVBoxLayout(self.boxASS)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listSequences = QListView(self.boxASS)
        self.listSequences.setObjectName(u"listSequences")

        self.verticalLayout_2.addWidget(self.listSequences)

        self.splitter_3 = QSplitter(self.boxASS)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Orientation.Horizontal)
        self.btnAddSequence = QPushButton(self.splitter_3)
        self.btnAddSequence.setObjectName(u"btnAddSequence")
        self.splitter_3.addWidget(self.btnAddSequence)
        self.btnDelSequence = QPushButton(self.splitter_3)
        self.btnDelSequence.setObjectName(u"btnDelSequence")
        self.splitter_3.addWidget(self.btnDelSequence)

        self.verticalLayout_2.addWidget(self.splitter_3)

        self.listShots = QListView(self.boxASS)
        self.listShots.setObjectName(u"listShots")

        self.verticalLayout_2.addWidget(self.listShots)

        self.splitter_4 = QSplitter(self.boxASS)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Orientation.Horizontal)
        self.btnAddShot = QPushButton(self.splitter_4)
        self.btnAddShot.setObjectName(u"btnAddShot")
        self.splitter_4.addWidget(self.btnAddShot)
        self.btnDelShot = QPushButton(self.splitter_4)
        self.btnDelShot.setObjectName(u"btnDelShot")
        self.splitter_4.addWidget(self.btnDelShot)

        self.verticalLayout_2.addWidget(self.splitter_4)


        self.horizontalLayout.addWidget(self.boxASS)

        self.boxProperties = QGroupBox(self.centralwidget)
        self.boxProperties.setObjectName(u"boxProperties")
        self.boxProperties.setMinimumSize(QSize(500, 0))
        self.boxProperties.setMaximumSize(QSize(500, 16777215))
        self.boxProperties.setFlat(True)
        self.verticalLayout_3 = QVBoxLayout(self.boxProperties)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.layoutProperties = QVBoxLayout()
        self.layoutProperties.setObjectName(u"layoutProperties")

        self.verticalLayout_3.addLayout(self.layoutProperties)


        self.horizontalLayout.addWidget(self.boxProperties)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        ProjectManager.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ProjectManager)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1013, 33))
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuEve = QMenu(self.menubar)
        self.menuEve.setObjectName(u"menuEve")
        ProjectManager.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(ProjectManager)
        self.statusbar.setObjectName(u"statusbar")
        ProjectManager.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuEve.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuHelp.addAction(self.actionEveDocs)
        self.menuEve.addAction(self.actionSettings)

        self.retranslateUi(ProjectManager)

        QMetaObject.connectSlotsByName(ProjectManager)
    # setupUi

    def retranslateUi(self, ProjectManager):
        ProjectManager.setWindowTitle(QCoreApplication.translate("ProjectManager", u"Eve Project Manager", None))
        self.actionEveDocs.setText(QCoreApplication.translate("ProjectManager", u"Eve Documentation", None))
        self.actionSettings.setText(QCoreApplication.translate("ProjectManager", u"Settings", None))
        self.actionCreateDatabase.setText(QCoreApplication.translate("ProjectManager", u"Create Database", None))
        self.boxProjects.setTitle(QCoreApplication.translate("ProjectManager", u"Projects", None))
        self.btnAddProject.setText(QCoreApplication.translate("ProjectManager", u"+", None))
        self.btnDelProject.setText(QCoreApplication.translate("ProjectManager", u"-", None))
        self.groupBox.setTitle(QCoreApplication.translate("ProjectManager", u"Assets", None))
        self.btnAddAsset.setText(QCoreApplication.translate("ProjectManager", u"+", None))
        self.btnDelAsset.setText(QCoreApplication.translate("ProjectManager", u"-", None))
        self.boxASS.setTitle(QCoreApplication.translate("ProjectManager", u"Sequences | Shots", None))
        self.btnAddSequence.setText(QCoreApplication.translate("ProjectManager", u"+", None))
        self.btnDelSequence.setText(QCoreApplication.translate("ProjectManager", u"-", None))
        self.btnAddShot.setText(QCoreApplication.translate("ProjectManager", u"+", None))
        self.btnDelShot.setText(QCoreApplication.translate("ProjectManager", u"-", None))
        self.boxProperties.setTitle(QCoreApplication.translate("ProjectManager", u"Properties", None))
        self.menuHelp.setTitle(QCoreApplication.translate("ProjectManager", u"Help", None))
        self.menuEve.setTitle(QCoreApplication.translate("ProjectManager", u"Eve", None))
    # retranslateUi

