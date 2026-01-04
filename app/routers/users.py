from fastapi import APIRouter , Depends , HTTPException 
from app.database.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.service import UserService , UserAlreadyExistsError
from app.schemas.schemuser import UserCreateSchema , UserReadSchema , UserUpdateSchema
from app.security.jwt import get_current_user
from app.database.models import UserModel
router = APIRouter(prefix="/users",
                   tags=["User"])


@router.post("/" , response_model= UserReadSchema)
async def create_user(todo: UserCreateSchema,
                    session: AsyncSession = Depends(get_session)):
    try:
        return await UserService.create_user(session, todo)
    except UserAlreadyExistsError:  
        raise HTTPException(
            status_code=400,
            detail={"error": "Пользователь уже существует"}
        )

@router.get("/", response_model=UserReadSchema)
async def get_user(session: AsyncSession = Depends(get_session),
                   user_id: int = Depends(get_current_user)):
    return await UserService.get_user_by_id(session, user_id)

@router.patch("/", response_model=UserReadSchema)
async def update_user(data: UserUpdateSchema ,user_id: int = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await UserService.update_user(session, user_id, data)

@router.delete("/")
async def delete_user(user_id: int = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    return await UserService.delete_user(session, user_id)