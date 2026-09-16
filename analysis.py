import tkinter as tk
from tkinter import ttk
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

    # =================================================
    # MOUSE SCROLL
    # =================================================

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

    title.pack(
        pady=(25, 5)
    )

    subtitle = tk.Label(
        content_frame,
        text="Analyze your income, expenses and savings",
        font=("Arial", 11),
        bg="#f4f6f8"
    )

    subtitle.pack(
        pady=(0, 20)
    )

    # =================================================
    # SUMMARY CARDS
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
    ).pack(
        pady=(20, 5)
    )

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
    ).pack(
        pady=(20, 5)
    )

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
    ).pack(
        pady=(20, 5)
    )

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
        padx=30
    )

    columns = (
        "Category",
        "Total Expense"
    )

    analysis_table = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=6
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
    # CHART BUTTONS
    # =================================================

    chart_button_title = tk.Label(
        content_frame,
        text="Data Visualizations",
        font=("Arial", 17, "bold"),
        bg="#f4f6f8"
    )

    chart_button_title.pack(
        pady=(25, 10)
    )

    chart_buttons_frame = tk.Frame(
        content_frame,
        bg="#f4f6f8"
    )

    chart_buttons_frame.pack(
        pady=5
    )

    # =================================================
    # CHART CONTAINER
    # =================================================

    chart_container = tk.Frame(
        content_frame,
        bg="#f4f6f8"
    )

    chart_container.pack(
        padx=30,
        pady=10
    )

    # =================================================
    # BAR CHART FRAME
    # =================================================

    bar_chart_frame = tk.Frame(
        chart_container,
        bg="white",
        bd=1,
        relief="solid",
        width=950,
        height=390
    )

    bar_chart_frame.pack_propagate(False)

    bar_figure = Figure(
        figsize=(9, 3.5),
        dpi=100
    )

    bar_chart = bar_figure.add_subplot(111)

    bar_canvas = FigureCanvasTkAgg(
        bar_figure,
        master=bar_chart_frame
    )

    bar_canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # =================================================
    # PIE CHART FRAME
    # =================================================

    pie_chart_frame = tk.Frame(
        chart_container,
        bg="white",
        bd=1,
        relief="solid",
        width=950,
        height=390
    )

    pie_chart_frame.pack_propagate(False)

    pie_figure = Figure(
        figsize=(9, 3.5),
        dpi=100
    )

    pie_chart = pie_figure.add_subplot(111)

    pie_canvas = FigureCanvasTkAgg(
        pie_figure,
        master=pie_chart_frame
    )

    pie_canvas.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    # =================================================
    # SHOW BAR CHART
    # =================================================

    def show_bar_chart():

        pie_chart_frame.pack_forget()

        bar_chart_frame.pack()

    # =================================================
    # SHOW PIE CHART
    # =================================================

    def show_pie_chart():

        bar_chart_frame.pack_forget()

        pie_chart_frame.pack()

    # =================================================
    # CHART BUTTONS
    # =================================================

    bar_button = tk.Button(
        chart_buttons_frame,
        text="CATEGORY EXPENSE",
        font=("Arial", 10, "bold"),
        width=22,
        height=2,
        command=show_bar_chart
    )

    bar_button.grid(
        row=0,
        column=0,
        padx=10
    )

    pie_button = tk.Button(
        chart_buttons_frame,
        text="EXPENSE DISTRIBUTION",
        font=("Arial", 10, "bold"),
        width=22,
        height=2,
        command=show_pie_chart
    )

    pie_button.grid(
        row=0,
        column=1,
        padx=10
    )

    # =================================================
    # MONTHLY FINANCIAL TABLE
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
    # LOAD DATA
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
        # CATEGORY DATA
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

        categories = []
        category_expenses = []

        for record in records:

            category = record[0]
            amount = float(record[1])

            categories.append(category)
            category_expenses.append(amount)

            analysis_table.insert(
                "",
                "end",
                values=(
                    category,
                    "₹ " + format(
                        amount,
                        ",.2f"
                    )
                )
            )

        # =================================================
        # BAR CHART
        # =================================================

        bar_chart.clear()

        bar_chart.set_title(
            "Category-wise Expense"
        )

        bar_chart.set_xlabel(
            "Category"
        )

        bar_chart.set_ylabel(
            "Expense (₹)"
        )

        if categories:

            bar_chart.bar(
                categories,
                category_expenses
            )

            bar_chart.tick_params(
                axis="x",
                rotation=30
            )

        else:

            bar_chart.text(
                0.5,
                0.5,
                "No expense data available",
                ha="center",
                va="center"
            )

        bar_figure.tight_layout()

        bar_canvas.draw()

        # =================================================
        # PIE CHART
        # =================================================

        pie_chart.clear()

        pie_chart.set_title(
            "Expense Distribution by Category"
        )

        if categories:

            pie_chart.pie(
                category_expenses,
                labels=categories,
                autopct="%1.1f%%",
                startangle=90
            )

            pie_chart.axis("equal")

        else:

            pie_chart.text(
                0.5,
                0.5,
                "No expense data available",
                ha="center",
                va="center"
            )

        pie_figure.tight_layout()

        pie_canvas.draw()

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

        for record in monthly_records:

            monthly_income = float(
                record[1]
            )

            monthly_expense = float(
                record[2]
            )

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
    # DEFAULT CHART
    # =================================================

    show_bar_chart()

    # =================================================
    # LOAD DATA
    # =================================================

    load_analysis()
