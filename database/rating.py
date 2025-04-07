import sqlite3

def init_table(db):
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS ratings(
            ratingID INTEGER PRIMARY KEY AUTOINCREMENT,
            filmID INTEGER NOT NULL,
            userID INTEGER NOT NULL,
            comment TEXT NOT NULL,
            FOREIGN KEY(filmID) REFERENCES films(id),
            FOREIGN KEY(userID) REFERENCES users(id)
    )''')
    db.commit()


def add_rating(db, film_id, user_id, comment):
    cursor = db.cursor()

    cursor.execute('INSERT INTO ratings (filmID, userID, comment) VALUES (?, ?, ?)', 
                   (film_id, user_id, comment))
    db.commit()
    db.close()


def get_all(db):
    cursor = db.cursor()
    cursor.execute('SELECT * from ratings')
    comments = cursor.fetchall()
    db.close()
    return comments


def get_rating_for_user(db, user_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM ratings WHERE userID = ?', (user_id,))
    raings = cursor.fetchall()
    db.close()
    return raings


def delete_rating(db, rating_id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM ratings WHERE ratingID = ?', (rating_id,))
    db.commit()
    db.close()
