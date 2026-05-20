"""
tests/ui/conftest.py - Playwright browser fixtures
====================================================
This file sets up the browser for UI tests.

Playwright supports three browsers: chromium, firefox, webkit.
We use chromium (Chrome/Edge) by default.

The fixtures here are used by all UI test files.
"""

import pytest
from playwright.sync_api import sync_playwright, Page, Browser


@pytest.fixture(scope="session")
def browser_instance():
    """
    Starts a browser once for the entire test session.
    'scope=session' means we launch the browser once and reuse it
    for all UI tests (much faster than launching per test).

    headless=True  → browser runs in background, no window opens (good for CI)
    headless=False → you can SEE the browser while tests run (good for debugging)
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,  # Change to True to run in background (CI/headless mode)
        )
        yield browser
        browser.close()  # Close the browser after all tests finish


@pytest.fixture
def page(browser_instance, base_url):
    """
    Creates a fresh browser page (tab) for each test.
    Each test gets its own isolated page so tests don't interfere with each other.

    This fixture also navigates to the homepage before the test starts,
    so every test begins from a known state.
    """
    # Create a new browser context (like a fresh incognito window)
    context = browser_instance.new_context()

    # Create a new page (tab) in that context
    page = context.new_page()

    # Navigate to the homepage to start each test from a clean state
    page.goto(base_url)
    page.wait_for_load_state("networkidle")  # Wait until page fully loads

    yield page  # give the page to the test

    # Cleanup: close the page and context after each test
    page.close()
    context.close()
