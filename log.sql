-- Keep a log of any SQL queries you execute.

-- Execute ==> sqlite3 tanvi.db ==> to begin running queries on the database.
-- sqlite> .tables
-- Exit ==> .quit

-- Table for users
CREATE TABLE 'users'
('id' INTEGER,
'username' TEXT NOT NULL,
hash TEXT NOT NULL,
PRIMARY KEY('id'));



