from fastapi import FastAPI, HTTPException
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError
from models import Account, AccountUpdate, MoneyRequest
from database import accounts_collection

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Banking Account API is running"}


@app.post("/accounts")
def create_account(account: Account):
    account_data = account.model_dump()

    try:
        result = accounts_collection.insert_one(account_data)

    except DuplicateKeyError:
        raise HTTPException(
            status_code=400,
            detail="Account number already exists"
        )

    return {
        "message": "Account created successfully",
        "id": str(result.inserted_id)
    }

@app.get("/accounts")
def get_accounts():
    accounts = list(accounts_collection.find())

    for account in accounts:
        account["id"] = str(account["_id"])
        del account["_id"]

    return accounts

@app.get("/accounts/{id}")
def get_account(id: str):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid account ID"
        )

    account = accounts_collection.find_one({"_id": object_id})

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    account["id"] = str(account["_id"])
    del account["_id"]

    return account

@app.put("/accounts/{id}")
def update_account(id: str, account: AccountUpdate):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid account ID"
        )

    result = accounts_collection.update_one(
        {"_id": object_id},
        {"$set": {"account_holder": account.account_holder}}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return {
        "message": "Account holder updated successfully"
    }

@app.delete("/accounts/{id}")
def delete_account(id: str):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid account ID"
        )

    result = accounts_collection.delete_one(
        {"_id": object_id}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return {
        "message": "Account closed successfully"
    }

@app.post("/accounts/{id}/deposit")
def deposit_money(id: str, money: MoneyRequest):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid account ID"
        )

    result = accounts_collection.update_one(
        {"_id": object_id},
        {"$inc": {"balance": money.amount}}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return {
        "message": "Money deposited successfully",
        "amount": money.amount
    }

@app.post("/accounts/{id}/withdraw")
def withdraw_money(id: str, money: MoneyRequest):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid account ID"
        )

    result = accounts_collection.update_one(
        {
            "_id": object_id,
            "balance": {"$gte": money.amount}
        },
        {
            "$inc": {"balance": -money.amount}
        }
    )

    if result.matched_count == 0:
        account = accounts_collection.find_one({"_id": object_id})

        if account is None:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    return {
        "message": "Money withdrawn successfully",
        "amount": money.amount
    }