"""Test suite for the Books API endpoints."""

from unittest.mock import MagicMock

from fastapi.testclient import TestClient

# Importamos la app principal
from main import app


def test_list_books_empty():
    """Prueba simple para verificar el endpoint GET /book/."""
    # Simulamos (Mock) la base de datos para no requerir MongoDB ejecutándose
    mock_db = MagicMock()
    app.database = mock_db

    # Simulamos la respuesta limpia de MongoDB (sin libros en BD)
    # routes.py hace: find().sort().skip().limit()
    mock_db.books.find.return_value.sort.return_value.skip.return_value.limit.return_value = []  # noqa: E501

    # Usamos TestClient para simular la petición de un usuario
    with TestClient(app) as client:
        response = client.get('/book/')
        status_code = 200
        # Verificamos que el servidor responde con status 200 (OK)
        assert response.status_code == status_code    # noqa: S101
        # Verificamos que regresa una lista vacía (como mockeamos)
        assert response.json() == []  # noqa: S101


def test_create_book_missing_data():
    """Prueba simple de que falla al mandar datos
    incompletos en POST /book/.
    """  # noqa: D205
    with TestClient(app) as client:
        # Mandamos un body vacío para simular mala petición
        response = client.post('/book/', json={})

        # Debería regresar 422 Unprocessable Entity porque faltan campos obligatorios en el schema  # noqa: E501
        assert response.status_code == 422  # noqa: PLR2004, S101
