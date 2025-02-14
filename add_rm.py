from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog
from PyQt5 import uic
import os
import json
import sys

class Add_rm(QMainWindow):
    def __init__(self):
        super(Add_rm, self).__init__()

        ui_file = "Add_r-m.ui"

        # Ensure the UI file exists before loading
        if not os.path.exists(ui_file):
            print(f"Error: {ui_file} not found!")
            return

        uic.loadUi(ui_file, self)

        # Set window title
        self.setWindowTitle("Add Raw Material")

        # Find input fields
        self.name_le1 = self.findChild(QLineEdit, "lineEdit")
        self.name_le2 = self.findChild(QLineEdit, "lineEdit_2")
        self.name_le3 = self.findChild(QLineEdit, "lineEdit_3")
        self.name_le4 = self.findChild(QLineEdit, "lineEdit_4")

        # Find cancel button
        self.cancel_pb = self.findChild(QPushButton, "cancel_pb")
        self.add_to_list_pb = self.findChild(QPushButton, "add_it_pb")

        # Connect cancel button
        self.cancel_pb.clicked.connect(self.close)

        # Connect add_to_list button to save data to file
        self.add_to_list_pb.clicked.connect(self.save_data)

    import os
    import json

    def save_data(self):
        # Collect text from line edits
        name1 = self.name_le1.text()
        name2 = self.name_le2.text()
        name3 = self.name_le3.text()
        name4 = self.name_le4.text()

        # Ensure all fields have data before saving
        if name1 and name2 and name3 and name4:
            try:
                data = {
                    "Name": name1,
                    "Quant": name2,
                    "Price": name3,
                    "Min Quantity": name4
                }

                folder_path = os.path.join(os.getcwd())
                file_path = os.path.join(folder_path, "raw_m.json")

                os.makedirs(folder_path, exist_ok=True)  # Ensure directory exists

                # Load existing data
                try:
                    with open(file_path, "r") as f:
                        existing_data = json.load(f)
                        if not isinstance(existing_data, list):
                            existing_data = []
                except (FileNotFoundError, json.JSONDecodeError):
                    existing_data = []

                # Append new data
                existing_data.append(data)

                # Save updated JSON
                with open(file_path, "w") as f:
                    json.dump(existing_data, f, indent=4)

                print("Data saved successfully.")

            except Exception as e:
                print(f"Error saving data: {e}")

        else:
            print("Error: All fields must be filled in.")

