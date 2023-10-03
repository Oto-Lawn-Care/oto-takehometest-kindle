'''API layer'''

from flask import Blueprint


api_bp = Blueprint('api', __name__)


def add_book():
    pass


def get_last_read_page_number():
    pass


@api_bp.route('/book/<int:book_id>')
def get_book_metadata(book_id: int):
    return {'book': book_id}
