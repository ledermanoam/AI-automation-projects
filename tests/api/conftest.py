"""
tests/api/conftest.py - API test fixtures
==========================================
This file contains fixtures that are shared across all API tests.
It sets up a reusable HTTP session so we don't open a new connection
for every single test.
"""

import pytest
import requests


@pytest.fixture(scope="session")
def http_session(base_url):
    """
    Creates a persistent HTTP session for all API tests.

    Using a session (instead of requests.get directly) lets us:
    - Reuse TCP connections (faster tests)
    - Automatically handle cookies across requests
    - Set default headers in one place

    'scope=session' = created once, shared by all API tests.
    """
    session = requests.Session()

    # Set a default timeout so tests don't hang forever (10 seconds)
    session.request = lambda method, url, **kwargs: requests.Session.request(
        session, method, url, timeout=kwargs.pop("timeout", 10), **kwargs
    )

    yield session  # give the session to the test

    session.close()  # cleanup after all tests finish


@pytest.fixture
def api(http_session, base_url):
    """
    A helper object that bundles the session + base_url together.
    Tests receive this fixture and call api.get("/path") instead of
    writing the full URL every time.
    """

    class APIClient:
        def __init__(self, session, url):
            self.session = session
            self.base = url

        def get(self, path, **kwargs):
            """Send a GET request to base_url + path"""
            return self.session.get(self.base + path, **kwargs)

        def post(self, path, **kwargs):
            """Send a POST request to base_url + path"""
            return self.session.post(self.base + path, **kwargs)

    return APIClient(http_session, base_url)
