import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import connect_database


def open_budget(user_id, dashboard):

    budget_window = tk.Toplevel(dashboard)

    dashboard.withdraw()

    budget_window.title("Budget Management")
    budget_window.geometry("1100x700")
    budget_window.resizable(False, False)
    budget_window.configure(bg="#f4f6f8")

    # ================= TITLE =================

    title = tk.Label(
        budget_window,
        text="Budget Management",
        font=("Arial", 24, "bold"),
        bg="#f4f6f8"
    )
    title.pack(pady=(25, 5))

    subtitle = tk.Label(
        budget_window,
        text="Set and monitor your monthly category budgets",
        font=("Arial", 11),
        bg="#f4f6f8"
    )
    subtitle.pack(pady=(0, 20))

    # ================= INPUT FRAME =================

    input_frame = tk.Frame(
        budget_window,
        bg="white",
        bd=1,
        relief="solid"
    )
    input_frame.pack(padx=30, fill="x")

    # Category

    tk.Label(
        input_frame,
        text="Category",
        font=("Arial", 11),
        bg="white"
    ).grid(
        row=0,
        column=0,
        padx=25,
        pady=(20, 5),
        sticky="w"
    )

    category_combo = ttk.Combobox(
        input_frame,
        values=[
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
        width=20,
        state="readonly"
    )

    category_combo.grid(
        row=1,
        column=0,
        padx=25,
        pady=(0, 20)
    )

    # Budget Amount

    tk.Label(
        input_frame,
        text="Budget Amount",
        font=("Arial", 11),
        bg="white"
    ).grid(
        row=0,
        column=1,
        padx=25,
        pady=(20, 5),
        sticky="w"
    )

    amount_entry = tk.Entry(
        input_frame,
        font=("Arial", 11),
        width=23
    )

    amount_entry.grid(
        row=1,
        column=1,
        padx=25,
        pady=(0, 20)
    )

    # Month

    tk.Label(
        input_frame,
        text="Month",
        font=("Arial", 11),
        bg="white"
    ).grid(
        row=0,
        column=2,
        padx=25,
        pady=(20, 5),
        sticky="w"
    )

    month_entry = tk.Entry(
        input_frame,
        font=("Arial", 11),
        width=23
    )

    month_entry.grid(
        row=1,
        column=2,
        padx=25,
        pady=(0, 20)
    )

    month_entry.insert(
        0,
        datetime.now().strftime("%Y-%m-01")
    )

    # ================= TABLE =================

    table_title = tk.Label(
        budget_window,
        text="Budget Overview",
        font=("Arial", 17, "bold"),
        bg="#f4f6f8"
    )

    table_title.pack(pady=(25, 10))

    table_frame = tk.Frame(
        budget_window,
        bg="white",
        bd=1,
        relief="solid"
    )

    table_frame.pack(
        padx=30,
        fill="both",
        expand=True
    )

    columns = (
        "ID",
        "Category",
        "Budget",
        "Actual Expense",
        "Remaining",
        "Status"
    )

    budget_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=11
    )

    budget_table.heading("ID", text="ID")
    budget_table.heading("Category", text="Category")
    budget_table.heading("Budget", text="Budget Amount")
    budget_table.heading("Actual Expense", text="Actual Expense")
    budget_table.heading("Remaining", text="Remaining")
    budget_table.heading("Status", text="Status")

    budget_table.column("ID", width=60, anchor="center")
    budget_table.column("Category", width=150, anchor="center")
    budget_table.column("Budget", width=170, anchor="center")
    budget_table.column("Actual Expense", width=180, anchor="center")
    budget_table.column("Remaining", width=170, anchor="center")
    budget_table.column("Status", width=150, anchor="center")

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=budget_table.yview
    )

    budget_table.configure(
        yscrollcommand=scrollbar.set
    )

    budget_table.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # ================= FUNCTIONS =================

    def clear_fields():

        category_combo.set("")

        amount_entry.delete(0, tk.END)

        month_entry.delete(0, tk.END)

        month_entry.insert(
            0,
            datetime.now().strftime("%Y-%m-01")
        )

    def load_budgets():

        for item in budget_table.get_children():
            budget_table.delete(item)

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
        SELECT
            b.budget_id,
            b.category,
            b.budget_amount,
            COALESCE(SUM(t.amount), 0)
        FROM budgets b

        LEFT JOIN transactions t
            ON b.category = t.category
            AND b.budget_month = DATE_FORMAT(
                t.transaction_date,
                '%Y-%m-01'
            )
            AND t.transaction_type = 'Expense'
            AND t.user_id = %s

        GROUP BY
            b.budget_id,
            b.category,
            b.budget_amount,
            b.budget_month

        ORDER BY
            b.budget_month DESC,
            b.budget_id DESC
        """

        cursor.execute(
            query,
            (user_id,)
        )

        records = cursor.fetchall()

        for record in records:

            budget_amount = float(record[2])
            actual_expense = float(record[3])
            remaining = budget_amount - actual_expense

            if remaining >= 0:
                status = "Within Budget"
            else:
                status = "Over Budget"

            budget_table.insert(
                "",
                "end",
                values=(
                    record[0],
                    record[1],
                    "₹ " + format(budget_amount, ",.2f"),
                    "₹ " + format(actual_expense, ",.2f"),
                    "₹ " + format(remaining, ",.2f"),
                    status
                )
            )

        cursor.close()
        connection.close()

    def add_budget():

        category = category_combo.get()
        amount = amount_entry.get().strip()
        month = month_entry.get().strip()

        if category == "" or amount == "" or month == "":
            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        try:

            amount_value = float(amount)

            if amount_value <= 0:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid budget amount."
            )
            return

        try:

            datetime.strptime(
                month,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Month",
                "Month must be in YYYY-MM-01 format."
            )
            return

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
        INSERT INTO budgets
        (
            category,
            budget_amount,
            budget_month
        )
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (
                category,
                amount_value,
                month
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Budget added successfully."
        )

        clear_fields()
        load_budgets()

    def select_budget(event):

        selected = budget_table.selection()

        if not selected:
            return

        values = budget_table.item(
            selected[0],
            "values"
        )

        category_combo.set(values[1])

        amount_entry.delete(0, tk.END)

        amount = values[2].replace(
            "₹ ",
            ""
        ).replace(
            ",",
            ""
        )

        amount_entry.insert(
            0,
            amount
        )

    def update_budget():

        selected = budget_table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Budget",
                "Please select a budget to update."
            )
            return

        budget_id = budget_table.item(
            selected[0],
            "values"
        )[0]

        category = category_combo.get()
        amount = amount_entry.get().strip()
        month = month_entry.get().strip()

        if category == "" or amount == "" or month == "":
            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        try:

            amount_value = float(amount)

            if amount_value <= 0:
                raise ValueError

            datetime.strptime(
                month,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Data",
                "Please enter valid budget amount and month."
            )
            return

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
        UPDATE budgets
        SET
            category = %s,
            budget_amount = %s,
            budget_month = %s
        WHERE budget_id = %s
        """

        cursor.execute(
            query,
            (
                category,
                amount_value,
                month,
                budget_id
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Budget updated successfully."
        )

        clear_fields()
        load_budgets()

    def delete_budget():

        selected = budget_table.selection()

        if not selected:
            messagebox.showwarning(
                "Select Budget",
                "Please select a budget to delete."
            )
            return

        budget_id = budget_table.item(
            selected[0],
            "values"
        )[0]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this budget?"
        )

        if not confirm:
            return

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
        DELETE FROM budgets
        WHERE budget_id = %s
        """

        cursor.execute(
            query,
            (budget_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Budget deleted successfully."
        )

        clear_fields()
        load_budgets()

    # ================= BUTTONS =================

    button_frame = tk.Frame(
        budget_window,
        bg="#f4f6f8"
    )

    button_frame.pack(pady=15)

    tk.Button(
        button_frame,
        text="ADD BUDGET",
        font=("Arial", 10, "bold"),
        width=14,
        command=add_budget
    ).grid(row=0, column=0, padx=7)

    tk.Button(
        button_frame,
        text="UPDATE",
        font=("Arial", 10, "bold"),
        width=12,
        command=update_budget
    ).grid(row=0, column=1, padx=7)

    tk.Button(
        button_frame,
        text="DELETE",
        font=("Arial", 10, "bold"),
        width=12,
        command=delete_budget
    ).grid(row=0, column=2, padx=7)

    tk.Button(
        button_frame,
        text="CLEAR",
        font=("Arial", 10, "bold"),
        width=12,
        command=clear_fields
    ).grid(row=0, column=3, padx=7)

    tk.Button(
        button_frame,
        text="REFRESH",
        font=("Arial", 10, "bold"),
        width=12,
        command=load_budgets
    ).grid(row=0, column=4, padx=7)

    def go_back():

        budget_window.destroy()
        dashboard.deiconify()

    tk.Button(
        button_frame,
        text="BACK",
        font=("Arial", 10, "bold"),
        width=12,
        command=go_back
    ).grid(row=0, column=5, padx=7)

    budget_table.bind(
        "<<TreeviewSelect>>",
        select_budget
    )

    load_budgets()
