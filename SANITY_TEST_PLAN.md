# Sanity Test Suite — Online Boutique

**Application Under Test:** Google Online Boutique (microservices demo)
**Environment:** Minikube — http://192.168.49.2:31885/
**Test Framework:** Playwright + pytest (Python)
**Author:** QA — Noam Lederman
**Last Updated:** 2026-05-10

---

## 1. Purpose

A **sanity test suite** is a small, fast set of tests that verifies the most critical user-facing flows are working after a deployment, configuration change, or microservice restart. It is **not** an exhaustive regression suite — it is the "is the app alive and usable?" check.

If any of these tests fail, the build should be considered **not ready** for deeper testing.

---

## 2. Scope

### In Scope
- Homepage loads and displays products
- Product detail pages load with correct data
- Add-to-cart flow works end-to-end
- Cart displays items and can be emptied
- Currency switch updates prices
- Site navigation (logo click) works

### Out of Scope (covered by regression / E2E suites)
- Full checkout / payment flow
- Recommendation algorithm correctness
- Cross-browser / responsive layout
- Performance / load testing
- Accessibility audits
- Backend microservice unit tests

---

## 3. Entry & Exit Criteria

**Entry criteria** (preconditions before running the suite):
- Minikube cluster is up and the `frontend` service is reachable at `http://192.168.49.2:31885/`.
- All 11 microservices report `Running` in `kubectl get pods`.
- Test framework dependencies installed (`pip install -r requirements.txt`) and Playwright browsers (`playwright install`) are available.

**Exit criteria** (run is considered a pass):
- 100% of sanity tests pass.
- Total wall-clock runtime under ~2 minutes.
- No flaky retries required.

---

## 4. Test Environment

| Item | Value |
|---|---|
| Base URL | http://192.168.49.2:31885 |
| Browser | Chromium (headless by default) |
| Run command | `pytest tests/ui/sanity -m sanity -v` |
| Marker | `@pytest.mark.sanity` |

---

## 5. Test Cases

> Each test is identified by `SAN-XXX`. Tests are independent — each starts from a fresh page and does not rely on state from a previous test.

---

### SAN-001 — Homepage loads and shows products

**Priority:** Critical
**Page:** HomePage

**Steps:**
1. Navigate to `http://192.168.49.2:31885/`.
2. Wait for `networkidle`.
3. Read all product cards (`.hot-product-card`).

**Expected:**
- HTTP response is 200.
- Page title contains "Online Boutique".
- At least 1 product card is visible (catalog has 9 known products).
- Header logo (`a.navbar-brand`) is visible.

---

### SAN-002 — Product detail page loads with name, price, description

**Priority:** Critical
**Page:** HomePage → ProductPage

**Steps:**
1. Navigate to homepage.
2. Click the **Sunglasses** product card.
3. Wait for `networkidle`.
4. Read product name, price, and description.

**Expected:**
- URL contains `/product/OLJCESPC7Z`.
- Product name (`h2`) equals `"Sunglasses"`.
- Price (`.product-price`) equals `"$19.99"`.
- Description contains `"Add a modern touch to your outfits"`.
- "Add To Cart" button is visible.

---

### SAN-003 — Logo click returns user to homepage

**Priority:** High
**Page:** ProductPage → HomePage

**Steps:**
1. Navigate directly to `/product/1YMWWN1N4O` (Watch).
2. Click the header logo (`a.navbar-brand`).
3. Wait for `networkidle`.

**Expected:**
- URL is the base URL (no `/product/` segment).
- At least one `.hot-product-card` is visible.

---

### SAN-004 — Add a product to the cart

**Priority:** Critical
**Page:** ProductPage → CartPage

**Steps:**
1. Navigate directly to `/product/OLJCESPC7Z` (Sunglasses).
2. Click **Add To Cart**.
3. Wait for `networkidle`.

**Expected:**
- URL changes to `/cart`.
- Page contains the product name `"Sunglasses"`.
- Page contains price `"$19.99"`.
- "Place Order" button is visible.

---

### SAN-005 — Cart displays multiple items

**Priority:** High
**Page:** ProductPage → CartPage

**Steps:**
1. Navigate to `/product/OLJCESPC7Z` (Sunglasses) and add to cart.
2. Navigate to `/product/1YMWWN1N4O` (Watch) and add to cart.
3. Navigate to `/cart`.

**Expected:**
- Both `"Sunglasses"` and `"Watch"` text appear on the cart page.
- "Place Order" button is visible.

---

### SAN-006 — Empty cart removes all items

**Priority:** High
**Page:** CartPage

**Steps:**
1. Add any product to the cart (e.g., Sunglasses).
2. Navigate to `/cart`.
3. Click **Empty Cart**.

**Expected:**
- The previously added product name is no longer visible on the page.
- "Place Order" button is no longer visible (empty cart state).

---

### SAN-007 — Currency switch updates the price symbol

**Priority:** Medium
**Page:** HomePage / ProductPage

**Steps:**
1. Navigate to `/product/OLJCESPC7Z` (Sunglasses) — default currency USD shows `$19.99`.
2. Change currency to `EUR` via the currency dropdown in the header.
3. Wait for `networkidle`.

**Expected:**
- The price text on the product page no longer starts with `$`.
- The price text starts with `€` (or contains `EUR`).

---

### SAN-008 — Recommendations section is shown on product page

**Priority:** Medium
**Page:** ProductPage

**Steps:**
1. Navigate to `/product/OLJCESPC7Z` (Sunglasses).
2. Wait for `networkidle`.

**Expected:**
- The text `"You May Also Like"` is visible on the page.

---

### SAN-009 — Invalid product ID returns an error response

**Priority:** Low (negative case)
**Page:** ProductPage

**Steps:**
1. Navigate to `/product/INVALID_ID_999`.

**Expected:**
- HTTP response status is 500 (per app behavior — not 404).
- The homepage selectors (`.hot-product-card`) are NOT present.

---

### SAN-010 — Quantity selector is present on product page

**Priority:** Low
**Page:** ProductPage

**Steps:**
1. Navigate to `/product/1YMWWN1N4O` (Watch).

**Expected:**
- Quantity dropdown (`select[name='quantity']`) is visible.
- "Add To Cart" button is visible next to it.

---

## 6. Suggested File Layout

```
tests/
├── conftest.py                        # already present — base_url + product_ids fixtures
├── pages/
│   ├── home_page.py                   # already present
│   ├── product_page.py                # already present
│   └── cart_page.py                   # already present
└── ui/
    └── sanity/
        ├── __init__.py
        ├── test_sanity_homepage.py    # SAN-001, SAN-003
        ├── test_sanity_product.py     # SAN-002, SAN-008, SAN-009, SAN-010
        ├── test_sanity_cart.py        # SAN-004, SAN-005, SAN-006
        └── test_sanity_currency.py    # SAN-007
```

A `sanity` marker should be registered in `pytest.ini`:

```ini
[pytest]
markers =
    sanity: quick smoke checks of core user journeys
```

Run only the sanity suite:

```bash
pytest -m sanity -v
```

---

## 7. Test Data

All product IDs already live in `tests/conftest.py` under the `product_ids` fixture — sanity tests should pull from there rather than hardcoding IDs.

| Key | ID | Used by |
|---|---|---|
| sunglasses | OLJCESPC7Z | SAN-002, SAN-004, SAN-005, SAN-006, SAN-007, SAN-008, SAN-009 |
| watch | 1YMWWN1N4O | SAN-003, SAN-005, SAN-010 |

---

## 8. Risks & Assumptions

- **Currency test (SAN-007)** assumes EUR is supported; if currencies change, the assertion must be loosened to "price symbol changed from $".
- **Invalid product ID test (SAN-009)** asserts HTTP 500 because that is the current frontend behavior; a fix to return 404 would require updating this test.
- The Minikube IP `192.168.49.2` is local-only — the suite cannot run against this URL from CI without network setup.

---

## 9. Next Steps

After approval of this plan:
1. Add the `sanity` marker to `pytest.ini`.
2. Create `tests/ui/sanity/` and the four test files above.
3. Reuse existing page objects (`HomePage`, `ProductPage`, `CartPage`) — extend them only if a selector is missing (e.g., currency dropdown).
4. Run the suite and confirm runtime stays under 2 minutes.
