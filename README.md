# Restaurant Management System

A desktop-based restaurant management application built with **Python** and **PyQt5**. It provides a complete operational workflow — from initial restaurant configuration through inventory tracking, recipe management, order taking, and bill generation — all within a native GUI without requiring a backend server or database engine.

---

## Features

- **Restaurant Configuration** — Store restaurant name, GSTIN, FSSAI licence number, and logo. Details persist across sessions and appear on the menu and billing screens.
- **Raw Material Management** — Add raw materials (ingredients) with name, quantity, price, and a minimum-stock threshold.
- **Inventory Viewer** — Display all raw materials in a synchronized, scrollable four-column list (name, quantity, price, minimum quantity). Items whose current stock falls below the minimum threshold are highlighted in red.
- **Recipe Management** — Define recipes by name, price, category (Appetizers, Main Courses, Beverages, Side Dishes), and a list of required raw materials with their per-serving quantities.
- **Menu & Order Management** — Browse recipes filtered by category. Items whose required raw materials are below the minimum threshold are visually greyed out. Adding an item to an order deducts the corresponding raw material quantities from inventory and records the order in a staging file.
- **Billing** — Generate an itemised bill from pending orders. Duplicate items are automatically merged into a single line with a combined quantity and amount. Supports percentage-based discount entry via checkbox. Displays subtotal, discount amount, and grand total in Indian Rupees (₹).
- **Light / Dark Theme** — Application-wide theme toggle propagated to all child windows at open time.
- **JSON-based Persistent Storage** — All data (restaurant details, raw materials, recipes, and in-progress bill) is stored as human-readable JSON files; no database installation required.
- **Automated Testing** — pytest test suite covering raw-material data entry, billing calculation logic, and recipe persistence.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Application language |
| PyQt5 5.15 | GUI framework and `.ui` file loading via `PyQt5.uic` |
| JSON (stdlib) | Persistent file-based storage |
| pytest 9.x | Automated unit and integration testing |

---

## Project Structure

```
woc7.0-python-gui-restaurant-management/
├── main_win.py              # Application entry point; main window
├── add_restro.py            # Restaurant details form (name, GSTIN, FSSAI, logo)
├── add_rm.py                # Add raw material form
├── inventory.py             # Inventory hub window (links to sub-windows)
├── curr_inventory_win.py    # Current inventory viewer with low-stock highlighting
├── recipe.py                # Add/configure recipes
├── menu_win.py              # Menu browser, order selection, and stock deduction
├── billing_window.py        # Bill generation, duplicate merging, and discount
│
├── *.ui                     # Qt Designer UI layout files (loaded at runtime)
│
├── restro_details.json      # Persisted restaurant profile
├── raw_m.json               # Persisted raw material inventory
├── recipe_list.json         # Persisted recipe catalogue
├── recipe_bill.json         # Staging file for the current open order
│
├── restro_logos/            # Restaurant logo images (copied here on save)
│
└── tests/
    ├── test_add_rm.py       # Tests for raw material form validation and save
    ├── test_billing.py      # Tests for billing merge logic and total calculations
    └── test_recipe.py       # Tests for recipe save and raw-material association
```

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `main_win.py` | Bootstraps `QApplication`, renders the main dashboard, reads the restaurant name from `restro_details.json`, and navigates to all sub-windows. |
| `add_restro.py` | Form for entering/updating restaurant profile. Copies the chosen logo into `restro_logos/` and appends the record to `restro_details.json`. |
| `add_rm.py` | Form for adding a raw material entry (name, quantity, price, minimum quantity) to `raw_m.json`. |
| `inventory.py` | Hub window with buttons that open `Add_rm` (add stock), `Curr_inventory` (view stock), and `recipe` (add recipes). |
| `curr_inventory_win.py` | Reads `raw_m.json` and renders four synchronised `QListView` columns. Rows where `Quant < Min Quantity` are coloured red. Supports row removal with live JSON update. |
| `recipe.py` | Form for defining a recipe: name, price, category (from a `QComboBox`), and one or more raw materials drawn from `raw_m.json`. Saves to `recipe_list.json`. |
| `menu_win.py` | Loads recipes from `recipe_list.json` filtered by the selected category. Checks each item's required materials against `raw_m.json` to colour-code availability. On order add, deducts quantities from `raw_m.json` and appends the item to `recipe_bill.json`. Clears `recipe_bill.json` on cancel. |
| `billing_window.py` | Reads `recipe_bill.json`, merges repeated items (accumulating quantity and amount), and renders an itemised bill. Applies a percentage discount when the checkbox is checked. Clears `recipe_bill.json` on close. |

### JSON Data Files

| File | Structure | Description |
|---|---|---|
| `restro_details.json` | `[{Name, gstin, fssai, Logo}]` | Restaurant profile. Only the first element is read by the UI. |
| `raw_m.json` | `[{Name, Quant, Price, Min Quantity}]` | Running inventory. Quantities are stored as strings and decremented on order. |
| `recipe_list.json` | `[{name, price, type, raw_materials[], quantities[]}]` | Full recipe catalogue. `raw_materials` and `quantities` are parallel arrays. |
| `recipe_bill.json` | `[{recipe_name, price}]` | Transient staging file for one open order session. Cleared when the menu or billing window is closed. |

---

## Application Workflow

```
1. Launch (main_win.py)
       │
       ├─► Edit Details → add_restro.py
       │       Saves restaurant name, GSTIN, FSSAI, logo → restro_details.json
       │
       ├─► Raw Materials → add_rm.py
       │       Adds ingredient entries → raw_m.json
       │
       ├─► Inventory → inventory.py
       │       ├─► View Stock  → curr_inventory_win.py  (reads raw_m.json, highlights low stock)
       │       └─► Add Recipe  → recipe.py              (reads raw_m.json, writes recipe_list.json)
       │
       ├─► Menu → menu_win.py
       │       Displays recipes by category, checking raw_m.json for availability.
       │       "Add to Order" deducts stock and appends item → recipe_bill.json
       │
       └─► Billing → billing_window.py
               Reads recipe_bill.json, merges duplicates, applies optional discount.
               Displays subtotal, discount, and grand total. Clears recipe_bill.json on close.
```

---

## Installation

### Prerequisites

- Python 3.10 or later
- Git

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/Dharmraj06/woc7.0-python-gui-restaurant-management.git
cd woc7.0-python-gui-restaurant-management

# 2. Create and activate a virtual environment
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install PyQt5 pytest

# 4. Run the application
python main_win.py
```

> **Note:** All `.ui` files must remain in the project root directory alongside the Python modules, as they are loaded at runtime relative to the working directory.

### Running Tests

The test suite must be executed from the project root so that the JSON data files resolve correctly.

```bash
pytest tests/
```

---
