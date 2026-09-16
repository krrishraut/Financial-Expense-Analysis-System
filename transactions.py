import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import connect_database


def open_transactions(user_id, dashboard, refresh_dashboard):

    transaction_window = tk.Toplevel(dashboard)

    dashboard.withdraw()

    transaction_window.title("Transaction Management")
    transaction_window.geometry("1100x650")
    transaction_window.resizable(False, False)
    transaction_window.configure(bg="#f4f6f8")

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------

    title = tk.Label(
        transaction_window,
        text="Transaction Management",
        font=("Arial", 24, "bold"),
        bg="#f4f6f8"
    )

    title.pack(pady=(25, 5))

    subtitle = tk.Label(
        transaction_window,
        text="Add, view, update and delete your financial transactions",
        font=("Arial", 11),
        bg="#f4f6f8"
    )

    subtitle.pack(pady=(0, 20))

    # -------------------------------------------------
    # INPUT FRAME
    # -------------------------------------------------

    input_frame = tk.Frame(
        transaction_window,
        bg="white",
        bd=1,
        relief="solid"
    )

    input_frame.pack(padx=30, fill="x")

    # Date
    tk.Label(
        input_frame,
        text="Date",
        font=("Arial", 11),
        bg="white"
    ).grid(row=0, column=0, padx=15, pady=(20, 5), sticky="w")

    date_entry = tk.Entry(
        input_frame,
        font=("Arial", 11),
        width=18
    )

    date_entry.grid(row=1, column=0, padx=15, pady=(0, 20))

    date_entry.insert(
        0,
        datetime.now().strftime("%Y-%m-%d")
    )

    # Type
    tk.Label(
        input_frame,
        text="Type",
        font=("Arial", 11),
        bg="white"
    ).grid(row=0, column=1, padx=15, pady=(20, 5), sticky="w")

    type_combo = ttk.Combobox(
        input_frame,
        values=["Income", "Expense"],
        font=("Arial", 11),
        width=16,
        state="readonly"
    )

    type_combo.grid(row=1, column=1, padx=15, pady=(0, 20))
    type_combo.set("Expense")

    # Category
    tk.Label(
        input_frame,
        text="Category",
        font=("Arial", 11),
        bg="white"
    ).grid(row=0, column=2, padx=15, pady=(20, 5), sticky="w")

    category_combo = ttk.Combobox(
        input_frame,
        values=[
            "Salary",
            "Food",
            "Travel",
            "Shopping",
            "Bills",
            "Education",
            "Health",
            "Entertainment",
            "Rent",
            "Other"
        ],
        font=("Arial", 11),
        width=16
    )

    category_combo.grid(row=1, column=2, padx=15, pady=(0, 20))

    # Amount
    tk.Label(
        input_frame,
        text="Amount",
        font=("Arial", 11),
        bg="white"
    ).grid(row=0, column=3, padx=15, pady=(20, 5), sticky="w")

    amount_entry = tk.Entry(
        input_frame,
        font=("Arial", 11),
        width=18
    )

    amount_entry.grid(row=1, column=3, padx=15, pady=(0, 20))

    # Payment Method
    tk.Label(
        input_frame,
        text="Payment Method",
        font=("Arial", 11),
        bg="white"
    ).grid(row=0, column=4, padx=15, pady=(20, 5), sticky="w")

    payment_combo = ttk.Combobox(
        input_frame,
        values=[
            "Cash",
            "UPI",
            "Card",
            "Bank"
        ],
        font=("Arial", 11),
        width=15,
        state="readonly"
    )

    payment_combo.grid(row=1, column=4, padx=15, pady=(0, 20))
    payment_combo.set("UPI")

    # -------------------------------------------------
    # BUTTONS
    # -------------------------------------------------

    button_frame = tk.Frame(
        transaction_window,
        bg="#f4f6f8"
    )

    button_frame.pack(pady=15)

    def go_back():

        transaction_window.destroy()

        dashboard.deiconify()
    
        refresh_dashboard()


    back_button = tk.Button(
        button_frame,
        text="BACK",
        font=("Arial", 10, "bold"),
        width=12,
        command=go_back
    )

    back_button.grid(row=0, column=5, padx=8)

    # -------------------------------------------------
    # TREEVIEW
    # -------------------------------------------------

    table_frame = tk.Frame(
        transaction_window,
        bg="white"
    )

    table_frame.pack(
        padx=30,
        fill="both",
        expand=True
    )

    columns = (
        "ID",
        "Date",
        "Type",
        "Category",
        "Amount",
        "Payment"
    )

    transaction_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=13
    )

    transaction_table.heading("ID", text="ID")
    transaction_table.heading("Date", text="Date")
    transaction_table.heading("Type", text="Type")
    transaction_table.heading("Category", text="Category")
    transaction_table.heading("Amount", text="Amount")
    transaction_table.heading("Payment", text="Payment Method")

    transaction_table.column("ID", width=60, anchor="center")
    transaction_table.column("Date", width=130, anchor="center")
    transaction_table.column("Type", width=120, anchor="center")
    transaction_table.column("Category", width=150, anchor="center")
    transaction_table.column("Amount", width=140, anchor="center")
    transaction_table.column("Payment", width=170, anchor="center")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=transaction_table.yview
    )

    transaction_table.configure(
        yscrollcommand=scrollbar.set
    )

    transaction_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # -------------------------------------------------
    # LOAD TRANSACTIONS
    # -------------------------------------------------

    def load_transactions():

        for item in transaction_table.get_children():
            transaction_table.delete(item)

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
        SELECT
            transaction_id,
            transaction_date,
            transaction_type,
            category,
            amount,
            payment_method
        FROM transactions
        WHERE user_id = %s
        ORDER BY transaction_date DESC, transaction_id DESC
        """

        cursor.execute(query, (user_id,))

        records = cursor.fetchall()

        for record in records:

            transaction_table.insert(
                "",
                "end",
                values=(
                    record[0],
                    record[1],
                    record[2],
                    record[3],
                    "₹ " + format(float(record[4]), ",.2f"),
                    record[5]
                )
            )

        cursor.close()
        connection.close()

    # -------------------------------------------------
    # CLEAR INPUTS
    # -------------------------------------------------

    def clear_fields():

        date_entry.delete(0, tk.END)
        date_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        type_combo.set("Expense")
        category_combo.set("")
        amount_entry.delete(0, tk.END)
        payment_combo.set("UPI")

    # -------------------------------------------------
    # ADD TRANSACTION
    # -------------------------------------------------

    def add_transaction():

        transaction_date = date_entry.get().strip()
        transaction_type = type_combo.get()
        category = category_combo.get().strip()
        amount = amount_entry.get().strip()
        payment_method = payment_combo.get()

        if (
            transaction_date == ""
            or transaction_type == ""
            or category == ""
            or amount == ""
            or payment_method == ""
        ):
            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        try:

            datetime.strptime(
                transaction_date,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Date",
                "Date must be in YYYY-MM-DD format."
            )
            return

        try:

            amount_value = float(amount)

            if amount_value <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid amount greater than 0."
            )
            return

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
        INSERT INTO transactions
        (
            user_id,
            transaction_date,
            transaction_type,
            category,
            amount,
            payment_method
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            user_id,
            transaction_date,
            transaction_type,
            category,
            amount_value,
            payment_method
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Transaction added successfully."
        )

        clear_fields()
        load_transactions()

    # -------------------------------------------------
    # SELECT TRANSACTION
    # -------------------------------------------------

    def select_transaction(event):

        selected = transaction_table.selection()

        if not selected:
            return

        values = transaction_table.item(
            selected[0],
            "values"
        )

        date_entry.delete(0, tk.END)
        date_entry.insert(0, values[1])

        type_combo.set(values[2])
        category_combo.set(values[3])

        amount_entry.delete(0, tk.END)

        amount = values[4].replace("₹ ", "").replace(",", "")

        amount_entry.insert(0, amount)

        payment_combo.set(values[5])

    # -------------------------------------------------
    # UPDATE TRANSACTION
    # -------------------------------------------------

    def update_transaction():

        selected = transaction_table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Transaction",
                "Please select a transaction to update."
            )
            return

        transaction_id = transaction_table.item(
            selected[0],
            "values"
        )[0]

        transaction_date = date_entry.get().strip()
        transaction_type = type_combo.get()
        category = category_combo.get().strip()
        amount = amount_entry.get().strip()
        payment_method = payment_combo.get()

        if (
            transaction_date == ""
            or transaction_type == ""
            or category == ""
            or amount == ""
            or payment_method == ""
        ):
            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        try:

            datetime.strptime(
                transaction_date,
                "%Y-%m-%d"
            )

            amount_value = float(amount)

            if amount_value <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Data",
                "Please enter valid date and amount."
            )
            return

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
        UPDATE transactions
        SET
            transaction_date = %s,
            transaction_type = %s,
            category = %s,
            amount = %s,
            payment_method = %s
        WHERE transaction_id = %s
        AND user_id = %s
        """

        values = (
            transaction_date,
            transaction_type,
            category,
            amount_value,
            payment_method,
            transaction_id,
            user_id
        )

        cursor.execute(query, values)

        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Transaction updated successfully."
        )

        clear_fields()
        load_transactions()

    # -------------------------------------------------
    # DELETE TRANSACTION
    # -------------------------------------------------

    def delete_transaction():

        selected = transaction_table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Transaction",
                "Please select a transaction to delete."
            )
            return

        transaction_id = transaction_table.item(
            selected[0],
            "values"
        )[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this transaction?"
        )

        if not confirm:
            return

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
        DELETE FROM transactions
        WHERE transaction_id = %s
        AND user_id = %s
        """

        cursor.execute(
            query,
            (transaction_id, user_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Transaction deleted successfully."
        )

        clear_fields()
        load_transactions()

    # -------------------------------------------------
    # BUTTONS
    # -------------------------------------------------

    add_button = tk.Button(
        button_frame,
        text="ADD TRANSACTION",
        font=("Arial", 10, "bold"),
        width=18,
        command=add_transaction
    )

    add_button.grid(row=0, column=0, padx=8)

    update_button = tk.Button(
        button_frame,
        text="UPDATE",
        font=("Arial", 10, "bold"),
        width=12,
        command=update_transaction
    )

    update_button.grid(row=0, column=1, padx=8)

    delete_button = tk.Button(
        button_frame,
        text="DELETE",
        font=("Arial", 10, "bold"),
        width=12,
        command=delete_transaction
    )

    delete_button.grid(row=0, column=2, padx=8)

    clear_button = tk.Button(
        button_frame,
        text="CLEAR",
        font=("Arial", 10, "bold"),
        width=12,
        command=clear_fields
    )

    clear_button.grid(row=0, column=3, padx=8)

    refresh_button = tk.Button(
        button_frame,
        text="REFRESH",
        font=("Arial", 10, "bold"),
        width=12,
        command=load_transactions
    )

    refresh_button.grid(row=0, column=4, padx=8)

    # -------------------------------------------------
    # TABLE SELECTION
    # -------------------------------------------------

    transaction_table.bind(
        "<<TreeviewSelect>>",
        select_transaction
    )

    # Load existing transactions
    load_transactions()
