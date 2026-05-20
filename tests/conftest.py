"""
conftest.py - Shared test configuration and fixtures
=====================================================
This file is automatically loaded by pytest before running any tests.
Fixtures defined here are available to ALL tests in the project.

A "fixture" is a reusable piece of setup/teardown code that tests can use.
For example, a fixture can set up a browser, run a test, then close the browser.
"""

import pytest


# ─────────────────────────────────────────────
# GLOBAL SETTINGS
# ─────────────────────────────────────────────

# The base URL of the application we are testing.
# Change this if the app moves to a different host/port.
BASE_URL = "http://192.168.49.2:31885"

# Known product IDs from the Online Boutique catalog
PRODUCT_IDS = {
    "sunglasses":       "OLJCESPC7Z",
    "tank_top":         "66VCHSJNUP",
    "watch":            "1YMWWN1N4O",
    "loafers":          "L9ECAV7KIM",
    "hairdryer":        "2ZYFJ3GM2N",
    "candle_holder":    "0PUK6V6EV0",
    "salt_pepper":      "LS4PSXUNUM",
    "bamboo_jar":       "9SIQT8TOJO",
    "mug":              "6E92ZMYYFZ",
}


# ─────────────────────────────────────────────
# SHARED FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture(scope="session")
def base_url():
    """
    Returns the base URL of the application.
    'scope=session' means this is created once per test run (not per test).
    """
    return BASE_URL


@pytest.fixture(scope="session")
def product_ids():
    """
    Returns the dictionary of known product IDs.
    Tests can use this to avoid hardcoding product IDs.
    """
    return PRODUCT_IDS
