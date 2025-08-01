# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_pm_add_asset.ui'
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

class Ui_AddAsset(object):
    def setupUi(self, AddAsset):
        if not AddAsset.objectName():
            AddAsset.setObjectName(u"AddAsset")
        AddAsset.resize(370, 89)
        self.verticalLayout = QVBoxLayout(AddAsset)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutAsset = QVBoxLayout()
        self.layoutAsset.setObjectName(u"layoutAsset")

        self.verticalLayout.addLayout(self.layoutAsset)

        self.btnAddAsset = QPushButton(AddAsset)
        self.btnAddAsset.setObjectName(u"btnAddAsset")
        self.btnAddAsset.setMinimumSize(QSize(0, 40))

        self.verticalLayout.addWidget(self.btnAddAsset)


        self.retranslateUi(AddAsset)

        QMetaObject.connectSlotsByName(AddAsset)
    # setupUi

    def retranslateUi(self, AddAsset):
        AddAsset.setWindowTitle(QCoreApplication.translate("AddAsset", u"Add Asset", None))
        self.btnAddAsset.setText(QCoreApplication.translate("AddAsset", u"Add Asset", None))
    # retranslateUi

