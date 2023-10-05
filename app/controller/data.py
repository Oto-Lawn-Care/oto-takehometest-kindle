import datetime
import json
from flask import current_app

from app.model.kindle_model import Book
from app.model.kindle_model import UserBook
from .exceptions import BookNotFoundException
from .exceptions import UserDoesNotOwnBookException


def _retrieve_global_library():
    with open(current_app.config['GLOBAL_LIBRARY_PATH'], 'r') as global_library_f:
        return json.load(global_library_f)


def _retrieve_user_library():
    with open(current_app.config['USER_LIBRARY_PATH'], 'r') as user_library_f:
        try:
            return json.load(user_library_f)

        # this means the library is empty
        except json.decoder.JSONDecodeError:
            return []


def _save_user_library(new_user_library):
    with open(current_app.config['USER_LIBRARY_PATH'], 'w') as user_library_f:
        json.dump(new_user_library, user_library_f, indent=2)


def retrieve_book_from_global_library(book_id: int):
    global_books = _retrieve_global_library()

    try:
        book_meta = global_books[book_id]
    except IndexError:
        raise BookNotFoundException from IndexError

    return Book.from_dict(book_meta)


def retrieve_last_accessed_user_book():
    user_books = _retrieve_user_library()

    latest_access_date = None
    latest_book = None

    for book_meta in user_books:
        access_date = datetime.datetime.strptime(
            book_meta['last_accessed'], '%Y-%m-%d'
        )

        if latest_access_date is None or access_date > latest_access_date:
            latest_access_date = access_date
            latest_book = book_meta

    return UserBook.from_dict(latest_book) if latest_book else None


def retrieve_user_book(book_id: int):
    user_books = _retrieve_user_library()

    for book_meta in user_books:
        if book_meta['book_id'] == book_id:
            return UserBook.from_dict(book_meta)

    raise UserDoesNotOwnBookException


def remove_user_book(book_id: int):
    user_books = _retrieve_user_library()

    for book_meta in user_books:
        if book_meta['book_id'] == book_id:
            user_books.remove(book_meta)
            _save_user_library(user_books)
            return user_books

    raise UserDoesNotOwnBookException


def upsert_user_book(user_book: UserBook):
    user_books = _retrieve_user_library()

    # if update_index gets set, then the book exists and this operation is an
    # update, otherwise insert.
    update_index = -1

    for book_index, book_meta in enumerate(user_books):
        if book_meta['book_id'] == user_book.book_id:
            update_index = book_index
            break

    if update_index != -1:
        user_books[update_index] = user_book.__dict__
    else:
        user_books.append(user_book.__dict__)

    _save_user_library(user_books)
    return user_books
