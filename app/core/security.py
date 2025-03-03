from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from typing import Optional
from .config import settings

FLIC_TOKEN_HEADER = APIKeyHeader(name="Flic-Token", auto_error=False)

async def verify_token(flic_token: Optional[str] = Security(FLIC_TOKEN_HEADER)) -> bool:
    if not flic_token:
        raise HTTPException(
            status_code=401,
            detail="Missing Flic-Token header"
        )
    
    if flic_token != settings.FLIC_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid Flic-Token"
        )
    
    return True

def get_token_header():
    return {"Flic-Token": settings.FLIC_TOKEN} 