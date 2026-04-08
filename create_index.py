#!/usr/bin/env python3
"""Create MongoDB indexes for the Books API."""
import os

from pymongo import ASCENDING, TEXT, MongoClient

# Read MongoDB connection details from environment variables
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'books')


def create_indexes():
    """Create indexes for the books collection."""
    # Connect to your MongoDB instance
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    collection = db['books']

    # Create index for average_rating (numeric)
    collection.create_index([('average_rating', ASCENDING)])
    print('Created index for average_rating')

    # Create index for num_pages (numeric)
    collection.create_index([('num_pages', ASCENDING)])
    print('Created index for num_pages')

    # Create text index for title (text)
    collection.create_index([('title', TEXT)])
    print('Created text index for title')

    # Create author index for authors (text)
    # "authors" is a list of strings, so we need to create a text index on
    # each author
    collection.create_index([('authors', TEXT)])
    print('Created text index for authors')

    print('All indexes created successfully')

    # Close the connection
    client.close()


if __name__ == '__main__':
    create_indexes()
