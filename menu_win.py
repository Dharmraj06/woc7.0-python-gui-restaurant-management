from statistics import quantiles

from PyQt5.QtCore import QSysInfo, Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QComboBox, QListView
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QPixmap
from PyQt5 import uic
import sys, os
import json


class menu(QMainWindow):
    def __init__(self,theme):
        super(menu, self).__init__()

        self.theme = theme
        ui_file = "menu_win.ui"
        if not os.path.exists(ui_file):
            print(f"Error: {ui_file} not found!")
            return

        uic.loadUi(ui_file, self)

        # Inherit widgets using findChild
        self.logo_label = self.findChild(QLabel, "logo_label")  # shows the logo of the restro
        self.name_label = self.findChild(QLabel, "label_name")  # shows the name of the restro
        self.item_list = self.findChild(QListView, "item_list")  # shows the name of the recipe
        self.price_label = self.findChild(QLabel, "price_label")
        self.price_list = self.findChild(QListView, "price_list")  # shows the price of the recipe
        self.type_comboBox = self.findChild(QComboBox, "type_comboBox")  # type of the recipe
        self.cancel_pb = self.findChild(QPushButton, "cancel_pb")
        self.add_recipe_pb = self.findChild(QPushButton, "add_recipe_pb")

        # connecting the function
        self.type_comboBox.currentTextChanged.connect(self.type_change)
        self.add_recipe_pb.clicked.connect(self.add_recipe)

        self.item_list_model = QStandardItemModel()
        self.price_list_model = QStandardItemModel()
        self.type_list_model = QStandardItemModel()

        self.item_list.setModel(self.item_list_model)
        self.price_list.setModel(self.price_list_model)

        # calling functions
        self.default_type()
        self.set_logo_name()
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
                print("invalid")

            if "Logo" in data[0]:

                logo_filename = data[0]["Logo"]  # as "Logo" stores the file path of the logo

                if logo_filename:
                    pixmap = QPixmap(logo_filename)

                    # Scale the image to fit the label size while maintaining aspect ratio
                    scaled_pixmap = pixmap.scaled(self.logo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

                    self.logo_label.setPixmap(scaled_pixmap)
                    self.logo_label.setScaledContents(False)

        except:
            pass

    def type_change(self):
        selected_text = self.type_comboBox.currentText()
        json_file = "recipe_list.json"

        if not os.path.exists(json_file):
            print(f"Error: {json_file} not found!")
            return

        try:
            with open(json_file, "r") as f:
                data = json.load(f)

            if not isinstance(data, list):
                print("Error: Invalid JSON format!")
                return

            self.item_list_model.clear()
            self.price_list_model.clear()

            for item in data:
                if item["type"] == selected_text:
                    name_item = QStandardItem(item["name"])
                    price_item = QStandardItem(item["price"])

                    raw_material_file = "raw_m.json"
                    if not os.path.exists(raw_material_file):
                        print(f"Error: {json_file} not found!")
                        return
                    try:
                        with open(raw_material_file, "r") as rm_file:
                            rm_data = json.load(rm_file)

                        if not isinstance(data, list):
                            print("Error: Invalid JSON format!")
                            return

                        for raw_material in rm_data:
                            if raw_material["Name"] in item["raw_materials"]:
                                # material_index = item["raw_materials"].index(raw_material["Name"])
                                if int(raw_material["Quant"]) < int(raw_material["Min Quantity"]):
                                    name_item.setForeground(QColor(169, 169, 169))
                                    price_item.setForeground(QColor(169, 169, 169))
                                else:
                                    name_item.setForeground(QColor(47, 128, 166))
                                    price_item.setForeground(QColor(47, 128, 166))


                    except Exception as e:
                        print(f"Error occurred(nested): {e}")

                    self.item_list_model.appendRow(name_item)
                    self.price_list_model.appendRow(price_item)

        except Exception as e:
            print(f"Error occurred: {e}")

    def default_type(self):
        selected_text = self.type_comboBox.currentText()
        json_file = "recipe_list.json"

        if not os.path.exists(json_file):
            print(f"Error: {json_file} not found!")
            return

        try:
            with open(json_file, "r") as f:
                data = json.load(f)

            if not isinstance(data, list):
                print("Error: Invalid JSON format!")
                return

            self.item_list_model.clear()
            self.price_list_model.clear()

            for item in data:
                if item["type"] == selected_text:
                    name_item = QStandardItem(item["name"])
                    price_item = QStandardItem(item["price"])

                    raw_material_file = "raw_m.json"
                    if not os.path.exists(raw_material_file):
                        print(f"Error: {json_file} not found!")
                        return
                    try:
                        with open(raw_material_file, "r") as rm_file:
                            rm_data = json.load(rm_file)

                        if not isinstance(data, list):
                            print("Error: Invalid JSON format!")
                            return

                        for raw_material in rm_data:
                            if raw_material["Name"] in item["raw_materials"]:
                                # material_index = item["raw_materials"].index(raw_material["Name"])
                                if int(raw_material["Quant"]) < int(raw_material["Min Quantity"]):
                                    name_item.setForeground(QColor(169, 169, 169))
                                    price_item.setForeground(QColor(169, 169, 169))
                                else:
                                    name_item.setForeground(QColor(47, 128, 166))
                                    price_item.setForeground(QColor(47, 128, 166))


                    except Exception as e:
                        print(f"Error occurred(nested): {e}")

                    self.item_list_model.appendRow(name_item)
                    self.price_list_model.appendRow(price_item)

        except Exception as e:
            print(f"Error occurred: {e}")

    def add_recipe(self):
        indexes = self.item_list.selectedIndexes()

        recipe_json_file = "recipe_list.json"

        if not os.path.exists(recipe_json_file):
            print(f"Error: {recipe_json_file} not found!")
            return

        try:
            with open(recipe_json_file, "r") as f:
                data = json.load(f)

            if not isinstance(data, list):
                print("Error: Invalid JSON format!")
                return

        except Exception as e:
            print(f"1) Error occurred while saving: {e}")

        if indexes:
            try:
                for idx in indexes:
                    recipe_name = self.item_list_model.data(idx)

                    for item in data:
                        raw_material_file = "raw_m.json"
                        if not os.path.exists(raw_material_file):
                            print(f"Error: {raw_material_file} not found!")
                            return
                        try:
                            with open(raw_material_file, "r") as rm_file:
                                rm_data = json.load(rm_file)

                            if not isinstance(data, list):
                                print("Error: Invalid JSON format!")
                                return

                            for raw_material in rm_data:
                                if raw_material["Name"] in item["raw_materials"]:
                                    idx = item["raw_materials"].index[raw_material["Name"]]
                                    raw_material["quant"] = str(int(raw_material["quant"]) - int(item["quantities"][idx]))
                        except Exception as e:
                            print(f"error occured: {e}")

                        if recipe_name == item["name"]:
                            price = item["price"]


                    bill_data = {
                        "recipe_name": recipe_name,
                        "price": price
                    }
                    #print(f"price: {bill_data["price"]}")

                    folder_path = os.path.join(os.getcwd())
                    file_path = os.path.join(folder_path, "recipe_bill.json")

                    os.makedirs(folder_path, exist_ok=True)  # Ensure directory exists

                    try:
                        with open(file_path, "r") as f:
                            existing_data = json.load(f)
                            if not isinstance(existing_data, list):
                                existing_data = []
                    except (FileNotFoundError, json.JSONDecodeError):
                        existing_data = []

                    existing_data.append(bill_data)

                    # Write the updated data to the file
                    with open(file_path, "w") as f:
                        json.dump(existing_data, f, indent=4)

                    print("Data saved successfully.")

            except Exception as e:
                print(f"2) Error occurred while saving: {e}")

            self.type_change()

    def change_theme(self):

        if self.theme == "Dark":
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
        else:  # Light theme
            self.setStyleSheet("background-color: white; color: black;")