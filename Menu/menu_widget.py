
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
        
    # add menu items to combo box
    def add_item_selection(self):
        response = (db.supabase.table('menu_item').select('name',"id").execute())
        if response.data:
            for item in response.data:
                item_name = item['name']
                item_id = item['id']
                self.menu_addItem_comboBox.addItem(item_name,item_id)

    def show_menu(self):
        # select menu items to display
        response = (db.supabase.table('restaurant_menu').select('item_id, menu_item(name), price').eq("available", "true").order("item_id",desc=True).execute())
        if response.data:
           list_wid = self.menu_listWidget
           # change font
           for item in response.data:
                item_obj = QListWidgetItem(f"{item['item_id']}: {item['menu_item']['name']} - £{item['price']}")
                list_wid.addItem(item_obj)

    def add_item(self):
        # check if capitlization is good
        item_name = self.menu_addItem_comboBox.currentText().strip().capitalize()
        item_id = self.menu_addItem_comboBox.currentData()
        item_price = f"{self.menu_addItem_price.value():.2f}"

        if not item_name: return
        # check if item already connected to menu 
        res = (db.supabase.table("restaurant_menu").select("item_id, price,available, menu_item(name)").eq("item_id",item_id).execute())
        is_match = False
        # check if name matches 
        if res.data:
            item_name_check = res.data[0]['menu_item']['name'].strip()
            # check if they have the same to avoid errors of getting item data
            is_match = item_name_check.lower() == item_name.lower()

        # the item entered matches the name of the item that has the current id in the combo box
        if is_match:
            # check if item has been removed
            is_available = res.data[0]['available']
            # if the item has been removed from the menu we will add it back
            if not is_available:
                confirmation = self.showDialog(item_name, item_price,"add")
                if confirmation:
                    res = db.supabase.table('restaurant_menu').update({'price':item_price, "available":"true"}).eq('item_id',item_id).execute()
                    self.item_added_message("add",item_name)
                    self.show_item(item_id,item_name,item_price)
            # update already existing item that is available on the menu
            else:
                old_price = res.data[0]['price']
                confirmation = self.showDialog(item_name, item_price,"update")
                if confirmation:
                    # update the price
                    res = db.supabase.table('restaurant_menu').update({'price':item_price}).eq('item_id',item_id).select('item_id,price').execute()
                    if res.data:
                        self.update_item_on_list(item_id,item_name,old_price,item_price)
                        self.item_added_message("updated", item_name)
                        self.sales_widget.get_menu_items()
        else: # add a new item to the menu, the item name does not match the item name retrieved from id
            confirmation = self.showDialog(item_name, item_price,"add")
            # double check if user wants to add the item to menu
            if confirmation:
                # check if item is in menu_item table so we can connect it or insert then connect 
                new_item_id = self.get_new_item_id(item_name)
                # connect item to the restaurant
                self.connect_menu(new_item_id,item_price)
                self.show_item(new_item_id,item_name,item_price)
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

    # show dialog to confirm if user wants to update item
    def showDialog(self,item_name,item_price, state):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Question)
        message_box.setWindowTitle("Update item price")
        message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if state == "update":
            message_box.setText(f"{item_name} is already in your menu.\nDo you want to update the price to £{item_price}? ")
        else:
            message_box.setText(f"Are you sure you want to add {item_name} with price £{item_price} to your menu?")
        
        return message_box.exec() == QMessageBox.StandardButton.Yes

    def get_new_item_id(self, item_name):
        res = (db.supabase.table("menu_item").select('id').eq('name', item_name).execute())
        if res.data:
            return res.data[0]['id']
        else:
            res = (db.supabase.table("menu_item").insert({'name':item_name}).select('id').execute())
            return res.data[0]['id']

    def delete_item(self):
        item = self.menu_listWidget.selectedItems()
        if item:
            item = item[0]
            item_index = self.menu_listWidget.indexFromItem(item).row()
            item_id = item.text().split(":")[0]
            db.supabase.table("restaurant_menu").update({"available": "false"}).eq('item_id',item_id).execute()
            self.menu_listWidget.takeItem(item_index)
            self.item_added_message("delete", item.text().split(" ")[1])
        self.sales_widget.get_menu_items() # refresh combobox when an item is deleted
    def connect_menu(self, item_id,price):
        db.supabase.table('restaurant_menu').insert({"restaurant_id":self.restaurant_id,
                                        "item_id":item_id,
                                        "price":price}).execute()