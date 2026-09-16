import sys
import os
import pytest
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from add_rm import Add_rm

app = QApplication(sys.argv)


@pytest.fixture
def win():
    return Add_rm("light")


@pytest.mark.parametrize("name, quantity, price, min_quantity", [
    ("salt", "5", "20", "1"),
    ("sugar", "10", "40", "2"),
    ("flour", "8", "50", "3")
])
def test_save_data(win, name, quantity, price, min_quantity):
    win.name_le1.setText(name)
    win.name_le2.setText(quantity)
    win.name_le3.setText(price)
    win.name_le4.setText(min_quantity)

    win.save_data()

    assert win.name_le1.text() == name
    assert win.name_le2.text() == quantity
    assert win.name_le3.text() == price
    assert win.name_le4.text() == min_quantity


def test_save_data_empty_field(win):
    win.name_le1.setText("salt")
    win.name_le2.setText("5")
    win.name_le3.setText("20")
    win.name_le4.setText("")

    win.save_data()

    assert win.name_le4.text() == ""