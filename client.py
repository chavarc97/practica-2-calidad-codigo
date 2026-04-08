#!/usr/bin/env python3
"""Client for the Books API."""
import argparse
import logging
import os
import sys

import requests

# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('books.log')
handler.setFormatter(
    logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
)
log.addHandler(handler)

# Read env vars related to API connection
BOOKS_API_URL = os.getenv('BOOKS_API_URL', 'http://localhost:8000')


def print_book(book):
    """
    Print book details.

    Parameters
    ----------
    book : dict
        Book data.
    """
    for k in book.keys():
        print(f'{k}: {book[k]}')
    print('=' * 50)


def list_books(rating, num_pages, title, limit, skip):
    """
    List books from the API.

    Parameters
    ----------
    rating : float
        Minimum rating.
    num_pages : int
        Number of pages.
    title : str
        Book title.
    limit : int
        Limit results.
    skip : int
        Skip results.
    """
    suffix = '/book'
    endpoint = BOOKS_API_URL + suffix
    params = {
        'rating': rating,
        'num_pages': num_pages,
        'title': title,
        'limit': limit,
        'skip': skip,
    }
    # Remove None values from params
    params = {k: v for k, v in params.items() if v is not None}
    response = requests.get(endpoint, params=params, timeout=10)
    if response.ok:
        json_resp = response.json()
        for book in json_resp:
            print_book(book)
    else:
        print(f'Error: {response.status_code} - {response.text}')


def get_book_by_id(id):
    """
    Get a book by ID.

    Parameters
    ----------
    id : str
        Book ID.
    """
    suffix = f'/book/{id}'
    endpoint = BOOKS_API_URL + suffix
    response = requests.get(endpoint, timeout=10)
    if response.ok:
        json_resp = response.json()
        print_book(json_resp)
    else:
        print(f'Error: {response}')


# UPDATE AND DELETE ACTIONS -------------------------------
def update_book(  # noqa: PLR0913, PLR0917
    id,
    title=None,
    authors=None,
    average_rating=None,
    isbn=None,
    isbn13=None,
    language_code=None,
    num_pages=None,
    ratings_count=None,
    text_reviews_count=None,
    publication_date=None,
    publisher=None,
):
    """
    Update a book.

    Parameters
    ----------
    id : str
        Book ID.
    title : str, optional
        Book title.
    authors : list, optional
        List of authors.
    average_rating : float, optional
        Average rating.
    isbn : str, optional
        ISBN.
    isbn13 : str, optional
        ISBN 13.
    language_code : str, optional
        Language code.
    num_pages : int, optional
        Number of pages.
    ratings_count : int, optional
        Ratings count.
    text_reviews_count : int, optional
        Text reviews count.
    publication_date : str, optional
        Publication date.
    publisher : str, optional
        Publisher.
    """
    suffix = f'/book/{id}'
    endpoint = BOOKS_API_URL + suffix

    # Prepare the payload, filtering out None values
    payload = {
        k: v
        for k, v in {
            'title': title,
            'authors': authors,
            'average_rating': average_rating,
            'isbn': isbn,
            'isbn13': isbn13,
            'language_code': language_code,
            'num_pages': num_pages,
            'ratings_count': ratings_count,
            'text_reviews_count': text_reviews_count,
            'publication_date': publication_date,
            'publisher': publisher,
        }.items()
        if v is not None
    }

    if not payload:
        print(
            'Error: At least one field must be provided for updating the book.'
        )
        return
    res = requests.put(endpoint, json=payload, timeout=10)
    if res.ok:
        json_resp = res.json()
        print_book(json_resp)
    else:
        print(f'Error: {res.status_code} - {res.text}')


def delete_book(id):
    """
    Delete a book.

    Parameters
    ----------
    id : str
        Book ID.
    """
    suffix = f'/book/{id}'
    endpoint = BOOKS_API_URL + suffix
    res = requests.delete(endpoint, timeout=10)
    if res.ok:
        json_res = res.json()
        print(json_res)
    else:
        print(f'Error: {res}')


# ---------------------------------------------------------


def main():
    """Execute the main function."""
    log.info(f'Welcome to books catalog. App requests to: {BOOKS_API_URL}')

    parser = argparse.ArgumentParser()

    list_of_actions = ['search', 'get', 'update', 'delete']
    parser.add_argument(
        'action',
        choices=list_of_actions,
        help='Action to be user for the books library',
    )
    parser.add_argument(
        '-i',
        '--id',
        help='Provide a book ID which related to the book action',
        default=None,
    )
    parser.add_argument(
        '-r',
        '--rating',
        help=(
            'Search parameter to look for books with average rating '
            'equal or above the param (0 to 5)'
        ),
        type=float,
        default=None,
    )
    parser.add_argument(
        '-p',
        '--pages',
        help='Search parameter to look for books with exact number of pages',
        type=int,
        default=None,
    )
    parser.add_argument(
        '-t',
        '--title',
        help=(
            'Search parameter to look for books with matching title '
            '(partial match)'
        ),
        default=None,
    )
    parser.add_argument(
        '-l',
        '--limit',
        help='Limit the number of results returned',
        type=int,
        default=None,
    )
    parser.add_argument(
        '-s', '--skip', help='Skip the first n results', type=int, default=None
    )
    parser.add_argument(
        '-a',
        '--authors',
        nargs='+',
        help=(
            "List of authors (e.g., --authors 'Julie Sylvester' "
            "'David Sylvester')"
        ),
        default=None,
    )
    parser.add_argument('--isbn', help='ISBN of the book', default=None)
    parser.add_argument('--isbn13', help='ISBN-13 of the book', default=None)
    parser.add_argument('--language', help='Language code', default=None)
    parser.add_argument(
        '--ratings_count', type=int, help='Number of ratings', default=None
    )
    parser.add_argument(
        '--reviews_count',
        type=int,
        help='Number of text reviews',
        default=None,
    )
    parser.add_argument('--pub_date', help='Publication date', default=None)
    parser.add_argument('--publisher', help='Publisher name', default=None)

    args = parser.parse_args()

    if args.id and args.action not in {'get', 'update', 'delete'}:
        log.error(f"Can't use arg id with action {args.action}")
        sys.exit(1)

    if args.rating and args.action != 'search':
        log.error('Rating arg can only be used with search action')
        sys.exit(1)

    if args.action == 'search':
        list_books(args.rating, args.pages, args.title, args.limit, args.skip)
    elif args.action == 'get' and args.id:
        get_book_by_id(args.id)
    elif args.action == 'update':
        update_book(
            args.id,
            args.title,
            args.authors,
            args.rating,
            args.isbn,
            args.isbn13,
            args.language,
            args.pages,
            args.ratings_count,
            args.reviews_count,
            args.pub_date,
            args.publisher,
        )
    elif args.action == 'delete':
        delete_book(args.id)


if __name__ == '__main__':
    main()
