from app.model import kindle_model

# Global allowed keys for searching
ALLOWED_KEYS = [
    "pages",
    "year",
    "title",
    "author",
    "uuid",
    "reading_status",
    "genre",
    "last_read_date",
]

REQUIRED_KEYS = [
    "author",
    "country",
    "imageLink",
    "language",
    "link",
    "pages",
    "title",
    "year",
    "last_read_page",
    "percentage_read",
    "last_read_date",
]


class BookNotFoundError(Exception):
    """Raised when a book is not found."""

    pass


class ValidationError(Exception):
    """Raised when there's a validation error."""

    pass


class ValueError(Exception):
    """Raised when there's a validation error."""

    pass


# Define a function to validate the keys used for searching.
def validate_keys(target) -> None:
    if target is not None and target not in ALLOWED_KEYS:
        raise ValidationError(
            f"Invalid target. Allowed keys for searching are {', '.join(ALLOWED_KEYS)}."
        )


def validate_json(json_data) -> None:
    if not json_data:
        raise ValidationError("JSON data is None.")

    json_keys = set(json_data.keys())
    required_keys_set = set(REQUIRED_KEYS)

    if json_keys != required_keys_set:
        missing_keys = required_keys_set - json_keys
        extra_keys = json_keys - required_keys_set

        error_messages = []

        if missing_keys:
            error_messages.append(f"Missing keys: {', '.join(missing_keys)}")

        if extra_keys:
            error_messages.append(f"Extra keys: {', '.join(extra_keys)}")

        raise ValidationError(f"Invalid JSON. {' '.join(error_messages)}")


# Define a function to list all the books from a library.
def list_books(library_path: str) -> list:
    library_instance = kindle_model.Library(library_path)
    return library_instance.list_books()


# Define a function to find a book based on a key and value.
def find_book(key: str, value: str, library_path: str, target=None) -> list:
    validate_keys(target)
    validate_keys(key)

    library_instance = kindle_model.Library(library_path)
    found = library_instance.find_books(**{key: value})
    if not found:
        raise BookNotFoundError("No books found matching the criteria.")
    if target:
        return [{target: book[target]} for book in found]
    return found


# Define a function to add a book to a user's library.
def add_book_user(
    book_uuid: str, global_library_path: str, user_library_path: str
) -> dict:
    user_library_instance = kindle_model.Library(user_library_path)
    global_library_instance = kindle_model.Library(global_library_path)
    found_user = user_library_instance.find_books(uuid=book_uuid)
    if found_user:
        raise ValidationError("Book already exists in the user's library.")
    found_global = global_library_instance.find_books(uuid=book_uuid)
    if not found_global:
        raise BookNotFoundError("Book not found in the global library.")
    book_to_add = kindle_model.Book.from_json(found_global[0])
    user_library_instance.add_book(book_to_add)
    return {"status": "success", "book added": book_to_add.to_dict()}


# Define a function to add a book to a user's library.
def add_book_global(json: str, global_library_path: str) -> dict:
    validate_json(json)
    global_library_instance = kindle_model.Library(global_library_path)
    new_book = kindle_model.Book(**json)
    global_library_instance.add_book(new_book)

    return {"status": "success", "book added": new_book.to_dict()}


# Define a function to remove a book from a user's library.
def subtract_book_user(book_uuid: str, user_library_path: str) -> list:
    user_library_instance = kindle_model.Library(user_library_path)
    found_user = user_library_instance.find_books(uuid=book_uuid)
    if not found_user:
        raise BookNotFoundError("Book not found in the user library.")
    user_library_instance.remove_book(book_uuid)
    return {"status": "success", "book removed": book_uuid}


# Define a function to find the book with the highest value for a certain key in a user's library.
def find_top_book_user(user_library_path: str, target: str) -> dict:
    validate_keys(target)
    user_library_instance = kindle_model.Library(user_library_path)
    books_user = user_library_instance.list_books()
    if not books_user:
        raise BookNotFoundError("No books in the user's library.")
    top_book = max(books_user, key=lambda book: book.get(target, float("-inf")))
    return {"status": "success", f"highest_value: {target}": top_book}


# Define a function to update the reading status (page number) of a book in a user's library.
def change_book_page_user(
    book_uuid: str, page_number: int, user_library_path: str
) -> dict:
    try:
        page_number = int(page_number)
    except ValueError:
        raise ValidationError("Page number must be an integer.")
    user_library_instance = kindle_model.Library(user_library_path)
    found_books = user_library_instance.find_books(uuid=book_uuid)
    if not found_books:
        raise BookNotFoundError(
            "No book with the specified UUID exists in the user's library."
        )
    total_pages = found_books[0].get("pages", None)
    if total_pages is not None and page_number > total_pages:
        raise ValidationError("Page number exceeds total pages of the book.")
    user_library_instance.update_reading_status(book_uuid, page_number)
    return {"status": "success", "book updated": book_uuid}
