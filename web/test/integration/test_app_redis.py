# test/integration/test_app_redis.py

# similar to unit test but we aren't mocking the Redis client

import pytest

@pytest.mark.timeout(1.5)  # timeout after 1.5s
def test_should_update_redis(redis_client, http_client):
    # Given
    redis_client.set("page_views", 4)

    # When
    response = http_client.get("/")

    # Then
    assert response.status_code == 200
    assert response.text == "This page has been seen 5 times."
    assert redis_client.get("page_views") == b"5"
        # byte string since that's what redis client stores ig
