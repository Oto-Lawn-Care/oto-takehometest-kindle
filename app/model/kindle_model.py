class Book:
    '''Model class for Book'''
    def __init__(self, book_id: int, author: str, country: str, image_link: str, language: str, link: str, pages: int, title: str, year: int):
        '''Model Constructor'''
        self.id = book_id
        self.author = author
        self.country = country
        self.image_link = image_link
        self.language = language
        self.link = link
        self.pages = pages
        self.title = title
        self.year = year

    @classmethod
    def from_dict(cls, dict_book):
        return cls(
            book_id=dict_book['id'],
            author=dict_book['author'],
            country=dict_book['country'],
            image_link=dict_book['imageLink'],
            language=dict_book['language'],
            link=dict_book['link'],
            pages=dict_book['pages'],
            title=dict_book['title'],
            year=dict_book['year'],
        )


class UserBook():
    '''Model class for a Book that belongs to User'''
    def __init__(
        self,
        book_id: int,
        last_page: int,
        last_accessed: str
    ):
        self.book_id = book_id
        self.last_page = last_page
        self.last_accessed = last_accessed

    @classmethod
    def from_dict(cls, dict_user_book):
        return cls(
            book_id=dict_user_book['book_id'],
            last_page=dict_user_book['last_page'],
            last_accessed=dict_user_book['last_accessed']
        )
