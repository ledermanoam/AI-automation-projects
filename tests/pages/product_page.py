"""
product_page.py - Page object for the Online Boutique product detail page.
"""


class ProductPage:
    """
    Represents a product detail page of the Online Boutique app (/product/{id}).

    This page shows the product name, price, description, a quantity selector,
    and an 'Add to Cart' button.
    """

    # Locators — defined once here so they're easy to find and update
    PRODUCT_NAME = "h2"
    PRODUCT_PRICE = ".product-price"
    # The description is the first <p> tag that has no class attribute.
    # We use XPath here because CSS cannot select "p without a class".
    PRODUCT_DESCRIPTION = "//div[contains(@class,'product')]//p[not(@class)]"
    ADD_TO_CART_BUTTON = "button:has-text('Add To Cart')"
    QUANTITY_SELECTOR = "select[name='quantity']"
    RECOMMENDATIONS = "text=You May Also Like"

    def __init__(self, page):
        self.page = page

    def navigate(self, base_url, product_id):
        """Navigate directly to a product detail page by product ID."""
        self.page.goto(f"{base_url}/product/{product_id}", wait_until="networkidle")

    def get_product_name(self):
        """Return the product name text shown in the <h2> heading."""
        return self.page.locator(self.PRODUCT_NAME).first.text_content().strip()

    def get_price(self):
        """Return the product price text (e.g. '$19.99')."""
        return self.page.locator(self.PRODUCT_PRICE).text_content().strip()

    def get_description(self):
        """Return the product description paragraph text."""
        return self.page.locator(self.PRODUCT_DESCRIPTION).first.text_content().strip()

    def click_add_to_cart(self):
        """Click the 'Add To Cart' button and wait for the resulting navigation."""
        self.page.locator(self.ADD_TO_CART_BUTTON).click()
        self.page.wait_for_load_state("networkidle")

    def is_add_to_cart_visible(self):
        """Return True if the 'Add To Cart' button is visible on the page."""
        return self.page.locator(self.ADD_TO_CART_BUTTON).is_visible()

    def is_quantity_selector_visible(self):
        """Return True if the quantity dropdown is visible on the page."""
        return self.page.locator(self.QUANTITY_SELECTOR).is_visible()

    def is_recommendations_visible(self):
        """Return True if the 'You May Also Like' recommendations section is visible."""
        return self.page.locator(self.RECOMMENDATIONS).is_visible()
