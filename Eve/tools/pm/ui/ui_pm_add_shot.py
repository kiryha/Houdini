# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_pm_add_shot.ui'
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

class Ui_AddShot(object):
    def setupUi(self, AddShot):
        if not AddShot.objectName():
            AddShot.setObjectName(u"AddShot")
        AddShot.resize(370, 89)
        self.verticalLayout = QVBoxLayout(AddShot)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutShot = QVBoxLayout()
        self.layoutShot.setObjectName(u"layoutShot")

        self.verticalLayout.addLayout(self.layoutShot)

        self.btnAddShot = QPushButton(AddShot)
        self.btnAddShot.setObjectName(u"btnAddShot")
        self.btnAddShot.setMinimumSize(QSize(0, 40))

        self.verticalLayout.addWidget(self.btnAddShot)


        self.retranslateUi(AddShot)

        QMetaObject.connectSlotsByName(AddShot)
    # setupUi

    def retranslateUi(self, AddShot):
        AddShot.setWindowTitle(QCoreApplication.translate("AddShot", u"Add Shot", None))
        self.btnAddShot.setText(QCoreApplication.translate("AddShot", u"Add Shot", None))
    # retranslateUi

