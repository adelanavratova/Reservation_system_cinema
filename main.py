import tkinter as tk
from admin_management import *
from user_management import *
from login_management import *
import database.database_manager as dbm

WINDOW_SIZE = '500x350'
MIN_WIDTH = '500'
MIN_HEIGHT = '350'


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        dbm.init_db()
        dbm.init_default_data()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int((screen_width - int(MIN_WIDTH)) / 2)
        center_y = int((screen_height - int(MIN_HEIGHT)) / 2)
        self.geometry(f"+{center_x}+{center_y}")

        self.title("Přihlášení")
        self.resizable(width=False, height=False)
        self.geometry(WINDOW_SIZE)

        self.user_screen = UserScreen(self)
        self.admin_screen = AdminScreen(self)

        self.new_reservation_screen = NewReservationScreen(self)
        self.my_reservation_screen = MyReservationScreen(self)
        self.rating_screen = RatingScreen(self)

        self.all_reservations_screen = AllReservationsScreen(self)
        self.add_film_screen = AddFilmScreen(self)
        self.all_rating_screen = AllRatingScreen(self)

        self.login_screen = LoginScreen(self)
        self.registration_screen = RegistrationScreen(self)

        self.login_screen.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()
