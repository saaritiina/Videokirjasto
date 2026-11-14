import sqlite3
from flask import Flask, abort, redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db

import comments
import videos

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
    username = request.form.get("username", "").strip()
    password1 = request.form.get("password1", "")
    password2 = request.form.get("password2", "")

    if not username:
        return render_template(
            "message.html",
            message="Käyttäjätunnus ei voi olla tyhjä.",
            back_url="/register"
        )
    
    if not password1.strip():
        return render_template(
            "message.html",
            message="Salasana ei voi olla tyhjä.",
            back_url="/register"
        )
    
    if password1 != password2:
        return render_template(
            "message.html",
            message="Salasanat eivät ole samat.",
            back_url="/register"
        )
    
    password_hash = generate_password_hash(password1)

    try:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            [username, password_hash]
        )
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
    # If user is no longer logged in they will be redirected to login page
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "GET":
        return render_template(
            "link_form.html",
            heading="Lisää videolinkki",
            form_action="/add_link",
            title="",
            youtube_url="",
            classes= videos.get_classes(),
            selected_class_ids=[],
            button_text="Lisää linkki")
    
    title = request.form["title"].strip()
    youtube_url = request.form["youtube_url"].strip()
    
    db.execute(
        """
        INSERT INTO video_links (title, youtube_url, user_id)
        VALUES (?, ?, ?)
        """,
        [title, youtube_url, session["user_id"]]
    )

    link_id= db.last_insert_id()
    videos.save_link_classes(link_id)

    return redirect("/links")

@app.route("/edit_link/<int:link_id>", methods=["GET", "POST"])
def edit_link(link_id):
    if "user_id" not in session:
        return redirect("/login")

    # It is only allowed to edit the links that you have added.
    # Search for the links that has the same user_id that is logged in.
    result = db.query(
        """
        SELECT id, title, youtube_url
        FROM video_links
        WHERE id = ? AND user_id = ?
        """,
        [link_id, session["user_id"]]
    )

    if not result:
        return redirect("/links")

    link = result[0]

    if request.method == "POST":
        title = request.form["title"].strip()
        youtube_url = request.form["youtube_url"].strip()

        db.execute(
            """
            UPDATE video_links
            SET title = ?, youtube_url = ?
            WHERE id = ? AND user_id = ?
            """,
            [title, youtube_url, link_id, session["user_id"]]
        )

        videos.save_link_classes(link_id)
        return redirect("/links")

    selected = db.query(
        """
        SELECT class_id
        FROM video_link_classes
        WHERE video_link_id = ?
        """,
        [link_id]
    )

    return render_template(
        "link_form.html",
        heading="Muokkaa videolinkkiä",
        form_action=f"/edit_link/{link_id}",
        title=link["title"],
        youtube_url=link["youtube_url"],
        classes=videos.get_classes(),
        selected_class_ids=[int(item["class_id"]) for item in selected],
        button_text="Tallenna muutokset"
    )

@app.route("/link/<int:link_id>")
def link_detail(link_id):
    if "user_id" not in session:
        return redirect("/login")

    result = db.query(
        """
        SELECT
            v.id,
            v.user_id,
            v.title,
            v.youtube_url,
            u.username
        FROM video_links v
        JOIN users u ON v.user_id = u.id
        WHERE v.id = ?
        """,
        [link_id]
    )

    if not result:
        abort(404)

    classes = db.query(
        """
        SELECT c.name
        FROM classes c
        JOIN video_link_classes vlc ON vlc.class_id = c.id
        WHERE vlc.video_link_id = ?
        ORDER BY c.name
        """,
        [link_id]
    )

    comment_list = comments.get_comments(link_id)

    return render_template(
        "link_page.html",
        link=result[0],
        classes=classes,
        comments=comment_list
    )

@app.route("/delete_link/<int:link_id>", methods=["POST"])
def delete_link(link_id):
    if "user_id" not in session:
        return redirect("/login")

    db.execute(
        """
        DELETE FROM video_links
        WHERE id = ? AND user_id = ?
        """,
        [link_id, session["user_id"]]
    )

    return redirect("/links")


@app.route("/links")
def links():
    if "user_id" not in session:
        return redirect("/login")

    query = request.args.get("query", "").strip()

    sql = """
    SELECT
        v.id,
        v.user_id,
        v.title,
        v.youtube_url,
        u.username
    FROM video_links v
    JOIN users u ON v.user_id = u.id
    """

    if query:
        pattern = "%" + query + "%"
        sql += """
        WHERE v.title LIKE ?
           OR v.youtube_url LIKE ?
           OR EXISTS (
                SELECT 1
                FROM video_link_classes vlc
                JOIN classes c ON c.id = vlc.class_id
                WHERE vlc.video_link_id = v.id
                  AND c.name LIKE ?
           )
        """
        params = [pattern, pattern, pattern]
    else:
        params = []

    sql += " ORDER BY v.id DESC"

    links = db.query(sql, params)

    return render_template(
        "links.html",
        links=links,
        query=query
    )

@app.route("/new_comment", methods=["POST"])
def new_comment():
    if "user_id" not in session:
        return redirect("/login")

    content = request.form.get("content", "").strip()
    video_link_id = request.form.get("video_link_id", type=int)

    if not video_link_id:
        abort(400)

    link = db.query(
        "SELECT id FROM video_links WHERE id = ?",
        [video_link_id]
    )

    if not link:
        abort(404)

    if content and len(content) <= 1000:
        comments.add_comment(
            content,
            session["user_id"],
            video_link_id
        )

    return redirect("/link/" + str(video_link_id))

@app.route("/delete_comment/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    if "user_id" not in session:
        return redirect("/login")

    video_link_id = comments.remove_comment(
        comment_id,
        session["user_id"]
    )

    if video_link_id is None:
        abort(404)

    return redirect("/link/" + str(video_link_id))
