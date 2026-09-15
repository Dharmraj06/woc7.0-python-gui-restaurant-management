import sys
import os
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from billing_window import billing

app = QApplication(sys.argv)


def test_merge_duplicate_items_empty_list():
    bill = billing("light")

    result = bill.merge_duplicate_items([])

    assert result == []


def test_merge_duplicate_items_unique_items():
    bill = billing("light")

    data = [
        {"recipe_name": "Burger", "price": "150"},
        {"recipe_name": "Fries", "price": "80"}
    ]

    result = bill.merge_duplicate_items(data)

    assert len(result) == 2
    assert result[0] == {
        "name": "Burger",
        "price": 150.0,
        "qty": 1,
        "amount": 150.0
    }
    assert result[1] == {
        "name": "Fries",
        "price": 80.0,
        "qty": 1,
        "amount": 80.0
    }


def test_merge_duplicate_items_with_duplicates():
    bill = billing("light")

    data = [
        {"recipe_name": "Burger", "price": "150"},
        {"recipe_name": "Burger", "price": "150"},
        {"recipe_name": "Fries", "price": "80"}
    ]

    result = bill.merge_duplicate_items(data)

    assert len(result) == 2
    assert result[0] == {
        "name": "Burger",
        "price": 150.0,
        "qty": 2,
        "amount": 300.0
    }
    assert result[1] == {
        "name": "Fries",
        "price": 80.0,
        "qty": 1,
        "amount": 80.0
    }


def test_calculate_totals_no_items():
    bill = billing("light")

    bill.bill_items = []
    bill.discount = 0

    bill.calculate_totals()

    assert bill.subtotal_label.text() == "₹0.00"
    assert bill.discount_label.text() == "₹0.00"
    assert bill.gtotal_label.text() == "₹0.00"


def test_calculate_totals_no_discount():
    bill = billing("light")

    bill.bill_items = [
        {"name": "Burger", "price": 150.0, "qty": 2, "amount": 300.0},
        {"name": "Fries", "price": 80.0, "qty": 1, "amount": 80.0}
    ]
    bill.discount = 0

    bill.calculate_totals()

    assert bill.subtotal_label.text() == "₹380.00"
    assert bill.discount_label.text() == "₹0.00"
    assert bill.gtotal_label.text() == "₹380.00"


def test_calculate_totals_with_discount():
    bill = billing("light")

    bill.bill_items = [
        {"name": "Burger", "price": 150.0, "qty": 2, "amount": 300.0},
        {"name": "Fries", "price": 80.0, "qty": 1, "amount": 80.0}
    ]
    bill.discount = 10

    bill.calculate_totals()

    assert bill.subtotal_label.text() == "₹380.00"
    assert bill.discount_label.text() == "₹38.00"
    assert bill.gtotal_label.text() == "₹342.00"