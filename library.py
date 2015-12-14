class Library:
    def __init__(self):
        self.__books = []

    def append(self, book):
        self.__books.append(book)

    def books(self):
        return self.__books

    def sort(self, sorter, criteria):
        self.__books = sorter.sort(self.__books, criteria)
