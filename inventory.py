from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QWidget
from PyQt5 import uic
import os
import json
import sys

from add_rm import Add_rm
from curr_inventory_win import Curr_inventory
from recipe import recipe

class Inventory(QMainWindow):
    def __init__(self,theme):
        super(Inventory,self).__init__()
        #super(Add_rm, self).__init__()

        self.theme = theme
        ui_file = "Inventory.ui"

        self.add_rm_window = None
        self.add_curr_inven_window = None
        self.add_recipe_window = None


        if not os.path.exists(ui_file):
            print(f"Error: {ui_file} not found!")
            return

        uic.loadUi(ui_file, self)


        self.setWindowTitle("Inventory")

        # inheriting the widgets
        self.curr_inven_pb = self.findChild(QPushButton,"curr_inven_pb")#opens the dialog box which shows the current storage
        self.add_pb = self.findChild(QPushButton,"add_pb")#add items to inventory
        self.addrecipe_pb = self.findChild(QPushButton, "addrecipe_pb")#opens the recipe dialog box

        self.add_pb.clicked.connect(self.open_raw_material)
        self.curr_inven_pb.clicked.connect(self.open_inventory_data)
        self.addrecipe_pb.clicked.connect(self.open_recipe)

        self.change_theme()

    def open_raw_material(self):
        self.add_rm_window = Add_rm(self.theme)
            #print("till this the code has run!! 2")
        self.add_rm_window.show()

    def open_inventory_data(self):
        #pass
        self.add_curr_inven_window = Curr_inventory(self.theme)
        self.add_curr_inven_window.show()

    def open_recipe(self):
        self.add_recipe_window = recipe(self.theme)
        self.add_recipe_window.show()


    def change_theme(self):

        if self.theme == "Dark":
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
        else:  # Light theme
            self.setStyleSheet("background-color: white; color: black;")