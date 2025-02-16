import json
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QListView, QLineEdit, QCheckBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PyQt5 import uic

class billing(QMainWindow):
    def __init__(self):
        super(billing, self).__init__()

        ui_file = "bill_win.ui"
        if not os.path.exists(ui_file):
            print(f"Error: {ui_file} not found!")
            return

        uic.loadUi(ui_file, self)

        # Inherit widgets using findChild
        self.logo_label = self.findChild(QLabel, "logo_label")
        self.name_label = self.findChild(QLabel, "label_name")
        self.gst_label = self.findChild(QLabel, "label_gst")
        self.fssai_label = self.findChild(QLabel, "label_gst")

        self.subtotal_label = self.findChild(QLabel, "show_subtotal_label")
        self.discount_label = self.findChild(QLabel, "show_discount_label")
        self.gtotal_label = self.findChild(QLabel, "show_gtotal_label")

        self.amt_list = self.findChild(QListView, "amt_list")
        self.qty_list = self.findChild(QListView, "qty_list")
        self.item_list = self.findChild(QListView, "item_list")
        self.price_list = self.findChild(QListView, "price_list")

        self.add_disc_lineedit = self.findChild(QLineEdit, "add_disc_lineEdit")

        self.cancel_pb = self.findChild(QPushButton, "cancel_pb")
        self.print_pb = self.findChild(QPushButton, "print_pb")

        self.discount_cb = self.findChild(QCheckBox, "discount_cb")

        # Connecting button
        self.cancel_pb.clicked.connect(self.close)
        self.discount_cb.stateChanged.connect(self.add_discount)
        self.discount = 0

        self.bill_items = []  # Store merged bill items

        self.set_logo_name()
        self.process_bill_items()

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

        except json.JSONDecodeError:
            print("Error: Invalid JSON format in recipe_bill.json")
        except Exception as e:
            print(f"Unexpected error in process_bill_items: {e}")

    def merge_duplicate_items(self, bill_data):
        item_dict = {}

        for item in bill_data:
            name = item["recipe_name"]
            price = float(item["price"])
            qty = 1

            if name in item_dict:
                item_dict[name]["qty"] += 1
                item_dict[name]["amount"] += price
            else:
                item_dict[name] = {"name": name, "price": price, "qty": 1, "amount": price}

        return list(item_dict.values())

    def update_ui_lists(self):
        item_model = QStandardItemModel()
        qty_model = QStandardItemModel()
        price_model = QStandardItemModel()
        amt_model = QStandardItemModel()

        for item in self.bill_items:
            item_model.appendRow(QStandardItem(item["name"]))
            qty_model.appendRow(QStandardItem(str(item["qty"])))
            price_model.appendRow(QStandardItem(f"{item['price']:.2f}"))
            amt_model.appendRow(QStandardItem(f"{item['amount']:.2f}"))

        self.item_list.setModel(item_model)
        self.qty_list.setModel(qty_model)
        self.price_list.setModel(price_model)
        self.amt_list.setModel(amt_model)

    def calculate_totals(self):
        subtotal = sum(item["amount"] for item in self.bill_items)
        discount_amount = (self.discount / 100) * subtotal if self.discount > 0 else 0
        grand_total = subtotal - discount_amount

        self.subtotal_label.setText(f"₹{subtotal:.2f}")
        self.discount_label.setText(f"₹{discount_amount:.2f}")
        self.gtotal_label.setText(f"₹{grand_total:.2f}")

    def add_discount(self):
        if self.discount_cb.isChecked():
            discount_value = self.add_disc_lineedit.text().strip()
            if discount_value:
                try:
                    self.discount = int(discount_value)
                    print(f"Discount set to: {self.discount}%")
                except ValueError:
                    print("Invalid discount value. Please enter a valid number.")
            else:
                print("No discount entered.")
        else:
            self.discount = 0
            print("Discount removed.")

        self.calculate_totals()
