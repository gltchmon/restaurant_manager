import PySide6
from PySide6.QtWidgets import QAbstractItemView, QMessageBox,QWidget
from Sales.ui_sales_widget import Ui_manage_sales_widget as Ui_sales_widget
from datetime import date
from datetime import datetime
from Sales.search_dialogs.day_dialog import DayDialog
from Sales.search_dialogs.year_dialog import YearDialog
from Sales.search_dialogs.month_dialog import MonthDialog
from Sales.search_dialogs.item_dialog import ItemDialog
import calendar
import requests
from Database import db
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

# widget for managing the restaurant sales
class SalesWidget(QWidget, Ui_sales_widget):
    def __init__(self,restaurant_id):
        super().__init__()
        self.restaurant_id = restaurant_id
        self.setupUi(self)
        self.setWindowTitle("Manage sales")
        self.manage_sales_tabWidget.setCurrentIndex(0)

        
        # view all sales as default
        self.view_sales()

        # change the table selection mode
        self.view_sales_tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.view_sales_tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # initialise dialogs
        # combo box that opens the specified dialog to filter sales view
        self.view_sales_search_comboBox.currentTextChanged.connect(self.open_search_dialog)
        # day dialog - choose the sales to see on a specific day
        self.day_dialog = DayDialog()
        self.day_dialog.day_dialog_ok_Button.clicked.connect(self.display_specified_day_sales)
        # year dialog
        self.year_dialog = YearDialog()
        self.year_dialog.year_dialog_select_year_spinBox.setMaximum(datetime.now().year)
        self.year_dialog.year_dialog_select_year_spinBox.setValue(datetime.now().year)
        self.year_dialog.year_dialog_okButton.clicked.connect(self.display_sales_by_year)

        # month dialog
        self.month_dialog = MonthDialog()
        self.month_dialog.month_dialog_ok_button.clicked.connect(self.get_sales_by_month_dialog)
        # item dialog - connecting buttons
        self.item_dialog = ItemDialog()
        self.item_dialog.item_view_all_button.clicked.connect(self.get_sales_by_item_dialog)
        self.item_dialog.item_year_button.clicked.connect(self.get_sales_by_item_dialog)
        self.item_dialog.item_month_button.clicked.connect(self.get_sales_by_item_dialog)

        # add menu items to comboBoxes
        self.get_menu_items()
        # -- ADDING SALES FUNCTIONALITY --
        self.add_sales_listWidget.setStyleSheet("font-size:15pt;")

        # design functionality
        # set up date to automatically show up as today
        self.add_sales_date.setDate(date.today())

        # add menu items to combo box
        self.add_sales_item_name_comboBox.setEditable(True)
        self.add_sales_amount_sold_spinBox.setMinimum(1)
      
        # change prices based on what has been selected
        self.change_price()

        # --CANNOT DO MULTIPLE SELECTION--

        # every time you change amount and selection change the total
        self.add_sales_item_name_comboBox.currentTextChanged.connect(self.change_price)
        self.add_sales_amount_sold_spinBox.valueChanged.connect(self.change_price)

        # pressing confirm adds sale to the list
        self.add_sales_confirm_button.clicked.connect(self.add_sale_to_list)

        # delete items in list
        self.add_sales_delete_button.clicked.connect(self.add_sales_delete_sale)

        #submit sales
        self.add_sales_submit_button.clicked.connect(self.submit_added_sales)

        #--MAKING VIEW SALES TAB INTERACTIVE--

        # retrieve and display all sales made by current user
        #self.retrieve_sales()
        # add functionality to buttons
        # view daily sales button
        self.view_sales_daily_button.clicked.connect(self.view_daily_sales)
        # view weekly sales button
        self.view_sales_weekly_button.clicked.connect(self.view_weekly_sales)
        # view monthly sales button
        self.view_sales_monthly_button.clicked.connect(self.view_monthly_sales)
        # view yearly sales button
        self.view_sales_yearly_sales.clicked.connect(self.view_yearly_sales)

        # view all sales button
        self.view_sales_view_all_button.clicked.connect(self.view_sales)
        # search by comboBox
            # adding items
        self.view_sales_search_comboBox.addItem("Day")
        self.view_sales_search_comboBox.addItem("Month")
        self.view_sales_search_comboBox.addItem("Year")
        self.view_sales_search_comboBox.addItem("Item")
        self.view_sales_search_comboBox.addItem("-")

        self.view_sales_delete_button.clicked.connect(self.find_sale_id)
        self.show()
        
        # adding functionality to delete button
        #self.view_sales_delete_button.clicked.connect(self.delete_items)

# adding menu to combo box
    def get_menu_items(self):
        self.add_sales_item_name_comboBox.clear()
        response = (db.supabase.rpc('get_all_menu_items').execute())
        if response.data:
            for item in response.data:
                item_name = item['name']
                #item_id = item['menu_item']['id']
                self.add_sales_item_name_comboBox.addItem(item_name)
                # adding items to item combo box
                self.item_dialog.item_select_item_comboBox.addItem(f"{item_name}")

# change total price whenever the quantity has changed
    def change_price(self):
        current_comboBox_item = self.add_sales_item_name_comboBox.currentText()
        response = db.supabase.table("restaurant_menu").select("price,menu_item!inner(name)").eq("menu_item.name",current_comboBox_item).execute()
        if response.data:
            item_price = Decimal(response.data[0]['price'])
            quantity = self.add_sales_amount_sold_spinBox.value()
            total = item_price * quantity
            self.add_sales_total_lineEdit.setText(str(total))
        
# confirming and adding a single sales entry to the list
    def add_sale_to_list(self):
        date = self.add_sales_date.date().toString("dd-MM-yyyy")
        item_name = self.add_sales_item_name_comboBox.currentText()
        items = [self.add_sales_item_name_comboBox.itemText(i) for i in range(self.add_sales_item_name_comboBox.count())]
        amount_sold = self.add_sales_amount_sold_spinBox.value()
        total = self.add_sales_total_lineEdit.text()
        try:
            Decimal(total)
        except InvalidOperation:
            QMessageBox.critical(None, "Invalid total",
                        "Invalid total amount please edit and try again.",
                        QMessageBox.StandardButton.Ok)
            return
        # validate total input incase user has changed the amount themselves , check if the decimal place is higher than 2
        total_dec_split = total.split(".")
        if len(total_dec_split[1]) > 2:
            QMessageBox.critical(None, "Invalid total",
                                    "Invalid total amount please edit and try again.",
                                    QMessageBox.StandardButton.Ok)
            return
        total = Decimal(total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        # error checking to see if the item actually exists in menu before submission
        if item_name not in items:
            error_message = QMessageBox.critical(None, "Could not add sale", f"{item_name} does not exist in your menu. Add this item to your menu and try again.",
                                                 QMessageBox.StandardButton.Ok)
            return
        else:
            # avoid adding duplicates by checking if its already in the list
            items = [self.add_sales_listWidget.item(x).text() for x in range(self.add_sales_listWidget.count())]
            sale_str = f"{date} | {item_name} | {amount_sold} | {total}"
            if sale_str in items:
                error_message = QMessageBox.warning(None, "Could not add sale",
                                                     f"{item_name} is already in your sales made list.",
                                                     QMessageBox.StandardButton.Ok)
                return
            else:
                self.add_sales_listWidget.addItem(sale_str)    

     # delete selected sale from list before submitting
# delete selected sale from list widget on the add sale functionality
    def add_sales_delete_sale(self):
        items = self.add_sales_listWidget.selectedItems()
        for item in items:
            self.add_sales_listWidget.takeItem(self.add_sales_listWidget.row(item))

    # must check if the item is connected to the restaurant menu before submission
# submit and insert the sale into the database
    def submit_added_sales(self):
        items = [self.add_sales_listWidget.item(x).text() for x in range(self.add_sales_listWidget.count())]
        for item in items:
            # format the sales
            data = item.split(" | ")
            date_sold = datetime.strptime(data[0],"%d-%m-%Y").date()
            # FIX DELETING ITEMS
            response = db.supabase.table("restaurant_menu").select("menu_item!inner(id)").eq("menu_item.name",data[1]).execute()
            print(response)
            if not response:
                QMessageBox.critical(self,"Item not in menu", "This sale cannot be added as item does not exist in your menu.\n Please add this item to your menu and try again.", QMessageBox.StandardButton.Ok)
                self.add_sales_listWidget.clear()
                return
            item_id = response.data[0]['menu_item']['id']
            quantity = data[2]
            total = data[3]
            #print(f"id:{item_id}, name:{data[1]}, date sold:{date_sold}, quantity:{quantity}, total:{total}")
            response = (
                db.supabase.table("sale_made")
                .insert({"restaurant_id": self.restaurant_id, "item_id":item_id, 
                         "date":str(date_sold), "quantity":quantity, "total":total })
                .execute()
            )
        self.add_sales_listWidget.clear()

    def view_sales(self):
        self.view_sales_tableWidget.clear()
        # get all sales
        response = (
            db.supabase.table("sale_made")
            .select("*",count="exact").order("date", desc=True).execute()
        )
        if response.data:
            self.view_sales_tableWidget.setRowCount(response.count)
            # change columns if needed
            if self.view_sales_tableWidget.columnCount() != 4:
                self.view_sales_tableWidget.setColumnCount(4)
            self.view_sales_tableWidget.setHorizontalHeaderItem(0, PySide6.QtWidgets.QTableWidgetItem("Date"))
            self.view_sales_tableWidget.setHorizontalHeaderItem(1, PySide6.QtWidgets.QTableWidgetItem("Item"))
            self.view_sales_tableWidget.setHorizontalHeaderItem(2, PySide6.QtWidgets.QTableWidgetItem("Quantity"))
            self.view_sales_tableWidget.setHorizontalHeaderItem(3, PySide6.QtWidgets.QTableWidgetItem("Total"))
            self.view_sales_tableWidget.setStyleSheet("font-size: 15pt;") 
            counter = 0
            # get data from each sale
            for sale in response.data:
                current_row =  self.manage_sales_tabWidget.count()
                item_name = self.get_item_name_by_id(sale['item_id'])
                quantity = sale['quantity']
                total = sale['total']
                date_sold =  datetime.strptime(sale['date'], '%Y-%m-%d').date()
                date_sold = date_sold.strftime("%d-%b-%Y")
                self.view_sales_tableWidget.setItem(counter,0,PySide6.QtWidgets.QTableWidgetItem(date_sold))
                self.view_sales_tableWidget.setItem(counter, 1, PySide6.QtWidgets.QTableWidgetItem(item_name))
                self.view_sales_tableWidget.setItem(counter, 2, PySide6.QtWidgets.QTableWidgetItem(f"{quantity}"))
                self.view_sales_tableWidget.setItem(counter, 3, PySide6.QtWidgets.QTableWidgetItem(f"£{total}"))
                counter+=1
        self.view_sales_delete_button.show()

    # helper function to find the name of items from id
    def get_item_name_by_id(self,id):
        response = (db.supabase.table("menu_item").select("name").eq("id",id).execute())
        name = response.data[0]['name']
        return name 

# GENERAL BUTTONS TO VIEW SALES
# view the sales grouped by day they were sold
    def view_daily_sales(self):
        response = (db.supabase.rpc('daily_sales').execute())
        if response.data:
            self.display_rows(response.data, "Date")
        self.view_sales_delete_button.hide()
    
# view all sales by week
    def view_weekly_sales(self):
        self.view_sales_tableWidget.clear()
        response = (db.supabase.rpc('weekly_sales').execute())
        if response.data:
            self.display_rows(response.data, "Week")
        self.view_sales_delete_button.hide()

    def delete_item_in_comboBox(self):
        response = db.supabase.table("restaurant_menu").select()


# view all sales by month
    def view_monthly_sales(self):
        self.view_sales_tableWidget.clear()
        response = (db.supabase.rpc('monthly_sales').execute())
        if response.data:
            self.display_rows(response.data, "Month")
        self.view_sales_delete_button.hide()
# view all sales by year
    def view_yearly_sales(self):
            self.view_sales_tableWidget.clear()
            response = (db.supabase.rpc('yearly_sales').execute())
            if response.data:
                self.view_sales_tableWidget.setRowCount(len(response.data))
                if self.view_sales_tableWidget.columnCount() != 2:
                    self.view_sales_tableWidget.setColumnCount(2)
                self.view_sales_tableWidget.setHorizontalHeaderItem(0, PySide6.QtWidgets.QTableWidgetItem("Year"))
                self.view_sales_tableWidget.setHorizontalHeaderItem(1, PySide6.QtWidgets.QTableWidgetItem("Total"))
                for row_count,sale in enumerate(response.data):
                    year = sale['year'].split("T")[0]
                    total = sale['total']
                    year = datetime.strptime(year, '%Y-%m-%d').date()
                    year = year.strftime('%Y')
                    self.view_sales_tableWidget.setItem(row_count, 0,PySide6.QtWidgets.QTableWidgetItem(year))
                    self.view_sales_tableWidget.setItem(row_count, 1,PySide6.QtWidgets.QTableWidgetItem(f"£{total}"))
            self.view_sales_delete_button.hide()

    def open_search_dialog(self,text):
        match text:
            case "Day":
                self.day_dialog.show()
            case "Year":
                self.year_dialog.show()
            case "Month":
                self.month_dialog.show()
            case "Item":
                self.item_dialog.show()
        self.view_sales_search_comboBox.setCurrentIndex(4) 

# DISPLAY RESULTS FROM THE DAY DIALOG
    def display_specified_day_sales(self):
        date_edit_date = self.day_dialog.day_dialog_dateEdit.date()
        date = datetime(date_edit_date.year(), date_edit_date.month(), date_edit_date.day()).strftime("%Y-%m-%d")
        response = (db.supabase.rpc('get_day_sales', params={'day':date}).execute())
        if response.data:
            self.view_sales_tableWidget.clear()
            self.view_sales_tableWidget.setRowCount(len(response.data))
            if self.view_sales_tableWidget.columnCount() != 4:
                self.view_sales_tableWidget.setColumnCount(4)
            self.view_sales_tableWidget.setHorizontalHeaderItem(0, PySide6.QtWidgets.QTableWidgetItem("Date"))
            self.view_sales_tableWidget.setHorizontalHeaderItem(1, PySide6.QtWidgets.QTableWidgetItem("Item"))
            self.view_sales_tableWidget.setHorizontalHeaderItem(2, PySide6.QtWidgets.QTableWidgetItem("Quantity"))
            self.view_sales_tableWidget.setHorizontalHeaderItem(3, PySide6.QtWidgets.QTableWidgetItem("Total"))
            for row_count, sale in enumerate(response.data):
                date_sold = sale['date']
                date_sold = self.date_to_str(date_sold)
                item_name = sale['name']
                quantity = sale['quantity']
                total = sale['total']
                self.view_sales_tableWidget.setItem(row_count, 0,PySide6.QtWidgets.QTableWidgetItem(date_sold))
                self.view_sales_tableWidget.setItem(row_count, 1,
                                                    PySide6.QtWidgets.QTableWidgetItem(item_name))
                self.view_sales_tableWidget.setItem(row_count, 2,
                                                    PySide6.QtWidgets.QTableWidgetItem(f"{quantity}"))
                self.view_sales_tableWidget.setItem(row_count, 3, PySide6.QtWidgets.QTableWidgetItem(f"£{total}"))
            self.view_sales_delete_button.show()
            self.view_sales_search_comboBox.setCurrentIndex(4)
            self.day_dialog.close()
        else:
            QMessageBox.warning(None, "No sales found",
                        "No sales were made on this date.\nPlease select another date or add sales made on this day.",
                        QMessageBox.StandardButton.Ok)

# DISPLAY RESULTS FROM MONTH DIALOG
    # functioin that gets results from the month dialog
    def get_sales_by_month_dialog(self):
        checked_button = self.month_dialog.month_dialog_display_option_group.checkedButton().text() if self.month_dialog.month_dialog_display_option_group.checkedButton() else None

        if checked_button:
            year = self.month_dialog.month_dialog_year_spinBox.text()
            month = self.month_dialog.month_dialog_month_spinBox.text()
            sales = None
            response =  None
            match checked_button:
                case "View by day":
                    response = (db.supabase.rpc('get_daily_sales_from_month', params={'month':month, 'year':year}).execute())
                    self.display_sales_by_month(response.data,checked_button,"Date", "Total")
                case "View by week":
                    response = (db.supabase.rpc('get_weekly_sales_from_month', params={'month':month, 'year':year}).execute())
                    self.display_sales_by_month(response.data,checked_button,"Week", "Total")
                case "View month total":
                    response = (db.supabase.rpc('get_monthly_sales_from_month', params={'month':month, 'year':year}).execute())
                    self.display_sales_by_month(response.data,checked_button,"Month", "Total")
                case _:
                    response = (db.supabase.rpc('get_all_sales_from_month', params={'month':month, 'year':year}).execute())
                    self.display_sales_by_month(response.data,checked_button,None, None)
            self.view_sales_delete_button.hide()
        else:
            error_message = QMessageBox.critical(None, "Choose a display option",
                                                 f"You must check one of the display options to view sales on specified month. Please try again",
                                                 QMessageBox.StandardButton.Ok)
    # helper function to displays results
    def display_sales_by_month(self, sales,display_type,col1,col2):
        self.view_sales_tableWidget.clear()
        self.view_sales_tableWidget.setRowCount(len(sales))
        if display_type.strip() != "View all sales":
            self.display_rows(sales,col1)
        else:
            self.display_all_rows(sales)
        self.month_dialog.close()

#DISPLAY RESULTS FROM YEAR DIALOG
    def display_sales_by_year(self):
        radio_button_selected = self.year_dialog.year_dialog_display_optionGroup.checkedButton()
        if radio_button_selected:
            get_button_text = radio_button_selected.text().split(" ")[0].lower()
            year = self.year_dialog.year_dialog_select_year_spinBox.value()
            if get_button_text == "view":
                get_button_text = "all"
            # retrieve data depending on option selected
            response = (db.supabase.rpc(f"get_{get_button_text}_sales_in_year", params={"year":year}).execute())
            if response.data:
                match get_button_text:
                    case "weekly":
                        self.display_rows(response.data, "Week")
                    case "daily":
                        self.display_rows(response.data, "Date")
                    case "monthly":
                        self.display_rows(response.data, "Month")
                    case "all":
                        self.display_all_rows(response.data)
            else:
                QMessageBox.warning(None, "No sales",
                                                "No sales have been made on this year. Please add sales and try again.",
                                                QMessageBox.StandardButton.Ok)
        else:
             QMessageBox.warning(None, "Select a display option",
                                "You must select a display option to view the sales on this year.",
                                QMessageBox.StandardButton.Ok)
        self.year_dialog.close()

# DISPLAY RESULTS FROM ITEM DIALOG
    def get_sales_by_item_dialog(self,button):
        item = self.item_dialog.item_select_item_comboBox.currentText()
        year = self.item_dialog.item_year_spinBox.value()
        month = self.item_dialog.item_month_spinBox.value()
        month_year = self.item_dialog.item_month_year_spinBox.value()
        button_clicked = self.sender().text()
        response = None
        if button_clicked == "View all item sales":
            response = (db.supabase.rpc('get_all_sales_with_item', params={"item":item}).execute())
        elif button_clicked == "View by year":
            response = (db.supabase.rpc('get_sales_with_item_in_year', params={"item":item, "year":year}).execute())
        elif button_clicked == "View by month":
            response = (db.supabase.rpc('get_sales_with_item_in_month', params={"item":item, "year":month_year, "month":month}).execute())
        if response.data:
            self.view_sales_tableWidget.clear()
            self.view_sales_tableWidget.setRowCount(len(response.data))
            self.display_all_rows(response.data)
        else:
            QMessageBox.warning(None, "No sales found",
                    "No sales were made on this date with this item.\nPlease select another date or add sales made on this day.",
                    QMessageBox.StandardButton.Ok)
        self.item_dialog.close()

# DELETE SALE 
    def delete_sale(self):
        selected_row = self.view_sales_tableWidget.currentRow()
        self.view_sales_tableWidget.removeRow(selected_row)
# FIND SALE ID 
    def find_sale_id(self):
        selected_row = self.view_sales_tableWidget.selectedItems()
        selected_row_items = [cell.text() for cell in selected_row]
        sale_date = self.str_to_date(selected_row_items[0]).strftime("%Y-%m-%d")
        sale_total = selected_row_items[3][1:]
        item_id = (db.supabase.table("menu_item").select("id").eq("name", selected_row_items[1]).execute()).data[0]['id']
        sale_id = (db.supabase.rpc("get_sale_id", params={"date":sale_date,"item_id": item_id, "quantity": selected_row_items[2], "total": sale_total}).execute())
        if sale_id.data:
            self.delete_sale()
            db.supabase.table("sale_made").delete().eq("id",sale_id.data[0]['id']).execute()
        else:
            print("sale id not found")
        

# HELPER FUNCTIONS 
    def display_rows(self, sales,col_name1):
        self.view_sales_tableWidget.clear()
        self.view_sales_tableWidget.setRowCount(len(sales))
        if self.view_sales_tableWidget.columnCount() != 2:
            self.view_sales_tableWidget.setColumnCount(2)
        self.view_sales_tableWidget.setHorizontalHeaderItem(0, PySide6.QtWidgets.QTableWidgetItem(f"{col_name1}"))
        self.view_sales_tableWidget.setHorizontalHeaderItem(1, PySide6.QtWidgets.QTableWidgetItem("Total"))
        for row_count, sale in enumerate(sales):
            if col_name1 == "Date":
                self.view_sales_tableWidget.setItem(row_count, 0,
                                                    PySide6.QtWidgets.QTableWidgetItem(
                                                        self.str_to_date(sale['date']).strftime("%d-%b-%Y")))
            elif col_name1 == "Week":
                self.view_sales_tableWidget.setItem(row_count, 0,
                                                    PySide6.QtWidgets.QTableWidgetItem(
                                                        self.str_to_week(sale)))
            elif col_name1 == "Month":
                month = sale['month'].split("T")[0]
                month = datetime.strptime(month,"%Y-%m-%d")
                month = month.strftime("%b-%Y")
                self.view_sales_tableWidget.setItem(row_count, 0,
                                                    PySide6.QtWidgets.QTableWidgetItem(
                                                        f"{month}"))
            self.view_sales_tableWidget.setItem(row_count, 1,
                                                PySide6.QtWidgets.QTableWidgetItem(f"£{sale['total']}"))
        self.view_sales_delete_button.hide()

    def display_all_rows(self,sales):
        self.view_sales_tableWidget.clear()
        self.view_sales_tableWidget.setRowCount(len(sales))
        if self.view_sales_tableWidget.columnCount() != 4:
            self.view_sales_tableWidget.setColumnCount(4)
        self.view_sales_tableWidget.setHorizontalHeaderItem(0, PySide6.QtWidgets.QTableWidgetItem(f"Date"))
        self.view_sales_tableWidget.setHorizontalHeaderItem(1, PySide6.QtWidgets.QTableWidgetItem(f"Item"))
        self.view_sales_tableWidget.setHorizontalHeaderItem(2, PySide6.QtWidgets.QTableWidgetItem(f"Quantity"))
        self.view_sales_tableWidget.setHorizontalHeaderItem(3, PySide6.QtWidgets.QTableWidgetItem(f"Total"))
        for row_count, sale in enumerate(sales):
            self.view_sales_tableWidget.setItem(row_count, 0,
                                                    PySide6.QtWidgets.QTableWidgetItem(
                                                        self.str_to_date(sale['date']).strftime("%d-%b-%Y")))
            self.view_sales_tableWidget.setItem(row_count, 1,
                                                PySide6.QtWidgets.QTableWidgetItem(f"{sale['name']}"))
            self.view_sales_tableWidget.setItem(row_count, 2,
                                                PySide6.QtWidgets.QTableWidgetItem(f"{sale['quantity']}"))
            self.view_sales_tableWidget.setItem(row_count, 3,
                                                PySide6.QtWidgets.QTableWidgetItem(f"£{sale['total']}"))
        self.view_sales_delete_button.show()
    

    def date_to_str(self, date):
        date = datetime.strptime(date, '%Y-%m-%d').date()
        date = date.strftime('%d-%b-%Y')
        return date

    def str_to_date(self,date_str):
        try:
            date_obj = datetime.strptime(date_str,"%Y-%m-%d")
            return date_obj
        except Exception as e:
            date_obj = datetime.strptime(date_str,"%d-%b-%Y")
            return date_obj


    def str_to_week(self,sale):
        week_start = sale['week_start'].split("T")[0]
        week_end = sale['week_end'].split("T")[0]
        week_start = datetime.strptime(week_start, '%Y-%m-%d').date()
        week_end = datetime.strptime(week_end, '%Y-%m-%d').date()
        week = f"{week_start.strftime("%d-%b-%Y")} to {week_end.strftime("%d-%b-%Y")}"
        return week

        # SHOW DATE AS SEP 13 2025