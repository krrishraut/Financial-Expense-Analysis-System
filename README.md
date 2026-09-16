# Financial Expense Analysis System

A desktop-based financial expense management and analysis system built using Python, Tkinter, and MySQL.

## Features

- User Login and Signup
- Add, View, Update, and Delete Transactions
- Income and Expense Tracking
- Category-wise Expense Analysis
- Expense Distribution Visualization
- Monthly Financial Analysis
- Budget Management
- Budget vs Actual Expense Tracking
- Future Expense Prediction using Linear Regression
- Personalized Financial Recommendations

## Tech Stack

- Python
- Tkinter
- MySQL
- Pandas
- NumPy
- Matplotlib
- Scikit-learn

## Project Structure

```text
Financial-Expense-Analysis-System/
│
├── database.py
├── login.py
├── dashboard.py
├── transactions.py
├── analysis.py
├── budget.py
├── prediction.py
├── recommendations.py
├── .gitignore
└── README.md
```

## Database

The project uses a MySQL database named:

```text
financial_expense_tracker
```

Create the required database and tables in MySQL before running the application.

## How to Run

1. Install Python and MySQL.
2. Install the required Python packages:

```bash
pip install mysql-connector-python pandas numpy matplotlib scikit-learn
```

3. Configure your MySQL credentials in `database.py`.
4. Run:

```bash
python login.py
```

## Note

This project was developed as a BCA Data Science academic project.
