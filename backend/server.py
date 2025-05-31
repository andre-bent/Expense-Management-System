from fastapi import FastAPI, HTTPException
from datetime import date
import collections
from backend import db_helper
from pydantic import BaseModel

app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    notes: str

class DateExpense(BaseModel):
    expense_date: date
    amount: float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date


@app.get("/expenses/{expense_date}", response_model=list[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper.fetch_expenses_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expenses from the database.")

    return expenses


@app.get("/view_expenses/{start_date}/{end_date}", response_model=list[DateExpense])
def get_expenses_for_dates(start_date: date, end_date: date):
    expenses = db_helper.fetch_expenses_between_dates(start_date, end_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database")

    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses:list[Expense]):
    db_helper.delete_expenses_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date, expense.amount, expense.category, expense.notes)

    return {"message": "Expenses updated successfully"}


@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database")

    total = sum([row['total'] for row in data])

    breakdown = {}
    for row in data:
        percentage = round(((row['total'])/total*100),2) if total != 0 else 0
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }
    return breakdown


@app.post("/analytics/stack")
def get_analytics_stack(date_range: DateRange):
    data = db_helper.fetch_expense_month_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail="Failed to retrieve expense summary from the database")

    # Extract all unique categories
    categories = {entry["category"] for entry in data}

    # Create a nested dictionary with default values
    nested_dict = collections.defaultdict(lambda: {category: 0 for category in categories})

    # Populate the dictionary with actual values
    for entry in data:
        nested_dict[entry["y_month"]][entry["category"]] = entry["total_amount"]

    # Convert defaultdict to a normal dictionary
    nested_dict = dict(nested_dict)

    return nested_dict




