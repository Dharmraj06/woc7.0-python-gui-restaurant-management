import sys
import os
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from add_rm import Add_rm

app = QApplication(sys.argv)


def test_save_data():
    win = Add_rm("light")

    win.name_le1.setText("salt")
    win.name_le2.setText("5")
    win.name_le3.setText("20")
    win.name_le4.setText("1")

    win.save_data()

    assert win.name_le1.text() == "salt"
    assert win.name_le2.text() == "5"
    assert win.name_le3.text() == "20"
    assert win.name_le4.text() == "1"


def test_save_data_empty_field():
    win = Add_rm("light")

    win.name_le1.setText("salt")
    win.name_le2.setText("5")
    win.name_le3.setText("20")
    win.name_le4.setText("")

    win.save_data()

    assert win.name_le4.text() == ""