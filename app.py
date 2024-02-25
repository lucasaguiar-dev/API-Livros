from flask import Flask, request
# from flasgger import Swagger, swag_from
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("url_postgresql")
db = SQLAlchemy(app)

class Livro(db.model):


@app.route("/")
def home():
    return ("hello world")

if __name__ == "__main__":
    app.run(debug=True)