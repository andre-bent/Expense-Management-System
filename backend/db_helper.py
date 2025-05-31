import mysql.connector
from contextlib import contextmanager
from backend.logging_setup import setup_logger


#For logging recording
logger = setup_logger('db_helper')

#SQL database connection
@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date = %s", (expense_date,))
        returned_expenses = cursor.fetchall()
        return returned_expenses

def fetch_expenses_between_dates(start_date, end_date):
    logger.info(f"fetch_expenses_between_dates called with start {start_date} and : {end_date}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("SELECT * FROM expenses WHERE expense_date BETWEEN %s and %s", (start_date, end_date))
        returned_expenses = cursor.fetchall()
        return returned_expenses

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
                       (expense_date, amount, category, notes)
        )

def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start: {start_date} and: {end_date}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute(
            "SELECT category, ROUND(SUM(amount),2) as total FROM expenses WHERE expense_date BETWEEN %s and %s GROUP BY category;",
                (start_date, end_date)
        )
        data = cursor.fetchall()
        return data

def fetch_expense_month_summary(start_date, end_date):
    logger.info(f"fetch_expense_month_summary called with start: {start_date} and: {end_date}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute(
            "SELECT DATE_FORMAT(expense_date, '%Y-%m') AS y_month, category, ROUND(SUM(amount),2) AS total_amount FROM expenses WHERE expense_date BETWEEN %s and %s GROUP BY y_month, category ORDER BY y_month, category;",
                (start_date, end_date)
        )
        data = cursor.fetchall()
        return data


