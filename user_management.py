import tkinter as tk
import database.database_manager as dbm
from tkinter import ttk
from tkinter import scrolledtext
from scrollable import ScrollableFrame
from tkinter import messagebox
from tkinter import font as tkfont


class UserScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        custom_font = tkfont.Font(family="Helvetica", size=12)
        
        btn4 = tk.Button(self, text="Zobrazit moje rezervace", font=custom_font, command=self.show_my_reservation)
        btn4.pack(padx=10, pady=(40, 10))

        btn2 = tk.Button(self, text="Vytvořit novou rezervaci", font=custom_font, command=self.show_new_reservation)
        btn2.pack(padx=10, pady=10)
        btn3 = tk.Button(self, text="Vytvořit nové hodnocení", font=custom_font, command=self.show_rating)
        btn3.pack(padx=10, pady=10)

        btn1 = tk.Button(self, text="Odhlásit", font=custom_font, command=self.show_login)
        btn1.pack(padx=10, pady=10)

    def show_login(self):
        self.master.title("Přihlášení")
        self.pack_forget()
        self.master.login_screen.pack()

    def show_new_reservation(self):
        self.master.title("Vytvoření nové rezervace")
        self.pack_forget()
        self.master.new_reservation_screen.pack()

    def show_rating(self):
        self.master.title("Vytvoření nového hodnocení")
        self.pack_forget()
        self.master.rating_screen.pack()

    def show_my_reservation(self):
        self.master.title("Zobrazení mých rezervací")
        self.pack_forget()
        self.master.my_reservation_screen.create_my_reservations_display()
        self.master.my_reservation_screen.pack()


class NewReservationScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.user_name = ""

    def create_widgets(self):
        custom_font = tkfont.Font(family="Helvetica", size=12)
        self.available_seats = tk.StringVar(value="Počet míst (0):")
        for widget in self.winfo_children():
            widget.destroy()

        user_label_frame = tk.Frame(self)
        user_label_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(user_label_frame, text=f"Uživatel: {self.user_name}", font=custom_font).pack(side="left", pady=(40,10))

        film_label_frame = tk.Frame(self)
        film_label_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(film_label_frame, text="Film:", font=custom_font).pack(side="left")
        self.film_combobox = ttk.Combobox(film_label_frame, state="readonly", font=custom_font)
        self.film_combobox.pack(side="left", expand=True)

        self.all_films = ["-- Select film --"]
        self.titles_all_films = []
        for _, name, type in dbm.get_all_films():
            new_string = name + " - " + type
            self.all_films.append(new_string)
            self.titles_all_films.append(name)

        self.film_combobox['values'] = self.all_films
        self.film_combobox.set("-- Select film --")
        self.film_combobox.bind('<<ComboboxSelected>>', self.on_film_select)

        date_label_frame = tk.Frame(self)
        date_label_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(date_label_frame, text="Datum:", font=custom_font).pack(side="left")
        self.date_combobox = ttk.Combobox(date_label_frame, state="readonly", font=custom_font)
        self.date_combobox.pack(side="left", expand=True)
        self.date_combobox.bind('<<ComboboxSelected>>', lambda e: self.show_avaible_seats())

        seats_label_frame = tk.Frame(self)
        seats_label_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(seats_label_frame, textvariable=self.available_seats, font=custom_font).pack(side="left")
        self.seats_entry = tk.Entry(seats_label_frame, font=custom_font, highlightthickness=2, highlightbackground='black')
        self.seats_entry.pack(side="left", expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(fill='x', padx=10, pady=10)
        tk.Button(button_frame, text="Zrušit", command=self.show_user, font=custom_font).pack(side="left", padx=5)
        tk.Button(button_frame, text="Potvrdit", command=self.make_reservation, font=custom_font).pack(side="left", padx=5)

    def show_avaible_seats(self):
        if self.date_combobox.get() == "-- Select date --":
            pocet_mist = 0
        else:
            for i in range(len(self.result)):
                if self.result[i] == self.date_combobox.get():
                    position = i
            screening_id = self.screning[position - 1]
            pocet_mist = dbm.get_seats_for_screening(screening_id)[0]
        self.available_seats.set(f"Počet míst ({pocet_mist}) :")

    def reset_new_reservation(self):
        self.film_combobox.set("-- Select film --")
        self.date_combobox.set("-- Select date --")
        self.date_combobox['values'] = ["-- Select date --"]
        self.seats_entry.delete(0, tk.END)
        self.available_seats.set("Počet míst (0):")

    def on_film_select(self, event=None):
        film = self.film_combobox.get()
        available_dates = self.get_dates_for_film(film)
        self.date_combobox['values'] = available_dates
        self.date_combobox.set(available_dates[0])

    def get_dates_for_film(self, film):
        for i in range(len(self.all_films)):
            if self.all_films[i] == film:
                position = i
                break
        self.result = ["-- Select date --"]
        self.screning = []
        id, _, _ = dbm.get_film_by_title(self.titles_all_films[position - 1])
        for id_screning, date, _, _ in dbm.get_screening_for_film(id):
            self.screning.append(id_screning)
            self.result.append(date)
        return self.result

    def show_user(self):
        self.pack_forget()
        self.master.user_screen.pack()
        self.reset_new_reservation()

    def make_reservation(self):
        user_id, _, _, _, _ = dbm.get_user(self.user_name)

        for i in range(len(self.result)):
            if self.result[i] == self.date_combobox.get():
                position = i
        screening_id = self.screning[position - 1]

        try:
            number_of_seats = self.get_seats()
        except ValueError:
            messagebox.showerror("Chybný formát", "Počet míst neodpovídá očekávanému formátu.")
            self.seats_entry.delete(0, tk.END)
            return

        try:
            dbm.subtract_seats(screening_id, number_of_seats)
        except ValueError:
            messagebox.showerror("Chyba", "Nedostatek volných míst")
            self.seats_entry.delete(0, tk.END)
            return

        dbm.add_reservation(user_id, screening_id, number_of_seats)
        self.reset_new_reservation()

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


class RatingScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

    def create_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        custom_font = tkfont.Font(family="Helvetica", size=12)
        user_label_frame = tk.Frame(self)
        user_label_frame.pack(fill='x', padx=10, pady=10)
        tk.Label(user_label_frame, text=f"Uživatel: {self.user_name}", font=custom_font).pack(side="left")

        self.all_films = ["-- Select film --"]
        self.id_all_films = []
        for id, name, type in dbm.get_all_films():
            new_string = name + " - " + type
            self.all_films.append(new_string)
            self.id_all_films.append(id)
        
        film_label_frame = tk.Frame(self)
        film_label_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(film_label_frame, text="Film:", font=custom_font).pack(side="left")
        self.film_combobox = ttk.Combobox(film_label_frame, state="readonly", values=self.all_films, height=5, font=custom_font)
        self.film_combobox.pack(side="left", fill='x', expand=True)
        self.film_combobox.set("-- Select film --")

        tk.Label(self, text="Zadejte své hodnocení filmu", font=custom_font).pack(padx=10, pady=(10, 0))
        self.rating_text = scrolledtext.ScrolledText(self, wrap=tk.WORD, height=5)
        self.rating_text.pack(padx=10, pady=10, fill='both', expand=True)
        self.rating_text.insert(tk.INSERT, "")

        button_frame = tk.Frame(self)
        button_frame.pack(fill='x', pady=10)
        tk.Button(button_frame, text="Zrušit", command=self.show_user, font=custom_font).pack(side="left", padx=10)
        tk.Button(button_frame, text="Potvrdit", command=self.confirm_rating, font=custom_font).pack(side="right", padx=10)

    def show_user(self):
        self.master.title("Uživatel")
        self.pack_forget()
        self.master.user_screen.pack()
        self.reset_new_rating()

    def confirm_rating(self):
        for i in range(len(self.all_films)):
            if self.all_films[i] == self.film_combobox.get():
                film_id = self.id_all_films[i - 1]
                break
        user_id, _, _, _, _ = dbm.get_user(self.user_name)
        rating_text = self.rating_text.get("1.0", tk.END)
        dbm.add_rating(film_id, user_id, rating_text)
        self.reset_new_rating()
    
    def reset_new_rating(self):
        self.film_combobox.set("-- Select film --")
        self.rating_text.delete("1.0", tk.END)


class MyReservationScreen(ScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.user_name = ""

        custom_font = tkfont.Font(family="Helvetica", size=12)
        btn = tk.Button(self, text="Zpět", font=custom_font, command=self.show_user)
        btn.pack()

    def clear_my_reservations_display(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def create_my_reservations_display(self):
        self.clear_my_reservations_display()
        custom_font = tkfont.Font(family="Helvetica", size=12)

        user_id, user_name, _, first_name, last_name = dbm.get_user(self.user_name)

        user_frame = tk.LabelFrame(self.frame, text=f"{first_name} {last_name} ({user_name})", padx=10, pady=10, font=custom_font)
        user_frame.pack(fill="x", padx=5, pady=5)

        for reservation_id, _, screening_id, number_of_seats in dbm.get_reservation_for_user(user_id):
            _, datetime, film_id, _ = dbm.get_screening(screening_id)
            _, film_title, _ = dbm.get_film(film_id)

            res_frame = tk.Frame(user_frame, borderwidth=2, relief="groove")
            res_frame.pack(fill="x", pady=5)

            tk.Label(res_frame, text=film_title, font=custom_font).pack(side="top", anchor="w")
            tk.Label(res_frame, text=f"Datum: {datetime}", font=custom_font).pack(side="top", anchor="w")
            tk.Label(res_frame, text=f"Pocet lidi: {number_of_seats}", font=custom_font).pack(side="top", anchor="w")

            cancel_button = tk.Button(res_frame, text="Zrušit",
                                        command=lambda r_id=reservation_id: self.delete_reservation(r_id), font=custom_font)
            cancel_button.pack(side="right")

    def show_user(self):
        self.master.title("Uživatel")
        self.pack_forget()
        self.master.user_screen.pack()

    def delete_reservation(self, reservation_id):
        dbm.delete_reservation(reservation_id)
        self.create_my_reservations_display()
