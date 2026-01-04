from fastapi import APIRouter , Depends
from app.schemas.schemtodo import TodoCreateSchema , TodoUpdateSchema , TodoReadSchema
from typing import Annotated
from app.database.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.service import TodoService 
from app.security.jwt import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["Todo"]
)

@router.post("/" , response_model= TodoReadSchema)
async def post_todo(
                    todo: TodoCreateSchema,
                    session: AsyncSession = Depends(get_session),
                    user_id: int = Depends(get_current_user)
                    ):
    
    return await TodoService.create_todo(todo , session , user_id)

@router.get("/" , response_model=list[TodoReadSchema])
async def get_todos(user_id: int = Depends(get_current_user),
                    session: AsyncSession = Depends(get_session)):
    
    todos = await TodoService.get_todos(session, user_id)  
    return todos

@router.put("/{todo_id}")
async def update_todo_route(
    todo_id: int,
    todo: TodoUpdateSchema,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    
    return await TodoService.update_todo(todo_id, todo, session, user_id)

@router.delete("/{todo_id}")
async def delete_todo_route(
    todo_id: int,
    user_id: int = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    return await TodoService.delete_todo(session, todo_id, user_id)

