import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QListView, QLineEdit, QCheckBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PyQt5 import uic

class billing(QMainWindow):
    def __init__(self,theme):
        super(billing, self).__init__()

        self.theme = theme

        self.amt_model = QStandardItemModel()
        self.price_model = QStandardItemModel()
        self.qty_model = QStandardItemModel()
        self.item_model = QStandardItemModel()
        ui_file = "bill_win.ui"
        if not os.path.exists(ui_file):
            print(f"Error: {ui_file} not found!")
            return

        uic.loadUi(ui_file, self)

        # Inherit widgets using findChild
        self.logo_label = self.findChild(QLabel, "logo_label")
        self.name_label = self.findChild(QLabel, "label_name")
        self.gst_label = self.findChild(QLabel, "label_gst")
        self.fssai_label = self.findChild(QLabel, "label_fssai")

        self.subtotal_label = self.findChild(QLabel, "show_subtotal_label")
        self.discount_label = self.findChild(QLabel, "show_discount_label")
        self.gtotal_label = self.findChild(QLabel, "show_gtotal_label")

        self.amt_list = self.findChild(QListView, "amt_list")
        self.qty_list = self.findChild(QListView, "qty_list")
        self.item_list = self.findChild(QListView, "item_list")
        self.price_list = self.findChild(QListView, "price_list")

        self.add_disc_lineedit = self.findChild(QLineEdit, "add_disc_lineEdit")

        self.cancel_pb = self.findChild(QPushButton, "cancel_pb")
        #self.print_pb = self.findChild(QPushButton, "print_pb")

        self.discount_cb = self.findChild(QCheckBox, "discount_cb")

        # Connecting button
        self.cancel_pb.clicked.connect(self.close_window)
        self.discount_cb.stateChanged.connect(self.add_discount)
        self.discount = 0
        self.subtotal = 0
        self.bill_items = []  # Store merged bill items

        self.set_logo_name()
        self.process_bill_items()
        self.change_theme()



    def set_logo_name(self):
        restro_json_file = "restro_details.json"

        if not os.path.exists(restro_json_file):
            print(f"Error: {restro_json_file} not found!")
            return

        try:
            with open(restro_json_file, "r") as f:
                data = json.load(f)

            if "Name" in data[0]:
                self.name_label.setText(data[0]["Name"])
            else:
                print("Invalid data in JSON")

            if "Logo" in data[0]:
                logo_filename = data[0]["Logo"]

                if logo_filename:
                    pixmap = QPixmap(logo_filename)
                    scaled_pixmap = pixmap.scaled(self.logo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.logo_label.setPixmap(scaled_pixmap)
                    self.logo_label.setScaledContents(False)

            if "fssai" in data[0]:
                self.fssai_label.setText(f"{data[0]["fssai"]}")

            if "gstin" in data[0]:
                self.gst_label.setText(f"{data[0]["gstin"]}")

        except Exception as e:
            print(f"Error loading restaurant details: {e}")

    def process_bill_items(self):
        bill_json_file = "recipe_bill.json"

        if not os.path.exists(bill_json_file):
            print(f"Error: {bill_json_file} not found!")
            return

        try:
            with open(bill_json_file, "r") as f:
                bill_data = json.load(f)

            self.bill_items = self.merge_duplicate_items(bill_data)  # Merge duplicate items
            self.update_ui_lists()
            self.calculate_totals()  # Calculate totals after processing

        except Exception as e:
            print(f"Unexpected error in process_bill_items: {e}")

    def merge_duplicate_items(self, bill_data):
        item_dict = {}

        for item in bill_data:
            name = item["recipe_name"]
            price = float(item["price"])

            if name in item_dict:
                item_dict[name]["qty"] += 1
                item_dict[name]["amount"] += price
            else:
                item_dict[name] = {"name": name, "price": price, "qty": 1, "amount": price}

        return list(item_dict.values())

    def update_ui_lists(self):
        for item in self.bill_items:
            item_name = QStandardItem(str(item["name"]))
            item_qty = QStandardItem(str(item["qty"]))
            item_price = QStandardItem(f"₹{item['price']:.2f}")
            item_amt = QStandardItem(f"₹{item['amount']:.2f}")

            self.item_model.appendRow(item_name)
            self.qty_model.appendRow(item_qty)
            self.price_model.appendRow(item_price)
            self.amt_model.appendRow(item_amt)

        self.item_list.setModel(self.item_model)
        self.qty_list.setModel(self.qty_model)
        self.price_list.setModel(self.price_model)
        self.amt_list.setModel(self.amt_model)

    def calculate_totals(self):

        subtotal = sum(item["amount"] for item in self.bill_items)
        discount_amt = (self.discount / 100) * subtotal if self.discount > 0 else 0
        g_total = subtotal - discount_amt

        self.subtotal_label.setText(f"₹{subtotal:.2f}")
        self.discount_label.setText(f"₹{discount_amt:.2f}")
        self.gtotal_label.setText(f"₹{g_total:.2f}")

    def add_discount(self):
        if self.discount_cb.isChecked():
            discount_value = self.add_disc_lineedit.text().strip()
            if discount_value:
                    self.discount = int(discount_value)
            else:
                print("No discount entered.")
        else:
            self.discount = 0

        self.calculate_totals()

    def close_window(self):

        bill_json_file = "recipe_bill.json"
        try:
            with open(bill_json_file, "w") as f:
                json.dump([], f)  # Overwrite with an empty list
        except Exception as e:
            print(f"Error clearing JSON file: {e}")

        self.amt_list.setModel(None)
        self.price_list.setModel(None)
        self.qty_list.setModel(None)
        self.item_list.setModel(None)

        self.amt_model.clear()
        self.price_model.clear()
        self.qty_model.clear()
        self.item_model.clear()

        self.amt_list.setModel(self.amt_model)
        self.price_list.setModel(self.price_model)
        self.qty_list.setModel(self.qty_model)
        self.item_list.setModel(self.item_model)

        self.close

    def change_theme(self):

        if self.theme == "Dark":
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
        else:  # Light theme
            self.setStyleSheet("background-color: white; color: black;")