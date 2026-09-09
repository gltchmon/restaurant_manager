# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menu_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(592, 421)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.menu_addItem_comboBox = QComboBox(self.frame)
        self.menu_addItem_comboBox.setObjectName(u"menu_addItem_comboBox")

        self.verticalLayout_2.addWidget(self.menu_addItem_comboBox)


        self.horizontalLayout_3.addWidget(self.frame)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(self.frame_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.menu_addItem_price = QDoubleSpinBox(self.frame_2)
        self.menu_addItem_price.setObjectName(u"menu_addItem_price")

        self.verticalLayout_3.addWidget(self.menu_addItem_price)


        self.horizontalLayout_3.addWidget(self.frame_2)

        self.menu_addItem_button = QPushButton(Form)
        self.menu_addItem_button.setObjectName(u"menu_addItem_button")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.menu_addItem_button.sizePolicy().hasHeightForWidth())
        self.menu_addItem_button.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.menu_addItem_button)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.menu_listWidget = QListWidget(Form)
        self.menu_listWidget.setObjectName(u"menu_listWidget")

        self.verticalLayout.addWidget(self.menu_listWidget)

        self.frame_3 = QFrame(Form)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.menu_deleteItems_button = QPushButton(self.frame_3)
        self.menu_deleteItems_button.setObjectName(u"menu_deleteItems_button")

        self.horizontalLayout.addWidget(self.menu_deleteItems_button)


        self.verticalLayout.addWidget(self.frame_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Item name:", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Price:", None))
        self.menu_addItem_button.setText(QCoreApplication.translate("Form", u"Add item to menu", None))
        self.menu_deleteItems_button.setText(QCoreApplication.translate("Form", u"Delete item from menu", None))
    # retranslateUi

