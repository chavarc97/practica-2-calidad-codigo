#!/usr/bin/env python3
"""Populate the database with sample data."""
import csv

import requests

BASE_URL = 'http://localhost:8000'


def main():
    """Read CSV and populate the database."""
    with open('books.csv', encoding='utf-8') as fd:
        books_csv = csv.DictReader(fd)
        for book in books_csv:
            del book['bookID']
            book['authors'] = book['authors'].split('/')
            x = requests.post(BASE_URL + '/book', json=book, timeout=10)
            if not x.ok:
                print(f'Failed to post book {x} - {book}')


if __name__ == '__main__':
    main()
