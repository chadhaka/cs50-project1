import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String, primary_key=True)
    password = db.Column(db.String,nullable=False)

class Book(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    publishYear = db.Column(db.Integer,nullable=False)    
    reviews = db.relationship("Review", backref="bookreview", lazy=True)

    def submitReview(self, username, rating, review):
        review = Review(book_id=self.isbn, user_id=username, rating=rating, review=review)
        db.session.add(review)
        db.session.commit()


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String, db.ForeignKey('books.isbn'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)
    rating = db.Column(db.Integer,nullable=False)
    review = db.Column(db.String, nullable=True)

