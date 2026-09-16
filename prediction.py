import tkinter as tk
from tkinter import messagebox
from database import connect_database
from sklearn.linear_model import LinearRegression


def open_prediction(user_id, dashboard):

    prediction_window = tk.Toplevel(dashboard)

    dashboard.withdraw()

    prediction_window.title("Expense Prediction")
    prediction_window.geometry("900x600")
    prediction_window.resizable(False, False)
    prediction_window.configure(bg="#f4f6f8")

    # ================= TITLE =================

    title = tk.Label(
        prediction_window,
        text="Expense Prediction",
        font=("Arial", 24, "bold"),
        bg="#f4f6f8"
    )

    title.pack(pady=(30, 5))

    subtitle = tk.Label(
        prediction_window,
        text="Predict your next month's expense using transaction history",
        font=("Arial", 11),
        bg="#f4f6f8"
    )

    subtitle.pack(pady=(0, 30))

    # ================= RESULT CARD =================

    result_card = tk.Frame(
        prediction_window,
        bg="white",
        width=600,
        height=180,
        bd=1,
        relief="solid"
    )

    result_card.pack(pady=20)

    result_card.pack_propagate(False)

    tk.Label(
        result_card,
        text="PREDICTED NEXT MONTH EXPENSE",
        font=("Arial", 13, "bold"),
        bg="white"
    ).pack(pady=(35, 10))

    prediction_label = tk.Label(
        result_card,
        text="₹ 0.00",
        font=("Arial", 30, "bold"),
        bg="white"
    )

    prediction_label.pack()

    # ================= INFORMATION =================

    info_label = tk.Label(
        prediction_window,
        text="",
        font=("Arial", 11),
        bg="#f4f6f8",
        justify="center"
    )

    info_label.pack(pady=20)

    # ================= PREDICTION =================

    def predict_expense():

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        query = """
        SELECT
            YEAR(transaction_date),
            MONTH(transaction_date),
            SUM(amount)
        FROM transactions
        WHERE user_id = %s
        AND transaction_type = 'Expense'
        GROUP BY
            YEAR(transaction_date),
            MONTH(transaction_date)
        ORDER BY
            YEAR(transaction_date),
            MONTH(transaction_date)
        """

        cursor.execute(
            query,
            (user_id,)
        )

        records = cursor.fetchall()

        cursor.close()
        connection.close()

        # Need at least 2 months of data

        if len(records) < 2:

            messagebox.showwarning(
                "Insufficient Data",
                "At least 2 months of expense data are required for prediction."
            )

            prediction_label.config(
                text="₹ 0.00"
            )

            info_label.config(
                text="Add transactions from at least two different months."
            )

            return

        # ================= PREPARE DATA =================

        x_values = []
        y_values = []

        for index, record in enumerate(records):

            month_number = index + 1

            expense_amount = float(record[2])

            x_values.append([month_number])

            y_values.append(expense_amount)

        # ================= LINEAR REGRESSION =================

        model = LinearRegression()

        model.fit(
            x_values,
            y_values
        )

        # Next month

        next_month = len(records) + 1

        predicted_expense = model.predict(
            [[next_month]]
        )[0]

        # Expense cannot be negative

        if predicted_expense < 0:
            predicted_expense = 0

        # ================= DISPLAY =================

        prediction_label.config(
            text="₹ " + format(
                predicted_expense,
                ",.2f"
            )
        )

        info_label.config(
            text=
            "Based on "
            + str(len(records))
            + " months of expense history.\n"
            "Machine Learning Model: Linear Regression"
        )

    # ================= BUTTONS =================

    predict_button = tk.Button(
        prediction_window,
        text="PREDICT EXPENSE",
        font=("Arial", 11, "bold"),
        width=22,
        height=2,
        command=predict_expense
    )

    predict_button.pack(pady=15)

    def go_back():

        prediction_window.destroy()

        dashboard.deiconify()

    back_button = tk.Button(
        prediction_window,
        text="BACK",
        font=("Arial", 10, "bold"),
        width=15,
        command=go_back
    )

    back_button.pack(pady=5)
