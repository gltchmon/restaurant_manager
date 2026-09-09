
# class to manage menu widget 
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget,QMessageBox, QListWidgetItem
from Menu.ui_menu_widget import Ui_Form as Ui_menu_widget
from Database import db

class MenuWidget(QWidget, Ui_menu_widget):
    def __init__(self,restaurant_id,sales_widget):
        super().__init__()
        self.restaurant_id = restaurant_id
        self.sales_widget = sales_widget
        self.setupUi(self)
        self.setWindowTitle("Manage menu")

        self.add_item_selection()
        self.show_menu()

        self.menu_addItem_comboBox.setEditable(True)

        # add menu item
        self.menu_addItem_button.clicked.connect(self.add_item)

        self.menu_deleteItems_button.clicked.connect(self.delete_item)
        
    
    def add_item_selection(self):
        response = (db.supabase.table('menu_item').select('name').execute())
        if response.data:
            for item in response.data:
                item_name = item['name']
                self.menu_addItem_comboBox.addItem(item_name)

    def show_menu(self):
        # select menu items to display
        response = (db.supabase.table('restaurant_menu').select('item_id, menu_item(name), price').order("item_id",desc=True).execute())
        if response.data:
           list_wid = self.menu_listWidget
           # change font
           for item in response.data:
                item_obj = QListWidgetItem(f"{item['item_id']}: {item['menu_item']['name']} - £{item['price']}")
                list_wid.addItem(item_obj)

    def add_item(self):
        # check if capitlization is good
        item_name = self.menu_addItem_comboBox.currentText().capitalize()
        item_price = f"{self.menu_addItem_price.value():.2f}"
    
        #check if item already exists 
        res = (db.supabase.table("menu_item").select("id").eq("name",item_name).execute())
        if res.data:
            item_id = res.data[0]['id']
            # check if they already have it in their menu
            check_entry = (db.supabase.table("restaurant_menu").select("item_id,price").eq("item_id",item_id).execute())
            if check_entry.data:
                old_price = check_entry.data[0]['price']
                # double check if user wishes to overwrite
                warning = QMessageBox.question(None, "Update Item",
                f"{item_name} is already in your menu.\nDo you want to update the price to £{item_price}? ",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                # user selected okay , wants to update price
                if warning == 1024:
                    # add update policy to allow users to update
                    res = db.supabase.table('restaurant_menu').update({'price':item_price}).eq('item_id',check_entry.data[0]['item_id']).select('item_id,price').execute()
                    if res.data:
                        self.update_item_on_list(check_entry.data[0]['item_id'],item_name,old_price,item_price)
                        self.item_added_message("updated", item_name)
                        self.sales_widget.get_menu_items()
            # if the item exists in the database but is not connected to the restaurant we can connect it
            else:
                self.connect_menu(item_id,item_price)
                self.show_item(item_id,item_name,item_price)
                self.item_added_message("add",item_name)
                self.sales_widget.get_menu_items()
        else:
            # add to menu_item to store the name of the item and then connect it to restaurant 
            if item_name: # check it is not empty
                new_item_id = (db.supabase.table("menu_item").insert({'name':item_name}).select('id').execute())
                # connect item to the restaurant
                self.connect_menu(new_item_id.data[0]['id'],item_price)
                self.show_item(new_item_id.data[0]['id'],item_name,item_price)
                self.item_added_message("add",item_name)
                self.sales_widget.get_menu_items()
        
    def show_item(self,item_id,item_name,price):
        self.menu_listWidget.insertItem(0,f"{item_id}: {item_name} - £{price}")
        self.menu_addItem_comboBox.addItem(item_name)

    def item_added_message(self,message_type,item):
        text = ""
        if message_type == "add":
            text = f"Item: {item} added successfully! "
            QMessageBox.information(None, "Success",text,QMessageBox.StandardButton.Ok)
        elif message_type == "updated":
            text = f"Item: {item} updated sucessfully! "
            QMessageBox.information(None, "Update complete",text,QMessageBox.StandardButton.Ok)
        else:
            text = f"Item: {item} has been deleted! "
            QMessageBox.information(None, "Item deleted",text,QMessageBox.StandardButton.Ok)

    def update_item_on_list(self,item_id,item_name,old_price, new_price):
        item = self.menu_listWidget.findItems(f"{item_id}: {item_name} - £{old_price}",Qt.MatchExactly)
        if item:
            item[0].setText(f"{item_id}: {item_name} - £{new_price}")

    def delete_item(self):
        item = self.menu_listWidget.selectedItems()
        if item:
            item = item[0]
            item_index = self.menu_listWidget.indexFromItem(item).row()
            item_id = item.text().split(":")[0]
            db.supabase.table("restaurant_menu").delete().eq('item_id',item_id).execute()
            self.menu_listWidget.takeItem(item_index)
            self.item_added_message("delete", item.text().split(" ")[1])
        self.sales_widget.get_menu_items() # refresh combobox when an item is deleted
    def connect_menu(self, item_id,price):
        db.supabase.table('restaurant_menu').insert({"restaurant_id":self.restaurant_id,
                                        "item_id":item_id,
                                        "price":price}).execute()