import tkinter as tk
from tkinter import messagebox
import database.database_manager as dbm
from tkinter import font as tkfont

WINDOW_SIZE = '500x350'
MIN_WIDTH = '500'
MIN_HEIGHT = '350'


class LoginScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.config(padx=20, pady=50)
        custom_font = tkfont.Font(family="Helvetica", size=12)

        self.username_label = tk.Label(self, text="Uživatelské jméno:", font=custom_font)
        self.username_label.pack()

        self.username_input = tk.Entry(self, font=custom_font, highlightthickness=2, highlightbackground='black')
        self.username_input.pack(pady=(0, 10))

        self.password_label = tk.Label(self, text="Uživatelské heslo:", font=custom_font)
        self.password_label.pack()

        self.password_input = tk.Entry(self, show="*", font=custom_font, highlightthickness=2, highlightbackground='black')
        self.password_input.pack(pady=(0, 10))

        btn_1 = tk.Button(self, text="Přihlásit", command=self.login, font=custom_font)
        btn_1.pack(side="left")
        btn_2 = tk.Button(self, text="Registrovat", command=self.show_registration, font=custom_font)
        btn_2.pack(side="right")

    def clear_entries(self):
        self.username_input.delete(0, tk.END)
        self.password_input.delete(0, tk.END)    

    def login(self):
        user_name = self.username_input.get()
        password = self.password_input.get()
        self.clear_entries()

        if not self.is_inputs_valid(user_name, password):
            return

        if not self.user_exists(user_name):
            tk.messagebox.showinfo("Login info", "Uživatel neexistuje")
            return

        if not self.password_valid(user_name, password):
            tk.messagebox.showinfo("Login info", "Špatné heslo")
            return

        if self.is_admin(user_name):
            self.show_admin()
        else:
            self.master.my_reservation_screen.user_name = user_name
            self.master.my_reservation_screen.create_my_reservations_display()

            self.master.new_reservation_screen.user_name = user_name
            self.master.new_reservation_screen.create_widgets()

            self.master.rating_screen.user_name = user_name
            self.master.rating_screen.create_widgets()

            self.show_user()

    def is_inputs_valid(self, user_name, password):
        if user_name == "":
            tk.messagebox.showinfo("Login info", "Nezadané uživatelské jméno")
            return False

        if password == "":
            tk.messagebox.showinfo("Login info", "Nezadané heslo")
            return False
        return True

    def user_exists(self, user_name):
        return dbm.user_exists(user_name)

    def is_admin(self, user_name):
        return dbm.is_admin(user_name)

    def password_valid(self, user_name, password):
        _, _, actual_password, _, _ = dbm.get_user(user_name)
        return password == actual_password

    def show_user(self):
        self.master.title("Uživatel")
        self.pack_forget()
        self.master.user_screen.pack()

    def show_admin(self):
        self.master.title("Administrátor")
        self.pack_forget()
        self.master.admin_screen.pack()
        self.clear_entries()

    def show_registration(self):
        self.master.title("Registrace")
        self.pack_forget()
        self.master.registration_screen.pack()
        self.clear_entries()


class RegistrationScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        custom_font = tkfont.Font(family="Helvetica", size=12)

        self.first_name = tk.Label(self, text="Jméno:", font=custom_font)
        self.first_name.pack()

        self.first_name_input = tk.Entry(self, font=custom_font, highlightthickness=2, highlightbackground='black')
        self.first_name_input.pack(pady=(0, 10))

        self.last_name = tk.Label(self, text="Příjmení:", font=custom_font)
        self.last_name.pack()

        self.last_name_input = tk.Entry(self, font=custom_font, highlightthickness=2, highlightbackground='black')
        self.last_name_input.pack(pady=(0, 10))

        self.username_label = tk.Label(self, text="Nové uživatelské jméno:", font=custom_font)
        self.username_label.pack()

        self.username_input = tk.Entry(self, font=custom_font, highlightthickness=2, highlightbackground='black')
        self.username_input.pack(pady=(0, 10))

        self.password_label = tk.Label(self, text="Nové heslo:", font=custom_font)
        self.password_label.pack()

        self.password_input = tk.Entry(self, show="*", font=custom_font, highlightthickness=2, highlightbackground='black')
        self.password_input.pack(pady=(0, 10))

        self.password_label_second = tk.Label(self, text="Heslo znovu:", font=custom_font)
        self.password_label_second.pack()

        self.password_input_second = tk.Entry(self, show="*", font=custom_font, highlightthickness=2, highlightbackground='black')
        self.password_input_second.pack(pady=(0, 10))

        login_btn = tk.Button(self, text="Zrušit", command=self.show_login, font=custom_font)
        login_btn.pack(side="left")

        register_btn = tk.Button(self, text="Registrovat", command=self.register, font=custom_font)
        register_btn.pack(side="right")

    def clear_entries(self):
        self.first_name_input.delete(0, tk.END)
        self.last_name_input.delete(0, tk.END)
        self.username_input.delete(0, tk.END)
        self.password_input_second.delete(0, tk.END)
        self.password_input.delete(0, tk.END)

    def show_login(self):
        self.master.title("Přihlášení")
        self.pack_forget()
        self.master.login_screen.pack()
        self.clear_entries()

    def register(self):
        user_name = self.username_input.get()
        password = self.password_input.get()
        password_second = self.password_input_second.get()

        first_name = self.first_name_input.get()
        last_name = self.last_name_input.get()

        self.clear_entries()

        if not self.is_inputs_valid(user_name, password, password_second):
            return

        dbm.add_user(user_name, password, first_name, last_name)
        self.show_login()

    def is_inputs_valid(self, user_name, password, password_second):
        if user_name == "":
            tk.messagebox.showinfo("Login info", "Neuvedené žádné uživatelské jméno")
            return False

        if password == "":
            tk.messagebox.showinfo("Login info", "Neuvedené žádné heslo")
            return False

        if password != password_second:
            tk.messagebox.showinfo("Login info", "Hesla se neshodují")
            return False

        return True
