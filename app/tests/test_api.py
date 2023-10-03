def test_get_book_metadata(client):
    test_id = 0

    response = client.get(f'/book/{test_id}')

    assert response.status_code == 200
    assert response.json['book'] == test_id
