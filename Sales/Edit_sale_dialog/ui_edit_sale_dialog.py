# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'edit_sale_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDateEdit, QDialog, QDoubleSpinBox,
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpinBox, QVBoxLayout, QWidget)

class Ui_edit_sale_dialog(object):
    def setupUi(self, edit_sale_dialog):
        if not edit_sale_dialog.objectName():
            edit_sale_dialog.setObjectName(u"edit_sale_dialog")
        edit_sale_dialog.resize(293, 236)
        self.verticalLayout_4 = QVBoxLayout(edit_sale_dialog)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.sale_name = QLabel(edit_sale_dialog)
        self.sale_name.setObjectName(u"sale_name")

        self.verticalLayout_4.addWidget(self.sale_name)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(edit_sale_dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.edit_sale_date = QDateEdit(edit_sale_dialog)
        self.edit_sale_date.setObjectName(u"edit_sale_date")

        self.verticalLayout.addWidget(self.edit_sale_date)


        self.verticalLayout_4.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(edit_sale_dialog)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.edit_sale_qty = QSpinBox(edit_sale_dialog)
        self.edit_sale_qty.setObjectName(u"edit_sale_qty")

        self.verticalLayout_2.addWidget(self.edit_sale_qty)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_2 = QLabel(edit_sale_dialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.edit_sale_price = QDoubleSpinBox(edit_sale_dialog)
        self.edit_sale_price.setObjectName(u"edit_sale_price")

        self.verticalLayout_3.addWidget(self.edit_sale_price)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.edit_confirm_button = QPushButton(edit_sale_dialog)
        self.edit_confirm_button.setObjectName(u"edit_confirm_button")

        self.horizontalLayout.addWidget(self.edit_confirm_button)

        self.edit_cancel_button = QPushButton(edit_sale_dialog)
        self.edit_cancel_button.setObjectName(u"edit_cancel_button")

        self.horizontalLayout.addWidget(self.edit_cancel_button)


        self.verticalLayout_4.addLayout(self.horizontalLayout)


        self.retranslateUi(edit_sale_dialog)

        QMetaObject.connectSlotsByName(edit_sale_dialog)
    # setupUi

    def retranslateUi(self, edit_sale_dialog):
        edit_sale_dialog.setWindowTitle(QCoreApplication.translate("edit_sale_dialog", u"Dialog", None))
        self.sale_name.setText(QCoreApplication.translate("edit_sale_dialog", u"Edit sale for ", None))
        self.label.setText(QCoreApplication.translate("edit_sale_dialog", u"Date:", None))
        self.label_3.setText(QCoreApplication.translate("edit_sale_dialog", u"Quantity:", None))
        self.label_2.setText(QCoreApplication.translate("edit_sale_dialog", u"Price:", None))
        self.edit_confirm_button.setText(QCoreApplication.translate("edit_sale_dialog", u"Confirm", None))
        self.edit_cancel_button.setText(QCoreApplication.translate("edit_sale_dialog", u"Cancel", None))
    # retranslateUi

