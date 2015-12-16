#!/usr/bin/python3

# from book import Book
# from library import Library
from libgen import generate
from mergesort import sort_parallel

# TODO: Instead of generating the library, get data from some API

try:
    lib = generate(100000)
    part_results = sort_parallel(lib, 'title', 4)

    for res in part_results:
        print(len(res))
        print("-----------------------------------")

except Exception as exc:
    print("ERROR: ", exc)
