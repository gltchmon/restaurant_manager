from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QMainWindow
from MainWindow.ui_mainWindow import Ui_MainWindow
from Sales.sales_widget import SalesWidget
from Menu.menu_widget import MenuWidget

# main window that holds all other widgets 
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,rest_id):
        super().__init__()
        self.id = rest_id
        self.setupUi(self)
        self.setWindowTitle("Manage Restaurant")
        self.sales_widget = SalesWidget(rest_id)
        self.menu_widget = MenuWidget(rest_id,self.sales_widget)

        # adding widgets to main window
        self.main_stackedWidget.addWidget(self.sales_widget)
        self.main_stackedWidget.addWidget(self.menu_widget)
        self.main_stackedWidget.setCurrentIndex(1)

        self.action_manage_menu.triggered.connect(lambda: self.menu_clicked("menu"))
        self.action_manage_sales.triggered.connect(lambda: self.menu_clicked("sales"))
    def menu_clicked(self,action):
        if action == "menu":
            self.main_stackedWidget.setCurrentIndex(1)
        else:
            self.main_stackedWidget.setCurrentIndex(0)

        