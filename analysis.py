import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_database

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def open_analysis(user_id, dashboard):

    analysis_window = tk.Toplevel(dashboard)

    dashboard.withdraw()

    analysis_window.title("Financial Analysis")
    analysis_window.geometry("1100x750")
    analysis_window.resizable(False, False)
    analysis_window.configure(bg="#f4f6f8")

    # =================================================
    # SCROLLABLE PAGE
    # =================================================

    main_canvas = tk.Canvas(
        analysis_window,
        bg="#f4f6f8",
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        analysis_window,
        orient="vertical",
        command=main_canvas.yview
    )

    main_canvas.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    main_canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    content_frame = tk.Frame(
        main_canvas,
        bg="#f4f6f8"
    )

    canvas_window = main_canvas.create_window(
        (0, 0),
        window=content_frame,
        anchor="nw"
    )

    def update_scroll_region(event=None):

        main_canvas.configure(
            scrollregion=main_canvas.bbox("all")
        )

        main_canvas.itemconfig(
            canvas_window,
            width=main_canvas.winfo_width()
        )

    content_frame.bind(
        "<Configure>",
        update_scroll_region
    )

    main_canvas.bind(
        "<Configure>",
        update_scroll_region
    )

    # Mouse wheel scrolling

    def mouse_wheel(event):

        main_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    main_canvas.bind_all(
        "<MouseWheel>",
        mouse_wheel
    )

    # =================================================
    # TITLE
    # =================================================

    title = tk.Label(
        content_frame,
        text="Financial Analysis",
        font=("Arial", 24, "bold"),
        bg="#f4f6f8"
    )

    title.pack(pady=(25, 5))

    subtitle = tk.Label(
        content_frame,
        text="Analyze your income, expenses and savings",
        font=("Arial", 11),
        bg="#f4f6f8"
    )

    subtitle.pack(pady=(0, 20))

    # =================================================
    # SUMMARY
    # =================================================

    summary_frame = tk.Frame(
        content_frame,
        bg="#f4f6f8"
    )

    summary_frame.pack()

    # ---------------- INCOME ----------------

    income_card = tk.Frame(
        summary_frame,
        bg="white",
        width=300,
        height=120,
        relief="solid",
        bd=1
    )

    income_card.grid(
        row=0,
        column=0,
        padx=15
    )

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

    # ---------------- EXPENSE ----------------

    expense_card = tk.Frame(
        summary_frame,
        bg="white",
        width=300,
        height=120,
        relief="solid",
        bd=1
    )

    expense_card.grid(
        row=0,
        column=1,
        padx=15
    )

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

    # ---------------- SAVINGS ----------------

    savings_card = tk.Frame(
        summary_frame,
        bg="white",
        width=300,
        height=120,
        relief="solid",
        bd=1
    )

    savings_card.grid(
        row=0,
        column=2,
        padx=15
    )

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

    # =================================================
    # CATEGORY TABLE
    # =================================================

    table_title = tk.Label(
        content_frame,
        text="Category-wise Expense Analysis",
        font=("Arial", 17, "bold"),
        bg="#f4f6f8"
    )

    table_title.pack(
        pady=(30, 10)
    )

    table_frame = tk.Frame(
        content_frame,
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

    # =================================================
    # CATEGORY CHART
    # =================================================

    chart_title = tk.Label(
        content_frame,
        text="Expense by Category",
        font=("Arial", 17, "bold"),
        bg="#f4f6f8"
    )

    chart_title.pack(
        pady=(25, 10)
    )

    chart_frame = tk.Frame(
        content_frame,
        bg="white",
        bd=1,
        relief="solid"
    )

    chart_frame.pack(
        padx=30
    )

    figure = Figure(
        figsize=(9, 3.5),
        dpi=100
    )

    chart = figure.add_subplot(111)

    canvas = FigureCanvasTkAgg(
        figure,
        master=chart_frame
    )

    canvas.get_tk_widget().pack(
        padx=10,
        pady=10
    )

    # =================================================
    # MONTHLY TABLE
    # =================================================

    monthly_title = tk.Label(
        content_frame,
        text="Monthly Financial Analysis",
        font=("Arial", 17, "bold"),
        bg="#f4f6f8"
    )

    monthly_title.pack(
        pady=(30, 10)
    )

    monthly_frame = tk.Frame(
        content_frame,
        bg="white",
        bd=1,
        relief="solid"
    )

    monthly_frame.pack(
        padx=30
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
        height=6
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

    # =================================================
    # MONTHLY EXPENSE TREND CHART
    # =================================================

    monthly_chart_title = tk.Label(
        content_frame,
        text="Monthly Expense Trend",
        font=("Arial", 17, "bold"),
        bg="#f4f6f8"
    )

    monthly_chart_title.pack(
        pady=(30, 10)
    )

    monthly_chart_frame = tk.Frame(
        content_frame,
        bg="white",
        bd=1,
        relief="solid"
    )

    monthly_chart_frame.pack(
        padx=30
    )

    monthly_figure = Figure(
        figsize=(9, 3.5),
        dpi=100
    )

    monthly_chart = monthly_figure.add_subplot(111)

    monthly_canvas = FigureCanvasTkAgg(
        monthly_figure,
        master=monthly_chart_frame
    )

    monthly_canvas.get_tk_widget().pack(
        padx=10,
        pady=10
    )

    # =================================================
    # INCOME VS EXPENSE CHART
    # =================================================

    comparison_title = tk.Label(
        content_frame,
        text="Monthly Income vs Expense",
        font=("Arial", 17, "bold"),
        bg="#f4f6f8"
    )

    comparison_title.pack(
        pady=(30, 10)
    )

    comparison_frame = tk.Frame(
        content_frame,
        bg="white",
        bd=1,
        relief="solid"
    )

    comparison_frame.pack(
        padx=30
    )

    comparison_figure = Figure(
        figsize=(9, 3.5),
        dpi=100
    )

    comparison_chart = comparison_figure.add_subplot(111)

    comparison_canvas = FigureCanvasTkAgg(
        comparison_figure,
        master=comparison_frame
    )

    comparison_canvas.get_tk_widget().pack(
        padx=10,
        pady=10
    )

    # =================================================
    # LOAD ANALYSIS
    # =================================================

    def load_analysis():

        connection = connect_database()

        if connection is None:
            return

        cursor = connection.cursor()

        # =================================================
        # TOTAL INCOME AND EXPENSE
        # =================================================

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
            text="₹ " + format(
                income,
                ",.2f"
            )
        )

        expense_label.config(
            text="₹ " + format(
                expense,
                ",.2f"
            )
        )

        savings_label.config(
            text="₹ " + format(
                savings,
                ",.2f"
            )
        )

        # =================================================
        # CATEGORY-WISE EXPENSE
        # =================================================

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
                    "₹ " + format(
                        float(record[1]),
                        ",.2f"
                    )
                )
            )

        # =================================================
        # CATEGORY CHART
        # =================================================

        categories = []
        category_expenses = []

        for record in records:

            categories.append(record[0])
            category_expenses.append(
                float(record[1])
            )

        chart.clear()

        chart.set_title(
            "Category-wise Expense"
        )

        chart.set_xlabel(
            "Category"
        )

        chart.set_ylabel(
            "Expense (₹)"
        )

        if categories:

            chart.bar(
                categories,
                category_expenses
            )

            chart.tick_params(
                axis="x",
                rotation=30
            )

        else:

            chart.text(
                0.5,
                0.5,
                "No expense data available",
                ha="center",
                va="center"
            )

        figure.tight_layout()

        canvas.draw()

        # =================================================
        # MONTHLY ANALYSIS
        # =================================================

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

        months = []
        monthly_expenses = []
        monthly_incomes = []

        for record in monthly_records:

            monthly_income = float(record[1])
            monthly_expense = float(record[2])
            monthly_savings = (
                monthly_income
                - monthly_expense
            )

            monthly_table.insert(
                "",
                "end",
                values=(
                    record[0],
                    "₹ " + format(
                        monthly_income,
                        ",.2f"
                    ),
                    "₹ " + format(
                        monthly_expense,
                        ",.2f"
                    ),
                    "₹ " + format(
                        monthly_savings,
                        ",.2f"
                    )
                )
            )

            months.append(record[0])
            monthly_incomes.append(
                monthly_income
            )
            monthly_expenses.append(
                monthly_expense
            )

        # =================================================
        # MONTHLY EXPENSE TREND
        # =================================================

        monthly_chart.clear()

        monthly_chart.set_title(
            "Monthly Expense Trend"
        )

        monthly_chart.set_xlabel(
            "Month"
        )

        monthly_chart.set_ylabel(
            "Expense (₹)"
        )

        if months:

            monthly_chart.plot(
                months,
                monthly_expenses,
                marker="o"
            )

            monthly_chart.tick_params(
                axis="x",
                rotation=30
            )

        else:

            monthly_chart.text(
                0.5,
                0.5,
                "No monthly expense data available",
                ha="center",
                va="center"
            )

        monthly_figure.tight_layout()

        monthly_canvas.draw()

        # =================================================
        # INCOME VS EXPENSE
        # =================================================

        comparison_chart.clear()

        comparison_chart.set_title(
            "Monthly Income vs Expense"
        )

        comparison_chart.set_xlabel(
            "Month"
        )

        comparison_chart.set_ylabel(
            "Amount (₹)"
        )

        if months:

            x_values = list(
                range(len(months))
            )

            width = 0.35

            income_positions = [
                x - width / 2
                for x in x_values
            ]

            expense_positions = [
                x + width / 2
                for x in x_values
            ]

            comparison_chart.bar(
                income_positions,
                monthly_incomes,
                width=width,
                label="Income"
            )

            comparison_chart.bar(
                expense_positions,
                monthly_expenses,
                width=width,
                label="Expense"
            )

            comparison_chart.set_xticks(
                x_values
            )

            comparison_chart.set_xticklabels(
                months,
                rotation=30
            )

            comparison_chart.legend()

        else:

            comparison_chart.text(
                0.5,
                0.5,
                "No monthly data available",
                ha="center",
                va="center"
            )

        comparison_figure.tight_layout()

        comparison_canvas.draw()

        cursor.close()
        connection.close()

        main_canvas.configure(
            scrollregion=main_canvas.bbox("all")
        )

    # =================================================
    # BACK BUTTON
    # =================================================

    def go_back():

        main_canvas.unbind_all(
            "<MouseWheel>"
        )

        analysis_window.destroy()

        dashboard.deiconify()

    back_button = tk.Button(
        content_frame,
        text="BACK TO DASHBOARD",
        font=("Arial", 10, "bold"),
        width=20,
        height=2,
        command=go_back
    )

    back_button.pack(
        pady=30
    )

    # =================================================
    # LOAD DATA
    # =================================================

    load_analysis()
