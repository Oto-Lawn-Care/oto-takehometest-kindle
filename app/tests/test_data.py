import copy

from app.controller.data import retrieve_book_from_global_library
from app.controller.data import retrieve_user_book
from app.controller.data import retrieve_last_accessed_user_book
from app.controller.data import remove_user_book
from app.controller.data import upsert_user_book
from app.model.kindle_model import UserBook


def test_retrieve_library_book(mocker, mock_global_library):
    mocker.patch(
        'app.controller.data._retrieve_global_library',
        return_value=mock_global_library
    )

    result = retrieve_book_from_global_library(0)

    assert result.id == mock_global_library[0]['id']


def test_retrieve_user_book_meta(mocker, mock_user_library):
    mocker.patch(
        'app.controller.data._retrieve_user_library',
        return_value=mock_user_library
    )

    result = retrieve_user_book(0)

    assert result.book_id == mock_user_library[0]['book_id']
    assert result.last_page == mock_user_library[0]['last_page']


def test_insert_using_upsert_user_book_meta(mocker):
    mocker.patch(
        'app.controller.data._retrieve_user_library',
        return_value=[]
    )
    mocker.patch('app.controller.data._save_user_library')

    test_book_insert = UserBook(
        book_id=368,
        last_page=1,
        last_accessed='2023-10-10',
    )

    result = upsert_user_book(test_book_insert)

    assert len(result) == 1
    assert result[0]['book_id'] == test_book_insert.book_id


def test_update_using_upsert_user_book_meta(mocker, mock_user_library):
    mocker.patch(
        'app.controller.data._retrieve_user_library',
        return_value=mock_user_library
    )
    mocker.patch('app.controller.data._save_user_library')

    test_book_update = UserBook(
        book_id=mock_user_library[0]['book_id'],
        last_page=100,
        last_accessed='0'
    )

    result = upsert_user_book(test_book_update)

    assert result[0]['last_page'] == test_book_update.last_page
    assert result[0]['last_accessed'] == test_book_update.last_accessed


def test_retrieve_last_accessed(mocker, mock_user_library):
    mocker.patch(
        'app.controller.data._retrieve_user_library',
        return_value=mock_user_library
    )

    result = retrieve_last_accessed_user_book()

    assert result.book_id == 9


def test_remove_user_book(mocker, mock_user_library):
    mocker.patch(
        'app.controller.data._retrieve_user_library',
        return_value=mock_user_library
    )
    mocker.patch('app.controller.data._save_user_library')

    result = remove_user_book(0)

    assert len(result) == 1
    assert result[0]['book_id'] == 9
