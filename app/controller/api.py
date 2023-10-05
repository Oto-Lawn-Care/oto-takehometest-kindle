'''API layer'''

from flask import Blueprint
from flask_restful import Api
from flask_restful import Resource
from flask_restful import request


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


@api.resource('/book/<int:book_id>')
class BookItem(Resource):
    def get(self, book_id: int):
        return {'book_id': book_id}

    def delete(self, book_id: int):
        return {}

    def put(self, book_id: int):
        json_data = request.get_json()
        page = json_data['page']
        last_accessed = json_data['last_accessed']

        return {
            'book_id': book_id,
            'page': page,
            'last_accessed': last_accessed
        }


@api_bp.route('/book')
def get_last_read_book():
    return {
        'book_id': -1
    }


@api_bp.route('/book/<int:book_id>/page')
def get_last_read_page_number(book_id: int):
    '''Return the last read page of a specific book'''
    return {
        'book_id': book_id,
        'page': -1
    }
