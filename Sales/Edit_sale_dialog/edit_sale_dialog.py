from PySide6.QtWidgets import QDialog
from Sales.Edit_sale_dialog.ui_edit_sale_dialog import Ui_edit_sale_dialog
from datetime import datetime
from PySide6.QtCore import Qt
from Database import db
from decimal import Decimal


class EditSaleDialog(QDialog,Ui_edit_sale_dialog):
    def __init__(self,sales_widget):
            super().__init__()
            self.setupUi(self)
            self.setWindowTitle("Edit sale")

            self.item = None
            self.sale_id = None
            self.sales_widget = sales_widget

            current_date = datetime.now()
            self.edit_sale_date.setMaximumDate(current_date)
            self.edit_sale_date.setDate(current_date)
            self.change_price()
            self.edit_sale_qty.valueChanged.connect(self.change_price)

            self.edit_confirm_button.clicked.connect(self.update_sale)
            self.edit_cancel_button.clicked.connect(lambda: self.close())

    def edit_sale(self,item):
        self.item = item.text().strip()
        self.sale_name.setText(f"Edit sale for: {item.text()}")
        self.sale_id = item.data(Qt.UserRole)
        self.show()

    def change_price(self):
        if self.item:
            response = db.supabase.table("restaurant_menu").select("price,menu_item!inner(name)").eq("menu_item.name",self.item).execute()
            if response.data:
                price = response.data[0]['price']
                price = Decimal(price) * self.edit_sale_qty.value()
                self.edit_sale_price.setValue(price)

    def update_sale(self):
        new_qty = self.edit_sale_qty.value()
        new_price = f"{self.edit_sale_price.value():.2f}"
        new_date = self.edit_sale_date.date().toString("yyyy-MM-dd")

        response = db.supabase.table('sale_made').update({'total':new_price, 'quantity':new_qty, 'date':new_date}).eq('id',self.sale_id).select('id,quantity,total,date').execute()

        if response.data:
            quantity = response.data[0]['quantity']
            total = response.data[0]['total']
            date = response.data[0]['date']
            self.change_row(quantity,total,date)
        self.close()
     

    def change_row(self,quantity,total,date):
        items = self.sales_widget.view_sales_tableWidget.selectedItems()
        date = datetime.strptime(date, '%Y-%m-%d').date()
        date = date.strftime('%d-%b-%Y')
        items[0].setText(date)
        items[2].setText(f"{quantity}")
        items[3].setText(f"£{total}")