# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_sequence_properties.ui'
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
    QVBoxLayout, QWidget)

class Ui_SequenceProperties(object):
    def setupUi(self, SequenceProperties):
        if not SequenceProperties.objectName():
            SequenceProperties.setObjectName(u"SequenceProperties")
        SequenceProperties.resize(369, 103)
        self.verticalLayout = QVBoxLayout(SequenceProperties)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.layoutSequence = QVBoxLayout()
        self.layoutSequence.setObjectName(u"layoutSequence")

        self.verticalLayout.addLayout(self.layoutSequence)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.btnUpdateSequence = QPushButton(SequenceProperties)
        self.btnUpdateSequence.setObjectName(u"btnUpdateSequence")
        self.btnUpdateSequence.setMinimumSize(QSize(0, 45))

        self.verticalLayout.addWidget(self.btnUpdateSequence)


        self.retranslateUi(SequenceProperties)

        QMetaObject.connectSlotsByName(SequenceProperties)
    # setupUi

    def retranslateUi(self, SequenceProperties):
        SequenceProperties.setWindowTitle(QCoreApplication.translate("SequenceProperties", u"Form", None))
        self.btnUpdateSequence.setText(QCoreApplication.translate("SequenceProperties", u"Update Sequence Data", None))
    # retranslateUi

