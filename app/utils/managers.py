import mongomock
from pydantic import PositiveInt
from pymongo import ASCENDING
from sqlalchemy.orm import Session

from app.models.users.user_notify_settings import UserNotifySettings
from app.models.users.user_status import UserStatus
from app.utils.mongo import MongoContextManager

mongo_mock_client = mongomock.MongoClient()


async def make_user_reset(
    db_session: Session,
    user_status: UserStatus,
    user_settings: UserNotifySettings,
    user_telegram_id: PositiveInt,
    *,
    refresh_after_commit: bool = False,
) -> None:
    """
    Transactional function for reset user status and user notify settings.
    """

    user_status.authenticated = False
    db_session.add(user_status)
    user_settings.fill(user_telegram_id=user_telegram_id)
    db_session.add(user_settings)
    db_session.commit()

    if refresh_after_commit:
        db_session.refresh(user_status)
        db_session.refresh(user_settings)

    async with MongoContextManager("users_data", "cookies") as mongo:
        await mongo.delete_one({"user_telegram_id": user_telegram_id})

    for collection_name in ("marks", "news", "homeworks", "requests"):
        async with MongoContextManager(
            database="tracking_data", collection=collection_name
        ) as mongo:
            await mongo.delete_many({"id": user_telegram_id})


async def make_user_authorized(
    db_session: Session,
    user_status: UserStatus,
    user_telegram_id: PositiveInt,
    cookies: dict[str, str],
    *,
    refresh_after_commit: bool = False,
) -> None:
    user_status.authenticated = True
    db_session.add(user_status)
    db_session.commit()

    if refresh_after_commit:
        db_session.refresh(user_status)

    async with MongoContextManager("users_data", "cookies") as mongo:
        await mongo.insert_one(
            {"user_telegram_id": user_telegram_id, "cookies": cookies}
        )
        # create index for user_telegram_id
        await mongo.collection.create_index(
            [('user_telegram_id', ASCENDING)], unique=True
        )
