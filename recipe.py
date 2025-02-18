from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QWidget, QComboBox, QListView
from PyQt5 import uic
import os
import json


class recipe(QMainWindow):

    def __init__(self, theme):
        super(recipe, self).__init__()
        # super(Add_rm, self).__init__()

        self.theme = theme
        ui_file = "recipe_win.ui"

        if not os.path.exists(ui_file):
            print(f"Error: {ui_file} not found!")
            return

        uic.loadUi(ui_file, self)

        self.setWindowTitle("Add Recipe")

        self.cancel_pb = self.findChild(QPushButton, "cancel_pb")

        self.recipe_lineEdit = self.findChild(QLineEdit, "recipe_lineEdit")  # main name of the recipe
        self.add_recipe_pb = self.findChild(QPushButton, "add_recipe_pb")  # adds the recipe to the json file
        self.price_lineEdit = self.findChild(QLineEdit, "price_lineEdit")  # sets the price of the recipe
        self.type_comboBox = self.findChild(QComboBox, "type_comboBox")  # sets the type of the recipe
        self.rm_list = self.findChild(QListView, "rm_list")  # shows the list of the raw materials
        self.quant_list = self.findChild(QListView, "quant_list")  # list of the quantity of the raw material
        self.add_rm_pb = self.findChild(QPushButton, "add_rm_pb")  # adds the rm to the list
        self.quant_lineEdit = self.findChild(QLineEdit, "quant_lineEdit")  # enters the quant of the rm
        self.rm_comboBox = self.findChild(QComboBox, "rm_comboBox")  # enters the name of th rm

        # connecting the pushbuttons
        self.add_recipe_pb.clicked.connect(self.add_recipe)
        self.add_rm_pb.clicked.connect(self.add_rm)
        self.cancel_pb.clicked.connect(self.close)

        self.rm_name_model = QStandardItemModel()
        self.quant_list_model = QStandardItemModel()

        self.rm_list.setModel(self.rm_name_model)
        self.quant_list.setModel(self.quant_list_model)
        self.change_theme()
        self.show_rm()

    def add_recipe(self):
        name = self.recipe_lineEdit.text().strip()
        price = self.price_lineEdit.text().strip()
        recipe_type = self.type_comboBox.currentText().strip()

        raw_m_list = []
        quant_m_list = []
        for i in range(self.rm_name_model.rowCount()):
            raw_m_list.append(self.rm_name_model.item(i).text())

        for i in range(self.quant_list_model.rowCount()):
            quant_m_list.append(self.quant_list_model.item(i).text())

            # Create a dictionary to store the recipe data
        recipe_data = {
            "name": name,
            "price": price,
            "type": recipe_type,

            "raw_materials": raw_m_list,
            "quantities": quant_m_list
        }

        # Open (or create) the JSON file to save the data
        try:
            # Open file in read-write mode ('r+')
            with open("recipe_list.json", "r+") as file:
                try:
                    # Load the existing data
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    # If the file is empty or invalid, initialize an empty list
                    existing_data = []

                # Append the new recipe data
                existing_data.append(recipe_data)

                # Move the file pointer to the beginning to overwrite the file
                file.seek(0)

                # Write the updated data to the file
                json.dump(existing_data, file, indent=4)

                file.truncate()

            print("Recipe added successfully!")
        except Exception as e:
            print(f"Error saving recipe: {e}")

        self.recipe_lineEdit.setText("")
        self.price_lineEdit.setText("")
        self.rm_name_model.clear()
        self.quant_list_model.clear()

    def add_rm(self):
        rm_name = self.rm_comboBox.currentText().strip()
        quant = self.quant_lineEdit.text().strip()

        if not rm_name and quant:
            print("invalid input!!")
        else:
            # rm_data = {
            #     "rm_name" : rm_name,
            #     "quant" : quant
            #     }
            rm_name_item = QStandardItem(rm_name)
            quant_item = QStandardItem(quant)

            self.rm_name_model.appendRow(rm_name_item)
            self.quant_list_model.appendRow(quant_item)

            self.quant_lineEdit.setText("")



    def change_theme(self):

        if self.theme == "Dark":
            self.setStyleSheet("background-color: #2E2E2E; color: white;")
        else:  # Light theme
            self.setStyleSheet("background-color: white; color: black;")

    def show_rm(self):
        try:
            with open("raw_m.json", "r") as file:
                try:
                    existing_data = json.load(file)
                except json.JSONDecodeError:
                    existing_data = []
        except FileNotFoundError:
            print("Error: raw_m.json not found!")
            existing_data = []

        self.rm_comboBox.clear()

        if isinstance(existing_data, list):
            for item in existing_data:
                self.rm_comboBox.addItem(item["Name"])
        else:
            print("Error: Invalid format in raw_m.json")


