from fastapi import APIRouter

router = APIRouter()

@router.get("/prices")
async def get_crypto_prices():
    return {"msg": "Crypto prices endpoint"}