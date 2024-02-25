from flask import Flask, request
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


@app.route("/")
def home():
    return ("hello world")

if __name__ == "__main__":
    app.run(debug=True)