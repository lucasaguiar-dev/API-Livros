from flask import Flask, request, jsonify
# from flasgger import Swagger, swag_from
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("url_postgresql")
db = SQLAlchemy(app)

class Books(db.Model): 
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(70), nullable = False)
    author = db.Column(db.String(50), nullable = False)
    published_year = db.Column(db.Integer, nullable = False)
    obs = db.Column(db.String(500), nullable = True) 


# Rota para criar um novo livro
@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    new_book = Books(title=data['title'], author=data['author'], published_year=data['published_year'], obs=data['obs'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Livro criado com sucesso"}), 201


# Rota para obter todos os livros
@app.route("/books", methods=["GET"])
def get_all_books():
    books = Books.query.all()
    result = []
    for book in books:
        book_data = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "published_year": book.published_year,
            "obs": book.obs
        }
        result.append(book_data)
    return jsonify({"books": result})

if __name__ == "__main__":
    app.run(debug=True)