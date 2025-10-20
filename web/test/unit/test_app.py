# test/unit/test_app.py

import pytest
import unittest.mock
from page_tracker.app import app
from redis import ConnectionError


# Behavioral specifications type of unit test
# testing happy path
# setup mock Redis client
@unittest.mock.patch("page_tracker.app.redis")
def test_should_call_redis_incr(mock_redis, http_client):
    # Given
    mock_redis.return_value.incr.return_value=5
    # When
    response = http_client.get("/")
    # Then
    assert response.status_code == 200 # status is ok
    assert response.text == "This page has been seen 5 times."
    mock_redis.return_value.incr.assert_called_once_with("page_views")

# testing connection error
@unittest.mock.patch("page_tracker.app.redis")
def test_should_handle_redis_connection_error(mock_redis, http_client):
    # Given
    mock_redis.return_value.incr.side_effect = ConnectionError

    # When
    response = http_client.get("/")

    # Then
    assert response.status_code == 500  # status not ok
    assert response.text == "Sorry, something went wrong \N{thinking face}"
