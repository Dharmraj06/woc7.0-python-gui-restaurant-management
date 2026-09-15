import sys
import random
from PySide6 import QtCore, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.button = QtWidgets.QPushButton("click me!")
        self.text = QtWidgets.QLabel("Hello world",
                                     alignment=QtCore.Qt.AlignLeft)
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(500, 100)
    widget.show()
    sys.exit(app.exec())