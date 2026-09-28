# Simple Banking Account API

A REST API built with FastAPI and MongoDB that manages bank accounts. The API supports creating accounts, checking balances, depositing money, withdrawing money, updating account holders, and closing accounts.

## Technologies Used

- Python
- FastAPI
- MongoDB
- PyMongo
- Pydantic
- Uvicorn

## Features

- Create a bank account
- List all accounts
- View an account by ID
- Update account holder information
- Close an account
- Deposit money
- Withdraw money
- Prevent negative balances
- Prevent duplicate account numbers
- Validate positive deposit and withdrawal amounts
- Use MongoDB `$inc` for atomic balance updates

## Project Structure

```text
banking-account-api/
│
├── database.py
├── examples.md
├── main.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
└── venv/