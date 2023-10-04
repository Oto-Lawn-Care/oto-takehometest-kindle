'''Iterate over data.json and add an id field to each book

Usage: run from the root directory that contains data.json
    python scripts/set_data_book_id.py
'''

import json


LIBRARY_DATA_PATH = 'data.json'


if __name__ == '__main__':
    with open(LIBRARY_DATA_PATH, 'r') as library_file_in:
        library_json = json.load(library_file_in)

    for book_index, book in enumerate(library_json):
        book['id'] = book_index
    print(library_json)

    with open(LIBRARY_DATA_PATH, 'w') as library_file_out:
        json.dump(library_json, library_file_out, indent=2)
