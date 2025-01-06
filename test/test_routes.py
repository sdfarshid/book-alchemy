import pytest
from app import app, db, Author, Book

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Library' in response.data

def test_add_author(client):
    response = client.post('/add_author', data={
        'name': 'Jane Austen',
        'birthdate': '1775-12-16',
        'date_of_death': '1817-07-18'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Jane Austen' in response.data

def test_add_book(client):
    # First, add an author
    client.post('/add_author', data={
        'name': 'J.K. Rowling',
        'birthdate': '1965-07-31'
    }, follow_redirects=True)

    # Then, add a book
    response = client.post('/add_book', data={
        'title': 'Harry Potter',
        'isbn': '1234567890',
        'publication_year': 1997,
        'author_id': 1
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Harry Potter' in response.data
