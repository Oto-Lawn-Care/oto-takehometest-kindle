from flask import Blueprint, request, jsonify
from app.controller.business import (
    find_book,
    add_book_user,
    subtract_book_user,
    find_top_book_user,
    change_book_page_user,
    add_book_global,
    list_books,
    ValidationError,
    BookNotFoundError,
    ValueError,
)
from typing import List, Dict, Union, Any

global_json = "data.json"
user_json = "user_library/user_library.json"

book_routes = Blueprint("book_routes", __name__)


# Function to register the defined blueprint with the Flask app.
def register_routes(app: Any) -> None:
    app.register_blueprint(book_routes)


# Utility function to format API responses in a consistent manner.
def format_response(
    data: Union[List[Dict[str, Any]], Dict[str, Any]], status: int = 200
) -> Any:
    return jsonify({"data": data, "status": status})


# Endpoint to retrieve all books from the user library.
@book_routes.route("/user/books", methods=["GET"])
def get_all_books_user() -> Any:
    try:
        books = list_books(user_json)
        return format_response(books)
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


# Endpoint to retrieve all books from the global library.
@book_routes.route("/global/books", methods=["GET"])
def get_all_books_global() -> Any:
    try:
        books = list_books(global_json)
        return format_response(books)
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


# Endpoints to search for books in the global library based on key and value.
@book_routes.route(
    "/global/books/search/<key>/<value>", defaults={"target": None}, methods=["GET"]
)
@book_routes.route("/global/books/search/<key>/<value>/<target>", methods=["GET"])
def search_book_global(key: str, value: str, target: str = None) -> Any:
    try:
        books = find_book(key, value, global_json, target=target)
        return jsonify(books)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


# Endpoints to search for books in the user library based on key and value.
@book_routes.route(
    "/user/books/search/<key>/<value>", defaults={"target": None}, methods=["GET"]
)
@book_routes.route("/user/books/search/<key>/<value>/<target>", methods=["GET"])
def search_book_user(key: str, value: str, target: str = None) -> Any:
    try:
        books = find_book(key, value, global_json, target=target)
        return jsonify(books)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


# Endpoint to add a new book to the global library.
@book_routes.route("/user/books/<uuid>", methods=["POST"])
def add_book_to_user_library(uuid: str) -> Any:
    try:
        response = add_book_user(uuid, global_json, user_json)
        return format_response(response)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


# Endpoint to add a new book to the global library.
@book_routes.route("/global/books", methods=["POST"])
def add_book_to_global_library() -> Any:
    try:
        data = request.get_json()
        response = add_book_global(data, global_json)
        return format_response(response)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


# Endpoint to remove a specific book from the user library using its UUID.
@book_routes.route("/user/books/<uuid>", methods=["DELETE"])
def remove_book_from_user_library(uuid: str) -> Any:
    try:
        response = subtract_book_user(uuid, user_json)
        return format_response(response)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


# Endpoint to get the top book in the user library based on a specific attribute.
@book_routes.route("/user/books/top/<target>", methods=["GET"])
def get_top_user_book(target: str = None) -> Any:
    try:
        book = find_top_book_user(user_json, target=target)
        return format_response(book)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


# Endpoint to get the last book read by the user.
@book_routes.route("/user/books/last-read", methods=["GET"])
def get_last_user_book() -> Any:
    try:
        book = find_top_book_user(user_json, "last_read_date")
        return format_response(book)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404


# Endpoint to update the reading status of a book in the user library.
@book_routes.route("/user/books/<uuid>/page/<page_number>", methods=["PATCH"])
def update_book_page_for_user(uuid: str, page_number: str) -> Any:
    try:
        page_number = int(page_number)
        response = change_book_page_user(uuid, page_number, user_json)
        return format_response(response)
    except ValidationError as ve:
        return {"error": str(ve)}, 400
    except BookNotFoundError as bnf:
        return {"error": str(bnf)}, 404
    except ValueError as vee:
        return {"error": str(vee)}, 400
