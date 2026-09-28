from pydantic import BaseModel, Field


class Account(BaseModel):
    account_holder: str
    account_number: str
    balance: float = Field(default=0, ge=0)

class AccountUpdate(BaseModel):
    account_holder: str

class MoneyRequest(BaseModel):
    amount: float = Field(gt=0)