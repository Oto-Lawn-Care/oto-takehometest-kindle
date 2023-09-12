from flask import Blueprint, request, jsonify, url_for
from app.controller.business import (
    find_book,
    add_book_user,
    subtract_book_user,
    find_top_book_user,
    change_book_page_user,
    add_book_global,
    list_books,
    BookNotFoundError,
    ValidationError,
)
from typing import List, Dict, Union, Any

global_json = "data.json"
user_json = "user_library/user_library.json"

book_routes = Blueprint("book_routes", __name__)


def register_routes(app: Any) -> None:
    app.register_blueprint(book_routes)


def format_response(
    data: Union[List[Dict[str, Any]], Dict[str, Any]], status: int = 200
) -> Any:
    """
    Format the API response as JSON with a status code.

    Args:
        data (Union[List[Dict[str, Any]], Dict[str, Any]]): Data to include in the response.
        status (int): HTTP status code.

    Returns:
        Any: JSON response with data and status code.
    """
    return jsonify({"data": data, "status": status})


@book_routes.route("/user/books", methods=["GET"])
def get_all_books_user() -> Any:
    """
    Get a list of all books in the user's library.

    Returns:
        Any: JSON response with the list of books.
    """
    books = list_books(user_json)
    return format_response(books)


@book_routes.route("/global/books", methods=["GET"])
def get_all_books_global() -> Any:
    """
    Get a list of all books in the global library.

    Returns:
        Any: JSON response with the list of books.
    """
    books = list_books(global_json)
    return format_response(books)


@book_routes.route(
    "/global/books/search/<key>/<value>", defaults={"target": None}, methods=["GET"]
)
@book_routes.route("/global/books/search/<key>/<value>/<target>", methods=["GET"])
def search_book_global(key: str, value: str, target: str = None) -> Any:
    """
    Search for books in the global library based on a key-value pair.

    Args:
        key (str): The key to search for (e.g., "title", "author").
        value (str): The value to search for.
        target (str, optional): The target key to retrieve from matching books.

    Returns:
        Any: JSON response with the list of matching books.
    """
    books = find_book(key, value, global_json, target=target)
    return format_response(books)


@book_routes.route(
    "/user/books/search/<key>/<value>", defaults={"target": None}, methods=["GET"]
)
@book_routes.route("/user/books/search/<key>/<value>/<target>", methods=["GET"])
def search_book_user(key: str, value: str, target: str = None) -> Any:
    """
    Search for books in the user's library based on a key-value pair.

    Args:
        key (str): The key to search for (e.g., "title", "author").
        value (str): The value to search for.
        target (str, optional): The target key to retrieve from matching books.

    Returns:
        Any: JSON response with the list of matching books.
    """
    try:
        books = find_book(key, value, user_json, target=target)
        return format_response(books)
    except BookNotFoundError:
        return jsonify({"error": "No books found matching the criteria."}), 404


@book_routes.route("/user/books/<uuid>", methods=["POST"])
def add_book_to_user_library(uuid: str) -> Any:
    """
    Add a book to the user's library.

    Args:
        uuid (str): The UUID of the book to add.

    Returns:
        Any: JSON response with the status and the added book details.
    """
    try:
        response = add_book_user(uuid, global_json, user_json)
        return format_response(response)
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@book_routes.route("/global/books", methods=["POST"])
def add_book_to_global_library() -> Any:
    """
    Add a book to the global library.

    Returns:
        Any: JSON response with the status and the added book details.
    """
    data: Dict[str, Union[str, int]] = request.get_json()
    response = add_book_global(data, global_json)
    return format_response(response)


@book_routes.route("/user/books/<uuid>", methods=["DELETE"])
def remove_book_from_user_library(uuid: str) -> Any:
    """
    Remove a book from the user's library.

    Args:
        uuid (str): The UUID of the book to remove.

    Returns:
        Any: JSON response with the status and the removed book UUID.
    """
    response = subtract_book_user(uuid, user_json)
    return format_response(response)


@book_routes.route("/user/books/top/<target>", methods=["GET"])
def get_top_user_book(target: str = None) -> Any:
    """
    Get the top book in the user's library based on a target key.

    Args:
        target (str, optional): The target key to use for finding the top book.

    Returns:
        Any: JSON response with the status and the top book based on the target key.
    """
    book = find_top_book_user(user_json, target=target)
    return format_response(book)


@book_routes.route("/user/books/last-read", methods=["GET"])
def get_last_user_book() -> Any:
    """
    Get the last-read book in the user's library.

    Returns:
        Any: JSON response with the status and the last-read book.
    """
    book = find_top_book_user(user_json, "last_read_date")
    return format_response(book)


@book_routes.route("/user/books/<uuid>/page/<page_number>", methods=["PATCH"])
def update_book_page_for_user(uuid: str, page_number: str) -> Any:
    """
    Update the page number of a book in the user's library.

    Args:
        uuid (str): The UUID of the book to update.
        page_number (str): The new page number.

    Returns:
        Any: JSON response with the status and the updated book UUID.
    """
    try:
        page_number = int(page_number)
    except ValueError:
        return {"status": "error", "message": "Page number must be an integer."}, 400

    try:
        response = change_book_page_user(uuid, page_number, user_json)
        return format_response(response)
    except ValidationError as ve:
        return {"status": "error", "message": str(ve)}, 400
    except BookNotFoundError as bne:
        return {
            "status": "error",
            "message": "No book with the specified UUID exists in the user's library.",
        }, 404
