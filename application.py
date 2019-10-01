import os

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


@app.route("/account?find", methods=["POST"])
def book():
    isbn=request.form.get("isbn")
    book_name=request.form.get("book_name")
    author_name=request.form.get("author_name")

    try:
        books=db.execute("SELECT * FROM public.books WHERE isbn = :isbn OR title = :book_name OR author = :author_name",{"isbn":isbn,"book_name":book_name,"author_name":author_name}).fetchall()
        return render_template("account.html", books=books)
    except Exception as a:
        return render_template("account.html", error_massage=a)
