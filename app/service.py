from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.schemtodo import TodoCreateSchema , TodoUpdateSchema
from app.database.models import TodoModel , UserModel
from app.schemas.schemuser import UserCreateSchema ,  UserUpdateSchema
from sqlalchemy.orm import selectinload
from app.security.password import hash_password

class TodoService:
    
    @staticmethod
    async def create_todo(todo : TodoCreateSchema , session : AsyncSession , user_id : int):
        user = await session.get(UserModel, user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        task_data = todo.model_dump()
        task_data["user_id"] = user_id
        task = TodoModel(**task_data)
        session.add(task)
        await session.commit()
        await session.refresh(task)
        
        return task
      
    @staticmethod
    async def get_todos(session : AsyncSession , user_id : int ):
        stmt = select(UserModel).options(selectinload(UserModel.todos)).where(UserModel.id == user_id)
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return list(user.todos)
    
    @staticmethod
    async def update_todo(todo_id: int, todo: TodoUpdateSchema, session: AsyncSession, user_id: int):
        task = await session.get(TodoModel, todo_id)

        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Todo not found or access denied")

        if todo.title is not None:
            task.title = todo.title
        if todo.description is not None:
            task.description = todo.description

        await session.commit()
        await session.refresh(task)

        return task
    
    @staticmethod
    async def delete_todo(session: AsyncSession, todo_id: int, user_id: int):
        task = await session.get(TodoModel, todo_id)

        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Todo not found or access denied")
        
        await session.delete(task)
        await session.commit()

        return {"detail": "Todo deleted successfully"}
        
  
  
  
  

class UserAlreadyExistsError(Exception):
    """Выбрасывается, если пользователь уже существует"""
    pass
  
  
        
class UserService:
    
    @staticmethod
    async def create_user(session : AsyncSession , user : UserCreateSchema):
        data_dict = user.model_dump()
        data_dict["password"] = hash_password(data_dict["password"])
        dict = UserModel(**data_dict)
        session.add(dict)
        await session.commit()
        await session.refresh(dict)
        
        return dict
    
    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> UserModel:
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await session.execute(stmt)
        user_obj = result.scalar_one_or_none()
        
        if not user_obj:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user_obj
        
    @staticmethod
    async def update_user(session: AsyncSession, user_id: int, data: UserUpdateSchema) -> UserModel:
        user = await session.get(UserModel, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = data.model_dump(exclude_none=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def delete_user(session: AsyncSession, user_id: int) -> dict:
        user = await session.get(UserModel, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        await session.delete(user)
        await session.commit()
        return {"deleted": True}
    
    @staticmethod
    async def get_user_by_username(username: str, session: AsyncSession): 
        stmt = select(UserModel).where(UserModel.username == username)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
    

        
        
        
        
    
    
        
    
    
    