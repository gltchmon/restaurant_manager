# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStackedWidget, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.action_logOut = QAction(MainWindow)
        self.action_logOut.setObjectName(u"action_logOut")
        self.action_delete_account = QAction(MainWindow)
        self.action_delete_account.setObjectName(u"action_delete_account")
        self.action_manage_sales = QAction(MainWindow)
        self.action_manage_menu = QAction(MainWindow)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.main_stackedWidget = QStackedWidget(self.centralwidget)
        self.main_stackedWidget.setObjectName(u"main_stackedWidget")
        
    

        self.verticalLayout.addWidget(self.main_stackedWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))

        self.menu_option_menu = QMenu(self.menubar)
        self.menu_option_menu.setObjectName(u"menu_option_menu")
        self.menu_option_menu.addAction(self.action_manage_menu)
        self.menu_option_sales = QMenu(self.menubar)
        self.menu_option_sales.setObjectName(u"menu_option_sales")
        self.menu_option_expenses = QMenu(self.menubar)
        self.menu_option_expenses.setObjectName(u"menu_option_expenses")
        self.menu_option_account = QMenu(self.menubar)
        self.menu_option_account.setObjectName(u"menu_option_account")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_option_menu.menuAction())
        self.menubar.addAction(self.menu_option_sales.menuAction())
        self.menu_option_sales.addAction(self.action_manage_sales)
        self.menubar.addAction(self.menu_option_expenses.menuAction())
        self.menubar.addAction(self.menu_option_account.menuAction())
        self.menu_option_account.addAction(self.action_logOut)
        self.menu_option_account.addAction(self.action_delete_account)

        self.retranslateUi(MainWindow)

        self.main_stackedWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.action_logOut.setText(QCoreApplication.translate("MainWindow", u"Log out", None))
        self.action_delete_account.setText(QCoreApplication.translate("MainWindow", u"Delete account", None))
        self.action_manage_sales.setText(QCoreApplication.translate("MainWindow", u"Manage sales", None))
        self.action_manage_menu.setText(QCoreApplication.translate("MainWindow", u"Manage menu", None))
        self.menu_option_menu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.menu_option_sales.setTitle(QCoreApplication.translate("MainWindow", u"Sales", None))
        self.menu_option_expenses.setTitle(QCoreApplication.translate("MainWindow", u"Expenses", None))
        self.menu_option_account.setTitle(QCoreApplication.translate("MainWindow", u"Account", None))
    # retranslateUi

