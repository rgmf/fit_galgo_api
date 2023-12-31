from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, status, Depends, Query

from app.database.activities import ActivitiesManager
from app.database.models import ActivityOut, User
from app.database.query_builder import QueryBuilder
from app.config import Settings, get_settings
from app.auth.auth import get_auth_user

router = APIRouter(
    prefix="/activities",
    tags=["activities"]
)


@router.get("/", response_model=ActivityOut, status_code=status.HTTP_200_OK)
async def read_activities(
        settings: Annotated[Settings, Depends(get_settings)],
        user: Annotated[User, Depends(get_auth_user)],
        from_date: Annotated[datetime | None, Query(
            title="Initial datetime (from datetime)",
            description="Initial UTC ISO-8601 datetime for filtering")] = None,
        to_date: Annotated[datetime | None, Query(
            title="End datetime (to datetime)",
            description="End UTC ISO-8601 datetime for filtering")] = None
) -> ActivityOut:
    query_builder: QueryBuilder = QueryBuilder()
    db_manager: ActivitiesManager = ActivitiesManager(settings, user)

    if from_date:
        query_builder.from_date(from_date)
    if to_date:
        query_builder.to_date(to_date)

    db_manager.add_query_builder(query_builder)

    return ActivityOut(data=db_manager.get())
