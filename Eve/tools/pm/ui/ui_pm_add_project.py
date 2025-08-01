# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_pm_add_project.ui'
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
from PySide6.QtWidgets import (QApplication, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_AddProject(object):
    def setupUi(self, AddProject):
        if not AddProject.objectName():
            AddProject.setObjectName(u"AddProject")
        AddProject.resize(369, 92)
        self.verticalLayout = QVBoxLayout(AddProject)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutProject = QVBoxLayout()
        self.layoutProject.setObjectName(u"layoutProject")

        self.verticalLayout.addLayout(self.layoutProject)

        self.btnAddProject = QPushButton(AddProject)
        self.btnAddProject.setObjectName(u"btnAddProject")
        self.btnAddProject.setMinimumSize(QSize(0, 40))

        self.verticalLayout.addWidget(self.btnAddProject)


        self.retranslateUi(AddProject)

        QMetaObject.connectSlotsByName(AddProject)
    # setupUi

    def retranslateUi(self, AddProject):
        AddProject.setWindowTitle(QCoreApplication.translate("AddProject", u"Add Project", None))
        self.btnAddProject.setText(QCoreApplication.translate("AddProject", u"Add Project", None))
    # retranslateUi

