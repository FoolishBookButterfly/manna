import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from bible import fetch_passage, bible

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database/bible_app.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    OLD_TESTAMENT = list(bible.keys())[:39]
    NEW_TESTAMENT = list(bible.keys())[39:]

    return render_template("index.html", bible=bible, old_testament=OLD_TESTAMENT, new_testament=NEW_TESTAMENT)


@app.route("/chapter/<book_name>/<int:chapter_num>")
def chapter(book_name, chapter_num):
    chapters = bible[book_name]
    verses = chapters[str(chapter_num)]

    return render_template(
        "chapter.html",
        book_name=book_name,
        chapter_num=chapter_num,
        chapters=chapters,
        verses=verses
    )