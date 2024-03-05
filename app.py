# Importing all the libraries
from flask import Flask, request, jsonify, abort 
# from flasgger import Swagger, swag_from
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

load_dotenv() # Loading the environment variables from a file named .env into the app.py

app = Flask(__name__) # Initialize a Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = (os.getenv("url_postgresql")) # Configure the SQLAlchemy database URI using environment variables
# The URI is retrieved from the "url_postgresql" variable defined in the .env file
db = SQLAlchemy(app) 
ma = Marshmallow(app) 

# This class below represents a book model, whic contains : id, title, author and observations
class Books(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    title = db.Column(db.String(70), nullable = False) 
    author = db.Column(db.String(50), nullable = False) 
    published_year = db.Column(db.Integer, nullable = False) 
    obs = db.Column(db.String(500), nullable = True) 

# A schema class for serializing and deserializing Book objects.
class BookSchema(ma.SQLAlchemyAutoSchema): 
    #  Attributes:
    #     Meta: Contains metadata about the schema.
    #         model: Specifies the model to be used for serialization and deserialization.
    class Meta:
        model = Books

# Instantiate a BookSchema object with the parameter many=True, indicating that it will handle multiple books.
book_schema = BookSchema(many=True) 

# Route to create a new book using the POST method
@app.route("/books", methods=["POST"])
def add_book():
# This function takes no arguments and performs the creation of a book in the DataBase
    data = request.get_json()
    new_book = Books(title=data['title'], author=data['author'], published_year=data['published_year'], obs=data['obs'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book created succefully"}), 201


# Route to pick all the books from DataBase with GET method
@app.route("/books", methods=["GET"])
def get_all_books():
# This function takes no arguments and performs the book's picking from the DataBase
    books = Books.query.all()
    result = book_schema.dump(books)
    return jsonify({"books": result})

# Route to pick a book from DataBase by its ID with GET method
@app.route("/books/<int:id>", methods=["GET"])  # We have added <int:id> to insure taht the ID will be known as a integer
def get_book_by_id(id):
# This function has the ID as an argument and performs the book picking from the DataBase
    try:
        # Try to pick a book from the DataBase
        book = Books.query.get(id)
        if book is None: # If the book's ID requested doesn't exist...
            raise ValueError("Book not found... :(")
        
        result = book_schema.dump([book])
        return jsonify(result), 200 # Returning the specific book from the ID requested
    except Exception as e:
        return jsonify({"error": str(e)}), 404 # Returning error in case of exception
    
# Route to edit book data from DataBase with PUT method
@app.route("/books/<int:id>", methods=["PUT"]) 
# This function has the ID as an argument and perform the book update in the DataBase
def update_book(id): 
    try:
        # Try to edit a book in the DataBase 
        book = Books.query.get(id)
        if not book: # If the ID requested doesn't exist...
            abort(404, description="Book not found.")

        data = request.get_json()
        
        # Verifying if the atributes exists on JSON before assigning
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.published_year = data.get('published_year', book.published_year)
        book.obs = data.get('obs', book.obs)

        db.session.commit()
        return jsonify({'message': 'Book updated successfully! :)'}), 200 # Returning a success message
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update book. Error: {str(e)}'}), 500 # Error in case of exception

# Running the application
if __name__ == "__main__":
    app.run(debug=True) 