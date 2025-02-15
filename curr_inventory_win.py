from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QListView
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QStandardItem,QStandardItemModel, QColor
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
        self.cancel_pb = self.findChild(QPushButton, "cancel_pb")
        self.remove_pb = self.findChild(QPushButton, "remove_pb")

        # Connect button
        self.cancel_pb.clicked.connect(self.close)
        self.remove_pb.clicked.connect(self.remove_item)

        # QStditem model
        self.price_model = QStandardItemModel()
        self.name_model = QStandardItemModel()
        self.quant_model = QStandardItemModel()
        self.min_qantity_model = QStandardItemModel()

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



            for item in data:
                # name_list.append(item["Name"])
                #quant_list.append(item["Quant"])
                #price_list.append(item["Price"])
                # min_qantity_list.append(item["Min Quantity"])

                name_item = QStandardItem(item["Name"])
                price_item = QStandardItem(item["Price"])
                quant_item = QStandardItem(item["Quant"])
                min_quant_item = QStandardItem(item["Min Quantity"])

                # adding the list as the quantity
                if item["Quant"] < item["Min Quantity"]:
                    name_item.setForeground(QColor("red"))
                    quant_item.setForeground(QColor("red"))

                #adding the items to the model
                self.name_model.appendRow(name_item)
                self.price_model.appendRow(price_item)
                self.quant_model.appendRow(quant_item)
                self.min_qantity_model.appendRow(min_quant_item)

                # Setting the models on the display
                self.item_list.setModel(self.name_model)
                self.price_list.setModel(self.price_model)
                self.qty_list.setModel(self.quant_model)
                self.m_qty_list.setModel(self.min_qantity_model)

        except json.JSONDecodeError:
            print("Error: Failed to decode JSON file!")



    def remove_item(self):
        selected_idx = self.item_list.selectedIndexes()

        if selected_idx:
            idx = selected_idx[0]

            # Remove the row
            self.name_model.removeRow(idx.row())
            self.price_model.removeRow(idx.row())
            self.quant_model.removeRow(idx.row())
            self.min_qantity_model.removeRow(idx.row())




