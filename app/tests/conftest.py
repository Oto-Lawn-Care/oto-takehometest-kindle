import pytest
from app import create_app
from app.model.kindle_model import Book


@pytest.fixture()
def app():
    test_app = create_app()

    with test_app.app_context():
        yield test_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def mock_global_library():
    return [{
        'id': 0,
        'author': 'Sheldon Allen',
        'country': 'Canada',
        'imageLink': 'https://google.com/',
        'language': 'English',
        'link': 'https://shelsoloa.com/',
        'pages': 100,
        'title': 'Mock Book',
        'year': 2023
    }]


@pytest.fixture
def mock_user_library():
    return [
        {
            'book_id': 0,
            'last_page': 32,
            'last_accessed': '2023-10-04',
        },
        {
            'book_id': 9,
            'last_page': 64,
            'last_accessed': '2023-10-05',
        }
    ]
