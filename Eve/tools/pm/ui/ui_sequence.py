# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_sequence.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QSizePolicy,
    QSpacerItem, QSplitter, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Sequence(object):
    def setupUi(self, Sequence):
        if not Sequence.objectName():
            Sequence.setObjectName(u"Sequence")
        Sequence.resize(367, 182)
        self.shotLayout = QVBoxLayout(Sequence)
        self.shotLayout.setContentsMargins(0, 0, 0, 0)
        self.shotLayout.setObjectName(u"shotLayout")
        self.splitter_2 = QSplitter(Sequence)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.label_3 = QLabel(self.splitter_2)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 0))
        self.label_3.setMaximumSize(QSize(120, 16777215))
        self.splitter_2.addWidget(self.label_3)
        self.linProjectName = QLineEdit(self.splitter_2)
        self.linProjectName.setObjectName(u"linProjectName")
        self.linProjectName.setEnabled(False)
        self.linProjectName.setAlignment(Qt.AlignCenter)
        self.splitter_2.addWidget(self.linProjectName)

        self.shotLayout.addWidget(self.splitter_2)

        self.splitter = QSplitter(Sequence)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.label = QLabel(self.splitter)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(120, 0))
        self.label.setMaximumSize(QSize(120, 16777215))
        self.splitter.addWidget(self.label)
        self.linSequenceName = QLineEdit(self.splitter)
        self.linSequenceName.setObjectName(u"linSequenceName")
        self.linSequenceName.setAlignment(Qt.AlignCenter)
        self.splitter.addWidget(self.linSequenceName)

        self.shotLayout.addWidget(self.splitter)

        self.label_2 = QLabel(Sequence)
        self.label_2.setObjectName(u"label_2")

        self.shotLayout.addWidget(self.label_2)

        self.txtDescription = QTextEdit(Sequence)
        self.txtDescription.setObjectName(u"txtDescription")
        self.txtDescription.setMaximumSize(QSize(16777215, 100))

        self.shotLayout.addWidget(self.txtDescription)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.shotLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Sequence)

        QMetaObject.connectSlotsByName(Sequence)
    # setupUi

    def retranslateUi(self, Sequence):
        Sequence.setWindowTitle(QCoreApplication.translate("Sequence", u"Sequence", None))
        self.label_3.setText(QCoreApplication.translate("Sequence", u"Project Name", None))
        self.label.setText(QCoreApplication.translate("Sequence", u"Sequence Name", None))
        self.label_2.setText(QCoreApplication.translate("Sequence", u"Sequence Description:", None))
    # retranslateUi

