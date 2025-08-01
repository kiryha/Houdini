# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_pm_warning.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Warning(object):
    def setupUi(self, Warning):
        if not Warning.objectName():
            Warning.setObjectName(u"Warning")
        Warning.resize(347, 60)
        self.verticalLayout = QVBoxLayout(Warning)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labWarning = QLabel(Warning)
        self.labWarning.setObjectName(u"labWarning")
        self.labWarning.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.labWarning)

        self.buttonBox = QDialogButtonBox(Warning)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Yes)
        self.buttonBox.setCenterButtons(True)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Warning)
        self.buttonBox.accepted.connect(Warning.accept)
        self.buttonBox.rejected.connect(Warning.reject)

        QMetaObject.connectSlotsByName(Warning)
    # setupUi

    def retranslateUi(self, Warning):
        Warning.setWindowTitle(QCoreApplication.translate("Warning", u"Warning", None))
        self.labWarning.setText(QCoreApplication.translate("Warning", u"TextLabel", None))
    # retranslateUi

