import random
from book import Book
from library import Library

def generate(n):
    lib = Library()

    for i in range(0, n):
        lib.append(Book(
            "Author{0}".format(random.randint(1, n)),
            "Title{0}".format(random.randint(1, n)),
            random.randint(1950, 2015),
            "Publ{0}".format(random.randint(1, n))))

    return lib
