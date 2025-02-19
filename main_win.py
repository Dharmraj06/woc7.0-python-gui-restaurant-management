from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QComboBox, QApplication
from PyQt5 import uic
import sys, os
import json
from add_restro import AddRestroWindow  # Import the AddRestroWindow class
from add_rm import Add_rm
from billing_window import billing
from inventory import Inventory
from menu_win import menu

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        ui_file = "main_win.ui"
        if not os.path.exists(ui_file):
            print(f"Error: {ui_file} not found!")
            return

        uic.loadUi(ui_file, self)


        # inheriting the widgets
        self.name_label = self.findChild(QLabel, "name_label")
        self.theme_cb = self.findChild(QComboBox, "theme")
        self.edit_det_pb = self.findChild(QPushButton, "edit_det_pb")
        self.bill_pb = self.findChild(QPushButton, "bill_pb")
        self.inven_pb = self.findChild(QPushButton, "inven_pb")
        self.menu_pb = self.findChild(QPushButton, "menu_pb")
        self.raw_m_pb = self.findChild(QPushButton, "raw_m_pb")

        #  setting the following the window
        self.add_restro_window = None
        self.add_rm_window = None
        self.inventory_window = None
        self.menu_window = None
        self.billing_window = None


        self.set_text()

        # Connect button to open the second window

        self.edit_det_pb.clicked.connect(self.open_add_restro_window)
        self.raw_m_pb.clicked.connect(self.open_add_raw_m_window)
        self.inven_pb.clicked.connect(self.open_inventory_window)
        self.menu_pb.clicked.connect(self.open_menu_window)
        self.bill_pb.clicked.connect(self.open_billing_window)
        self.theme_cb.currentTextChanged.connect(self.change_theme)
        self.theme = "light"
        # Show main window
        self.show()

    def open_add_restro_window(self):
        #self.hide()
        print("till this the code has ran!!")

        self.add_restro_window = AddRestroWindow(self.theme)
        self.add_restro_window.show()
        
    def open_add_raw_m_window(self):
        #self.hide()
        #print("till this the code has run!!")

        self.add_rm_window = Add_rm(self.theme)
        self.add_rm_window.show()

    def open_inventory_window(self):
        print("till this the code has ran!!")
        self.inventory_window = Inventory(self.theme)

        print("till this the code has ran!!")
        self.inventory_window.show()

    def open_menu_window(self):
        self.menu_window = menu(self.theme)
        self.menu_window.show()

    def set_text(self):
        json_file = "restro_details.json"

        if not os.path.exists(json_file):
            print(f"Error: {json_file} not found!")
            return

        try:
            with open(json_file, "r") as f:
                data = json.load(f)

            if "Name" in data[0]:
                self.name_label.setText(data[0]["Name"])
            else:
                print("invalid")


        except:
            pass

    def open_billing_window(self):
        self.billing_window = billing(self.theme)
        self.billing_window.show()

    def change_theme(self):
        self.theme = str(self.theme_cb.currentText())
        if self.theme == "Dark":
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
        else:  # Light theme
            self.setStyleSheet("background-color: white; color: black;")


# Initialize the application
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
