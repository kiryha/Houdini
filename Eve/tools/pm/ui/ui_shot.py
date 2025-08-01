# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_shot.ui'
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
    QListView, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QTextEdit, QVBoxLayout, QWidget)

class Ui_Shot(object):
    def setupUi(self, Shot):
        if not Shot.objectName():
            Shot.setObjectName(u"Shot")
        Shot.resize(369, 460)
        self.verticalLayout = QVBoxLayout(Shot)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter_3 = QSplitter(Shot)
        self.splitter_3.setObjectName(u"splitter_3")
        self.splitter_3.setOrientation(Qt.Horizontal)
        self.label_3 = QLabel(self.splitter_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(120, 0))
        self.label_3.setMaximumSize(QSize(120, 16777215))
        self.splitter_3.addWidget(self.label_3)
        self.linProjectName = QLineEdit(self.splitter_3)
        self.linProjectName.setObjectName(u"linProjectName")
        self.linProjectName.setEnabled(False)
        self.linProjectName.setAlignment(Qt.AlignCenter)
        self.splitter_3.addWidget(self.linProjectName)

        self.verticalLayout.addWidget(self.splitter_3)

        self.splitter_4 = QSplitter(Shot)
        self.splitter_4.setObjectName(u"splitter_4")
        self.splitter_4.setOrientation(Qt.Horizontal)
        self.label_5 = QLabel(self.splitter_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(120, 0))
        self.label_5.setMaximumSize(QSize(120, 16777215))
        self.splitter_4.addWidget(self.label_5)
        self.linSequenceName = QLineEdit(self.splitter_4)
        self.linSequenceName.setObjectName(u"linSequenceName")
        self.linSequenceName.setEnabled(False)
        self.linSequenceName.setAlignment(Qt.AlignCenter)
        self.splitter_4.addWidget(self.linSequenceName)

        self.verticalLayout.addWidget(self.splitter_4)

        self.splitter_8 = QSplitter(Shot)
        self.splitter_8.setObjectName(u"splitter_8")
        self.splitter_8.setOrientation(Qt.Horizontal)
        self.label = QLabel(self.splitter_8)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(120, 0))
        self.label.setMaximumSize(QSize(120, 16777215))
        self.splitter_8.addWidget(self.label)
        self.linShotName = QLineEdit(self.splitter_8)
        self.linShotName.setObjectName(u"linShotName")
        self.linShotName.setAlignment(Qt.AlignCenter)
        self.splitter_8.addWidget(self.linShotName)

        self.verticalLayout.addWidget(self.splitter_8)

        self.splitter_5 = QSplitter(Shot)
        self.splitter_5.setObjectName(u"splitter_5")
        self.splitter_5.setOrientation(Qt.Horizontal)
        self.label_7 = QLabel(self.splitter_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(120, 0))
        self.label_7.setMaximumSize(QSize(120, 16777215))
        self.splitter_5.addWidget(self.label_7)
        self.linStartFrame = QLineEdit(self.splitter_5)
        self.linStartFrame.setObjectName(u"linStartFrame")
        self.linStartFrame.setAlignment(Qt.AlignCenter)
        self.splitter_5.addWidget(self.linStartFrame)
        self.linEndFrame = QLineEdit(self.splitter_5)
        self.linEndFrame.setObjectName(u"linEndFrame")
        self.linEndFrame.setAlignment(Qt.AlignCenter)
        self.splitter_5.addWidget(self.linEndFrame)

        self.verticalLayout.addWidget(self.splitter_5)

        self.splitter_6 = QSplitter(Shot)
        self.splitter_6.setObjectName(u"splitter_6")
        self.splitter_6.setOrientation(Qt.Horizontal)
        self.label_8 = QLabel(self.splitter_6)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(120, 0))
        self.label_8.setMaximumSize(QSize(120, 16777215))
        self.splitter_6.addWidget(self.label_8)
        self.linWidth = QLineEdit(self.splitter_6)
        self.linWidth.setObjectName(u"linWidth")
        self.linWidth.setAlignment(Qt.AlignCenter)
        self.splitter_6.addWidget(self.linWidth)
        self.linHeight = QLineEdit(self.splitter_6)
        self.linHeight.setObjectName(u"linHeight")
        self.linHeight.setAlignment(Qt.AlignCenter)
        self.splitter_6.addWidget(self.linHeight)

        self.verticalLayout.addWidget(self.splitter_6)

        self.splitter_7 = QSplitter(Shot)
        self.splitter_7.setObjectName(u"splitter_7")
        self.splitter_7.setOrientation(Qt.Horizontal)
        self.label_2 = QLabel(self.splitter_7)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(120, 0))
        self.label_2.setMaximumSize(QSize(120, 16777215))
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.splitter_7.addWidget(self.label_2)
        self.splitter = QSplitter(self.splitter_7)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.listAssets = QListView(self.splitter)
        self.listAssets.setObjectName(u"listAssets")
        self.listAssets.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.splitter.addWidget(self.listAssets)
        self.splitter_2 = QSplitter(self.splitter)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.btnLinkAsset = QPushButton(self.splitter_2)
        self.btnLinkAsset.setObjectName(u"btnLinkAsset")
        self.btnLinkAsset.setMaximumSize(QSize(16777215, 30))
        self.splitter_2.addWidget(self.btnLinkAsset)
        self.btnUnlinkAsset = QPushButton(self.splitter_2)
        self.btnUnlinkAsset.setObjectName(u"btnUnlinkAsset")
        self.btnUnlinkAsset.setMaximumSize(QSize(16777215, 30))
        self.splitter_2.addWidget(self.btnUnlinkAsset)
        self.splitter.addWidget(self.splitter_2)
        self.splitter_7.addWidget(self.splitter)

        self.verticalLayout.addWidget(self.splitter_7)

        self.label_4 = QLabel(Shot)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.txtDescription = QTextEdit(Shot)
        self.txtDescription.setObjectName(u"txtDescription")
        self.txtDescription.setMaximumSize(QSize(16777215, 100))

        self.verticalLayout.addWidget(self.txtDescription)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Shot)

        QMetaObject.connectSlotsByName(Shot)
    # setupUi

    def retranslateUi(self, Shot):
        Shot.setWindowTitle(QCoreApplication.translate("Shot", u"Shot", None))
        self.label_3.setText(QCoreApplication.translate("Shot", u"Project Name", None))
        self.label_5.setText(QCoreApplication.translate("Shot", u"Sequence Name", None))
        self.label.setText(QCoreApplication.translate("Shot", u"Shot Name", None))
        self.label_7.setText(QCoreApplication.translate("Shot", u"Start | End", None))
        self.label_8.setText(QCoreApplication.translate("Shot", u"Width | Height", None))
        self.label_2.setText(QCoreApplication.translate("Shot", u"Linked Assets", None))
        self.btnLinkAsset.setText(QCoreApplication.translate("Shot", u"Link Asset", None))
        self.btnUnlinkAsset.setText(QCoreApplication.translate("Shot", u"Break Link", None))
        self.label_4.setText(QCoreApplication.translate("Shot", u"Shot Description", None))
    # retranslateUi

