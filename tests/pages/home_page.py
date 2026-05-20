"""
home_page.py - Page object for the Online Boutique homepage.
"""


class HomePage:
    """
    Represents the main homepage of the Online Boutique app (/).

    This page shows a grid of product cards. Each card has a product name,
    an image, a price, and a link to the product detail page.
    """

    # Locators — defined once here so they're easy to find and update
    LOGO_LINK = "a.navbar-brand"
    PRODUCT_CARD = ".hot-product-card"

    def __init__(self, page):
        self.page = page

    def navigate(self, base_url):
        """Navigate directly to the homepage."""
        self.page.goto(base_url)
        self.page.wait_for_load_state("networkidle")

    def click_product_by_name(self, product_name):
        """
        Click a product card on the homepage by matching the product name text.

        For example: click_product_by_name("Sunglasses")
        Each product card contains a name div and an image link — we find the
        card by its name text, then click the <a> link inside it.
        """
        # Find the product card that contains the matching product name
        card = self.page.locator(self.PRODUCT_CARD, has_text=product_name)
        # Click the link (<a> tag) inside that card
        card.locator("a").first.click()
        self.page.wait_for_load_state("networkidle")

    def click_logo(self):
        """Click the site logo in the header to return to the homepage."""
        self.page.locator(self.LOGO_LINK).click()
        self.page.wait_for_load_state("networkidle")
