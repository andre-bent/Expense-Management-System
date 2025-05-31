# Expense Management System

## Overview
The Expense Management System is a full-stack Python application designed to streamline expense tracking using a Streamlit frontend, FastAPI backend, and a MySQL database. This system allows users to log, analyze, and manage expenses efficiently through an intuitive interface and powerful data processing.

## Key Features
✅ **Interactive Expense Entry** – Users can add/update expenses via a dynamic Streamlit UI.  
✅ **Visual Expense Analytics** – View spending trends through stacked bar charts and donut charts.  
✅ **FastAPI Backend** – Handles expense data processing and retrieval efficiently.  
✅ **MySQL Database Integration** – Securely stores and manages expense records for long-term tracking.  
✅ **Logging Mechanism** – Backend logs track database activity for auditing and debugging.

## Project Structure
    expense-management-system/
    │── frontend/               # Streamlit application code
    │   ├── main.py             # Main file for executing Streamlit front end
    │   ├── add_update_ui.py    # Handles adding/updating expenses and displaying a table
    │   ├── analytics_ui.py     # Displays analytics via bar charts & donut charts
    │
    │── backend/                # FastAPI backend server code
    │   ├── server.py           # Defines FastAPI API endpoints
    │   ├── db_helper.py        # Sets up MySQL database connection & query execution
    │   ├── logging_setup.py    # Backend logging configuration
    │   ├── server.log          # Log file storing backend database activity
    │
    │── tests/                  # Unit tests for backend  
    │── requirements.txt        # List of required Python dependencies  
    │── README.md               # Project documentation

## Setup Instructions
1. **Clone Repository:** 
    ``` bash
    git clone https://github.com/yourusername/expense-management-system
    cd expense-management-system
    ```
2. **Install Dependencies:**
    ``` commandline
    pip install -r requirements.txt
    ```
3. **Set up MySQL database:**  
    Ensure you have MySQL installed and running. Then, create the required database and table:
    ``` Sql
    CREATE DATABASE expense_manager;
    USE expense_manager;

    CREATE TABLE expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        expense_date DATE NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        category VARCHAR(50),
        notes TEXT
    );
   ```
   Modify db_helper.py to configure your MySQL connection parameters
   ``` python
   import mysql.connector

   conn = mysql.connector.connect(
       host="your_mysql_host",
       user="your_username",
       password="your_password",
       database="expense_manager"
   )
   ```

4. **Run the FastAPI Server**
   ``` commandline
   uvicorn backend.server:app --reload
   ```
5. **Run the Streamlit frontend**
   ``` commandline
   streamlit run frontend/main.py
   ```

## Additional Information  
📌 **Technologies Used**
- Frontend: Streamlit
- Backend: FastAPI
- Database: MySQL
- Data Processing: Python  

📌 **Future Enhancement**  
🔹 Implement authentication & user roles  
🔹 Add export functionality for expense reports  
🔹 Integrate AI-based expense categorization




