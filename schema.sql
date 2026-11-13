-- Create a database with this file. 
-- You can do it in terminal after you have cloned the repository:
-- "sqlite 3 database.db < schema.sql"

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);