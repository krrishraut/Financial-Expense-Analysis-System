import tkinter as tk
from tkinter import messagebox
from database import connect_database
from dashboard import open_dashboard

def signup():
    signup_window = tk.Toplevel(login_window)

    signup_window.title("Create Account")
    signup_window.geometry("450x400")
    signup_window.resizable(False, False)
    signup_window.configure(bg="#f4f6f8")

    title = tk.Label(
        signup_window,
        text="Create New Account",
        font=("Arial", 22, "bold"),
        bg="#f4f6f8"
    )
    title.pack(pady=(40, 35))

    # Username
    username_label = tk.Label(
        signup_window,
        text="Username",
        font=("Arial", 12),
        bg="#f4f6f8"
    )
    username_label.place(x=65, y=130)

    username_entry = tk.Entry(
        signup_window,
        font=("Arial", 12),
        width=25
    )
    username_entry.place(x=180, y=125)

    # Password
    password_label = tk.Label(
        signup_window,
        text="Password",
        font=("Arial", 12),
        bg="#f4f6f8"
    )
    password_label.place(x=65, y=190)

    password_entry = tk.Entry(
        signup_window,
        font=("Arial", 12),
        width=25,
        show="*"
    )
    password_entry.place(x=180, y=185)

    # Confirm Password
    confirm_label = tk.Label(
        signup_window,
        text="Confirm",
        font=("Arial", 12),
        bg="#f4f6f8"
    )
    confirm_label.place(x=65, y=250)

    confirm_entry = tk.Entry(
        signup_window,
        font=("Arial", 12),
        width=25,
        show="*"
    )
    confirm_entry.place(x=180, y=245)

    def register_user():

        username = username_entry.get()
        password = password_entry.get()
        confirm_password = confirm_entry.get()

        if username == "" or password == "" or confirm_password == "":
            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        if password != confirm_password:
            messagebox.showerror(
                "Password Error",
                "Passwords do not match."
            )
            return

        connection = connect_database()

        if connection is None:
            messagebox.showerror(
                "Database Error",
                "Unable to connect to MySQL."
            )
            return

        cursor = connection.cursor()

        try:

            query = """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            """

            values = (username, password)

            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo(
                "Registration Successful",
                "Account created successfully."
            )

            signup_window.destroy()

        except Exception as error:

            if "Duplicate entry" in str(error):
                messagebox.showerror(
                    "Username Exists",
                    "This username is already registered."
                )
            else:
                messagebox.showerror(
                    "Registration Error",
                    str(error)
                )

        finally:
            cursor.close()
            connection.close()

    signup_button = tk.Button(
        signup_window,
        text="CREATE ACCOUNT",
        font=("Arial", 11, "bold"),
        width=20,
        command=register_user
    )

    signup_button.place(x=145, y=310)

def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showwarning(
            "Missing Information",
            "Please enter username and password."
        )
        return

    connection = connect_database()

    if connection is None:
        messagebox.showerror(
            "Database Error",
            "Unable to connect to MySQL."
        )
        return

    cursor = connection.cursor()

    query = """
    SELECT user_id, username
    FROM users
    WHERE username = %s AND password = %s
    """

    values = (username, password)

    cursor.execute(query, values)

    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        messagebox.showinfo(
            "Login Successful",
            "Welcome, " + user[1]
        )

        login_window.withdraw()

        open_dashboard(user[0], user[1])

    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )



# ---------------- LOGIN WINDOW ----------------

login_window = tk.Tk()

login_window.title("Financial Expense Analysis System - Login")
login_window.geometry("700x500")
login_window.resizable(False, False)
login_window.configure(bg="#f4f6f8")


title_label = tk.Label(
    login_window,
    text="Financial Expense",
    font=("Arial", 30, "bold"),
    bg="#f4f6f8"
)

title_label.pack(pady=(40, 5))


subtitle_label = tk.Label(
    login_window,
    text="Analysis System",
    font=("Arial", 24),
    bg="#f4f6f8"
)

subtitle_label.pack(pady=(0, 30))


# ---------------- LOGIN FORM ----------------

# Username
username_label = tk.Label(
    login_window,
    text="Username",
    font=("Arial", 12),
    bg="#f4f6f8"
)
username_label.place(x=162, y=265)

username_entry = tk.Entry(
    login_window,
    font=("Arial", 12),
    width=30
)
username_entry.place(x=300, y=265)


# Password
password_label = tk.Label(
    login_window,
    text="Password",
    font=("Arial", 12),
    bg="#f4f6f8"
)
password_label.place(x=162, y=323)

password_entry = tk.Entry(
    login_window,
    font=("Arial", 12),
    width=30,
    show="*"
)
password_entry.place(x=300, y=323)


# Login Button
login_button = tk.Button(
    login_window,
    text="LOGIN",
    font=("Arial", 12, "bold"),
    width=20,
    command=login
)
login_button.place(x=250, y=380)

signup_button = tk.Button(
    login_window,
    text="SIGN UP",
    font=("Arial", 12, "bold"),
    width=20,
    command=signup
)

signup_button.place(x=250, y=420)


login_window.mainloop()


