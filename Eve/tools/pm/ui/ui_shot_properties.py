# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_shot_properties.ui'
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

class Ui_ShotProperties(object):
    def setupUi(self, ShotProperties):
        if not ShotProperties.objectName():
            ShotProperties.setObjectName(u"ShotProperties")
        ShotProperties.resize(370, 193)
        self.verticalLayout = QVBoxLayout(ShotProperties)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutShot = QVBoxLayout()
        self.layoutShot.setObjectName(u"layoutShot")

        self.verticalLayout.addLayout(self.layoutShot)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.btnUpdateShot = QPushButton(ShotProperties)
        self.btnUpdateShot.setObjectName(u"btnUpdateShot")
        self.btnUpdateShot.setMinimumSize(QSize(0, 45))

        self.verticalLayout.addWidget(self.btnUpdateShot)

        self.splitter_6 = QSplitter(ShotProperties)
        self.splitter_6.setObjectName(u"splitter_6")
        self.splitter_6.setOrientation(Qt.Horizontal)
        self.btnCreateShot = QPushButton(self.splitter_6)
        self.btnCreateShot.setObjectName(u"btnCreateShot")
        self.splitter_6.addWidget(self.btnCreateShot)
        self.btnOpenShot = QPushButton(self.splitter_6)
        self.btnOpenShot.setObjectName(u"btnOpenShot")
        self.splitter_6.addWidget(self.btnOpenShot)

        self.verticalLayout.addWidget(self.splitter_6)

        self.splitter_7 = QSplitter(ShotProperties)
        self.splitter_7.setObjectName(u"splitter_7")
        self.splitter_7.setOrientation(Qt.Horizontal)
        self.btnCreateShotAnim = QPushButton(self.splitter_7)
        self.btnCreateShotAnim.setObjectName(u"btnCreateShotAnim")
        self.splitter_7.addWidget(self.btnCreateShotAnim)
        self.btnOpenShotAnim = QPushButton(self.splitter_7)
        self.btnOpenShotAnim.setObjectName(u"btnOpenShotAnim")
        self.splitter_7.addWidget(self.btnOpenShotAnim)

        self.verticalLayout.addWidget(self.splitter_7)


        self.retranslateUi(ShotProperties)

        QMetaObject.connectSlotsByName(ShotProperties)
    # setupUi

    def retranslateUi(self, ShotProperties):
        ShotProperties.setWindowTitle(QCoreApplication.translate("ShotProperties", u"Form", None))
        self.btnUpdateShot.setText(QCoreApplication.translate("ShotProperties", u"Update Shot Data", None))
        self.btnCreateShot.setText(QCoreApplication.translate("ShotProperties", u"Create Render Scene", None))
        self.btnOpenShot.setText(QCoreApplication.translate("ShotProperties", u"Open Render Scene", None))
        self.btnCreateShotAnim.setText(QCoreApplication.translate("ShotProperties", u"Create Animation Scene", None))
        self.btnOpenShotAnim.setText(QCoreApplication.translate("ShotProperties", u"Open Animation Scene", None))
    # retranslateUi

