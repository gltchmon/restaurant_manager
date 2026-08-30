from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QMainWindow
from MainWindow.ui_mainWindow import Ui_MainWindow
from Sales.sales_widget import SalesWidget

# main window that holds all other widgets 
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,rest_id):
        super().__init__()
        self.id = rest_id
        self.setupUi(self)
        self.setWindowTitle("Manage Restaurant")
        self.sales_widget = SalesWidget(rest_id)
        self.main_stackedWidget.addWidget(self.sales_widget)
        self.main_stackedWidget.setCurrentIndex(0)
        