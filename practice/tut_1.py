import PyQt5.QtWidgets as qtw
import PyQt5.QtGui as qtg

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        #Adding the title of the window
        self.setWindowTitle("Hi there!!")

        #Set the Layout
        #using the verticle box layout
        self.setLayout(qtw.QVBoxLayout())

        #create a label, this label function can be used to show multiple txt on the window
        my_label = qtw.QLabel("hello!!")#this will be shown in the main window
        #cahnge the font size of label
        my_label.setFont(qtg.QFont('Arial',24))
        #create a entry box
        my_entry = qtw.QLineEdit()
        my_entry.setObjectName("name_field")
        my_entry.setText("")


        #create a button
        my_button  = qtw.QPushButton("press",
                                     clicked = lambda: press_it())

        self.layout().addWidget(my_entry)
        self.layout().addWidget(my_label)
        self.layout().addWidget(my_button)

        self.show()

        def press_it():
            my_label.setText(f'Hello {my_entry.text()}')

        self.show()



## --- end of function ---
app= qtw.QApplication([])
mw  = MainWindow()

app.exec_()

