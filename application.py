import os, requests

from flask import Flask, render_template, request, session, abort, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import login_user, current_user

app= Flask(__name__)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


#hash = generate_password_hash('foobar')

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/account", methods=["POST"])
def account():
    user_email=request.form.get("email")
    user_password=request.form.get("password")
    try:
        user=db.execute("SELECT * FROM public.user WHERE email = :email AND password = :password",{"email": user_email.lower(),"password": user_password})
        if user.rowcount == 1:
            return render_template("account.html")
        else:
            return render_template("index.html", err_message="Email or password incorrect.")

    except Exception as e: 
        return render_template("index.html", err_message=e)

   #SELECT * FROM public.user WHERE email = "jamorales516@icloud.com" AND password = "12345"


@app.route("/account/find", methods=["POST"])
def book():
    isbn=request.form.get("isbn")
    book_name=request.form.get("book_name")
    author_name=request.form.get("author_name")

    if str(isbn)=="":
        isbn="null0"
    if str(book_name)=="":
        book_name="null0"
    if str(author_name)=="":
        author_name="null0"

    try:
        books=db.execute("SELECT * FROM public.books WHERE isbn LIKE :isbn OR title LIKE :book_name OR author LIKE :author_name",{"isbn":"%"+isbn+"%","book_name":"%"+book_name+"%","author_name":"%"+author_name+"%"}).fetchall()
        if str(books)=="[]":
            return render_template("account.html", error_massage="No se encontraron resultados.")
        else:
            return render_template("account.html", books=books)
    except Exception as a:
        return render_template("account.html", error_massage=a)

@app.route("/account/find/<isbn_book>")
def booked(isbn_book):
    try:
        book=db.execute("SELECT * FROM public.books WHERE isbn = :isbn_book",{"isbn_book":isbn_book})

        url="https://www.goodreads.com/book/review_counts.json"
        key="9tMr4aYUqp51SYMuqS8YPA"

        book_id=requests.get(url, params={"key":key, "isbns":isbn_book})


        return render_template("account.html", books=book)
    except Exception as eb:
        return render_template("account.html", error_massage=eb)
    




"""
key: 9tMr4aYUqp51SYMuqS8YPA
secret: 25NmsyrVul592FeEy9nVYQ6HwyD0xyZxMo1gSk9tlzo
"""
