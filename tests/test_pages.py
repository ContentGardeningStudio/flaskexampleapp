def test_home_page(client):
    """
    Test that the home page loads correctly.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Flask App Example" in response.data
