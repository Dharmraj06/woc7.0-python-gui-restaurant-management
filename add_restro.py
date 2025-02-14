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

        # Set window title
        self.setWindowTitle("Add Restaurant Details")

        # Get widgets
        self.logo_label = self.findChild(QLabel, "logo_label")
        self.add_logo_button = self.findChild(QPushButton, "add_logo_pb")
        self.cancel_pb = self.findChild(QPushButton, "cancel_pb")
        self.add_restro_pb = self.findChild(QPushButton, "add_restro_pb")

        self.name_edit = self.findChild(QLineEdit, "lineEdit")
        self.address_edit = self.findChild(QLineEdit, "lineEdit_2")
        self.contact_edit = self.findChild(QLineEdit, "lineEdit_3")

        self.selected_logo_path = None  # To store the selected logo path

        # Connect buttons
        self.add_logo_button.clicked.connect(self.add_logo)
        self.cancel_pb.clicked.connect(self.close)
        self.add_restro_pb.clicked.connect(self.save_restaurant_data)

    def add_logo(self):
        """ Opens file dialog to select an image and displays it in logo_label """
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Logo", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            pixmap = QPixmap(file_name)
            self.logo_label.setPixmap(pixmap)
            self.logo_label.setScaledContents(True)
            self.selected_logo_path = file_name  # Store selected image path

    def save_restaurant_data(self):
        name = self.name_edit.text().strip()
        address = self.address_edit.text().strip()
        contact = self.contact_edit.text().strip()

        if not name or not address or not contact:
            print("Error: All fields must be filled in.")
            return

        # Ensure logo is selected
        if not self.selected_logo_path:
            print("Error: No logo selected.")
            return

        # Create folder for storing logos
        logo_folder = os.path.join(os.getcwd(), "restro_logos")
        os.makedirs(logo_folder, exist_ok=True)

        # Save the image in the logo folder with a unique name
        logo_filename = f"{name.replace(' ', '_')}.png"  # Rename logo using restaurant name
        saved_logo_path = os.path.join(logo_folder, logo_filename)
        shutil.copy(self.selected_logo_path, saved_logo_path)  # Copy image to storage folder

        # Prepare data
        data = {
            "Name": name,
            "Address": address,
            "Contact": contact,
            "Logo": saved_logo_path  # Store image path in JSON
        }

        # File path for storing restaurant details
        file_path = os.path.join(os.getcwd(), "restro_details.json")

        # Read existing data
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

        # Append new restaurant data
        existing_data.append(data)

        # Write updated data back to file
        with open(file_path, "w") as f:
            json.dump(existing_data, f, indent=4)

        print("Restaurant details saved successfully.")
