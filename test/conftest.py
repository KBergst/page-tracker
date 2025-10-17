# test/conftest.py
# for common fixtures the different tests will share

import pytest
import redis

from page_tracker.app import app

# enable custom command-line arguments via pytest's arg parser
def pytest_addoption(parser):
    parser.addoption("--flask-url")
    parser.addoption("--redis-url")

@pytest.fixture(scope="session")
def flask_url(request):
    return request.config.getoption("--flask-url")

@pytest.fixture(scope="session")
def redis_url(request):
    return request.config.getoption("--redis-url")

# use test client (doesn't need real server)
@pytest.fixture
def http_client():
    return app.test_client()

@pytest.fixture(scope="module")
def redis_client(redis_url):
    if redis_url:  # if specifying where redis client is vs using default
        return redis.Redis.from_url(redis_url)
    return redis.Redis()
