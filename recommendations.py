import tkinter as tk
from tkinter import messagebox
from database import connect_database


def open_recommendations(user_id, dashboard):

    recommendation_window = tk.Toplevel(dashboard)

    dashboard.withdraw()

    recommendation_window.title("Financial Recommendations")
    recommendation_window.geometry("900x700")
    recommendation_window.resizable(False, False)
    recommendation_window.configure(bg="#f4f6f8")

    # ================= TITLE =================

    title = tk.Label(
        recommendation_window,
        text="Financial Recommendations",
        font=("Arial", 24, "bold"),
        bg="#f4f6f8"
    )

    title.pack(pady=(30, 5))

    subtitle = tk.Label(
        recommendation_window,
        text="Personalized suggestions based on your financial activity",
        font=("Arial", 11),
        bg="#f4f6f8"
    )

    subtitle.pack(pady=(0, 25))

    # ================= RECOMMENDATION AREA =================

    recommendation_frame = tk.Frame(
        recommendation_window,
        bg="white",
        bd=1,
        relief="solid",
        width=820,
        height=350
    )

    recommendation_frame.pack(
        padx=40,
        pady=5
    )

    recommendation_frame.pack_propagate(False)

    recommendation_text = tk.Text(
        recommendation_frame,
        font=("Arial", 12),
        bg="white",
        relief="flat",
        wrap="word",
        padx=25,
        pady=20
    )

    recommendation_text.pack(
        fill="both",
        expand=True
    )

    # ================= ANALYSIS =================

    def generate_recommendations():

        recommendation_text.config(state="normal")
        recommendation_text.delete("1.0", tk.END)

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        # Total income and expense

        summary_query = """
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
            summary_query,
            (user_id,)
        )

        summary = cursor.fetchone()

        income = float(summary[0])
        expense = float(summary[1])

        savings = income - expense

        recommendations = []

        # No transaction data

        if income == 0 and expense == 0:

            recommendations.append(
                "• Start adding your income and expense transactions "
                "to receive personalized financial recommendations."
            )

        else:

            # Savings recommendation

            if savings < 0:

                recommendations.append(
                    "• Your expenses are higher than your income. "
                    "Review your spending and consider reducing "
                    "non-essential expenses."
                )

            elif income > 0 and savings / income < 0.10:

                recommendations.append(
                    "• Your current savings are relatively low compared "
                    "with your income. Consider setting aside a fixed "
                    "amount before making discretionary purchases."
                )

            else:

                recommendations.append(
                    "• Your income is currently higher than your expenses. "
                    "Continue monitoring your spending to maintain savings."
                )

        # Category-wise expense

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

        categories = cursor.fetchall()

        if categories:

            highest_category = categories[0][0]
            highest_amount = float(categories[0][1])

            recommendations.append(
                "• Your highest expense category is "
                + highest_category
                + " with spending of ₹ "
                + format(highest_amount, ",.2f")
                + ". Consider reviewing this category for "
                "possible savings."
            )

            # Categories representing large spending

            if expense > 0:

                for category in categories:

                    category_name = category[0]
                    category_amount = float(category[1])

                    percentage = (
                        category_amount / expense
                    ) * 100

                    if percentage >= 30:

                        recommendations.append(
                            "• "
                            + category_name
                            + " accounts for approximately "
                            + format(percentage, ".1f")
                            + "% of your total expenses. "
                            "Consider monitoring this category closely."
                        )

        # Budget analysis

        budget_query = """
        SELECT
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
        """

        cursor.execute(
            budget_query,
            (user_id,)
        )

        budgets = cursor.fetchall()

        for budget in budgets:

            category_name = budget[0]
            budget_amount = float(budget[1])
            actual_expense = float(budget[2])

            if actual_expense > budget_amount:

                recommendations.append(
                    "• Your "
                    + category_name
                    + " spending has exceeded the budget by ₹ "
                    + format(
                        actual_expense - budget_amount,
                        ",.2f"
                    )
                    + ". Consider reducing spending in this category."
                )

        cursor.close()
        connection.close()

        # ================= DISPLAY =================

        if not recommendations:

            recommendations.append(
                "• Continue recording your transactions "
                "regularly to generate more detailed recommendations."
            )

        recommendation_text.insert(
            tk.END,
            "\n\n".join(recommendations)
        )

        recommendation_text.config(
            state="disabled"
        )

    # ================= BUTTONS =================

    button_frame = tk.Frame(
        recommendation_window,
        bg="#f4f6f8"
    )

    button_frame.pack(pady=20)

    generate_button = tk.Button(
        button_frame,
        text="GENERATE RECOMMENDATIONS",
        font=("Arial", 10, "bold"),
        width=25,
        height=2,
        command=generate_recommendations
    )

    generate_button.grid(
        row=0,
        column=0,
        padx=10
    )

    def go_back():

        recommendation_window.destroy()
        dashboard.deiconify()

    back_button = tk.Button(
        button_frame,
        text="BACK",
        font=("Arial", 10, "bold"),
        width=15,
        height=2,
        command=go_back
    )

    back_button.grid(
        row=0,
        column=1,
        padx=10
    )

    # Generate automatically when window opens

    generate_recommendations()
