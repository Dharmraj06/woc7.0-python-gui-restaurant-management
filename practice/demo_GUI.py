import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QComboBox, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
)


class ThemeSwitcher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Theme Switcher")
        self.setGeometry(100, 100, 400, 300)

        # Initialize UI elements
        self.initUI()

    def initUI(self):
        # ComboBox for theme selection
        self.comboBox = QComboBox(self)
        self.comboBox.addItems(["Light Theme", "Dark Theme"])
        self.comboBox.currentIndexChanged.connect(self.switch_theme)

        # Labels
        self.label1 = QLabel("This is Label 1.", self)
        self.label2 = QLabel("This is Label 2.", self)

        # Buttons
        self.button1 = QPushButton("Button 1", self)
        self.button2 = QPushButton("Button 2", self)

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.comboBox)

        # Horizontal layout for labels
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.label1)
        label_layout.addWidget(self.label2)
        layout.addLayout(label_layout)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.button1)
        button_layout.addWidget(self.button2)
        layout.addLayout(button_layout)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Apply the default (light) theme
        self.apply_light_theme()

    def switch_theme(self, index):
        if index == 0:  # Light Theme
            self.apply_light_theme()
        elif index == 1:  # Dark Theme
            self.apply_dark_theme()

    def apply_light_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
                color: #000000;
            }
            QLabel {
                font-size: 14px;
                color: #4caf50; /* Green for labels */
                font-weight: bold;
            }
            QComboBox {
                background-color: #e3f2fd; /* Light blue background */
                color: #000000;
                border: 1px solid #64b5f6; /* Light blue border */
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #ffffff;
                color: #000000;
                selection-background-color: #90caf9; /* Light blue selection */
                selection-color: #000000;
            }
            QPushButton {
                background-color: #ff5722; /* Vibrant orange */
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #e64a19; /* Slightly darker orange */
            }
        """)

    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2d2d2d;
                color: #ffffff;
            }
            QLabel {
                font-size: 14px;
                color: #f0f0f0;
            }
            QComboBox {
                background-color: #3e3e3e;
                color: #ffffff;
                border: 1px solid #5e5e5e;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #4e4e4e;
                color: #ffffff;
                selection-background-color: #757575;
                selection-color: #ffffff;
            }
            QPushButton {
                background-color: #3a86ff;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2b6dc6;
            }
        """)


# Main block
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ThemeSwitcher()
    window.show()
    sys.exit(app.exec_())
