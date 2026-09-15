import sys
import os
import json
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from add_rm import Add_rm

app = QApplication.instance() or QApplication(sys.argv)


def test_save_data_valid_input(tmp_path):
    # write an empty list to a temp file so the real raw_m.json is never touched
    json_file = tmp_path / "raw_m.json"
    json_file.write_text("[]")

    win = Add_rm("light")
    win.name_le1.setText("salt")
    win.name_le2.setText("5")
    win.name_le3.setText("20")
    win.name_le4.setText("1")


    # temporarily point cwd at tmp_path before calling it
    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        win.save_data()
    finally:
        os.chdir(original_cwd)

    data = json.loads(json_file.read_text())

    assert len(data) == 1
    assert data[0]["Name"] == "salt"
    assert data[0]["Quant"] == "5"
    assert data[0]["Price"] == "20"
    assert data[0]["Min Quantity"] == "1"


def test_save_data_empty_field(tmp_path):
    json_file = tmp_path / "raw_m.json"
    json_file.write_text("[]")

    win = Add_rm("light")
    win.name_le1.setText("salt")
    win.name_le2.setText("5")
    win.name_le3.setText("20")
    win.name_le4.setText("")  # one field left empty

    original_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        win.save_data()
    finally:
        os.chdir(original_cwd)

    data = json.loads(json_file.read_text())

    # nothing 
    assert len(data) == 0
