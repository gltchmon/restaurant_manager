import sys
import os
import json
from PySide6 import QtWidgets
from LogIn.login_dialog import LoginDialog
from Sales.sales_widget import SalesWidget
from MainWindow.mainWindow import MainWindow
from Database import db
from supabase import *
from dotenv import load_dotenv

load_dotenv()
email = os.getenv("USER_EMAIL")
pwd = os.getenv("USER_PASSWORD")

def login(email,password):
    response = db.supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password,
        }
    )
    if response.session:
        refresh_token = response.session.refresh_token
        with open("session/session_config.json", "w") as f:
            import json
            json.dump({"refresh_token": refresh_token},f)
    print("manual log in")
    return response.user.id

# restore user session
def auth_user(supbase_client : Client):
    if os.path.exists("session/session_config.json"):
        try:
            with open("session/session_config.json", "r") as s:
                data = json.load(s)
                refresh_token =  data.get("refresh_token")

            if refresh_token:
                print("CONTAINS REFRESH TOKEN: ", refresh_token)
                response = supbase_client.auth.refresh_session(refresh_token)
                with open("session/session_config.json", "w") as f:
                    json.dump({"refresh_token": response.session.refresh_token}, f)
                print("Session restored")
                return response.user.id
        except Exception as e:
            print(f"Could not restore local session: {e}")
    return False

if __name__ == "__main__":

    user_id = auth_user(db.supabase)
    # log the user in manually
    if not user_id:
        user_id = login(email, pwd)
    print("current user: ", user_id)

    # pass in user id to be used to find correct data for user 
    app = QtWidgets.QApplication(sys.argv)
    window =  MainWindow(user_id)
    window.show()
    app.exec()

  # PUSH TO GIT AND CREATE MAIN WINDOW

  # command to compile code
  # pyside6-uic widget.ui > widget_2.ui # then convert to utf8