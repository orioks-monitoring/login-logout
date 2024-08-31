from pymongo import ASCENDING

from app.utils.mongo import MongoContextManager


async def create_mongo_index_user_telegram_id() -> None:
    async with MongoContextManager("users_data", "cookies") as mongo:
        await mongo.collection.create_index(
            [("user_telegram_id", ASCENDING)],
            unique=True,
        )
