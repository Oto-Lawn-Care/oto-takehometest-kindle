# Usage Explanation

`GET /book` -> Retrieve the latest book

`GET /book/{book_id}` -> Retrieve the metadata for a specific book in the user library

`DELETE /book/{book_id}` -> Remove a book from the user library (returns updated copy of user library)

`PUT /book/{book_id}` -> Insert or update a book in the user library (returns updated copy of user library)
 * `page` (required) -> the last page read by user
 * `last_accessed` (required) -> the date the user last accessed (`YYYY-mm-dd`)

`GET /book/{book_id}/page` -> Retrieve the last read page of a book