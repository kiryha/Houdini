# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_asset.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSplitter,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_Asset(object):
    def setupUi(self, Asset):
        if not Asset.objectName():
            Asset.setObjectName(u"Asset")
        Asset.resize(367, 274)
        self.shotLayout = QVBoxLayout(Asset)
        self.shotLayout.setContentsMargins(0, 0, 0, 0)
        self.shotLayout.setObjectName(u"shotLayout")
        self.splitter_4 = QSplitter(Asset)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Horizontal)
        self.label_5 = QLabel(self.splitter_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(120, 0))
        self.label_5.setMaximumSize(QSize(120, 16777215))
        self.splitter_4.addWidget(self.label_5)
        self.linProjectName = QLineEdit(self.splitter_4)
        self.linProjectName.setObjectName(u"linProjectName")
        self.linProjectName.setEnabled(False)
        self.linProjectName.setAlignment(Qt.AlignCenter)
        self.splitter_4.addWidget(self.linProjectName)

        self.shotLayout.addWidget(self.splitter_4)

        self.splitter = QSplitter(Asset)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.label = QLabel(self.splitter)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(120, 0))
        self.label.setMaximumSize(QSize(120, 16777215))
        self.splitter.addWidget(self.label)
        self.linAssetName = QLineEdit(self.splitter)
        self.linAssetName.setObjectName(u"linAssetName")
        self.linAssetName.setAlignment(Qt.AlignCenter)
        self.splitter.addWidget(self.linAssetName)

        self.shotLayout.addWidget(self.splitter)

        self.splitter_2 = QSplitter(Asset)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.label_4 = QLabel(self.splitter_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(120, 0))
        self.label_4.setMaximumSize(QSize(120, 16777215))
        self.splitter_2.addWidget(self.label_4)
        self.comAssetType = QComboBox(self.splitter_2)
        self.comAssetType.setObjectName(u"comAssetType")
        self.splitter_2.addWidget(self.comAssetType)

        self.shotLayout.addWidget(self.splitter_2)

        self.splitter_5 = QSplitter(Asset)
        self.splitter_5.setObjectName(u"splitter_5")
        self.splitter_5.setOrientation(Qt.Horizontal)
        self.label_6 = QLabel(self.splitter_5)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(120, 0))
        self.label_6.setMaximumSize(QSize(120, 16777215))
        self.splitter_5.addWidget(self.label_6)
        self.linAssetPublish = QLineEdit(self.splitter_5)
        self.linAssetPublish.setObjectName(u"linAssetPublish")
        self.linAssetPublish.setEnabled(False)
        self.linAssetPublish.setAlignment(Qt.AlignCenter)
        self.splitter_5.addWidget(self.linAssetPublish)

        self.shotLayout.addWidget(self.splitter_5)

        self.pushButton = QPushButton(Asset)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 35))

        self.shotLayout.addWidget(self.pushButton)

        self.label_2 = QLabel(Asset)
        self.label_2.setObjectName(u"label_2")

        self.shotLayout.addWidget(self.label_2)

        self.txtDescription = QTextEdit(Asset)
        self.txtDescription.setObjectName(u"txtDescription")
        self.txtDescription.setMaximumSize(QSize(16777215, 100))

        self.shotLayout.addWidget(self.txtDescription)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.shotLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Asset)

        QMetaObject.connectSlotsByName(Asset)
    # setupUi

    def retranslateUi(self, Asset):
        Asset.setWindowTitle(QCoreApplication.translate("Asset", u"Asset", None))
        self.label_5.setText(QCoreApplication.translate("Asset", u"Project Name", None))
        self.label.setText(QCoreApplication.translate("Asset", u"Asset Name", None))
        self.label_4.setText(QCoreApplication.translate("Asset", u"Asset Type", None))
        self.label_6.setText(QCoreApplication.translate("Asset", u"Published Version", None))
        self.pushButton.setText(QCoreApplication.translate("Asset", u"Asset Configuration Manager", None))
        self.label_2.setText(QCoreApplication.translate("Asset", u"Asset Description:", None))
    # retranslateUi

