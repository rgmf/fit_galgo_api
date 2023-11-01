from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, status, Depends, Query

from app.database.activities import ActivitiesManager
from app.database.models import Activity, User
from app.database.query_builder import QueryBuilder
from app.config import Settings, get_settings
from app.auth.auth import get_auth_user

router = APIRouter(
    prefix="/activities",
    tags=["activities"]
)


@router.get("/", response_model=list[Activity], status_code=status.HTTP_200_OK)
async def read_activities(
        settings: Annotated[Settings, Depends(get_settings)],
        user: Annotated[User, Depends(get_auth_user)],
        from_date: Annotated[datetime | None, Query(
            title="Initial datetime (from datetime)",
            description="Initial UTC ISO-8601 datetime for the tasks to search")] = None,
        to_date: Annotated[datetime | None, Query(
            title="End datetime (to datetime)",
            description="End UTC ISO-8601 datetime for the tasks to search")] = None
) -> list[Activity]:
    db_manager: ActivitiesManager = ActivitiesManager(settings, user)

    if not from_date and not to_date:
        return db_manager.get()

    query_builder: QueryBuilder = QueryBuilder()
    if from_date:
        query_builder.gte("session.timestamp", from_date)
    if to_date:
        query_builder.lte("session.timestamp", to_date)

    return db_manager.filter(query_builder)
