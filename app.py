from flask import Flask, request, jsonify, abort
# from flasgger import Swagger, swag_from
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (os.getenv("url_postgresql"))
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Books(db.Model): 
    id = db.Column(db.Integer, primary_key = True) #pode colocar o id, sendo a primary_key = false or true? importa somente a posição do parâmetro ou o nome tbm?
    title = db.Column(db.String(70), nullable = False)
    author = db.Column(db.String(50), nullable = False)
    published_year = db.Column(db.Integer, nullable = False)
    obs = db.Column(db.String(500), nullable = True) 


class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Books

book_schema = BookSchema(many=True)


# Route for creating a new book
@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    new_book = Books(title=data['title'], author=data['author'], published_year=data['published_year'], obs=data['obs'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Livro criado com sucesso"}), 201


# Route for getting all books
@app.route("/books", methods=["GET"])
def get_all_books():
    books = Books.query.all()
    result = book_schema.dump(books)
    return jsonify({"books": result})


# Route for getting a book by id
@app.route("/books/<int:id>", methods=["GET"])  # Adicionei <int:id> para garantir que o ID seja interpretado como um número inteiro
def get_book_by_id(id):
    try:
        # Tentar buscar o livro pelo ID na db
        book = Books.query.get(id)
        if book is None:
            raise ValueError("Não encontramos esse livro... :(")
        
        result = book_schema.dump([book])
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 404
    

# Route for modifying a book
@app.route("/books/<int:id>", methods=["PUT"]) 
def update_book(id): 
    try:
        # Tentar editar um livro na DataBase
        book = Books.query.get(id)
        if not book:
            abort(404, description="Book not found.")

        data = request.get_json()
        
        # Verificar se os campos existem no JSON antes de atribuir
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.published_year = data.get('published_year', book.published_year)
        book.obs = data.get('obs', book.obs)

        db.session.commit()
        return jsonify({'message': 'Book updated successfully! :)'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update book. Error: {str(e)}'}), 500


# Route for deleting a book
@app.route("/books/delete/<int:id>", methods=["DELETE"])
def delete_his_book_by_id(id):
    try:
        del_book = Books.query.get(id)
        if del_book is None:
            return jsonify("error", "Livro não encontrado!"), 404

        db.session.delete(del_book)
        db.session.commit()
        result = book_schema.dump([del_book])
        return jsonify({f"Livro deletado com sucesso!": result}), 200
    
    except Exception as e:
        return jsonify("erro","Infelizmente ocorreu um erro! Não foi possivel deletar esse livro!"), 500


if __name__ == "__main__":
    app.run(debug=True)