
# class to manage menu widget 

from PySide6.QtWidgets import QWidget
from Menu.ui_menu_widget import Ui_Form as Ui_menu_widget

class MenuWidget(QWidget, Ui_menu_widget):
    def __init__(self,restaurant_id):
        super().__init__()
        self.restaurant_id = restaurant_id
        self.setupUi(self)
        self.setWindowTitle("Manage menu")

        # add menu to combobox 