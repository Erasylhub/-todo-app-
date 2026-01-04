from pydantic import Field , BaseModel 
from typing import Optional

class TodoCreateSchema(BaseModel):
    title : str = Field(... , min_length= 2 , max_length= 100)
    description : Optional[str] = None
    
class TodoUpdateSchema(BaseModel):
    title : Optional[str] = None
    description : Optional[str] = None
    completed : Optional[bool] = None
    
class TodoReadSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: Optional[bool]

    class Config:
        orm_mode = True
        
        

        
    