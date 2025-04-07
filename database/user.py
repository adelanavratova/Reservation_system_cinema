import sqlite3

def init_table(db):
    cursor = db.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(
            userID INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL
    )''')
    db.commit()


def add_user(db, username, password, first_name, last_name):
    if user_exists(db, username):
        # TODO: upozorneni
        print(f"Error: uzivatel {username} uz existuje")
        db.close()
        return

    cursor = db.cursor()
    cursor.execute('INSERT INTO users (username, password, firstName, lastName) VALUES (?, ?, ?, ?)', 
                    (username, password, first_name, last_name))
    db.commit()
    db.close()


def user_exists(db, username):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    return user is not None


def get_user(db, username):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    db.close()
    return user


def get_all(db):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    db.close()
    return users
