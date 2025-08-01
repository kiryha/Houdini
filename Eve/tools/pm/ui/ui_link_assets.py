# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_link_assets.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QLabel, QLineEdit,
    QListView, QPushButton, QSizePolicy, QSplitter,
    QVBoxLayout, QWidget)

class Ui_LinkAssets(object):
    def setupUi(self, LinkAssets):
        if not LinkAssets.objectName():
            LinkAssets.setObjectName(u"LinkAssets")
        LinkAssets.resize(241, 358)
        self.verticalLayout = QVBoxLayout(LinkAssets)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter = QSplitter(LinkAssets)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.label = QLabel(self.splitter)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(60, 0))
        self.label.setMaximumSize(QSize(85, 16777215))
        self.splitter.addWidget(self.label)
        self.linShotName = QLineEdit(self.splitter)
        self.linShotName.setObjectName(u"linShotName")
        self.linShotName.setEnabled(False)
        self.linShotName.setAlignment(Qt.AlignCenter)
        self.splitter.addWidget(self.linShotName)

        self.verticalLayout.addWidget(self.splitter)

        self.listAssets = QListView(LinkAssets)
        self.listAssets.setObjectName(u"listAssets")
        self.listAssets.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.verticalLayout.addWidget(self.listAssets)

        self.btnLinkAssets = QPushButton(LinkAssets)
        self.btnLinkAssets.setObjectName(u"btnLinkAssets")
        self.btnLinkAssets.setMinimumSize(QSize(0, 40))

        self.verticalLayout.addWidget(self.btnLinkAssets)


        self.retranslateUi(LinkAssets)

        QMetaObject.connectSlotsByName(LinkAssets)
    # setupUi

    def retranslateUi(self, LinkAssets):
        LinkAssets.setWindowTitle(QCoreApplication.translate("LinkAssets", u"Link Assets", None))
        self.label.setText(QCoreApplication.translate("LinkAssets", u"Shot Name", None))
        self.btnLinkAssets.setText(QCoreApplication.translate("LinkAssets", u"Link Selected Assets to the Shot", None))
    # retranslateUi

