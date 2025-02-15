from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QComboBox, QApplication
from PyQt5 import uic
import sys, os
import json
from add_restro import AddRestroWindow  # Import the AddRestroWindow class
from add_rm import Add_rm
from inventory import Inventory

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




        self.set_text()

        # Connect button to open the second window

        self.edit_det_pb.clicked.connect(self.open_add_restro_window)
        self.raw_m_pb.clicked.connect(self.open_add_raw_m_window)
        self.inven_pb.clicked.connect(self.open_inventory_window)

        # Show main window
        self.show()

    def open_add_restro_window(self):
        #self.hide()
        print("till this the code has ran!!")

        self.add_restro_window = AddRestroWindow()
        self.add_restro_window.show()
        
    def open_add_raw_m_window(self):
        #self.hide()
        #print("till this the code has ran!!")

        self.add_rm_window = Add_rm()
        self.add_rm_window.show()

    def open_inventory_window(self):
        print("till this the code has ran!!")
        self.inventory_window = Inventory()

        print("till this the code has ran!!")
        self.inventory_window.show()

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

# Initialize the application
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
