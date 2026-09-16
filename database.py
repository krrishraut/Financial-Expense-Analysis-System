import mysql.connector


def connect_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_MYSQL_PASSWORD",
            database="financial_expense_tracker"
        )

        print("MySQL database connected successfully.")

        return connection

    except mysql.connector.Error as error:
        print("Database connection failed.")
        print("Error:", error)

        return None
