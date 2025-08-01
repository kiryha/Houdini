# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_pm_add_sequence.ui'
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

class Ui_AddSequence(object):
    def setupUi(self, AddSequence):
        if not AddSequence.objectName():
            AddSequence.setObjectName(u"AddSequence")
        AddSequence.resize(370, 89)
        self.verticalLayout = QVBoxLayout(AddSequence)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutSequence = QVBoxLayout()
        self.layoutSequence.setObjectName(u"layoutSequence")

        self.verticalLayout.addLayout(self.layoutSequence)

        self.btnAddSequence = QPushButton(AddSequence)
        self.btnAddSequence.setObjectName(u"btnAddSequence")
        self.btnAddSequence.setMinimumSize(QSize(0, 40))

        self.verticalLayout.addWidget(self.btnAddSequence)


        self.retranslateUi(AddSequence)

        QMetaObject.connectSlotsByName(AddSequence)
    # setupUi

    def retranslateUi(self, AddSequence):
        AddSequence.setWindowTitle(QCoreApplication.translate("AddSequence", u"Add Sequence", None))
        self.btnAddSequence.setText(QCoreApplication.translate("AddSequence", u"Add Sequence", None))
    # retranslateUi

