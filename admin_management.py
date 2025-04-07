import datetime
import re
import tkinter as tk
from tkinter import messagebox
from scrollable import ScrollableFrame
import database.database_manager as dbm
from tkinter import font as tkfont



class AdminScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        custom_font = tkfont.Font(family="Helvetica", size=12)

        btn3 = tk.Button(self, text="Přidat nové promítání", command=self.show_add_film, font=custom_font)
        btn3.pack(padx=10, pady=(40, 10))
        
        btn2 = tk.Button(self, text="Zobrazit všechny rezervace", command=self.show_all_reservation, font=custom_font)
        btn2.pack(padx=10, pady=10)
        btn4 = tk.Button(self, text="Zobrazit všechny hodnocení", command=self.show_all_rating, font=custom_font)
        btn4.pack(padx=10, pady=10)

        btn1 = tk.Button(self, text="Odhlásit", command=self.show_login, font=custom_font)
        btn1.pack(padx=10, pady=10)

    def show_login(self):
        self.master.title("Přihlášení")
        self.pack_forget()
        self.master.login_screen.pack()

    def show_all_reservation(self):
        self.master.title("Zobrazení všech rezervací")
        self.pack_forget()
        self.master.all_reservations_screen.create_reservations_display()
        self.master.all_reservations_screen.pack()

    def show_add_film(self):
        self.master.title("Přidání nového filmu")
        self.pack_forget()
        self.master.add_film_screen.pack()

    def show_all_rating(self):
        self.master.title("Zobrazení všech hodnocení")
        self.pack_forget()
        self.master.all_rating_screen.create_ratings_display()
        self.master.all_rating_screen.pack()


class AllReservationsScreen(ScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_reservations_display()
        custom_font = tkfont.Font(family="Helvetica", size=12)

        btn = tk.Button(self, text="Zpět", command=self.show_admin, font=custom_font)
        btn.pack()

    def clear_reservations_display(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def create_reservations_display(self):
        self.config(pady=10)
        self.clear_reservations_display()
        custom_font = tkfont.Font(family="Helvetica", size=12)
        
        for user_id, user_name, _, first_name, last_name in dbm.get_all_users():
            if(dbm.get_reservation_for_user(user_id) == []):
                continue
            user_frame = tk.LabelFrame(self.frame, text=f"{first_name} {last_name} ({user_name})", padx=10, pady=10, font=custom_font)
            user_frame.pack(fill="x", padx=5, pady=5, expand=True)

            for reservation_id, _, screening_id, number_of_seats in dbm.get_reservation_for_user(user_id):
                _, datetime, film_id, _ = dbm.get_screening(screening_id)
                _, film_title, _ = dbm.get_film(film_id)

                res_frame = tk.Frame(user_frame, borderwidth=2, relief="groove")
                res_frame.pack(fill="x", pady=5, expand=True)

                tk.Label(res_frame, text=film_title, font=custom_font).pack(side="top", anchor="w")
                tk.Label(res_frame, text=f"Datum: {datetime}", font=custom_font).pack(side="top", anchor="w")
                tk.Label(res_frame, text=f"Počet lidí: {number_of_seats}", font=custom_font).pack(side="top", anchor="w")

                cancel_button = tk.Button(res_frame, text="Zrušit",
                                          command=lambda r_id=reservation_id: self.delete_reservation(r_id), font=custom_font)
                cancel_button.pack(side="right")

    def show_admin(self):
        self.master.title("Administrátor")
        self.pack_forget()
        self.master.admin_screen.pack()

    def delete_reservation(self, reservation_id):
        dbm.delete_reservation(reservation_id)
        self.create_reservations_display()


class AddFilmScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_add_film_display()

    def create_add_film_display(self):
        self.clear_add_film_display()
        custom_font = tkfont.Font(family="Helvetica", size=12)

        tk.Label(self, text="Přidat film (žánr):", font=custom_font).pack()
        self.film_name_entry = tk.Entry(self, font=custom_font, highlightthickness=2, highlightbackground='black')
        self.film_name_entry.pack(pady=(0, 5))

        tk.Label(self, text="Datum:", font=custom_font).pack()
        self.date_entry = tk.Entry(self, font=custom_font, highlightthickness=2, highlightbackground='black')
        self.date_entry.pack(pady=(0, 5))

        tk.Label(self, text="Počet míst:", font=custom_font).pack()
        self.seats_entry = tk.Entry(self, font=custom_font, highlightthickness=2, highlightbackground='black')
        self.seats_entry.pack(pady=(0, 5))

        tk.Label(self, text="Aktuální filmy:", font=custom_font).pack()

        self.scroll_frame = tk.Frame(self, highlightbackground="black", highlightcolor="black", highlightthickness=1, bd=0)
        self.scroll_frame.pack(fill="both", expand=True, pady=(0,5))

        self.current_films_frame = ScrollableFrame(self.scroll_frame)
        self.current_films_frame.canvas.config(width=300, height=100)

        for _, datetime, film_id, _ in dbm.get_all_screenings():
           _, film_title, _ = dbm.get_film(film_id)
           tk.Label(self.current_films_frame.frame, text=f"{film_title}: {datetime}", font=custom_font).pack()
        self.current_films_frame.pack()

        tk.Button(self, text="Zrušit", command=self.show_admin, font=custom_font).pack(side="left",pady=(0,5))

        tk.Button(self, text="Potvrdit", command=self.save_data, font=custom_font).pack(side="right", pady=(0,5))

    def show_admin(self):
        self.master.title("Administrátor")
        self.pack_forget()
        self.master.admin_screen.pack()
        self.clear_entries()

    def clear_entries(self):
        self.film_name_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.seats_entry.delete(0, tk.END)

    def clear_add_film_display(self):
        for widget in self.winfo_children():
            widget.destroy()

    def save_data(self):
        try:
            film_title, film_kind = self.get_film_data()
        except ValueError:
            messagebox.showerror("Chybný formát", "Řetězec neodpovídá očekávanému formátu.")
            self.film_name_entry.delete(0, tk.END)
            return

        try:
            datetime = self.get_datetime()
        except ValueError:
            messagebox.showerror("Chybný formát", "Datum a čas musí být ve formátu RRRR-MM-DD HH:MM.")
            self.date_entry.delete(0, tk.END)
            return

        try:
            avail_seats = self.get_seats()
        except ValueError:
            messagebox.showerror("Chybný formát", "Počet míst neodpovídá očekávanému formátu.")
            self.seats_entry.delete(0, tk.END)
            return

        if not dbm.film_exists(film_title):
            dbm.add_film(film_title, film_kind)

        film_id, _, _ = dbm.get_film_by_title(film_title)

        result = dbm.get_screening_by_data(datetime, film_id)
        if result:
            messagebox.showerror("Chyba", "Toto promítání už existuje")
            return

        dbm.add_screening(datetime, film_id, avail_seats)

        self.create_add_film_display()

    def get_datetime(self):
        input_datetime = self.date_entry.get().strip()
        try:
            valid_datetime = datetime.datetime.strptime(input_datetime, "%Y-%m-%d %H:%M")
            formatted_datetime = valid_datetime.strftime("%Y-%m-%d %H:%M")
            return formatted_datetime
        except ValueError:
            raise ValueError("Datum a čas musí být ve formátu RRRR-MM-DD HH:MM.")

    def get_film_data(self):
        match = re.match(r"(.*) \((.+)\)", self.film_name_entry.get())
        if match:
            return (match.group(1), match.group(2))
        else:
            raise ValueError("Řetězec neodpovídá očekávanému formátu.")

    def get_seats(self):
        avail_seats = self.seats_entry.get().strip()
        try:
            seats_number = int(avail_seats)
            if seats_number >= 0:
                return seats_number
            else:
                raise ValueError("Počet míst musí být nezáporné číslo.")
        except ValueError as e:
            raise ValueError("Chyba", str(e))


class AllRatingScreen(ScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_ratings_display()

        custom_font = tkfont.Font(family="Helvetica", size=12)
        btn = tk.Button(self, text="Zpět", font=custom_font, command=self.show_admin)
        btn.pack()

    def show_admin(self):
        self.master.title("Administrátor")
        self.pack_forget()
        self.master.admin_screen.pack()

    def clear_ratings_display(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def create_ratings_display(self):
        self.clear_ratings_display()
        custom_font = tkfont.Font(family="Helvetica", size=12)

        for user_id, user_name, _, first_name, last_name in dbm.get_all_users():
            if(dbm.get_rating_for_user(user_id) == []):
                continue
            user_frame = tk.LabelFrame(self.frame, text=f"{first_name} {last_name} ({user_name})", padx=10, pady=10, font=custom_font)
            user_frame.pack(fill="x", padx=5, pady=5, expand=True)

            for rating_id, film_id, user_id, comment in dbm.get_rating_for_user(user_id):
                _, film_title, _ = dbm.get_film(film_id)

                res_frame = tk.Frame(user_frame, borderwidth=2, relief="groove")
                res_frame.pack(fill="x", pady=5, expand=True)

                tk.Label(res_frame, text=film_title, font=custom_font).pack(side="top", anchor="w")
                tk.Label(res_frame, text=comment, font=custom_font).pack(side="top", anchor="w")

                cancel_button = tk.Button(res_frame, text="Zrušit",
                                          command=lambda r_id=rating_id: self.delete_rating(r_id), font=custom_font)
                cancel_button.pack(side="right")

    def delete_rating(self, rating_id):
        dbm.delete_rating(rating_id)
        self.create_ratings_display()
