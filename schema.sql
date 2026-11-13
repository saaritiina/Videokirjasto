-- Create a database with this file. 
-- You can do it in terminal after you have cloned the repository:
-- "sqlite 3 database.db < schema.sql"

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