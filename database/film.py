import sqlite3

def init_table(db):
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS films(
            filmID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            kind TEXT NOT NULL
    )''')
    db.commit()


def add_film(db, title, kind):
    cursor = db.cursor()

    if film_exists(db, title):
        # TODO: upozorneni
        print(f"Error: film {title} uz existuje")
        db.close()
        return

    cursor.execute('INSERT INTO films (title, kind) VALUES (?, ?)', (title, kind))
    db.commit()
    db.close()


def film_exists(db, title):
    cursor = db.cursor()
    cursor.execute('SELECT EXISTS(SELECT 1 FROM films WHERE title = ?)', (title,))
    exists = cursor.fetchone()[0]
    return bool(exists)


def get_film(db, film_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM films WHERE filmID = ?', (film_id,))
    film = cursor.fetchone()
    db.close()
    return film


def get_film_by_title(db, film_title):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM films WHERE title = ?', (film_title,))
    film = cursor.fetchone()
    return film


def get_all(db):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM films')
    films = cursor.fetchall()
    db.close()
    return films
