from types import LambdaType

import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg
from PyQt5.QtWidgets import QFormLayout, QLineEdit


class MainWindow(qtw.QWidget):
    def __init__(self, l_name=None):
        super().__init__()
        # Adding the title of the window
        self.setWindowTitle("Hi there!!")
        """
        In PyQt, a Form Layout is a type of layout manager that arranges widgets in a two-column format,
        which is commonly used for forms.
        The left column typically contains labels, 
        and the right column contains corresponding input widgets such as text boxes, combo boxes, checkboxes, etc. 
        It is ideal for creating user interfaces with labeled input fields.
        """
        # Set the Layout
        #self.setLayout(qtw.QVBoxLayout())
        form_layout = qtw.QFormLayout()
        self.setLayout(form_layout)

        # add stuff/widgets
        self.label_1 = qtw.QLabel("this is a cool label Row")
        self.label_1.setFont(qtg.QFont("Helvetica", 24))

        # entry box
        self.f_name = qtw.QLineEdit(self)  # taking the first name as input
        self.l_name = qtw.QLineEdit(self)  # taking the second name as input

        # Add rows to app for taking input of first name and last name
        form_layout.addRow(self.label_1)
        form_layout.addRow('First Name', self.f_name)
        form_layout.addRow('Last Name', self.l_name)
        form_layout.addRow(qtw.QPushButton("Press this button!!",
                                           clicked=lambda: self.press_it()))

        # Show the main window
        self.show()

    def press_it(self):
        # Update the label with the selected item in the combo box
        self.label_1.setText(f'you clicked the button,{self.f_name.text()}!')

        # current index will print the index value(0-based)


# Run the application
app = qtw.QApplication([])
mw = MainWindow()
app.exec_()
