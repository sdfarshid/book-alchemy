# Library Management System

This is a Flask-based web application for managing a library database. It allows users to perform CRUD operations for authors and books and includes advanced features like search, sort, and relationships between models.

## Features

- Add, view, and delete books.
- Add and view authors.
- Search books by title or author.
- Sort books by title or author name in ascending or descending order.
- Automatically delete authors with no associated books.

## Technologies Used

- **Backend**: Flask (Python), Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: Bootstrap 5

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/library-management.git
   cd library-management
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   Ensure the `data` directory exists and run the app to initialize the database.
   ```bash
   python app.py 
   ```

   Alternatively, you can create the database manually:
   ```bash
   python -c 'from app import create_database; create_database()'
   ```

5. **Run the application**:
   ```bash
   python app.py  OR  flask --app app run
   ```
   The app will be accessible at `http://localhost:5000`.

## Project Structure

```plaintext
.
├── app.py             # Main Flask application
├── data_models.py     # SQLAlchemy models for Author and Book
├── data/
│   └── library.sqlite # SQLite database (created at runtime)
├── templates/         # HTML templates (Jinja2)
│   ├── home.html
│   ├── add_author.html
│   └── add_book.html
├── test/            # Tests
│   ├── test_routes.py
│   ├── test_models.py
├── static/            # Static assets (CSS, JS)
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Routes

### Home Page (`/`)
- Displays a list of books with their authors.
- Allows sorting by title or author.
- Provides a search bar for filtering books by title or author name.

### Add Author (`/add_author`)
- Form to add a new author to the database.

### Add Book (`/add_book`)
- Form to add a new book to the database.
- Includes a dropdown for selecting an author.

### Delete Book (`/book/<int:book_id>/delete`)
- Deletes a book from the database.
- Automatically deletes the author if they have no other books.

## Example Queries

1. **Search Books**:
   - Search by title or author name using the search bar on the homepage.

2. **Sort Books**:
   - Sort by title or author name in ascending or descending order using the dropdowns on the homepage.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


Thank you for visiting this repository! If you find this project useful, please consider giving it a star! ⭐

