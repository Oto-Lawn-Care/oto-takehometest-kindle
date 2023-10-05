import json


def test_add_book(mocker, client, mock_global_library):
    mocker.patch(
        'app.controller.data._retrieve_global_library',
        return_value=mock_global_library
    )
    mocker.patch('app.controller.data._retrieve_user_library', return_value=[])
    mocker.patch('app.controller.data._save_user_library')  # do not save

    response = client.put(
        '/book/0',
        data=json.dumps({
            'page': 3,
            'last_accessed': '2023-10-10'
        }),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.json[0]['book_id'] == 0
    assert response.json[0]['last_page'] == 3
    assert response.json[0]['last_accessed'] == '2023-10-10'


def test_add_book_fails_with_invalid_date(mocker, client, mock_global_library):
    mocker.patch(
        'app.controller.data._retrieve_global_library',
        return_value=mock_global_library
    )
    mocker.patch('app.controller.data._retrieve_user_library', return_value=[])
    mocker.patch('app.controller.data._save_user_library')  # do not save

    response = client.put(
        '/book/0',
        data=json.dumps({
            'page': 3,
            'last_accessed': 'INVALID'
        }),
        content_type='application/json'
    )

    assert response.status_code == 400


def test_remove_book(mocker, client, mock_user_library):
    mocker.patch(
        'app.controller.data._retrieve_user_library',
        return_value=mock_user_library
    )
    mocker.patch('app.controller.data._save_user_library')  # do not save

    previous_user_library_size = len(mock_user_library)

    response = client.delete('/book/0')

    assert response.status_code == 200
    assert len(response.json) == previous_user_library_size - 1


def test_get_book_metadata(
    mocker, client, mock_global_library, mock_user_library
):
    mocker.patch(
        'app.controller.data._retrieve_global_library',
        return_value=mock_global_library
    )
    mocker.patch(
        'app.controller.data._retrieve_user_library',
        return_value=mock_user_library
    )

    mock_book = mock_global_library[0]
    mock_user_book = mock_user_library[0]

    response = client.get('/book/0')

    assert response.status_code == 200
    assert response.json['book_id'] == mock_book['id']
    assert response.json['author'] == mock_book['author']
    assert response.json['year'] == mock_book['year']
    assert response.json['percentage_read'] == 0.32
    assert response.json['last_page'] == mock_user_book['last_page']
