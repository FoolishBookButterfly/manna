import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from bible import fetch_passage, bible, format_slug

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database/bible_app.db")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template("500.html"), 500

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
     return render_template("index.html")

@app.route("/book")
def books():
    OLD_TESTAMENT = list(bible.keys())[:39]
    NEW_TESTAMENT = list(bible.keys())[39:]

    return render_template("book.html", bible=bible, old_testament=OLD_TESTAMENT, new_testament=NEW_TESTAMENT, format_slug=format_slug)


@app.route("/chapter/<book_slug>/<int:chapter_num>")
def chapter(book_slug, chapter_num):

    book_name = next(
        (book for book in bible if format_slug(book) == book_slug),
        None
    )

    if book_name is None:
        return render_template("404.html"), 404
    
    chapters = bible[book_name]

    if str(chapter_num) not in chapters:
            return render_template("404.html"), 404
    
    verses = chapters[str(chapter_num)]
    books = list(bible.keys())


    return render_template(
        "chapter.html",
        book_name=book_name,
        chapter_num=chapter_num,
        chapters=chapters,
        verses=verses,
        format_slug=format_slug,
        books=books,
        bible=bible
    )