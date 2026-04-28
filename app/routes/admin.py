from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel

from app.models.database import get_db, User, Transaction
from app.core.security import AuthService

router = APIRouter()


# 🔐 ADMIN CHECK
def get_current_admin(current_user: User = Depends(AuthService.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


# 📊 SUMMARY
@router.get("/summary")
def admin_summary(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    total_users = db.query(User).count()
    total_transactions = db.query(Transaction).count()

    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.transaction_type == "income"
    ).scalar() or 0

    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.transaction_type == "expense"
    ).scalar() or 0

    return {
        "total_users": total_users,
        "total_transactions": total_transactions,
        "total_income": total_income,
        "total_expense": total_expense,
        "global_balance": total_income - total_expense
    }


# 👥 GET USERS
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "created_at": u.created_at
        }
        for u in users
    ]


# 🔁 UPDATE ROLE
class UpdateUserRole(BaseModel):
    role: str


@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    data: UpdateUserRole,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    if data.role not in ["user", "admin"]:
        raise HTTPException(status_code=400, detail="Invalid role")

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.role = data.role
    db.commit()
    db.refresh(user)

    return {"message": "Role updated successfully"}


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="You cannot delete yourself")

    # delete related transactions
    db.query(Transaction).filter(Transaction.user_id == user_id).delete()

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}