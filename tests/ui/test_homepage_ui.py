"""
test_homepage_ui.py - UI tests for the Online Boutique homepage.
"""
import pytest

from tests.pages.home_page import HomePage


@pytest.mark.ui
class TestHomepageUI:
    """
    Verifies that the homepage displays all key elements correctly.
    """

    @pytest.mark.smoke
    def test_page_title_contains_online_boutique(self, page):
        """
        Check that the browser tab title contains 'Online Boutique'.
        Steps:
        1. Page is already on the homepage (page fixture navigates there)
        2. Read the page title
        3. Assert it contains 'Online Boutique'
        """
        title = page.title()
        assert "Online Boutique" in title, (
            f"Expected page title to contain 'Online Boutique', got '{title}'"
        )

    @pytest.mark.smoke
    def test_navbar_logo_is_visible(self, page):
        """
        Check that the navbar logo image is visible.
        Steps:
        1. Locate the logo image by src attribute
        2. Assert it is visible
        """
        logo = page.locator("img[src*='NavLogo']")
        assert logo.is_visible(), "Expected the navbar logo image to be visible"

    @pytest.mark.smoke
    def test_hot_products_section_is_visible(self, page):
        """
        Check that the 'Hot Products' section heading is visible.
        Steps:
        1. Locate any element containing the text 'Hot Products'
        2. Assert it is visible
        """
        section = page.locator("text=Hot Products")
        assert section.is_visible(), "Expected 'Hot Products' section to be visible on homepage"

    @pytest.mark.smoke
    def test_product_cards_are_displayed(self, page):
        """
        Check that at least one product card is shown in the product grid.
        Steps:
        1. Count elements matching the product card selector
        2. Assert count is greater than 0
        """
        cards = page.locator(".hot-product-card, .col-md-4")
        count = cards.count()
        assert count > 0, f"Expected at least one product card, found {count}"

    @pytest.mark.regression
    def test_currency_selector_is_visible(self, page):
        """
        Check that the currency dropdown is visible in the header.
        Steps:
        1. Locate the select element inside the setCurrency form
        2. Assert it is visible
        """
        selector = page.locator("form[action='/setCurrency'] select")
        assert selector.is_visible(), "Expected currency selector dropdown to be visible"

    @pytest.mark.regression
    def test_cart_link_is_visible(self, page):
        """
        Check that the cart icon link is visible in the header.
        Steps:
        1. Locate the cart link by href
        2. Assert it is visible
        """
        cart_link = page.locator("a[href='/cart']")
        assert cart_link.is_visible(), "Expected cart link to be visible in the header"


@pytest.mark.ui
class TestHomepageNavigation:
    """
    Verifies that clicking navigation elements goes to the correct pages.
    """

    @pytest.mark.smoke
    def test_clicking_product_goes_to_product_page(self, page):
        """
        Check that clicking a product card navigates to a product detail page.
        Steps:
        1. Click the first product card link
        2. Assert the URL contains '/product/'
        """
        page.locator("a[href*='/product/']").first.click()
        page.wait_for_load_state("networkidle")
        assert "/product/" in page.url, (
            f"Expected URL to contain '/product/' after clicking a product, got '{page.url}'"
        )

    @pytest.mark.regression
    def test_clicking_cart_icon_goes_to_cart(self, page):
        """
        Check that clicking the cart icon navigates to the cart page.
        Steps:
        1. Click the cart link
        2. Assert the URL ends with '/cart'
        """
        page.locator("a[href='/cart']").first.click()
        page.wait_for_load_state("networkidle")
        assert page.url.endswith("/cart"), (
            f"Expected URL to end with '/cart' after clicking cart, got '{page.url}'"
        )

    @pytest.mark.regression
    def test_clicking_logo_returns_to_homepage(self, page, base_url):
        """
        Check that clicking the logo from a product page returns to the homepage.
        Steps:
        1. Navigate to a product page
        2. Click the navbar logo
        3. Assert URL is the homepage URL
        """
        page.locator("a[href*='/product/']").first.click()
        page.wait_for_load_state("networkidle")
        home = HomePage(page)
        home.click_logo()
        assert page.url.rstrip("/") == base_url.rstrip("/"), (
            f"Expected URL to be homepage '{base_url}', got '{page.url}'"
        )
