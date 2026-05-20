"""
test_products_api.py - API tests for the Online Boutique product pages and metadata endpoint.
"""
import pytest


@pytest.mark.api
class TestProductPages:
    """
    Verifies that product detail pages return correct content via HTTP.
    """

    @pytest.mark.smoke
    def test_product_page_returns_200(self, api):
        """
        Check that the Sunglasses product page loads successfully.
        Steps:
        1. Send GET /product/OLJCESPC7Z
        2. Assert HTTP 200
        """
        response = api.get("/product/OLJCESPC7Z")
        assert response.status_code == 200, (
            f"Expected product page to return 200, got {response.status_code}"
        )

    @pytest.mark.regression
    def test_product_page_contains_product_name(self, api):
        """
        Check that the product page body contains the product name.
        Steps:
        1. Send GET /product/OLJCESPC7Z
        2. Assert body contains 'Sunglasses'
        """
        response = api.get("/product/OLJCESPC7Z")
        assert "Sunglasses" in response.text, (
            "Product page body does not contain 'Sunglasses'"
        )

    @pytest.mark.regression
    def test_product_page_contains_price(self, api):
        """
        Check that the product page body shows a price.
        Steps:
        1. Send GET /product/OLJCESPC7Z
        2. Assert body contains '$'
        """
        response = api.get("/product/OLJCESPC7Z")
        assert "$" in response.text, "Product page body does not contain a price ('$')"

    @pytest.mark.regression
    def test_product_page_contains_add_to_cart(self, api):
        """
        Check that the product page has an 'Add To Cart' button in the HTML.
        Steps:
        1. Send GET /product/OLJCESPC7Z
        2. Assert body contains 'Add To Cart'
        """
        response = api.get("/product/OLJCESPC7Z")
        assert "Add To Cart" in response.text, (
            "Product page body does not contain 'Add To Cart'"
        )

    @pytest.mark.regression
    def test_invalid_product_id_returns_error(self, api):
        """
        Check that requesting a non-existent product returns an error status.
        Steps:
        1. Send GET /product/INVALID_PRODUCT_ID_XXXX
        2. Assert status code is not 200
        """
        response = api.get("/product/INVALID_PRODUCT_ID_XXXX")
        assert response.status_code != 200, (
            f"Expected an error status for an invalid product ID, but got 200 (success)"
        )

    @pytest.mark.regression
    @pytest.mark.parametrize("product_id", [
        "OLJCESPC7Z",   # Sunglasses
        "66VCHSJNUP",   # Tank Top
        "1YMWWN1N4O",   # Watch
        "2ZYFJ3GM2N",   # Hairdryer
        "6E92ZMYYFZ",   # Mug
    ])
    def test_multiple_product_pages_return_200(self, api, product_id):
        """
        Check that each product detail page loads successfully.
        Steps:
        1. Send GET /product/{product_id} for each product
        2. Assert HTTP 200
        """
        response = api.get(f"/product/{product_id}")
        assert response.status_code == 200, (
            f"Expected /product/{product_id} to return 200, got {response.status_code}"
        )


@pytest.mark.api
class TestProductMetaAPI:
    """
    Verifies the product metadata API endpoint.
    """

    @pytest.mark.smoke
    def test_product_meta_single_id(self, api, product_ids):
        """
        Check that the product-meta endpoint returns 200 for a single product ID.
        Steps:
        1. Send GET /product-meta/{sunglasses_id}
        2. Assert HTTP 200
        """
        sunglasses_id = product_ids["sunglasses"]
        response = api.get(f"/product-meta/{sunglasses_id}")
        assert response.status_code == 200, (
            f"Expected /product-meta/{sunglasses_id} to return 200, "
            f"got {response.status_code}"
        )

    @pytest.mark.regression
    def test_product_meta_multiple_ids(self, api, product_ids):
        """
        Check that the product-meta endpoint returns 200 for multiple comma-separated IDs.
        Steps:
        1. Build a comma-separated list of two product IDs
        2. Send GET /product-meta/{id1},{id2}
        3. Assert HTTP 200
        """
        id1 = product_ids["sunglasses"]
        id2 = product_ids["watch"]
        response = api.get(f"/product-meta/{id1},{id2}")
        assert response.status_code == 200, (
            f"Expected /product-meta/{id1},{id2} to return 200, got {response.status_code}"
        )
