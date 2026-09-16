import tkinter as tk
from database import connect_database
from transactions import open_transactions
from analysis import open_analysis
from budget import open_budget
from prediction import open_prediction
from recommendations import open_recommendations

def get_financial_data(user_id):

    connection = connect_database()

    if connection is None:
        return 0, 0, 0

    cursor = connection.cursor()

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

    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    income = float(result[0])
    expense = float(result[1])
    savings = income - expense

    return income, expense, savings


def open_dashboard(user_id, username):

    dashboard = tk.Toplevel()

    dashboard.title("Financial Expense Analysis System")
    dashboard.geometry("1100x700")
    dashboard.resizable(False, False)
    dashboard.configure(bg="#f4f6f8")

    # ================= HEADER =================

    header = tk.Frame(
        dashboard,
        bg="#1f2937",
        height=110
    )

    header.pack(fill="x")

    title = tk.Label(
        header,
        text="Financial Expense Analysis System",
        font=("Arial", 25, "bold"),
        fg="white",
        bg="#1f2937"
    )

    title.pack(pady=(25, 5))

    welcome = tk.Label(
        header,
        text="Welcome, " + username,
        font=("Arial", 13),
        fg="white",
        bg="#1f2937"
    )

    welcome.pack()

    # ================= FINANCIAL SUMMARY =================

    income, expense, savings = get_financial_data(user_id)

    summary_title = tk.Label(
        dashboard,
        text="Financial Summary",
        font=("Arial", 18, "bold"),
        bg="#f4f6f8"
    )

    summary_title.pack(pady=(25, 15))

    cards_frame = tk.Frame(
        dashboard,
        bg="#f4f6f8"
    )

    cards_frame.pack()

    # ---------------- INCOME ----------------

    income_card = tk.Frame(
        cards_frame,
        bg="white",
        width=300,
        height=130,
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

    income_value_label = tk.Label(
        income_card,
        text="₹ " + format(income, ",.2f"),
        font=("Arial", 21, "bold"),
        bg="white"
    )

    income_value_label.pack()

    # ---------------- EXPENSE ----------------

    expense_card = tk.Frame(
        cards_frame,
        bg="white",
        width=300,
        height=130,
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

    expense_value_label = tk.Label(
        expense_card,
        text="₹ " + format(expense, ",.2f"),
        font=("Arial", 21, "bold"),
        bg="white"
    )

    expense_value_label.pack()

    # ---------------- SAVINGS ----------------

    savings_card = tk.Frame(
        cards_frame,
        bg="white",
        width=300,
        height=130,
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

    savings_value_label = tk.Label(
        savings_card,
        text="₹ " + format(savings, ",.2f"),
        font=("Arial", 21, "bold"),
        bg="white"
    )

    savings_value_label.pack()

    def refresh_dashboard():

        income, expense, savings = get_financial_data(user_id)

        income_value_label.config(
            text="₹ " + format(income, ",.2f")
        )

        expense_value_label.config(
            text="₹ " + format(expense, ",.2f")
        )

        savings_value_label.config(
            text="₹ " + format(savings, ",.2f")
        )

    # ================= MAIN MENU =================

    menu_title = tk.Label(
        dashboard,
        text="Main Menu",
        font=("Arial", 18, "bold"),
        bg="#f4f6f8"
    )

    menu_title.pack(pady=(30, 10))

    menu_frame = tk.Frame(
        dashboard,
        bg="#f4f6f8"
    )

    menu_frame.pack()

    button_font = ("Arial", 11, "bold")

    # TRANSACTIONS

    transaction_button = tk.Button(
        menu_frame,
        text="TRANSACTIONS",
        font=button_font,
        width=22,
        height=2,
        command=lambda: open_transactions(
            user_id,
            dashboard,
            refresh_dashboard
        )
    )

    transaction_button.grid(
        row=0,
        column=0,
        padx=12,
        pady=10
    )

    # ANALYSIS

    analysis_button = tk.Button(
        menu_frame,
        text="ANALYSIS",
        font=button_font,
        width=22,
        height=2,
        command=lambda: open_analysis(
            user_id,
            dashboard
        )
    )

    analysis_button.grid(
        row=0,
        column=1,
        padx=12,
        pady=10
    )

    # BUDGET

    budget_button = tk.Button(
        menu_frame,
        text="BUDGET",
        font=button_font,
        width=22,
        height=2,
        command=lambda: open_budget(
            user_id,
            dashboard
        )
    )

    budget_button.grid(
        row=0,
        column=2,
        padx=12,
        pady=10
    )

    # PREDICTION

    prediction_button = tk.Button(
        menu_frame,
        text="EXPENSE PREDICTION",
        font=button_font,
        width=22,
        height=2,
        command=lambda: open_prediction(
            user_id,
            dashboard
        )
    )   

    prediction_button.grid(
        row=1,
        column=0,
        padx=12,
        pady=10
    )

    # RECOMMENDATIONS

    recommendation_button = tk.Button(
        menu_frame,
        text="RECOMMENDATIONS",
        font=button_font,
        width=22,
        height=2,
        command=lambda: open_recommendations(
            user_id,
            dashboard
        )
    )

    recommendation_button.grid(
        row=1,
        column=1,
        padx=12,
        pady=10
    )

    # LOGOUT

    logout_button = tk.Button(
        menu_frame,
        text="LOGOUT",
        font=button_font,
        width=22,
        height=2,
        command=dashboard.destroy
    )

    logout_button.grid(
        row=1,
        column=2,
        padx=12,
        pady=10
    )

    # ================= FOOTER =================

    footer = tk.Label(
        dashboard,
        text="Financial Expense Analysis System | Python + MySQL",
        font=("Arial", 9),
        bg="#f4f6f8",
        fg="#666666"
    )

    footer.pack(side="bottom", pady=15)
