from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, status, Depends, Query

from app.database.monitor import MonitorManager
from app.database.models import Monitor, User
from app.database.query_builder import QueryBuilder
from app.config import Settings, get_settings
from app.auth.auth import get_auth_user

router = APIRouter(
    prefix="/monitorings",
    tags=["monitorings"]
)


@router.get("/steps", response_model=list[Monitor], status_code=status.HTTP_200_OK)
async def read_steps(
        settings: Annotated[Settings, Depends(get_settings)],
        user: Annotated[User, Depends(get_auth_user)],
        from_date: Annotated[datetime | None, Query(
            title="Initial datetime (from datetime)",
            description="Initial UTC ISO-8601 datetime for the tasks to search")] = None,
        to_date: Annotated[datetime | None, Query(
            title="End datetime (to datetime)",
            description="End UTC ISO-8601 datetime for the tasks to search")] = None
) -> list[Monitor]:
    query_builder: QueryBuilder = QueryBuilder()
    db_manager: MonitorManager = MonitorManager(settings, user)

    if from_date:
        query_builder.from_date(from_date)
    if to_date:
        query_builder.to_date(to_date)

    db_manager.add_query_builder(query_builder)

    return db_manager.get_monitor_with_steps()
