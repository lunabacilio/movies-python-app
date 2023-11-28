import sqlite3, random, datetime
from models import Movie

def getNewId():
    id = random.getrandbits(28)
    return id

movies = [
    {
        'available': True,
        'title': 'Dune',
        'timestamp': datetime.datetime.now()
    },
    {
        'available': False,
        'title': 'Toy Story',
        'timestamp': datetime.datetime.now()
    },
]    

def connect():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY, available BOOLEAN, title TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()
    for i in movies:
        mv = Movie(getNewId(), i['available'], i['title'], i['timestamp'])
        insert(mv)

def insert(movie):
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO movies VALUES (?,?,?,?)", (
        movie.id,
        movie.available,
        movie.title,
        movie.timestamp
    ))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies")
    rows = cur.fetchall()
    movies = []
    for i in rows:
        movie = Movie(i[0], True if i[1] == 1 else False, i[2], i[3])
        movies.append(movie)
    conn.close()
    return movies

def update(movie):
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("UPDATE movies SET available=?, title=? WHERE id=?", (movie.available, movie.title, movie.id))
    conn.commit()
    conn.close()

def delete(theId):
    conn = sqlite3.connect('movies.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM movies WHERE id=?", (theId,))
    conn.commit()
    conn.close()