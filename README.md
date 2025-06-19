# SQL Command Executor Web App

This project is a lightweight SQL command executor built with **Flask** and **SQLite**, allowing users to run SQL queries through a web interface. It also displays query results, execution history, and offers a reset function to drop all tables.

## Features

- 📝 Execute multiple SQL queries via a textarea.
- 📊 Display query results in a table format.
- 🧾 Maintain session-based history of all executed queries.
- 🧹 Reset the database (drops all tables).
- 📋 Automatically lists all existing table names.

## Technologies Used

- Python 3.x
- Flask
- Flask-SQLAlchemy
- SQLite (via SQLAlchemy)
- HTML + Jinja2 Templates (UI Layer)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sql-executor-app.git
cd sql-executor-app
