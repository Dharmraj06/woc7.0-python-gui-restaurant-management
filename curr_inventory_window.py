from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QListView
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import os
import json
from PyQt5.QtCore import QStringListModel

class Curr_inventory(QMainWindow):
    def __init__(self):
        super(Curr_inventory,self).__init__()


        ui_file = "curr_inven.ui"

        # checking if the file exists or not;
        if not os.path.exists(ui_file):
            print(f"Error: {ui_file} not found!")
            return

        uic.loadUi(ui_file, self)

        # Set window title
        self.setWindowTitle("Current Inventory")

        #inheriting the widgets
        self.price_list = self.findChild(QListView,"price_list")
        self.qty_list = self.findChild(QListView,"qty_list")
        self.item_list = self.findChild(QListView,"item_list")
        self.m_qty_list = self.findChild(QListView,"m_qty_list")

        # display the  inventory data
        self.show_inventory_data()

    def show_inventory_data(self):
        json_file = "raw_m.json"

        if not os.path.exists(json_file):
            print(f"Error: {json_file} not found!")
            return

        try:
            with open(json_file, "r") as f:
                data = json.load(f)

            if not isinstance(data, list):  # Ensure it's a list of dictionaries
                print("Error: Invalid JSON format!")
                return

            # Extract data into separate lists

            #now if we insert a list to the list view it will show the whole list
            name_list = []
            quant_list =[]
            price_list = []
            min_qantity_list = []

            for item in data:
                name_list.append(item["Name"])
                quant_list.append(item["Quant"])
                price_list.append(item["Price"])
                min_qantity_list.append(item["Min Quantity"])

                #QStringListModel
                price_model = QStringListModel(price_list)
                name_model = QStringListModel(name_list)
                quant_model = QStringListModel(quant_list)
                min_qantity_model = QStringListModel(min_qantity_list)

                # Set the models
                self.item_list.setModel(name_model)
                self.price_list.setModel(price_model)
                self.qty_list.setModel(quant_model)
                self.m_qty_list.setModel(min_qantity_model)

        except json.JSONDecodeError:
            print("Error: Failed to decode JSON file!")






