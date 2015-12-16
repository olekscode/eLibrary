class Library:
    def __init__(self):
        self.__books = []

    def append(self, book):
        self.__books.append(book)

    def books(self):
        return self.__books

    def __len__(self):
        return len(self.__books)

    def __getitem__(self, item):
        return self.__books[item]
