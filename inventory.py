from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QWidget
from PyQt5 import uic
import os
import json
import sys

from add_rm import Add_rm
from curr_inventory_window import Curr_inventory


class Inventory(QMainWindow):
    def __init__(self):
        super(Inventory,self).__init__()
        #super(Add_rm, self).__init__()

        ui_file = "Inventory.ui"

        self.add_rm_window = None
        self.add_curr_inven_window = None

        #checking if the file exists or not;
        if not os.path.exists(ui_file):
            print(f"Error: {ui_file} not found!")
            return

        uic.loadUi(ui_file, self)

        # Set window title
        self.setWindowTitle("Inventory")

        # inheriting the widgets
        self.curr_inven_pb = self.findChild(QPushButton,"curr_inven_pb")#opens the dialog box which shows the current storage
        self.add_pb = self.findChild(QPushButton,"add_pb")#add items to inventory
        self.addrecipe_pb = self.findChild(QPushButton, "addrecipe_pb")#opens the recipe dialog box
        self.set_thres_pb = self.findChild(QPushButton, "set_thres_pb")#used to make sure that the min amount of material is present in the inventory


        #setting up the add_pb button
        self.add_pb.clicked.connect(self.open_raw_material)
        self.curr_inven_pb.clicked.connect(self.open_inventory_data)
        #functions
    def open_raw_material(self):
        self.add_rm_window = Add_rm()
            #print("till this the code has run!! 2")
        self.add_rm_window.show()

    def open_inventory_data(self):
        #pass
        self.add_curr_inven_window = Curr_inventory()
        self.add_curr_inven_window.show()




