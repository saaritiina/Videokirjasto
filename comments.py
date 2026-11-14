import db

def get_comments(video_link_id):
    sql = """
    SELECT
        c.id,
        c.content,
        c.sent_at,
        c.user_id,
        u.username
    FROM comments c
    JOIN users u ON c.user_id = u.id
    WHERE c.video_link_id = ?
    ORDER BY c.id
    """
    return db.query(sql, [video_link_id])

def add_comment(content, user_id, video_link_id):
    sql = """
    INSERT INTO comments (content, sent_at, user_id, video_link_id)
    VALUES (?, datetime('now'), ?, ?)
    """
    db.execute(sql, [content, user_id, video_link_id])