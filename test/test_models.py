from data_models import Author, Book

def test_author_model():
    author = Author(name="Mark Twain", birth_date="1835-11-30", date_of_death="1910-04-21")
    assert author.name == "Mark Twain"
    assert author.birth_date == "1835-11-30"
    assert author.date_of_death == "1910-04-21"

def test_book_model():
    book = Book(title="Adventures of Huckleberry Finn", isbn="9780142437179", publication_year=1884)
    assert book.title == "Adventures of Huckleberry Finn"
    assert book.isbn == "9780142437179"
    assert book.publication_year == 1884
