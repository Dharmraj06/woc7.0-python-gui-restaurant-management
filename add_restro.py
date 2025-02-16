from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QLineEdit, QFileDialog
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import os
import json
import shutil  # For copying image files

class AddRestroWindow(QMainWindow):
    def __init__(self):
        super(AddRestroWindow, self).__init__()

        ui_file = "Add_restro_win.ui"
        uic.loadUi(ui_file, self)


        self.setWindowTitle("Add Restaurant Details")

        self.logo_label = self.findChild(QLabel, "logo_label")
        self.add_logo_button = self.findChild(QPushButton, "add_logo_pb")
        self.cancel_pb = self.findChild(QPushButton, "cancel_pb")
        self.add_restro_pb = self.findChild(QPushButton, "add_restro_pb")

        self.name_edit = self.findChild(QLineEdit, "lineEdit")
        self.gstin_edit = self.findChild(QLineEdit, "lineEdit_2")
        self.fssai_edit = self.findChild(QLineEdit, "lineEdit_3")

        self.selected_logo_path = None  # To store the selected logo path

        # Connect buttons
        self.add_logo_button.clicked.connect(self.add_logo)
        self.cancel_pb.clicked.connect(self.close)
        self.add_restro_pb.clicked.connect(self.save_restaurant_data)

    def add_logo(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(self.logo_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.logo_label.setPixmap(scaled_pixmap)
            self.logo_label.setScaledContents(False)
            self.selected_logo_path = file_name  # Store selected image path

    def save_restaurant_data(self):
        name = self.name_edit.text().strip()#strip removes the unwanted spaces
        gstin = self.gstin_edit.text().strip()
        fssai = self.fssai_edit.text().strip()

        if not name or not gstin or not fssai:
            print("Error: All fields must be filled in.")
            return

        # Ensure logo is selected
        if not self.selected_logo_path:
            print("Error: No logo selected.")
            return

        # Create folder for storing logos
        logo_folder = os.path.join(os.getcwd(), "restro_logos")
        os.makedirs(logo_folder, exist_ok=True)

        logo_filename = f"{name.replace(' ', '_')}.png"
        saved_logo_path = os.path.join(logo_folder, logo_filename)
        shutil.copy(self.selected_logo_path, saved_logo_path)

        # restro_data
        restro_data = {
            "Name": name,
            "gstin": gstin,
            "fssai": fssai,
            "Logo": saved_logo_path  # Store image path in JSON
        }

        file_path = os.path.join(os.getcwd(), "restro_details.json")

        try:
            with open(file_path, "r") as f:
                try:
                    existing_data = json.load(f)
                    if not isinstance(existing_data, list):
                        existing_data = []
                except json.JSONDecodeError:
                    existing_data = []
        except FileNotFoundError:
            existing_data = []

        # Append new restaurant restro_data
        existing_data.append(restro_data)

        # Write updated restro_data back to file
        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)

        print("Restro details saved successfully!")
