import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        # Adding the title of the window
        self.setWindowTitle("Hi there!!")

        # Set the Layout
        self.setLayout(qtw.QVBoxLayout())

        # Create a label
        self.my_label = qtw.QLabel("Pick something from the list below")
        self.my_label.setFont(qtg.QFont('Arial', 24))

        # Create a combo box
        self.my_combo = qtw.QComboBox(self,
                                      editable=True,
                                      insertPolicy=qtw.QComboBox.InsertAtTop)
        self.my_combo.addItem("Pepperoni", "something")  # here somthing is the data of the words
        self.my_combo.addItem("Pepper")  # this data can be shown using the CurrentData
        self.my_combo.addItem("Tomato")
        self.my_combo.addItem("Cheese")  # here we can also add a list, each element will be added separately
        self.my_combo.insertItem(2, "third thing")  # here first is the pos and second is the item name

        # create a spinn box
        self.my_spin = qtw.QSpinBox(self, value=10, maximum=100, minimum=0, singleStep=5,
                                    prefix="#", suffix="Order")
        self.my_spin.setFont(qtg.QFont('Arial', 24))

        # create a text box
        self.my_text = qtw.QTextEdit(self,
                                     acceptRichText=True,
                                     lineWrapMode=qtw.QTextEdit.FixedColumnWidth,
                                     lineWrapColumnOrWidth=50,
                                     placeholderText="Hello world!",
                                     readOnly=False, )

        # Create an entry box
        self.my_entry = qtw.QLineEdit()
        self.my_entry.setObjectName("name_field")
        self.my_entry.setText("")

        # Create a button
        self.my_button = qtw.QPushButton("Press", clicked=self.press_it, )

        # Add widgets to the layout (in a logical order)
        self.layout().addWidget(self.my_label)
        self.layout().addWidget(self.my_combo)
        self.layout().addWidget(self.my_entry)
        self.layout().addWidget(self.my_button)
        self.layout().addWidget(self.my_spin)
        self.layout().addWidget(self.my_text)

        # Show the main window
        self.show()

    def press_it(self):
        # Update the label with the selected item in the combo box
        self.my_label.setText(f'You picked -- {self.my_text.toPLainText()}')
        self.my_text.setPlainText("You Pressed the Button!")

        # currentindex will print the index value(0-based)


# Run the application
app = qtw.QApplication([])
mw = MainWindow()
app.exec_()
