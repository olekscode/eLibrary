#!/usr/bin/python3

from book import Book
from library import Library
from libgen import generate
from mergesorter import MergeSorter

# TODO: Instead of generating the library, get data from some API

try:
    lib = generate(10)
    sorter = MergeSorter(2)
    print(len(lib.books()))
    lib.sort(sorter, 'title')
    print(len(lib.books()))
    
    for book in lib.books():
        print(book);
        print("-----------------------------------")

except Exception as exc:
    print("ERROR: ", exc)
