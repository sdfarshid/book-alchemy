import secrets
from flask import Flask, render_template, request, flash, redirect, url_for
from data_models import db, Author, Book
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, DATABASE_NAME)}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"connect_args": {"timeout": 15}}

app.secret_key = secrets.token_hex(16)

db.init_app(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

def create_database():
    with app.app_context():
        db.create_all()
    print("Create!")


def load_page(template_name: str, args=None):
    if args is None:
        args = {}
    return render_template(f'{template_name}.html', **args)


def commit_model_query(model):
    try:
        db.session.add(model)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        raise error


@app.route("/", methods=["GET"], endpoint="home")
def home():
    sort_by = request.args.get("sort_by", "title")
    sort_order = request.args.get("sort_order", "asc")
    search_query = request.args.get("search", "").strip()

    if sort_by not in ["title", "author"]:
        sort_by = "title"

    query = Book.query

    if search_query:
        query = query.filter(
            Book.title.ilike(f"%{search_query}%") |
            Book.author.has(Author.name.ilike(f"%{search_query}%"))
        )

    if sort_by == "author":
        query = query.join(Author).order_by(
            Author.name.asc() if sort_order == "asc" else Author.name.desc()
        )
    else:
        query = query.order_by(
            Book.title.asc() if sort_order == "asc" else Book.title.desc()
        )

    books = query.all()

    return load_page("home", {"books": books, "sort_by": sort_by, "sort_order": sort_order})


@app.route("/add_author", methods=["GET", "POST"], endpoint="add_author")
def add_author():
    result = {}
    if request.method == "POST":
        result = add_new_author()

    return load_page("add_author", {"result": result})


def add_new_author() -> dict:
    try:
        name = request.form["name"]
        birth_date = request.form["birthdate"]
        date_of_death = request.form.get("date_of_death")
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)

        commit_model_query(new_author)

        return {"status": True, "message": f"{str(new_author)} added successfully!"}
    except Exception as error:
        return {"status": False, "message": f"Error: {str(error)}"}


@app.route("/add_book", methods=["GET", "POST"], endpoint="add_book")
def add_book():
    result = {}
    authors = Author.query.all()

    if request.method == "POST":
        result = add_new_book()

    return load_page("add_book", {"result": result, "authors": authors})


def add_new_book() -> dict:
    try:
        title = request.form.get("title")
        isbn = request.form.get("isbn")
        publication_year = int(request.form.get("publication_year"))
        author_id = int(request.form["author_id"])

        new_book = Book(
            title=title,
            isbn=isbn,
            publication_year=publication_year,
            author_id=author_id
        )

        commit_model_query(new_book)
        return {"status": True, "message": f"{str(new_book)} added successfully!"}
    except Exception as error:
        return {"status": False, "message": f"Error: {str(error)}"}



@app.route("/book/<int:book_id>/delete", methods=["POST"], endpoint="delete_book")
def delete_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        author = book.author

        db.session.delete(book)
        db.session.commit()

        if not author.books:
            db.session.delete(author)
            db.session.commit()

        flash("Book deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting book: {str(e)}", "danger")

    return redirect(url_for("home"))



if __name__ == "__main__":
    # Create the database if it doesn't exist
    if not os.path.exists(os.path.join(BASE_DIR, DATABASE_NAME)):
        create_database()
    app.run(host="0.0.0.0", port=5000, debug=True)
