"""Model definitions for the Books API."""
import uuid

from pydantic import BaseModel, Field


class Book(BaseModel):
    """
    Book model.

    Attributes
    ----------
    id : str
        The book ID.
    title : str
        The book title.
    authors : list
        The list of authors.
    average_rating : float
        The average rating.
    isbn : str
        The ISBN.
    isbn13 : str
        The ISBN 13.
    language_code : str
        The language code.
    num_pages : int
        The number of pages.
    ratings_count : int
        The ratings count.
    text_reviews_count : int
        The text reviews count.
    publication_date : str
        The publication date.
    publisher : str
        The publisher.
    """

    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    title: str = Field(...)
    authors: list = Field(...)
    average_rating: float = Field(...)
    isbn: str = Field(...)
    isbn13: str = Field(...)
    language_code: str = Field(...)
    num_pages: int = Field(...)
    ratings_count: int = Field(...)
    text_reviews_count: int = Field(...)
    publication_date: str = Field(...)
    publisher: str = Field(...)

    class Config:
        """Pydantic configuration."""

        allow_population_by_field_name = True
        scheme_extra = {
            'example': {
                '_id': '066de609-b04a-4b30-b46c-32537c7f1f6e',
                'title': 'Poor People',
                'authors': ['William T. Vollmann'],
                'average_rating': 3.5,
                'isbn': '0060878827',
                'isbn13': '9780060878825',
                'language_code': 'eng',
                'num_pages': 434,
                'ratings_count': 769,
                'text_reviews_count': 139,
                'publication_date': '2/27/2007',
                'publisher': 'Ecco',
            }
        }


class BookUpdate(BaseModel):
    """
    Book update model.

    Attributes
    ----------
    title : str, optional
        The book title.
    authors : list, optional
        The list of authors.
    average_rating : float, optional
        The average rating.
    isbn : str, optional
        The ISBN.
    isbn13 : str, optional
        The ISBN 13.
    language_code : str, optional
        The language code.
    num_pages : int, optional
        The number of pages.
    ratings_count : int, optional
        The ratings count.
    text_reviews_count : int, optional
        The text reviews count.
    publication_date : str, optional
        The publication date.
    publisher : str, optional
        The publisher.
    """

    title: str | None = None
    authors: list[str] | None = None
    average_rating: float | None = None
    isbn: str | None = None
    isbn13: str | None = None
    language_code: str | None = None
    num_pages: int | None = None
    ratings_count: int | None = None
    text_reviews_count: int | None = None
    publication_date: str | None = None
    publisher: str | None = None

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            'example': {
                'title': 'Poor People',
                'authors': ['William T. Vollmann'],
                'average_rating': 3.5,
                'isbn': '0060878827',
                'isbn13': '9780060878825',
                'language_code': 'eng',
                'num_pages': 434,
                'ratings_count': 769,
                'text_reviews_count': 139,
                'publication_date': '2/27/2007',
                'publisher': 'Ecco',
            }
        }
