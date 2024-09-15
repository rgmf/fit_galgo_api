from typing import Annotated
from datetime import datetime

from fastapi import APIRouter, status, Depends, Query

from app.database.monitor import MonitorManager
from app.database.sleep import SleepManager
from app.database.hrv import HrvManager
from app.database.models import MonitorOut, SleepOut, HrvOut, User
from app.database.query_builder import QueryBuilder
from app.config import Settings, get_settings
from app.auth.auth import get_auth_user

router = APIRouter(
    prefix="/monitorings",
    tags=["monitorings"]
)


@router.get("/steps/", response_model=MonitorOut, status_code=status.HTTP_200_OK)
async def read_steps(
        settings: Annotated[Settings, Depends(get_settings)],
        user: Annotated[User, Depends(get_auth_user)],
        from_date: Annotated[datetime | None, Query(
            title="Initial datetime (from datetime)",
            description="Initial UTC ISO-8601 datetime for filtering")] = None,
        to_date: Annotated[datetime | None, Query(
            title="End datetime (to datetime)",
            description="End UTC ISO-8601 datetime for filtering")] = None
) -> MonitorOut:
    query_builder: QueryBuilder = QueryBuilder()
    db_manager: MonitorManager = MonitorManager(settings, user)

    if from_date:
        query_builder.from_date(from_date)
    if to_date:
        query_builder.to_date(to_date)

    db_manager.add_query_builder(query_builder)

    return MonitorOut(data=db_manager.get_monitor_with_steps())


@router.get("/sleep/", response_model=SleepOut, status_code=status.HTTP_200_OK)
async def read_sleep(
        settings: Annotated[Settings, Depends(get_settings)],
        user: Annotated[User, Depends(get_auth_user)],
        from_date: Annotated[datetime | None, Query(
            title="Initial datetime (from datetime)",
            description="Initial UTC ISO-8601 datetime for filtering")] = None,
        to_date: Annotated[datetime | None, Query(
            title="End datetime (to datetime)",
            description="End UTC ISO-8601 datetime for filtering")] = None
) -> SleepOut:
    query_builder: QueryBuilder = QueryBuilder()
    db_manager: SleepManager = SleepManager(settings, user)

    if from_date:
        query_builder.from_date(from_date)
    if to_date:
        query_builder.to_date(to_date)

    db_manager.add_query_builder(query_builder)

    return SleepOut(data=db_manager.get())


@router.get("/hrv/", response_model=HrvOut, status_code=status.HTTP_200_OK)
async def read_hrv(
        settings: Annotated[Settings, Depends(get_settings)],
        user: Annotated[User, Depends(get_auth_user)],
        from_date: Annotated[datetime | None, Query(
            title="Initial datetime (from datetime)",
            description="Initial UTC ISO-8601 datetime for filtering")] = None,
        to_date: Annotated[datetime | None, Query(
            title="End datetime (to datetime)",
            description="End UTC ISO-8601 datetime for filtering")] = None
) -> HrvOut:
    query_builder: QueryBuilder = QueryBuilder()
    db_manager: HrvManager = HrvManager(settings, user)

    if from_date:
        query_builder.from_date(from_date)
    if to_date:
        query_builder.to_date(to_date)

    db_manager.add_query_builder(query_builder)

    return HrvOut(data=db_manager.get())
