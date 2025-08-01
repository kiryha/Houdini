# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_asset_properties.ui'
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

class Ui_AssetProperties(object):
    def setupUi(self, AssetProperties):
        if not AssetProperties.objectName():
            AssetProperties.setObjectName(u"AssetProperties")
        AssetProperties.resize(369, 101)
        self.verticalLayout = QVBoxLayout(AssetProperties)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutAsset = QVBoxLayout()
        self.layoutAsset.setObjectName(u"layoutAsset")

        self.verticalLayout.addLayout(self.layoutAsset)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.btnUpdateAsset = QPushButton(AssetProperties)
        self.btnUpdateAsset.setObjectName(u"btnUpdateAsset")
        self.btnUpdateAsset.setMinimumSize(QSize(0, 45))

        self.verticalLayout.addWidget(self.btnUpdateAsset)

        self.splitter_5 = QSplitter(AssetProperties)
        self.splitter_5.setObjectName(u"splitter_5")
        self.splitter_5.setOrientation(Qt.Horizontal)
        self.btnCreateHoudiniFile = QPushButton(self.splitter_5)
        self.btnCreateHoudiniFile.setObjectName(u"btnCreateHoudiniFile")
        self.splitter_5.addWidget(self.btnCreateHoudiniFile)
        self.btnOpenHoudiniFile = QPushButton(self.splitter_5)
        self.btnOpenHoudiniFile.setObjectName(u"btnOpenHoudiniFile")
        self.splitter_5.addWidget(self.btnOpenHoudiniFile)

        self.verticalLayout.addWidget(self.splitter_5)


        self.retranslateUi(AssetProperties)

        QMetaObject.connectSlotsByName(AssetProperties)
    # setupUi

    def retranslateUi(self, AssetProperties):
        AssetProperties.setWindowTitle(QCoreApplication.translate("AssetProperties", u"Form", None))
        self.btnUpdateAsset.setText(QCoreApplication.translate("AssetProperties", u"Update Asset Data", None))
        self.btnCreateHoudiniFile.setText(QCoreApplication.translate("AssetProperties", u"Create Houdini Scene", None))
        self.btnOpenHoudiniFile.setText(QCoreApplication.translate("AssetProperties", u"Open Houdini Scene", None))
    # retranslateUi

