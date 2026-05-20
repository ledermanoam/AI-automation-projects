"""
test_product_navigation.py - Navigation and product property verification tests.

These tests open a real browser and walk through the Online Boutique application,
clicking on products and verifying that the correct price and description are shown.
"""

import pytest
from tests.pages.home_page import HomePage
from tests.pages.product_page import ProductPage


@pytest.mark.ui
@pytest.mark.regression
class TestProductNavigation:
    """
    Tests that navigate between the homepage and product detail pages,
    verifying that key product properties (price, description) are correct.
    """

    def test_sunglasses_and_watch_properties(self, page, base_url):
        """
        Verify the following end-to-end navigation flow:

        1. Open the homepage.
        2. Click on 'Sunglasses'.
        3. Verify the price is $19.99.
        4. Verify the description is the expected aviator sunglasses text.
        5. Click the site logo to return to the homepage.
        6. Click on 'Watch'.
        7. Verify the price is $109.99.
        8. Verify the description is the expected gold-tone stainless steel text.
        """
        home = HomePage(page)
        product = ProductPage(page)

        # ── Step 1: Homepage is already loaded by the `page` fixture ──────────

        # ── Step 2: Click on the Sunglasses product card ──────────────────────
        home.click_product_by_name("Sunglasses")

        # ── Step 3: Verify Sunglasses price ───────────────────────────────────
        sunglasses_price = product.get_price()
        assert sunglasses_price == "$19.99", (
            f"Sunglasses price should be '$19.99', but got: '{sunglasses_price}'"
        )

        # ── Step 4: Verify Sunglasses description ─────────────────────────────
        expected_sunglasses_desc = (
            "Add a modern touch to your outfits with these sleek aviator sunglasses."
        )
        sunglasses_desc = product.get_description()
        assert sunglasses_desc == expected_sunglasses_desc, (
            f"Sunglasses description did not match.\n"
            f"  Expected: '{expected_sunglasses_desc}'\n"
            f"  Got:      '{sunglasses_desc}'"
        )

        # ── Step 5: Click the logo to return to the homepage ──────────────────
        home.click_logo()

        # Confirm we are back on the homepage
        assert page.url.rstrip("/") == base_url.rstrip("/"), (
            f"After clicking the logo, expected to be on the homepage.\n"
            f"Current URL: '{page.url}'"
        )

        # ── Step 6: Click on the Watch product card ───────────────────────────
        home.click_product_by_name("Watch")

        # ── Step 7: Verify Watch price ────────────────────────────────────────
        watch_price = product.get_price()
        assert watch_price == "$109.99", (
            f"Watch price should be '$109.99', but got: '{watch_price}'"
        )

        # ── Step 8: Verify Watch description ─────────────────────────────────
        expected_watch_desc = (
            "This gold-tone stainless steel watch will work with most of your outfits."
        )
        watch_desc = product.get_description()
        assert watch_desc == expected_watch_desc, (
            f"Watch description did not match.\n"
            f"  Expected: '{expected_watch_desc}'\n"
            f"  Got:      '{watch_desc}'"
        )
