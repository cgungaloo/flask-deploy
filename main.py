from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from db.database import SessionLocal, engine
from models.models import Base, User
from schemas.schemas import UserCreate
import datetime

app = FastAPI()

# Create DB tables on startup (for demo only)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency to get DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/")
def root():
    return {"message": f"Hello from FastAPI in Docker/Heroku! {datetime.datetime.now(datetime.timezone.utc)}"}

@app.get("/users")
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@app.post("/users")
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(name=user.name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
