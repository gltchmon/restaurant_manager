from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QDialog, QPushButton, QApplication, QGridLayout, QLabel, QLineEdit, QMessageBox)
from Sales.sales_widget import SalesWidget
from Database import db


# dialog to prompt user to log in if they have never signed on
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        # create grid layout for log in form
        layout = QGridLayout()
        self.setLayout(layout)
        self.sales_widget = None

        title = QLabel("Login or Register")
        title.setStyleSheet("font-size:14pt;")
        # title in middle
        layout.addWidget(title,0,0,1,3, Qt.AlignmentFlag.AlignCenter)

        # create username and password labels
        email_label = QLabel("Email:")
        layout.addWidget(email_label ,1,0)
        password_label =  QLabel("Password:")
        layout.addWidget(password_label,2,0)

        # create username and password line edits
        self.line_edits = {}
        self.line_edits["email_line_edit"] = QLineEdit()
        layout.addWidget(self.line_edits["email_line_edit"],1,1,1,2)
        self.line_edits["password_line_edit"] = QLineEdit()
        layout.addWidget(self.line_edits["password_line_edit"], 2, 1,1,2)

        self.log_in_button = QPushButton("Log in")
        layout.addWidget(self.log_in_button,3,1)
        self.create_account_button = QPushButton("Create account")
        layout.addWidget(self.create_account_button, 3, 2)

        self.log_in_button.clicked.connect(self.log_in_user)

    def log_in_user(self):
        email = self.line_edits["email_line_edit"].text()
        password = self.line_edits["password_line_edit"].text()

        response = db.supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password,
        }
    )

        if response.user.id:
            self.sales_widget = SalesWidget(response.user.id)
            self.sales_widget.show()
            self.close()
        else:
            QMessageBox.critical(None, "Error logging in",
            response,
            QMessageBox.StandardButton.Ok)

