from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_session
from app.service import UserService
from app.security.jwt import user_acces_token
from fastapi.security import OAuth2PasswordRequestForm
from app.security.password import verify_password

router = APIRouter(prefix="/login", tags=["Verification"])


@router.post("/" , include_in_schema=False)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    user = await UserService.get_user_by_username(
        form_data.username,
        session
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = user_acces_token(user.id)
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": token,
        "token_type": "bearer"
    }

