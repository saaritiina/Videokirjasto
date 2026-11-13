import sqlite3
from flask import Flask, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

# Registration
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return render_template(
            "message.html",
            message="Salasanat eivät ole samat.",
            back_url="/register"
        )
    
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return render_template(
            "message.html",
            message="Tunnus on jo varattu.",
            back_url="/register"
        )
    return render_template(
        "message.html",
        message="Tunnus luotu. Jatka kirjautumaan sisään.",
        back_url="/login",
        button_text="Kirjaudu sisään"
    )
# Login
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if result and check_password_hash(result[0]["password_hash"], password):
        session["user_id"] = result[0]["id"]
        session["username"] = username
        return redirect("/")

    return render_template(
        "message.html",
        message="Väärä käyttäjätunnus tai salasana.",
        back_url="/login"
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/add_link", methods= ["GET", "POST"])
def add_link():
    # If user is no longer logged in they will be redirected to login
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "GET":
        return render_template("add_link.html")
    
    title = request.form["title"]
    youtube_url = request.form["youtube_url"]

    sql = """
    INSERT INTO video_links
        (title, youtube_url, user_id)
    VALUES
        (?, ?, ?)
    """

    db.execute(
        sql,
        [title, youtube_url, session["user_id"]]
    )

    return redirect("/links")

@app.route("/links")
def links():
    # Users cannot see added links if they are not logged in.
    if "user_id" not in session:
        return redirect("/login")
    
    sql = """
    SELECT
        v.title,
        v.youtube_url,
        u.username
    FROM video_links v
    JOIN users u ON v.user_id = u.id
    ORDER BY v.id DESC
    """

    links = db.query(sql)

    return render_template(
        "links.html",
        links=links
    )
