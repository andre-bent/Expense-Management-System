import pytest
from unittest.mock import patch, MagicMock
from backend.db_helper import (
    fetch_expenses_for_date,
    fetch_expenses_between_dates,
    insert_expense,
    delete_expenses_for_date,
    fetch_expense_summary,
    fetch_expense_month_summary,
)

@pytest.fixture
def mock_cursor():
    """Fixture to mock the database cursor."""
    mock_conn = MagicMock()
    mock_cursor = mock_conn.cursor.return_value
    return mock_cursor

@patch("backend.db_helper.get_db_cursor")
def test_fetch_expenses_for_date(mock_get_db_cursor, mock_cursor):
    """Test fetch_expenses_for_date function."""
    mock_get_db_cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{"expense_date": "2025-05-26", "amount": 25.50, "category": "Food", "notes": "sushi lunch"}]

    result = fetch_expenses_for_date("2025-05-26")
    assert result == [{"expense_date": "2025-05-26", "amount": 25.50, "category": "Food", "notes": "sushi lunch"}]
    mock_cursor.execute.assert_called_once_with("SELECT * FROM expenses WHERE expense_date = %s", ("2025-05-26",))

@patch("backend.db_helper.get_db_cursor")
def test_fetch_expenses_between_dates(mock_get_db_cursor, mock_cursor):
    """Test fetch_expenses_between_dates function."""
    mock_get_db_cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{"expense_date": "2025-05-25", "amount": 30.00, "category": "Travel", "notes": "uber fare"}]

    result = fetch_expenses_between_dates("2025-05-25", "2025-05-26")
    assert result == [{"expense_date": "2025-05-25", "amount": 30.00, "category": "Travel", "notes": "uber fare"}]
    mock_cursor.execute.assert_called_once_with(
        "SELECT * FROM expenses WHERE expense_date BETWEEN %s and %s", ("2025-05-25", "2025-05-26")
    )

@patch("backend.db_helper.get_db_cursor")
def test_insert_expense(mock_get_db_cursor, mock_cursor):
    """Test insert_expense function."""
    mock_get_db_cursor.return_value.__enter__.return_value = mock_cursor

    insert_expense("2025-05-26", 20.00, "Entertainment", "Movie night")
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
        ("2025-05-26", 20.00, "Entertainment", "Movie night")
    )

@patch("backend.db_helper.get_db_cursor")
def test_delete_expenses_for_date(mock_get_db_cursor, mock_cursor):
    """Test delete_expenses_for_date function."""
    mock_get_db_cursor.return_value.__enter__.return_value = mock_cursor

    delete_expenses_for_date("2025-05-26")
    mock_cursor.execute.assert_called_once_with("DELETE FROM expenses WHERE expense_date = %s", ("2025-05-26",))

@patch("backend.db_helper.get_db_cursor")
def test_fetch_expense_summary(mock_get_db_cursor, mock_cursor):
    """Test fetch_expense_summary function."""
    mock_get_db_cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{"category": "Food", "total": 50.00}]

    result = fetch_expense_summary("2025-05-01", "2025-05-31")
    print(mock_cursor.execute.call_args)
    assert result == [{"category": "Food", "total": 50.00}]
    mock_cursor.execute.assert_called_once_with(
        "SELECT category, ROUND(SUM(amount),2) as total FROM expenses WHERE expense_date BETWEEN %s and %s GROUP BY category;",
        ("2025-05-01", "2025-05-31")
    )

@patch("backend.db_helper.get_db_cursor")
def test_fetch_expense_month_summary(mock_get_db_cursor, mock_cursor):
    """Test fetch_expense_month_summary function."""
    mock_get_db_cursor.return_value.__enter__.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{"y_month": "2025-05", "category": "Food", "total_amount": 150.00}]

    result = fetch_expense_month_summary("2025-05-01", "2025-05-31")
    print(mock_cursor.execute.call_args)
    assert result == [{"y_month": "2025-05", "category": "Food", "total_amount": 150.00}]
    mock_cursor.execute.assert_called_once_with(
        "SELECT DATE_FORMAT(expense_date, '%Y-%m') AS y_month, category, ROUND(SUM(amount),2) AS total_amount FROM expenses WHERE expense_date BETWEEN %s and %s GROUP BY y_month, category ORDER BY y_month, category;",
        ("2025-05-01", "2025-05-31")
    )

