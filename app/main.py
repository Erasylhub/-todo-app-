from fastapi import FastAPI
from app.routers.todos import router as task_router
from app.routers.users import router as user_router
from app.routers.verification import router as verif_router
from app.database.db import async_engine as engine, Base
 


app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)
app.include_router(verif_router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)