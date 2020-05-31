import csv
import os

from flask import Flask, render_template, request
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    f = open("books.csv")
    count = 1
    reader = csv.reader(f)
    for isbn, title, author, publishYear in reader:
        if count is not 1:
            book = Book(isbn=isbn, title=title, author=author, publishYear=publishYear)
            db.session.add(book)
            print(f"Added Book {count}")
        count += 1
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
