-- Create a database with this file. 
-- You can do it in terminal after you have cloned the repository:
-- "sqlite 3 database.db < schema.sql"

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS video_links;
DROP TABLE IF EXISTS classes;
DROP TABLE IF EXISTS video_link_classes;


CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE video_links (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    youtube_url TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE video_link_classes (
    video_link_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    PRIMARY KEY (video_link_id, class_id),
    FOREIGN KEY (video_link_id) REFERENCES video_links(id) ON DELETE CASCADE,
    FOREIGN KEY (class_id) REFERENCES classes(id) ON DELETE CASCADE
);