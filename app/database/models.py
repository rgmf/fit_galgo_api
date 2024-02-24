from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, computed_field
from fit_galgo.fit.models import (
    FileId as FitFileId,
    Session as FitSession,
    Workout as FitWorkout,
    WorkoutStep as FitWorkoutStep,
    Split as FitSplit,
    Set as FitSet,
    Lap as FitLap,
    MultiActivity as FitMultiActivity,
    Sleep as FitSleep,
    Hrv as FitHrv
)


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserIn(User):
    password: str


class UserDb(User):
    hashed_password: str

    @staticmethod
    def from_database_dict(user_dict):
        user_dict["hashed_password"] = user_dict["password"]
        return UserDb(**user_dict)


class Activity(BaseModel):
    _id: str
    username: str
    fit_file_path: str
    file_id: FitFileId
    zone_info: str
    session: FitSession
    workout: FitWorkout | None = None
    workout_steps: list[FitWorkoutStep] = []


class SplitsActivity(Activity):
    splits: list[FitSplit] | None = None


class SetsActivity(Activity):
    sets: list[FitSet] | None = None


class MultiActivity(FitMultiActivity):
    username: str


class ActivityOut(BaseModel):
    data: list[Activity | SetsActivity | SplitsActivity | MultiActivity]

    @computed_field
    @property
    def count(self) -> int:
        return len(self.data)


class Monitor(BaseModel):
    username: str
    datetime_utc: datetime
    total_steps: int
    total_distance: float
    total_calories: int
    zone_info: str | None = None

    @computed_field
    @property
    def datetime_local(self) -> datetime:
        tz: ZoneInfo | None = ZoneInfo(self.zone_info) if self.zone_info else None
        return self.datetime_utc.astimezone(tz)


class MonitorOut(BaseModel):
    data: list[Monitor]

    @computed_field
    @property
    def count(self) -> int:
        return len(self.data)


class Sleep(FitSleep):
    username: str


class SleepOut(BaseModel):
    data: list[Sleep]

    @computed_field
    @property
    def count(self) -> int:
        return len(self.data)


class Hrv(FitHrv):
    username: str


class HrvOut(BaseModel):
    data: list[Hrv]

    @computed_field
    @property
    def count(self) -> int:
        return len(self.data)
