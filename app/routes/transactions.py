from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime

from app.models.database import get_db, Transaction, User, TransactionType
from app.core.security import AuthService

router = APIRouter()


class TransactionCreate(BaseModel):
    amount: float
    description: str = "No description"
    category: str = ""
    transaction_type: str = "INCOME"

    @field_validator("transaction_type")
    @classmethod
    def validate_transaction_type(cls, v):
        v = v.upper()
        if v not in ["INCOME", "EXPENSE"]:
            raise ValueError("transaction_type must be INCOME or EXPENSE")
        return v


class TransactionResponse(BaseModel):
    id: int
    amount: float
    description: str
    category: str
    transaction_type: str
    date: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    try:
        db_type = (
            TransactionType.INCOME.value
            if transaction.transaction_type.upper() == "INCOME"
            else TransactionType.EXPENSE.value
        )

        new_transaction = Transaction(
            amount=transaction.amount,
            description=transaction.description,
            category=transaction.category,
            transaction_type=db_type,
            user_id=current_user.id,
            date=datetime.utcnow()
        )

        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

        return {
            "id": new_transaction.id,
            "amount": new_transaction.amount,
            "description": new_transaction.description,
            "category": new_transaction.category,
            "transaction_type": new_transaction.transaction_type,
            "date": new_transaction.date,
            "user_id": new_transaction.user_id,
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Transaction error: {str(e)}")


@router.get("/", response_model=List[TransactionResponse])
async def get_transactions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return [
        {
            "id": t.id,
            "amount": t.amount,
            "description": t.description,
            "category": t.category,
            "transaction_type": t.transaction_type,
            "date": t.date,
            "user_id": t.user_id,
        }
        for t in transactions
    ]


@router.get("/summary")
async def get_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user)
):
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == TransactionType.INCOME.value
    ).scalar() or 0.0

    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == current_user.id,
        Transaction.transaction_type == TransactionType.EXPENSE.value
    ).scalar() or 0.0

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": total_income - total_expense
    }