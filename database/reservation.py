import sqlite3

def init_table(db):
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reservation(
            reservationID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER NOT NULL,
            screeningID INTEGER NOT NULL,
            numberOfSeats INTEGER NOT NULL,
            FOREIGN KEY(userID) REFERENCES users(id),
            FOREIGN KEY(screeningID) REFERENCES screenings(id)
    )''')
    db.commit()


def add_reservation(db, user_id, screening_id, number_of_seats):
    cursor = db.cursor()
    cursor.execute('INSERT INTO reservation (userID, screeningID, numberOfSeats) VALUES (?, ?, ?)', 
                        (user_id, screening_id, number_of_seats))
    db.commit()
    db.close()


def get_reservation_for_user(db, user_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM reservation WHERE userID = ?', (user_id,))
    reservations = cursor.fetchall()
    db.close()
    return reservations


def delete_reservation(db, reservation_id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM reservation WHERE reservationID = ?', (reservation_id,))
    db.commit()
    db.close()
