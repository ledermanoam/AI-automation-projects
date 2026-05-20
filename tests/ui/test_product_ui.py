"""
test_product_ui.py - UI tests for the Online Boutique product detail page.
"""
import pytest

from tests.pages.product_page import ProductPage


@pytest.mark.ui
class TestProductPageUI:
    """
    Verifies that the product detail page displays all key elements.
    """

    @pytest.mark.smoke
    def test_product_name_is_visible(self, page, base_url, product_ids):
        """
        Check that the product name heading is visible on the product page.
        Steps:
        1. Navigate to the Sunglasses product page
        2. Assert the h2 heading contains 'Sunglasses' and is visible
        """
        product = ProductPage(page)
        product.navigate(base_url, product_ids["sunglasses"])
        heading = page.locator("h2").first
        assert heading.is_visible(), "Expected product name heading (h2) to be visible"
        assert "Sunglasses" in heading.text_content(), (
            "Expected product heading to contain 'Sunglasses'"
        )

    @pytest.mark.smoke
    def test_product_price_is_visible(self, page, base_url, product_ids):
        """
        Check that the product price is visible on the product page.
        Steps:
        1. Navigate to the Sunglasses product page
        2. Assert the .product-price element is visible
        """
        product = ProductPage(page)
        product.navigate(base_url, product_ids["sunglasses"])
        price = page.locator(ProductPage.PRODUCT_PRICE)
        assert price.is_visible(), "Expected product price element to be visible"
        assert "$" in price.text_content(), "Expected price to contain '$'"

    @pytest.mark.smoke
    def test_add_to_cart_button_is_visible(self, page, base_url, product_ids):
        """
        Check that the 'Add To Cart' button is visible on the product page.
        Steps:
        1. Navigate to the Sunglasses product page
        2. Assert the 'Add To Cart' button is visible
        """
        product = ProductPage(page)
        product.navigate(base_url, product_ids["sunglasses"])
        assert product.is_add_to_cart_visible(), (
            "Expected 'Add To Cart' button to be visible on product page"
        )

    @pytest.mark.regression
    def test_quantity_selector_is_visible(self, page, base_url, product_ids):
        """
        Check that the quantity dropdown is visible on the product page.
        Steps:
        1. Navigate to the Sunglasses product page
        2. Assert the quantity selector is visible
        """
        product = ProductPage(page)
        product.navigate(base_url, product_ids["sunglasses"])
        assert product.is_quantity_selector_visible(), (
            "Expected quantity selector to be visible on product page"
        )

    @pytest.mark.regression
    def test_recommendations_section_is_visible(self, page, base_url, product_ids):
        """
        Check that the 'You May Also Like' recommendations section is visible.
        Steps:
        1. Navigate to the Sunglasses product page
        2. Assert the recommendations section is visible
        """
        product = ProductPage(page)
        product.navigate(base_url, product_ids["sunglasses"])
        assert product.is_recommendations_visible(), (
            "Expected 'You May Also Like' recommendations section to be visible"
        )


@pytest.mark.ui
class TestAddToCartFlow:
    """
    Verifies the end-to-end flow of adding an item to the cart.
    Each test uses a fresh browser context (empty cart) via the page fixture.
    """

    @pytest.mark.smoke
    def test_add_to_cart_redirects_to_cart(self, page, base_url, product_ids):
        """
        Check that clicking 'Add To Cart' navigates to the cart page.
        Steps:
        1. Navigate to the Mug product page
        2. Click 'Add To Cart'
        3. Assert URL contains '/cart'
        """
        product = ProductPage(page)
        product.navigate(base_url, product_ids["mug"])
        product.click_add_to_cart()
        assert "/cart" in page.url, (
            f"Expected URL to contain '/cart' after adding to cart, got '{page.url}'"
        )

    @pytest.mark.regression
    def test_added_item_appears_in_cart(self, page, base_url, product_ids):
        """
        Check that the added item name appears on the cart page.
        Steps:
        1. Navigate to the Mug product page
        2. Click 'Add To Cart'
        3. Assert cart page contains 'Mug'
        """
        product = ProductPage(page)
        product.navigate(base_url, product_ids["mug"])
        product.click_add_to_cart()
        assert "Mug" in page.content(), (
            "Expected 'Mug' to appear in cart page after adding it"
        )

    @pytest.mark.regression
    def test_cart_shows_total_after_adding_item(self, page, base_url, product_ids):
        """
        Check that the cart page shows a price total after adding an item.
        Steps:
        1. Navigate to the Mug product page
        2. Click 'Add To Cart'
        3. Assert cart page contains '$'
        """
        product = ProductPage(page)
        product.navigate(base_url, product_ids["mug"])
        product.click_add_to_cart()
        assert "$" in page.content(), (
            "Expected cart page to show a price total ('$') after adding an item"
        )
