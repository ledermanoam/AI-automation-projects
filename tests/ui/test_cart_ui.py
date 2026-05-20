"""
test_cart_ui.py - UI tests for the Online Boutique cart page and currency switcher.
"""
import pytest

from tests.pages.cart_page import CartPage
from tests.pages.product_page import ProductPage


@pytest.mark.ui
class TestCartPageUI:
    """
    Verifies cart page UI elements and interactions.
    Each test uses a fresh browser context (empty cart) via the page fixture.
    """

    @pytest.mark.smoke
    def test_empty_cart_page_loads(self, page, base_url):
        """
        Check that navigating to /cart shows an empty cart message.
        Steps:
        1. Navigate to the cart page
        2. Assert the page title is not empty
        3. Assert the page contains the empty cart message
        """
        cart = CartPage(page)
        cart.navigate(base_url)
        assert page.title() != "", "Expected cart page to have a title"
        assert "empty" in page.content().lower(), (
            "Expected cart page to contain empty cart message"
        )

    @pytest.mark.regression
    def test_empty_cart_button_clears_items(self, page, base_url, product_ids):
        """
        Check that clicking 'Empty Cart' removes all items from the cart.
        Steps:
        1. Navigate to the Hairdryer product page
        2. Click 'Add To Cart'
        3. Click 'Empty Cart' on the cart page
        4. Assert the item is no longer shown
        """
        product = ProductPage(page)
        product.navigate(base_url, product_ids["hairdryer"])
        product.click_add_to_cart()
        cart = CartPage(page)
        cart.click_empty_cart()
        # After emptying, the app redirects to the homepage. Navigate back to the cart
        # to verify it is now empty.
        cart.navigate(base_url)
        assert "Hairdryer" not in page.content(), (
            "Expected 'Hairdryer' to be gone from cart after clicking 'Empty Cart'"
        )

    @pytest.mark.regression
    def test_place_order_button_visible_with_items(self, page, base_url, product_ids):
        """
        Check that the 'Place Order' button appears when the cart has items.
        Steps:
        1. Navigate to the Loafers product page
        2. Click 'Add To Cart'
        3. Assert 'Place Order' button is visible on the cart page
        """
        product = ProductPage(page)
        product.navigate(base_url, product_ids["loafers"])
        product.click_add_to_cart()
        cart = CartPage(page)
        assert cart.is_place_order_button_visible(), (
            "Expected 'Place Order' button to be visible when cart has items"
        )

    @pytest.mark.regression
    def test_cart_shows_added_product_name(self, page, base_url, product_ids):
        """
        Check that the added product name is shown on the cart page.
        Steps:
        1. Navigate to the Loafers product page
        2. Click 'Add To Cart'
        3. Assert cart page contains 'Loafers'
        """
        product = ProductPage(page)
        product.navigate(base_url, product_ids["loafers"])
        product.click_add_to_cart()
        assert "Loafers" in page.content(), (
            "Expected 'Loafers' to appear in cart page after adding it"
        )


@pytest.mark.ui
class TestCurrencySwitcherUI:
    """
    Verifies the currency switcher dropdown in the header.
    """

    @pytest.mark.regression
    def test_currency_dropdown_has_multiple_options(self, page):
        """
        Check that the currency dropdown offers at least 5 currency options.
        Steps:
        1. Count the options inside the currency select element
        2. Assert count is at least 5
        """
        options = page.locator("form[action='/setCurrency'] select option")
        count = options.count()
        assert count >= 5, (
            f"Expected at least 5 currency options in the dropdown, found {count}"
        )

    @pytest.mark.regression
    def test_switching_to_eur_shows_eur_prices(self, page):
        """
        Check that selecting EUR from the currency dropdown shows euro prices.
        Steps:
        1. Select 'EUR' from the currency dropdown (triggers form submit via onchange)
        2. Wait for the navigation to complete
        3. Assert the page contains the euro symbol '€'
        """
        with page.expect_navigation():
            page.select_option("form[action='/setCurrency'] select", "EUR")
        page.wait_for_load_state("networkidle")
        assert "€" in page.content(), (
            "Expected page to show euro prices ('€') after switching currency to EUR"
        )

    @pytest.mark.regression
    def test_switching_to_gbp_shows_gbp_prices(self, page):
        """
        Check that selecting GBP from the currency dropdown shows pound prices.
        Steps:
        1. Select 'GBP' from the currency dropdown (triggers form submit via onchange)
        2. Wait for the navigation to complete
        3. Assert the page contains the pound symbol '£'
        """
        with page.expect_navigation():
            page.select_option("form[action='/setCurrency'] select", "GBP")
        page.wait_for_load_state("networkidle")
        assert "£" in page.content(), (
            "Expected page to show pound prices ('£') after switching currency to GBP"
        )
