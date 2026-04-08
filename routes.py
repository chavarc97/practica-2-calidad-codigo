#!/usr/bin/env python3
"""Routes for the Books API."""

from fastapi import (
    APIRouter,
    Body,
    HTTPException,
    Query,
    Request,
    Response,
    status,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from model import Book, BookUpdate

router = APIRouter()


@router.post(
    '/',
    response_description='Post a new book',
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
)
def create_book(request: Request, book: Book = Body(...)):  # noqa: B008
    """
    Create a new book.

    Parameters
    ----------
    request : Request
        The request object.
    book : Book
        The book data to create.

    Returns
    -------
    Book
        The created book.
    """
    book = jsonable_encoder(book)
    new_book = request.app.database['books'].insert_one(book)
    created_book = request.app.database['books'].find_one(
        {'_id': new_book.inserted_id}
    )
    return created_book


# Get all books
# Query parameters: rating, num_pages, title, limit, skip
@router.get(
    '/', response_description='Get all books', response_model=list[Book]
)
def list_books(  # noqa: PLR0913, PLR0917
    request: Request,
    rating: float = Query(0, description='Minimum average rating'),
    num_pages: int | None = Query(None, description='Number of pages'),
    title: str | None = Query(
        None, description='Book title (partial match)'
    ),
    limit: int = Query(
        10, ge=1, le=100, description='Number of books to return'
    ),
    skip: int = Query(0, ge=0, description='Number of books to skip'),
):
    """
    List books with optional filtering.

    Parameters
    ----------
    request : Request
        The request object.
    rating : float, optional
        Minimum average rating.
    num_pages : int, optional
        Number of pages.
    title : str, optional
        Book title (partial match).
    limit : int, optional
        Number of books to return.
    skip : int, optional
        Number of books to skip.

    Returns
    -------
    List[Book]
        A list of books.
    """
    # Create a query dictionary based on the query parameters
    query = {'average_rating': {'$gte': rating}}
    if num_pages is not None:
        query['num_pages'] = num_pages
    if title is not None:
        query['$text'] = {'$search': title}

    # Get the books from the database based on the query
    books = list(
        request.app.database['books']
        .find(query)
        .sort('average_rating', -1)
        .skip(skip)
        .limit(limit)
    )
    return books


# Get a single book by id
@router.get(
    '/{id}',
    response_description='Get a single book by id',
    response_model=Book,
)
def find_book(id: str, request: Request):
    """
    Find a book by ID.

    Parameters
    ----------
    id : str
        The book ID.
    request : Request
        The request object.

    Returns
    -------
    Book
        The found book.

    Raises
    ------
    HTTPException
        If the book is not found.
    """
    if (
        book := request.app.database['books'].find_one({'_id': id})
    ) is not None:
        return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Book with ID {id} not found',
    )


# Update a book by id
@router.put(
    '/{id}', response_description='Update a book by id', response_model=Book
)
def update_book(id: str, request: Request, book: BookUpdate = Body(...)):  # noqa: B008
    """
    Update a book by ID.

    Parameters
    ----------
    id : str
        The book ID.
    request : Request
        The request object.
    book : BookUpdate
        The book data to update.

    Returns
    -------
    Book
        The updated book.

    Raises
    ------
    HTTPException
        If the book is not found or no update data is provided.
    """
    # Convert the incoming book data to a dictionary, excluding the None values
    update_data = {
        k: v
        for k, v in book.model_dump(exclude_unset=True).items()
        if v is not None
    }

    # check if the data is empty
    if len(update_data) < 1:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='At least one field must be provided',
        )

    # perform the update query
    res = request.app.database['books'].update_one(
        {'_id': id}, {'$set': update_data}
    )

    # if no document was modified, raise an HTTPException
    if res.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Book with ID {id} not found',
        )

    # Then return the updated book
    if (
        book := request.app.database['books'].find_one({'_id': id})
    ) is not None:
        return book

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Book with ID {id} not found',
    )


# Delete a book by id
@router.delete('/{id}', response_description='Delete a book')
def delete_book(id: str, request: Request, response: Response):
    """
    Delete a book by ID.

    Parameters
    ----------
    id : str
        The book ID.
    request : Request
        The request object.
    response : Response
        The response object.

    Returns
    -------
    JSONResponse
        Confirmation of deletion.

    Raises
    ------
    HTTPException
        If the book is not found.
    """
    # First find the book
    book = request.app.database['books'].find_one({'_id': id})

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Book with ID {id} not found',
        )

    # If the book exists, delete it
    delete_res = request.app.database['books'].delete_one({'_id': id})

    if delete_res.deleted_count == 1:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                'message': f'Book with ID {id} was successfully deleted',
                'deleted_book': {
                    'id': id,
                    'title': book.get('title'),
                    'authors': book.get('authors'),
                },
            },
        )

    # This case should rarely happen - the book was found but couldn't be
    # deleted
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail='Failed to delete the book',
    )
