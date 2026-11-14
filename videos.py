
import db
from flask import request

def get_classes():
    return db.query("SELECT id, name FROM classes ORDER BY name")

def save_link_classes(link_id):
    # Delete the classes that video may already have
    db.execute(
        "DELETE FROM video_link_classes WHERE video_link_id = ?",
        [link_id]
    )
    # Save the classes that already exists.
    existing_classes = get_classes()
    valid_ids = {int(item["id"]) for item in existing_classes}

    for class_id in request.form.getlist("class_ids"):
        try:
            class_id = int(class_id)
        except ValueError:
            continue

        if class_id in valid_ids:
            db.execute(
                """
                INSERT OR IGNORE INTO video_link_classes
                    (video_link_id, class_id)
                VALUES (?, ?)
                """,
                [link_id, class_id]
            )
    # Save new classes. There may be multiple classes separated with comma. 
    new_names = request.form.get("new_classes", "")
    names = {name.strip() for name in new_names.split(",") if name.strip()}

    for name in names:
        db.execute(
            "INSERT OR IGNORE INTO classes (name) VALUES (?)",
            [name]
        )

        result = db.query(
            "SELECT id FROM classes WHERE name = ?",
            [name]
        )

        if result:
            db.execute(
                """
                INSERT OR IGNORE INTO video_link_classes
                    (video_link_id, class_id)
                VALUES (?, ?)
                """,
                [link_id, result[0]["id"]]
            )