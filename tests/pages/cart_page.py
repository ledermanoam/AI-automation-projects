"""
cart_page.py - Page object for the Online Boutique shopping cart page.
"""


class CartPage:
    """
    Represents the shopping cart page of the Online Boutique app (/cart).

    This page shows the items in the cart, an 'Empty Cart' button,
    and a 'Place Order' button when items are present.
    """

    # Locators — defined once here so they're easy to find and update
    EMPTY_CART_BUTTON = "button:has-text('Empty Cart')"
    PLACE_ORDER_BUTTON = "button:has-text('Place Order')"

    def __init__(self, page):
        self.page = page

    def navigate(self, base_url):
        """Navigate directly to the cart page."""
        self.page.goto(f"{base_url}/cart", wait_until="networkidle")

    def click_empty_cart(self):
        """Click the 'Empty Cart' button and wait for the page to reload."""
        self.page.locator(self.EMPTY_CART_BUTTON).click()
        self.page.wait_for_load_state("networkidle")

    def is_place_order_button_visible(self):
        """Return True if the 'Place Order' button is visible on the page."""
        return self.page.locator(self.PLACE_ORDER_BUTTON).is_visible()

    def get_page_content(self):
        """Return the full HTML content of the cart page as a string."""
        return self.page.content()
