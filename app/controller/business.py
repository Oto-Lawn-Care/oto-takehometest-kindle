'''Business/Service layer'''

from app.controller.data import remove_user_book
from app.controller.data import retrieve_book_from_global_library
from app.controller.data import retrieve_last_accessed_user_book
from app.controller.data import retrieve_user_book
from app.controller.data import upsert_user_book

from app.model.kindle_model import UserBook


def get_book_metadata(book_id: int):
    book = retrieve_book_from_global_library(book_id)
    user_book = retrieve_user_book(book_id)

    return {
        'book_id': book.id,
        'author': book.author,
        'last_page': user_book.last_page,
        'percentage_read': round(user_book.last_page / book.pages, 2),
        'year': book.year,
    }


def get_last_read_book_metadata():
    last_read_book = retrieve_last_accessed_user_book()
    if last_read_book is None:
        return None
    return get_book_metadata(last_read_book.book_id)


def handle_user_library_addition(
    book_id: int,
    last_page: int,
    last_accessed: str
):
    '''Handle adding a new book to the user library or editing an entry'''

    # if this fails we allow BookNotFound to hit api layer
    book = retrieve_book_from_global_library(book_id)

    # We construct a new UserBook because the data layer performs an upsert.
    # Therefore no "if exists" validations are needed here.
    user_book = UserBook(
        book_id=book.id,
        last_page=last_page,
        last_accessed=last_accessed
    )

    updated_library = upsert_user_book(user_book)

    return updated_library


def handle_user_library_removal(book_id: int):
    updated_library = remove_user_book(book_id)
    return updated_library
