import os

from flask import Flask, session, render_template, jsonify, request
from models import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO"

@app.route("/register")
def register():
    username = str(request.form.get("name"))
    password = str(request.form.get("password")).strip("'")
    
    existUser = User.query.get(username)
    if not existUser:
        user = User(username=username,password=password)
        db.session.add(user)
        db.session.commit()
        return render_template("success.html", message="Thank you for signing up!")    
    else:
        return render_template("error.html", message="Username exists, please try logging in")

@app.route("/login")
def login():
    username = str(request.form.get("name"))
    password = str(request.form.get("password")).strip("'")
    existUser = User.query.get(username)
    if existUser:
        userPassword = User.query.filter_by(username=username).first()
    if existUser and password == userPassword:
        return render_template("success.html", message="Login Successful")    
    else:
        return render_template("error.html", message="Invalid credentials. Please try again")

@app.route("/logout")
def logout():
    # End session
    # Is it feasible to log out using button and direct user to login?

@app.route("/search")
def search:
    searchCriteria = str(request.form.get("Search Criteria"))
    searchCriteria = "%" + searchCriteria + "%"
    isbns = Book.query.filter(Book.isbn.like(searchCriteria)).all()
    titles = Book.query.filter(Book.title.like(searchCriteria)).all()
    authors = Book.query.filter(Book.author.like(searchCriteria)).all()

    if isbns is None and titles is None and authors is None:
        return render_template("error.html", message="No results found, please modify your search criteria")
    else:
        results = []
        if isbns:
            results.append(isbns)
        if titles:
            results.append(titles)
        if authors:
            results.append(titles)
        return render_template("search.html", results=results)

@app.route("books/<str:isbn>")
def bookPage(isbn):
    bookCheck = Book.query.get(isbn)    
    if bookCheck is None:
        return render_template("error.html", message="Book doesn't exist.")

    book = db.session.query(Book, Review).filter(isbn == Review.book_id).all()
    return render_template("bookPage.html", book=book)








