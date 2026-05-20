# Online Boutique — Test Automation Framework

## Overview

This is a test automation framework for the **Online Boutique** web application running on Minikube.

- **App URL:** http://192.168.49.2:31885/
- **Tech Stack:** Python + Pytest + Playwright + Requests
- **Test Types:** UI (browser) tests + API (HTTP) tests

---

## Project Structure

```
Agent/
├── tests/
│   ├── conftest.py              # Shared fixtures (base URL, product IDs)
│   │
│   ├── api/                     # API tests (no browser, fast)
│   │   ├── conftest.py          # API-specific fixtures (HTTP session, client)
│   │   ├── test_health.py       # Health check & availability tests
│   │   ├── test_products_api.py # Product catalog API tests
│   │   └── test_cart_api.py     # Cart, currency API tests
│   │
│   └── ui/                      # UI tests (real browser, Playwright)
│       ├── conftest.py          # Browser fixtures (page, browser instance)
│       ├── test_homepage_ui.py  # Homepage visual & navigation tests
│       ├── test_product_ui.py   # Product page & add-to-cart flow
│       └── test_cart_ui.py      # Cart management & currency switcher
│
├── reports/                     # Auto-generated HTML test reports (git-ignored)
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
└── TEST_FRAMEWORK.md            # This file
```

---

## Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright browsers

After installing the Python packages, you need to download the browsers:

```bash
playwright install chromium
```

---

## Running Tests

### Run ALL tests

```bash
pytest
```

### Run only API tests (fast, no browser)

```bash
pytest -m api
```

### Run only UI tests (opens browser)

```bash
pytest -m ui
```

### Run only smoke tests (quick health check)

```bash
pytest -m smoke
```

### Run only regression tests (full suite)

```bash
pytest -m regression
```

### Run tests in a specific file

```bash
pytest tests/api/test_health.py
pytest tests/ui/test_homepage_ui.py
```

### Run a single test by name

```bash
pytest -k "test_homepage_returns_200"
```

### Watch tests run in the browser (debug mode)

Edit `tests/ui/conftest.py` and change:
```python
headless=True  →  headless=False
```

---

## Test Reports

After running tests, an HTML report is automatically generated at:

```
reports/test_report.html
```

Open it in any web browser to see:
- Which tests passed / failed
- Error messages for failures
- Test execution time

---

## Test Markers (Categories)

| Marker       | What it runs                                 |
|--------------|----------------------------------------------|
| `smoke`      | Quick health checks (is the app alive?)      |
| `api`        | API/HTTP tests (no browser)                  |
| `ui`         | Browser-based UI tests (Playwright)          |
| `regression` | Full test suite                              |

---

## Application Endpoints Tested

| Endpoint              | Method | Test File               |
|-----------------------|--------|-------------------------|
| `/_healthz`           | GET    | test_health.py          |
| `/`                   | GET    | test_health.py, test_homepage_ui.py |
| `/product/{id}`       | GET    | test_products_api.py, test_product_ui.py |
| `/product-meta/{ids}` | GET    | test_products_api.py    |
| `/cart`               | GET    | test_cart_api.py, test_cart_ui.py |
| `/cart`               | POST   | test_cart_api.py, test_product_ui.py |
| `/cart/empty`         | POST   | test_cart_api.py, test_cart_ui.py |
| `/setCurrency`        | POST   | test_cart_api.py, test_cart_ui.py |

---

## Known Product IDs

These product IDs are defined in `tests/conftest.py` and used across tests:

| Product              | ID           | Price   |
|----------------------|--------------|---------|
| Sunglasses           | OLJCESPC7Z   | $19.99  |
| Tank Top             | 66VCHSJNUP   | $18.99  |
| Watch                | 1YMWWN1N4O   | $109.99 |
| Loafers              | L9ECAV7KIM   | $89.99  |
| Hairdryer            | 2ZYFJ3GM2N   | $24.99  |
| Candle Holder        | 0PUK6V6EV0   | $18.99  |
| Salt & Pepper Shakers| LS4PSXUNUM   | $18.49  |
| Bamboo Glass Jar     | 9SIQT8TOJO   | $5.49   |
| Mug                  | 6E92ZMYYFZ   | $8.99   |

---

## Troubleshooting

**Tests fail with "Connection refused"**
- Make sure Minikube is running: `minikube status`
- Make sure the app is deployed: `kubectl get pods`
- Verify the URL is reachable: `curl http://192.168.49.2:31885/_healthz`

**Playwright browser not found**
- Run: `playwright install chromium`

**Tests are slow**
- Run only API tests first: `pytest -m api` (no browser = much faster)
- For UI tests, `headless=True` is already set (no window = faster)
