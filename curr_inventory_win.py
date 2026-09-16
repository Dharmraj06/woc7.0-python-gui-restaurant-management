from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog, QListView
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QStandardItem,QStandardItemModel, QColor
import os
import json
from PyQt5.QtCore import QStringListModel

class Curr_inventory(QMainWindow):
    def __init__(self,theme):
        super(Curr_inventory,self).__init__()

        self.theme = theme
        ui_file = "curr_inven.ui"


        if not os.path.exists(ui_file):
            print(f"Error: {ui_file} not found!")
            return

        uic.loadUi(ui_file, self)


        self.setWindowTitle("Current Inventory")

        #inheriting
        self.price_list = self.findChild(QListView,"price_list")
        self.qty_list = self.findChild(QListView,"qty_list")
        self.item_list = self.findChild(QListView,"item_list")
        self.m_qty_list = self.findChild(QListView,"m_qty_list")
        self.cancel_pb = self.findChild(QPushButton, "cancel_pb")
        self.remove_pb = self.findChild(QPushButton, "remove_pb")

        # Ensure type checkers know these widgets were found before using them.
        assert self.price_list is not None
        assert self.qty_list is not None
        assert self.item_list is not None
        assert self.m_qty_list is not None
        assert self.cancel_pb is not None
        assert self.remove_pb is not None

        item_scrollbar = self.item_list.verticalScrollBar()
        qty_scrollbar = self.qty_list.verticalScrollBar()
        m_qty_scrollbar = self.m_qty_list.verticalScrollBar()
        price_scrollbar = self.price_list.verticalScrollBar()
        assert item_scrollbar is not None
        assert qty_scrollbar is not None
        assert m_qty_scrollbar is not None
        assert price_scrollbar is not None

        # Connect button
        self.cancel_pb.clicked.connect(self.close_window)
        self.remove_pb.clicked.connect(self.remove_item)

        #model
        self.price_model = QStandardItemModel()
        self.name_model = QStandardItemModel()
        self.quant_model = QStandardItemModel()
        self.min_qantity_model = QStandardItemModel()

        item_scrollbar.valueChanged.connect(
            qty_scrollbar.setValue
        )
        item_scrollbar.valueChanged.connect(
            m_qty_scrollbar.setValue
        )
        item_scrollbar.valueChanged.connect(
            price_scrollbar.setValue
        )


        qty_scrollbar.valueChanged.connect(
            item_scrollbar.setValue
        )
        qty_scrollbar.valueChanged.connect(
            price_scrollbar.setValue
        )
        qty_scrollbar.valueChanged.connect(
            m_qty_scrollbar.setValue
        )


        m_qty_scrollbar.valueChanged.connect(
            price_scrollbar.setValue
        )
        m_qty_scrollbar.valueChanged.connect(
            item_scrollbar.setValue
        )
        m_qty_scrollbar.valueChanged.connect(
            qty_scrollbar.setValue
        )


        price_scrollbar.valueChanged.connect(
            qty_scrollbar.setValue
        )
        price_scrollbar.valueChanged.connect(
            m_qty_scrollbar.setValue
        )
        price_scrollbar.valueChanged.connect(
            item_scrollbar.setValue
        )


        self.show_inventory_data()
        self.change_theme()

    def close_window(self) -> None:
        self.close()


    def show_inventory_data(self):
        json_file = "raw_m.json"

        if not os.path.exists(json_file):
            print(f"Error: {json_file} not found!")
            return

        try:
            with open(json_file, "r") as f:
                data = json.load(f)

            if not isinstance(data, list):
                print("Error: Invalid JSON format!")
                return


            for item in data:

                name_item = QStandardItem(item["Name"])
                price_item = QStandardItem(item["Price"])
                quant_item = QStandardItem(item["Quant"])
                min_quant_item = QStandardItem(item["Min Quantity"])

                if item["Quant"] < item["Min Quantity"]:
                    name_item.setForeground(QColor("red"))
                    quant_item.setForeground(QColor("red"))

                self.name_model.appendRow(name_item)
                self.price_model.appendRow(price_item)
                self.quant_model.appendRow(quant_item)
                self.min_qantity_model.appendRow(min_quant_item)

                self.item_list.setModel(self.name_model)
                self.price_list.setModel(self.price_model)
                self.qty_list.setModel(self.quant_model)
                self.m_qty_list.setModel(self.min_qantity_model)

        except json.JSONDecodeError:
            print("Error: Failed to decode JSON file!")

    def remove_item(self):
        selected_idx = self.item_list.selectedIndexes()

        if not selected_idx:
            print("No item selected!")
            return

        row = selected_idx[0].row()

        try:
            with open("raw_m.json", "r") as f:
                data = json.load(f)

            if 0 <= row < len(data):
                data.pop(row)

            with open("raw_m.json", "w") as f:
                json.dump(data, f, indent=4)

            self.name_model.removeRow(row)
            self.price_model.removeRow(row)
            self.quant_model.removeRow(row)
            self.min_qantity_model.removeRow(row)

            print("Item removed successfully")

        except :
            print("Error removing item")

    def change_theme(self):

        if self.theme == "Dark":
            self.setStyleSheet("background-color: #2E2E2E; color: black;")
        else:  # Light theme
            self.setStyleSheet("background-color: white; color: black;")


