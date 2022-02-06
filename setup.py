import sqlite3

def setup():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE Citycoords(
key text PRIMARY KEY,
lat integer,
long integer,
FOREIGN KEY(key) REFERENCES Populations(key))""")
    c.execute(""" CREATE TABLE Populations(
name text,
code text,
year integer,
population integer,
key text PRIMARY KEY)""")
    c.execute(""" CREATE TABLE Users(
username text
password text
uid text PRIMARY KEY""")
    c.execute(""" CREATE TABLE Nukes(
name text PRIMARY KEY,
yield integer,
uid text,
FOREIGN KEY(uid) REFERENCES Users(uid))""")

    conn.commit()

