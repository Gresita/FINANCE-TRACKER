from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, transactions
from . import auth, transactions
# Vetëm importoni crypto nëse e keni krijuar file-in
#from app.routes import crypto  

app = FastAPI(title="🚀 Finance Tracker Pro")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
# Shto crypto router vetëm nëse ekziston crypto.py
# app.include_router(crypto.router, prefix="/crypto", tags=["crypto"])

@app.get("/")
async def root():
    return {"message": "🚀 Finance Tracker Pro API - Ready!"}