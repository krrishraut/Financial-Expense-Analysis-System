import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_database


def open_analysis(user_id, dashboard):

    analysis_window = tk.Toplevel(dashboard)

    dashboard.withdraw()

    analysis_window.title("Financial Analysis")
    analysis_window.geometry("1100x700")
    analysis_window.resizable(False, False)
    analysis_window.configure(bg="#f4f6f8")

    # ================= TITLE =================

    title = tk.Label(
        analysis_window,
        text="Financial Analysis",
        font=("Arial", 24, "bold"),
        bg="#f4f6f8"
    )

    title.pack(pady=(25, 5))

    subtitle = tk.Label(
        analysis_window,
        text="Analyze your income, expenses and savings",
        font=("Arial", 11),
        bg="#f4f6f8"
    )

    subtitle.pack(pady=(0, 20))

    # ================= SUMMARY =================

    summary_frame = tk.Frame(
        analysis_window,
        bg="#f4f6f8"
    )

    summary_frame.pack()

    income_card = tk.Frame(
        summary_frame,
        bg="white",
        width=300,
        height=120,
        relief="solid",
        bd=1
    )

    income_card.grid(row=0, column=0, padx=15)
    income_card.pack_propagate(False)

    tk.Label(
        income_card,
        text="TOTAL INCOME",
        font=("Arial", 11, "bold"),
        bg="white"
    ).pack(pady=(20, 5))

    income_label = tk.Label(
        income_card,
        text="₹ 0.00",
        font=("Arial", 20, "bold"),
        bg="white"
    )

    income_label.pack()

    expense_card = tk.Frame(
        summary_frame,
        bg="white",
        width=300,
        height=120,
        relief="solid",
        bd=1
    )

    expense_card.grid(row=0, column=1, padx=15)
    expense_card.pack_propagate(False)

    tk.Label(
        expense_card,
        text="TOTAL EXPENSE",
        font=("Arial", 11, "bold"),
        bg="white"
    ).pack(pady=(20, 5))

    expense_label = tk.Label(
        expense_card,
        text="₹ 0.00",
        font=("Arial", 20, "bold"),
        bg="white"
    )

    expense_label.pack()

    savings_card = tk.Frame(
        summary_frame,
        bg="white",
        width=300,
        height=120,
        relief="solid",
        bd=1
    )

    savings_card.grid(row=0, column=2, padx=15)
    savings_card.pack_propagate(False)

    tk.Label(
        savings_card,
        text="TOTAL SAVINGS",
        font=("Arial", 11, "bold"),
        bg="white"
    ).pack(pady=(20, 5))

    savings_label = tk.Label(
        savings_card,
        text="₹ 0.00",
        font=("Arial", 20, "bold"),
        bg="white"
    )

    savings_label.pack()

    # ================= ANALYSIS TABLE =================

    table_title = tk.Label(
        analysis_window,
        text="Category-wise Expense Analysis",
        font=("Arial", 17, "bold"),
        bg="#f4f6f8"
    )

    table_title.pack(pady=(30, 10))

    table_frame = tk.Frame(
        analysis_window,
        bg="white",
        bd=1,
        relief="solid"
    )

    table_frame.pack(
        padx=30,
        fill="x"
    )

    columns = (
        "Category",
        "Total Expense"
    )

    analysis_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=7
    )

    analysis_table.heading(
        "Category",
        text="Category"
    )

    analysis_table.heading(
        "Total Expense",
        text="Total Expense"
    )

    analysis_table.column(
        "Category",
        width=400,
        anchor="center"
    )

    analysis_table.column(
        "Total Expense",
        width=400,
        anchor="center"
    )

    analysis_table.pack(
        padx=10,
        pady=10
    )

    # ================= FUNCTIONS =================

    def load_analysis():

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        # Total income and expense

        query = """
        SELECT
            COALESCE(SUM(
                CASE
                    WHEN transaction_type = 'Income'
                    THEN amount
                    ELSE 0
                END
            ), 0),

            COALESCE(SUM(
                CASE
                    WHEN transaction_type = 'Expense'
                    THEN amount
                    ELSE 0
                END
            ), 0)

        FROM transactions
        WHERE user_id = %s
        """

        cursor.execute(
            query,
            (user_id,)
        )

        result = cursor.fetchone()

        income = float(result[0])
        expense = float(result[1])
        savings = income - expense

        income_label.config(
            text="₹ " + format(income, ",.2f")
        )

        expense_label.config(
            text="₹ " + format(expense, ",.2f")
        )

        savings_label.config(
            text="₹ " + format(savings, ",.2f")
        )

        # Category-wise expenses

        for item in analysis_table.get_children():
            analysis_table.delete(item)

        category_query = """
        SELECT
            category,
            SUM(amount)
        FROM transactions
        WHERE user_id = %s
        AND transaction_type = 'Expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC
        """

        cursor.execute(
            category_query,
            (user_id,)
        )

        records = cursor.fetchall()

        for record in records:

            analysis_table.insert(
                "",
                "end",
                values=(
                    record[0],
                    "₹ " + format(float(record[1]), ",.2f")
                )
            )

        # Monthly financial analysis

        for item in monthly_table.get_children():
            monthly_table.delete(item)

        monthly_query = """
        SELECT
            DATE_FORMAT(
                MIN(transaction_date),
                '%M %Y'
            ) AS month,

            SUM(
                CASE
                    WHEN transaction_type = 'Income'
                    THEN amount
                    ELSE 0
                END
            ) AS income,

            SUM(
                CASE
                    WHEN transaction_type = 'Expense'
                    THEN amount
                    ELSE 0
                END
            ) AS expense

        FROM transactions

        WHERE user_id = %s

        GROUP BY
            YEAR(transaction_date),
            MONTH(transaction_date)

        ORDER BY
            YEAR(transaction_date),
            MONTH(transaction_date)
        """

        cursor.execute(
            monthly_query,
            (user_id,)
        )

        monthly_records = cursor.fetchall()

        for record in monthly_records:

            monthly_income = float(record[1])
            monthly_expense = float(record[2])
            monthly_savings = monthly_income - monthly_expense

            monthly_table.insert(
                "",
                "end",
                values=(
                    record[0],
                    "₹ " + format(monthly_income, ",.2f"),
                    "₹ " + format(monthly_expense, ",.2f"),
                    "₹ " + format(monthly_savings, ",.2f")
                )
            )

        cursor.close()
        connection.close()

    # ================= MONTHLY ANALYSIS =================

    monthly_title = tk.Label(
        analysis_window,
        text="Monthly Financial Analysis",
        font=("Arial", 17, "bold"),
        bg="#f4f6f8"
    )

    monthly_title.pack(pady=(25, 10))

    monthly_frame = tk.Frame(
        analysis_window,
        bg="white",
        bd=1,
        relief="solid"
    )

    monthly_frame.pack(
        padx=30,
        fill="x"
    )

    monthly_columns = (
        "Month",
        "Income",
        "Expense",
        "Savings"
    )

    monthly_table = ttk.Treeview(
        monthly_frame,
        columns=monthly_columns,
        show="headings",
        height=5
    )

    monthly_table.heading(
        "Month",
        text="Month"
    )

    monthly_table.heading(
        "Income",
        text="Total Income"
    )

    monthly_table.heading(
        "Expense",
        text="Total Expense"
    )

    monthly_table.heading(
        "Savings",
        text="Savings"
    )

    monthly_table.column(
        "Month",
        width=220,
        anchor="center"
    )

    monthly_table.column(
        "Income",
        width=220,
        anchor="center"
    )

    monthly_table.column(
        "Expense",
        width=220,
        anchor="center"
    )

    monthly_table.column(
        "Savings",
        width=220,
        anchor="center"
    )

    monthly_table.pack(
        padx=10,
        pady=10
    )

    # ================= BACK BUTTON =================

    def go_back():

        analysis_window.destroy()

        dashboard.deiconify()

    back_button = tk.Button(
        analysis_window,
        text="BACK",
        font=("Arial", 10, "bold"),
        width=15,
        command=go_back
    )

    back_button.pack(pady=20)

    # Load data

    load_analysis()
