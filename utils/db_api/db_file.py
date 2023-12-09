from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, update
from utils.db_api.users import Users
from utils.db_api.base import Base



class DataBase:
    def __init__(self, database):
        self.database = database

    async def check_start(self):
        engine = create_async_engine(url=self.database, echo=False)
        session = async_sessionmaker(engine, expire_on_commit=False)
        
        
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async with session() as cursor:
            self.cursor = cursor

    
    async def add_user(self, user_id: int) -> None:
        await self.cursor.merge(Users(user_id=user_id))
        await self.cursor.commit()


    async def get_status(self, user_id: int) -> bool:
        sql = select(Users).where((Users.user_id == user_id) & (Users.status == 1))
        f = await self.cursor.execute(sql)
        return f.fetchone()
    
    async def set_status(self, user_id: int) -> None:
        sql = update(Users).where(Users.user_id == user_id).values(status = 1)
        await self.cursor.execute(sql)
        await self.cursor.commit()
