# Test Automation — Online Boutique

[![CI](https://github.com/ledermanoam/AI-automation-projects/actions/workflows/ci.yml/badge.svg)](https://github.com/ledermanoam/AI-automation-projects/actions/workflows/ci.yml)

## What This Is

This is an automated test suite for the **Online Boutique** web application running at
`http://192.168.49.2:31885/`. It uses:

- **pytest** — the test runner
- **Playwright** — controls a real browser to simulate user actions
- **Page Object Model (POM)** — keeps test code organized and easy to maintain

There are two types of tests:

| Type | Folder | What it does |
|------|--------|--------------|
| UI tests | `tests/ui/` | Opens a real browser, clicks around, checks what the user sees |
| API tests | `tests/api/` | Sends HTTP requests directly to the app's backend |

---

## Requirements

- Python 3.10 or higher
- pip

---

## How to Install

**1. Clone or download this project**, then open a terminal in the project folder.

**2. Install Python dependencies:**

```bash
pip install -r requirements.txt
```

**3. Install the Playwright browser binaries** (one-time setup):

```bash
playwright install chromium
```

---

## How to Run Tests

### Run the product navigation tests (the main UI test)

```bash
pytest tests/ui/test_product_navigation.py -v
```

### Run all UI tests

```bash
pytest tests/ui/ -v
```

### Run all API tests

```bash
pytest tests/api/ -v
```

### Run everything

```bash
pytest -v
```

### Run tests by marker

```bash
pytest -m ui -v          # only UI tests
pytest -m api -v         # only API tests
pytest -m smoke -v       # only smoke tests
pytest -m regression -v  # only regression tests
```

### Headed mode vs headless mode

By default, tests run with `headless=False` — you can see the browser window open and
watch the test click through the app. This is great for debugging.

To run in **headless mode** (no browser window — useful for CI or running on a server),
open `tests/ui/conftest.py` and change line 29:

```python
# Before (headed — you see the browser):
browser = playwright.chromium.launch(headless=False)

# After (headless — no browser window):
browser = playwright.chromium.launch(headless=True)
```

### View the HTML test report

After any test run, an HTML report is automatically saved to:

```
reports/test_report.html
```

Open it in any browser to see a detailed pass/fail breakdown.

---

## Latest Test Results

Run on 2026-03-31 against `http://192.168.49.2:31885/`

```
tests/ui/test_product_navigation.py::TestProductNavigation::test_sunglasses_and_watch_properties PASSED

1 passed in 4.62s
```

**What the test covers:**

1. Opens the homepage
2. Clicks the Sunglasses product card
3. Verifies the price is `$19.99`
4. Verifies the description text is correct
5. Clicks the site logo to return to the homepage
6. Clicks the Watch product card
7. Verifies the price is `$109.99`
8. Verifies the description text is correct

---

## Project Structure

```
tests/
  pages/                    # Page Object classes (one file per page)
    __init__.py
    home_page.py            # HomePage — the main product grid
    product_page.py         # ProductPage — a single product detail page

  ui/                       # UI test files (use a real browser)
    __init__.py
    conftest.py             # Browser setup fixtures for UI tests
    test_product_navigation.py

  api/                      # API test files (HTTP only, no browser)
    __init__.py
    conftest.py
    test_cart_api.py
    test_health.py
    test_products_api.py

  __init__.py               # Makes 'tests' a Python package (required)
  conftest.py               # Shared fixtures: base_url, product_ids

pytest.ini                  # pytest settings (test paths, markers, HTML report)
requirements.txt            # Python package dependencies
reports/
  test_report.html          # Auto-generated HTML report after each run
```

---

## How to Add a New Test

Follow these four steps.

### Step 1 — Create a Page Object (if the page doesn't have one yet)

Create a new file in `tests/pages/`, for example `tests/pages/cart_page.py`:

```python
"""cart_page.py - Page object for the shopping cart page."""


class CartPage:
    """Represents the shopping cart page (/cart)."""

    # Define all locators here as class constants
    CART_ITEMS = ".cart-item"
    CHECKOUT_BUTTON = "button.checkout-btn"
    TOTAL_PRICE = ".cart-total"

    def __init__(self, page):
        self.page = page

    def get_item_count(self):
        """Return the number of items in the cart."""
        return self.page.locator(self.CART_ITEMS).count()

    def click_checkout(self):
        """Click the Checkout button."""
        self.page.locator(self.CHECKOUT_BUTTON).click()
        self.page.wait_for_load_state("networkidle")

    def get_total(self):
        """Return the total price text shown in the cart."""
        return self.page.locator(self.TOTAL_PRICE).text_content().strip()
```

**Rules for page objects:**
- No `assert` statements — those belong only in test files
- All locators at the top as class constants
- Methods describe user actions: `click_`, `get_`, `fill_`, etc.

### Step 2 — Write the test

Create a new file in `tests/ui/`, for example `tests/ui/test_cart.py`:

```python
"""test_cart.py - Tests for the shopping cart page."""

from tests.pages.home_page import HomePage
from tests.pages.product_page import ProductPage
from tests.pages.cart_page import CartPage


def test_adding_item_to_cart_increases_count(page, base_url):
    """Verify that adding a product adds it to the cart."""
    home = HomePage(page)
    product = ProductPage(page)
    cart = CartPage(page)

    # Click on a product and add it to the cart
    home.click_product_by_name("Sunglasses")
    product.click_add_to_cart()

    # Verify the cart has one item
    item_count = cart.get_item_count()
    assert item_count == 1, f"Expected 1 cart item, got: {item_count}"
```

**Rules for tests:**
- Each test function starts with `test_`
- Each test has a docstring explaining what it checks
- Tests are independent — do not rely on another test having run first
- Use `assert` with a helpful message so failures are easy to read

### Step 3 — Run your new test

```bash
pytest tests/ui/test_cart.py -v
```

### Step 4 — Mark your test (optional)

Add a marker to group the test with others of the same type:

```python
import pytest

@pytest.mark.regression
def test_adding_item_to_cart_increases_count(page, base_url):
    ...
```

Available markers are defined in `pytest.ini`: `ui`, `api`, `smoke`, `regression`.
