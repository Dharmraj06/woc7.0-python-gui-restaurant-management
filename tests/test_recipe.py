import sys
import os
import json
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QStandardItem

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recipe import recipe

app = QApplication.instance() or QApplication(sys.argv)

def test_add_recipe_saves_to_file():
    win = recipe("light")

    win.recipe_lineEdit.setText("Test Pizza")
    win.price_lineEdit.setText("299")
    
    win.add_recipe()

    with open("recipe_list.json", "r") as file:
        data = json.load(file)

    assert data[-1]["name"] == "Test Pizza"
    assert data[-1]["price"] == "299"

    # clean up the test data
    data.pop()
    with open("recipe_list.json", "w") as file:
        json.dump(data, file, indent=4)


def test_add_recipe_saves_raw_materials():
    win = recipe("light")

    win.recipe_lineEdit.setText("Test Cake")
    win.price_lineEdit.setText("450")

    win.rm_name_model.appendRow(QStandardItem("flour"))
    win.quant_list_model.appendRow(QStandardItem("2"))
    
    win.rm_name_model.appendRow(QStandardItem("sugar"))
    win.quant_list_model.appendRow(QStandardItem("1"))

    win.add_recipe()

    with open("recipe_list.json", "r") as file:
        data = json.load(file)

    assert data[-1]["name"] == "Test Cake"
    assert data[-1]["raw_materials"] == ["flour", "sugar"]
    assert data[-1]["quantities"] == ["2", "1"]

    data.pop()
    with open("recipe_list.json", "w") as file:
        json.dump(data, file, indent=4)
