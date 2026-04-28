from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import admin
from app.routes.auth import router as auth_router
from app.routes.transactions import router as transactions_router
from app.models.database import Base, engine

app = FastAPI(title="Finance Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {"message": "Finance Tracker API is running!"}


Base.metadata.create_all(bind=engine)