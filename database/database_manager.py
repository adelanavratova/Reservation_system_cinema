import sqlite3
import database.user as user
import database.reservation as reservation
import database.screening as screening
import database.film as film
import database.rating as rating

DATABASE = "cinema.db"
ADMINS = [("admin", "admin")]


def connect_db():
    return sqlite3.connect(DATABASE)


def init_db():
    db = connect_db()

    user.init_table(db)
    reservation.init_table(db)
    screening.init_table(db)
    film.init_table(db)
    rating.init_table(db)

    db.close()


# USER
def add_user(username, password, first_name, last_name):
    db = connect_db()
    user.add_user(db, username, password, first_name, last_name)


def get_user(username):
    db = connect_db()
    return user.get_user(db, username)


def user_exists(username):
    db = connect_db()
    return user.user_exists(db, username)


def get_all_users():
    db = connect_db()
    return user.get_all(db)
# ---------


# RESERVATION
def add_reservation(user_id, screening_id, number_of_seats):
    db = connect_db()
    reservation.add_reservation(db, user_id, screening_id, number_of_seats)


def get_reservation_for_user(user_id):
    db = connect_db()
    return reservation.get_reservation_for_user(db, user_id)


def delete_reservation(reservation_id):
    db = connect_db()
    reservation.delete_reservation(db, reservation_id)
# ---------


# SCREENING
def add_screening(datetime, film_id, available_seats):
    db = connect_db()
    screening.add_screening(db, datetime, film_id, available_seats)


def get_screening(screening_id):
    db = connect_db()
    return screening.get_screening(db, screening_id)


def get_all_screenings():
    db = connect_db()
    return screening.get_all(db)


def get_screening_for_film(film_id):
    db = connect_db()
    return screening.get_screening_for_film(db, film_id)


def subtract_seats(screening_id, number_of_seats):
    db = connect_db()
    screening.subtract_seats(db, screening_id, number_of_seats)


def get_seats_for_screening(screening_id):
    db = connect_db()
    return screening.get_seats_for_screening(db, screening_id)


def get_screening_by_data(datetime, film_id):
    db = connect_db()
    return screening.get_screening_by_data(db, datetime, film_id)
# ---------


# FILM
def add_film(title, kind):
    db = connect_db()
    film.add_film(db, title, kind)


def get_film(film_id):
    db = connect_db()
    return film.get_film(db, film_id)


def get_all_films():
    db = connect_db()
    return film.get_all(db)


def film_exists(film_title):
    db = connect_db()
    return film.film_exists(db, film_title)


def get_film_by_title(film_title):
    db = connect_db()
    return film.get_film_by_title(db, film_title)
# ---------


# RATING
def add_rating(film_id, user_id, comment):
    db = connect_db()
    rating.add_rating(db, film_id, user_id, comment)


def get_all_ratings():
    db = connect_db()
    return rating.get_all(db)


def get_rating_for_user(user_id):
    db = connect_db()
    return rating.get_rating_for_user(db, user_id)


def delete_rating(rating_id):
    db = connect_db()
    return rating.delete_rating(db, rating_id)
# ---------


def init_default_data():
    init_admin()
    init_default_users()
    init_default_films()
    init_default_screenings()
    init_default_rating()
    init_default_reservation()


def init_admin():
    for name, password in ADMINS:
        if get_user(name) is None:
            add_user(name, password, "_", "_")


def is_admin(name):
    for admin_name, _ in ADMINS:
        if admin_name == name:
            return True
    return False


def init_default_users():
    users = [
        ('Kedluben007', '123', 'John', 'Snow'),
        ('MoonRocket', 'rocket123', 'Bob', 'King')
    ]

    for user_name, password, first_name, last_name in users:
        if get_user(user_name) is None:
            add_user(user_name, password, first_name, last_name)


def init_default_films():
    films = [
        ('Interstellar', 'Sci-Fi'),
        ('Inception', 'Action'),
        ('The Dark Knight', 'Action')
    ]

    for new_title, new_kind in films:
        found = False
        for _,  title, kind in get_all_films():
            if new_title == title and new_kind == kind:
                found = True

        if not found:
            add_film(new_title, new_kind)


def init_default_screenings():
    screenings = [
        ('2024-04-01 20:00', 1, 50),
        ('2024-04-02 20:00', 2, 50),
        ('2024-04-03 20:00', 3, 50),
        ('2024-04-20 16:00', 2, 50),
        ('2024-04-21 20:00', 2, 50),
        ('2024-04-21 22:00', 1, 50),
        ('2024-04-22 12:00', 2, 50),
        ('2024-04-22 14:00', 3, 50)
    ]

    for new_datetime, new_film_id, new_available_seats in screenings:
        found = False
        for _, datetime, film_id, available_seats in get_all_screenings():
            if new_datetime == datetime and new_film_id == film_id and \
                    new_available_seats == available_seats:
                found = True

        if not found:
            add_screening(new_datetime, new_film_id, new_available_seats)


def init_default_rating():
    ratings = [
        (1, 2, "Good"),
        (2, 2, "Not good"),
        (3, 3, "Bad")
    ]

    for new_film_id, new_user_id, new_comment in ratings:
        found = False
        for _, film_id, user_id, comment in get_all_ratings():
            if new_film_id == film_id and new_user_id == user_id and \
                    new_comment == comment:
                found = True

        if not found:
            add_rating(new_film_id, new_user_id, new_comment)


def init_default_reservation():
    reservations = [
        (2, 1, 2),
        (3, 2, 1),
        (3, 3, 3)
    ]

    for new_user_id, new_screening_id, new_number_of_seats in reservations:
        found = False
        for user_id, _, _, _, _ in get_all_users():
            for _, _, screening_id, number_of_seats in get_reservation_for_user(user_id):
                if new_user_id == user_id and new_screening_id == screening_id and \
                        new_number_of_seats == number_of_seats:
                    found = True

        if not found:
            add_reservation(new_user_id, new_screening_id, new_number_of_seats)
