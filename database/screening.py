import sqlite3

def init_table(db):
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS screenings(
            screeningID INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT NOT NULL,
            filmID INTEGER NOT NULL,
            availableSeats INTEGER NOT NULL,
            FOREIGN KEY(filmID) REFERENCES films(filmID)
    )''')
    db.commit()


def add_screening(db, datetime, film_id, available_seats):
    cursor = db.cursor()
    cursor.execute('INSERT INTO screenings (datetime, filmID, availableSeats) VALUES (?, ?, ?)', 
                    (datetime, film_id, available_seats))
    db.commit()
    db.close()


def get_screening(db, screening_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM screenings WHERE screeningID = ?', (screening_id,))
    screening = cursor.fetchone()
    db.close()
    return screening


def get_screening_by_data(db, datetime, film_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM screenings WHERE datetime = ? AND filmID = ?', (datetime, film_id))
    screening = cursor.fetchone()
    db.close()
    return screening


def get_all(db):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM screenings')
    screenings = cursor.fetchall()
    db.close()
    return screenings


def get_screening_for_film(db, film_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM screenings WHERE filmID = ?', (film_id,))
    screenings = cursor.fetchall()
    db.close()
    return screenings


def get_seats_for_screening(db, screening_id):
    cursor = db.cursor()
    cursor.execute('SELECT availableSeats FROM screenings WHERE screeningID = ?', (screening_id,))
    screening = cursor.fetchone()
    db.close()
    return screening


def subtract_seats(db, screening_id, number_of_seats):
    cursor = db.cursor()

    cursor.execute('SELECT availableSeats FROM screenings WHERE screeningID = ?', (screening_id,))
    result = cursor.fetchone()
    if not result:
        db.close()
        raise Exception(f"Promitani s id {screening_id} nenalezeno")

    current_seats = result[0]
    if current_seats < number_of_seats:
        db.close()
        raise ValueError(f"Neni dostatek mista")

    new_seats = current_seats - number_of_seats
    cursor.execute('UPDATE screenings SET availableSeats = ? WHERE screeningID = ?', (new_seats, screening_id))
    db.commit()

    db.close()
