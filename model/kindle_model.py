class Book:
    '''Model class for Book'''
    def __init__(self, author: str, country: str, image_link: str, language: str, link: str, pages: int, title: str, year: int):
        '''Model Constructor'''
        self.author = author
        self.country = country
        self.image_link = image_link
        self.language = language
        self.link = link
        self.pages = pages
        self.title = title
        self.year = year