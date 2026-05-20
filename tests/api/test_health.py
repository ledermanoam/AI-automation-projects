"""
test_health.py - Smoke tests for the Online Boutique health and availability endpoints.
"""
import time

import pytest


@pytest.mark.api
@pytest.mark.smoke
class TestHealthAndAvailability:
    """
    Verifies that the application is up and reachable.
    These are the fastest checks — run them first on every deploy.
    """

    def test_healthz_endpoint_returns_200(self, api):
        """
        Check the Kubernetes liveness probe endpoint.
        Steps:
        1. Send GET /_healthz
        2. Assert HTTP 200
        """
        response = api.get("/_healthz")
        assert response.status_code == 200, (
            f"Expected /_healthz to return 200, got {response.status_code}"
        )

    def test_homepage_returns_200(self, api):
        """
        Check that the homepage loads successfully.
        Steps:
        1. Send GET /
        2. Assert HTTP 200
        """
        response = api.get("/")
        assert response.status_code == 200, (
            f"Expected homepage to return 200, got {response.status_code}"
        )

    def test_homepage_contains_online_boutique(self, api):
        """
        Check that the homepage body contains expected content (not an error page).
        Steps:
        1. Send GET /
        2. Assert body contains 'Online Boutique' and 'Hot Products'
        """
        response = api.get("/")
        body = response.text
        assert "Online Boutique" in body, "Homepage body does not contain 'Online Boutique'"
        assert "Hot Products" in body, "Homepage body does not contain 'Hot Products'"

    def test_homepage_content_type_is_html(self, api):
        """
        Check that the homepage returns HTML content (not JSON or an error).
        Steps:
        1. Send GET /
        2. Assert Content-Type header contains 'text/html'
        """
        response = api.get("/")
        content_type = response.headers.get("Content-Type", "")
        assert "text/html" in content_type, (
            f"Expected Content-Type to contain 'text/html', got '{content_type}'"
        )

    def test_homepage_response_time(self, api):
        """
        Check that the homepage responds within 5 seconds.
        Steps:
        1. Record start time
        2. Send GET /
        3. Assert elapsed time is under 5 seconds
        """
        start = time.time()
        api.get("/")
        elapsed = time.time() - start
        assert elapsed < 5, f"Homepage took {elapsed:.2f}s — expected under 5s"
