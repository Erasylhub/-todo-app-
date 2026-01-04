from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey
from app.database.db import Base

class TodoModel(Base):
    __tablename__ = "todos"
    
    id:  Mapped[int] = mapped_column(primary_key= True)
    title:  Mapped[str] = mapped_column(String)
    description:  Mapped[str] = mapped_column(String , nullable= True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    user: Mapped["UserModel"] = relationship(back_populates="todos")
    
class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    
    todos: Mapped[list["TodoModel"]] = relationship(back_populates="user")
    
    
    

    
    