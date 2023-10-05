'''API layer'''

import datetime

from flask import Blueprint
from flask_restful import Api
from flask_restful import Resource
from flask_restful import request
from flask_restful import reqparse
from flask_restful import inputs

from .business import get_book_metadata
from .business import get_last_read_book_metadata
from .business import handle_user_library_addition
from .business import handle_user_library_removal

from .exceptions import BookNotFoundException
from .exceptions import UserDoesNotOwnBookException


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

book_add_parser = reqparse.RequestParser()
book_add_parser.add_argument('page', type=int)
book_add_parser.add_argument('last_accessed', type=inputs.date)


@api.resource('/book/<int:book_id>')
class BookItem(Resource):
    def get(self, book_id: int):
        try:
            book_metadata = get_book_metadata(book_id)
        except BookNotFoundException:
            return f"Book {book_id} was not found.", 404
        except UserDoesNotOwnBookException:
            return f"User does not own Book {book_id}.", 404

        return book_metadata

    def delete(self, book_id: int):
        try:
            updated_library = handle_user_library_removal(book_id)
        except UserDoesNotOwnBookException:
            return f"User does not own Book {book_id}.", 404

        return updated_library

    def put(self, book_id: int):
        args = book_add_parser.parse_args()
        page = args['page']
        last_accessed = args['last_accessed'].strftime('%Y-%m-%d')

        try:
            updated_library = handle_user_library_addition(
                book_id, page, last_accessed,
            )
        except BookNotFoundException:
            return f"Book {book_id} was not found.", 404

        return updated_library


@api_bp.route('/book')
def get_last_read_book():
    book_metadata = get_last_read_book_metadata()

    if book_metadata is None:
        return "User library is empty.", 202

    return book_metadata


@api_bp.route('/book/<int:book_id>/page')
def get_last_read_page_number(book_id: int):
    '''Return the last read page of a specific book'''
    try:
        book_metadata = get_book_metadata(book_id)
    except (BookNotFoundException, UserDoesNotOwnBookException):
        # In this case, if the book does not exists, we just respond that the
        # user does not own the book. That said, logically, a
        # BookNotFoundException for last_read_page should never trigger.
        return f"User does not own Book {book_id}.", 404

    return {
        'last_page': book_metadata['last_page']
    }
