"""
test_cart_api.py - API tests for the Online Boutique cart and currency endpoints.
"""
import requests

import pytest


@pytest.mark.api
class TestCartPage:
    """
    Verifies that the cart page loads correctly via HTTP.
    """

    @pytest.mark.smoke
    def test_cart_page_returns_200(self, api):
        """
        Check that the cart page loads successfully.
        Steps:
        1. Send GET /cart
        2. Assert HTTP 200
        """
        response = api.get("/cart")
        assert response.status_code == 200, (
            f"Expected /cart to return 200, got {response.status_code}"
        )

    @pytest.mark.regression
    def test_cart_page_returns_html(self, api):
        """
        Check that the cart page returns HTML content.
        Steps:
        1. Send GET /cart
        2. Assert Content-Type contains 'text/html'
        """
        response = api.get("/cart")
        content_type = response.headers.get("Content-Type", "")
        assert "text/html" in content_type, (
            f"Expected Content-Type to contain 'text/html', got '{content_type}'"
        )

    @pytest.mark.regression
    def test_empty_cart_shows_empty_message(self, base_url):
        """
        Check that a brand new session shows an empty cart message.
        Uses a fresh session to avoid carrying over cookies from other tests.
        Steps:
        1. Create a new requests.Session (no prior cookies)
        2. Send GET /cart
        3. Assert body contains the empty cart message
        """
        session = requests.Session()
        response = session.get(f"{base_url}/cart", timeout=10)
        assert "Your shopping cart is empty" in response.text, (
            "Expected empty cart page to contain 'Your shopping cart is empty'"
        )


@pytest.mark.api
class TestAddToCart:
    """
    Verifies adding items to the cart via POST /cart.
    """

    @pytest.mark.smoke
    def test_post_to_cart_redirects(self, base_url, product_ids):
        """
        Check that posting to the cart endpoint redirects (302/303).
        Steps:
        1. POST /cart with a valid product_id and quantity=1
        2. Assert status code is 302 or 303 (redirect, not following it)
        """
        session = requests.Session()
        response = session.post(
            f"{base_url}/cart",
            data={"product_id": product_ids["mug"], "quantity": "1"},
            allow_redirects=False,
            timeout=10,
        )
        assert response.status_code in (302, 303), (
            f"Expected POST /cart to redirect (302/303), got {response.status_code}"
        )

    @pytest.mark.regression
    def test_added_item_visible_in_cart(self, base_url, product_ids):
        """
        Check that an item added to the cart appears on the cart page.
        Steps:
        1. POST /cart with the Mug product ID
        2. Follow the redirect to GET /cart
        3. Assert cart page body contains 'Mug'
        """
        session = requests.Session()
        session.post(
            f"{base_url}/cart",
            data={"product_id": product_ids["mug"], "quantity": "1"},
            timeout=10,
        )
        response = session.get(f"{base_url}/cart", timeout=10)
        assert "Mug" in response.text, (
            "Expected cart page to contain 'Mug' after adding it"
        )

    @pytest.mark.regression
    def test_multiple_items_visible_in_cart(self, base_url, product_ids):
        """
        Check that multiple items added to the cart all appear on the cart page.
        Steps:
        1. POST /cart with Sunglasses
        2. POST /cart with Watch
        3. GET /cart
        4. Assert body contains both 'Sunglasses' and 'Watch'
        """
        session = requests.Session()
        session.post(
            f"{base_url}/cart",
            data={"product_id": product_ids["sunglasses"], "quantity": "1"},
            timeout=10,
        )
        session.post(
            f"{base_url}/cart",
            data={"product_id": product_ids["watch"], "quantity": "1"},
            timeout=10,
        )
        response = session.get(f"{base_url}/cart", timeout=10)
        assert "Sunglasses" in response.text, (
            "Expected cart page to contain 'Sunglasses' after adding it"
        )
        assert "Watch" in response.text, (
            "Expected cart page to contain 'Watch' after adding it"
        )


@pytest.mark.api
class TestEmptyCart:
    """
    Verifies the POST /cart/empty endpoint.
    """

    @pytest.mark.regression
    def test_empty_cart_redirects(self, base_url):
        """
        Check that posting to /cart/empty redirects (302/303).
        Steps:
        1. POST /cart/empty
        2. Assert status code is 302 or 303
        """
        session = requests.Session()
        response = session.post(
            f"{base_url}/cart/empty",
            allow_redirects=False,
            timeout=10,
        )
        assert response.status_code in (302, 303), (
            f"Expected POST /cart/empty to redirect (302/303), got {response.status_code}"
        )

    @pytest.mark.regression
    def test_cart_is_empty_after_emptying(self, base_url, product_ids):
        """
        Check that emptying the cart removes all items.
        Steps:
        1. Add Hairdryer to cart
        2. POST /cart/empty
        3. GET /cart
        4. Assert body contains the empty cart message
        """
        session = requests.Session()
        session.post(
            f"{base_url}/cart",
            data={"product_id": product_ids["hairdryer"], "quantity": "1"},
            timeout=10,
        )
        session.post(f"{base_url}/cart/empty", timeout=10)
        response = session.get(f"{base_url}/cart", timeout=10)
        assert "Your shopping cart is empty" in response.text, (
            "Expected cart to be empty after POST /cart/empty, "
            "but empty cart message was not found"
        )


@pytest.mark.api
class TestCurrencyAPI:
    """
    Verifies the POST /setCurrency endpoint.
    """

    @pytest.mark.regression
    @pytest.mark.parametrize("currency", ["USD", "EUR", "GBP", "JPY", "TRY", "CAD"])
    def test_set_currency_redirects(self, base_url, currency):
        """
        Check that setting each supported currency redirects (302/303).
        Steps:
        1. POST /setCurrency with the currency_code value
        2. Assert status code is 302 or 303
        """
        session = requests.Session()
        response = session.post(
            f"{base_url}/setCurrency",
            data={"currency_code": currency},
            allow_redirects=False,
            timeout=10,
        )
        assert response.status_code in (302, 303), (
            f"Expected POST /setCurrency with '{currency}' to redirect (302/303), "
            f"got {response.status_code}"
        )

    @pytest.mark.regression
    def test_eur_currency_shown_on_homepage(self, base_url):
        """
        Check that switching to EUR makes the homepage display euro prices.
        Steps:
        1. POST /setCurrency with currency_code=EUR
        2. GET /
        3. Assert body contains the euro symbol '€'
        """
        session = requests.Session()
        session.post(
            f"{base_url}/setCurrency",
            data={"currency_code": "EUR"},
            timeout=10,
        )
        response = session.get(f"{base_url}/", timeout=10)
        assert "€" in response.text, (
            "Expected homepage to show euro prices ('€') after switching currency to EUR"
        )
