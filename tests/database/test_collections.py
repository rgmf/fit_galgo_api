from datetime import datetime

from fit_galgo.fit.models import (
    Activity,
    FileId,
    Session,
    Monitor,
    MonitoringInfo,
    Hrv,
    HrvStatusSummary,
    Sleep,
    SleepAssessment,
    SleepLevel
)

from app.database.files import FilesManager


def test_insert_activity(db_manager: FilesManager):
    time_created: datetime = datetime.now()
    file_id: FileId = FileId(
        type="activity",
        time_created=time_created
    )
    session: Session = Session(
        message_index=0,
        timestamp=datetime.now(),
        start_time=datetime.now(),
        total_elapsed_time=60.0,
        total_timer_time=60.0,
        sport="cycling",
        sub_sport="road cycling"
    )
    activity: Activity = Activity(
        fit_file_path="file_path.fit",
        file_id=file_id,
        session=session
    )

    id: str = db_manager.insert(activity)
    assert isinstance(id, str)

    time_created_str: str = time_created.strftime("%Y%m%d%H%M%S")
    assert id == f"activity_{time_created_str}"

    assert len(list(db_manager.get("activity"))) == 1


def test_insert_monitoring(db_manager: FilesManager):
    time_created: datetime = datetime.now()
    monitoring_info: MonitoringInfo = MonitoringInfo(timestamp=datetime.now())
    all_subtypes: list[str] = ["monitoring_a", "monitoring_b", "monitoring"]

    for type_ in all_subtypes:
        file_id: FileId = FileId(
            type=type_,
            time_created=time_created
        )
        monitor: Monitor = Monitor(
            fit_file_path="file_path.fit",
            file_id=file_id,
            monitoring_info=monitoring_info,
            monitorings=[]
        )

        id: str = db_manager.insert(monitor)
        assert isinstance(id, str)

        time_created_str: str = time_created.strftime("%Y%m%d%H%M%S")
        assert id == f"{type_}_{time_created_str}"

    assert len(list(db_manager.get("monitoring"))) == len(all_subtypes)


def test_insert_hrv(db_manager: FilesManager):
    time_created: datetime = datetime.now()
    summary: HrvStatusSummary = HrvStatusSummary(
        timestamp=datetime.now(),
        status="invented"
    )
    all_subtypes: list[str] = [68, "68"]

    for type_ in all_subtypes:
        file_id: FileId = FileId(
            type=type_,
            time_created=time_created
        )
        hrv: Hrv = Hrv(
            fit_file_path="file_path.fit",
            file_id=file_id,
            summary=summary
        )

        id: str = db_manager.insert(hrv)
        if id is not None:
            time_created_str: str = time_created.strftime("%Y%m%d%H%M%S")
            assert id == f"{type_}_{time_created_str}"

    assert len(list(db_manager.get("hrv"))) == 1


def test_insert_sleep(db_manager: FilesManager):
    time_created: datetime = datetime.now()
    assessment: SleepAssessment = SleepAssessment()
    level: SleepLevel = SleepLevel(timestamp=datetime.now())
    all_subtypes: list[str] = [49, "49"]

    for type_ in all_subtypes:
        file_id: FileId = FileId(
            type=type_,
            time_created=time_created
        )
        sleep: Sleep = Sleep(
            fit_file_path="file_path.fit",
            file_id=file_id,
            assessment=assessment,
            levels=[level, level]
        )

        id: str = db_manager.insert(sleep)
        if id is not None:
            time_created_str: str = time_created.strftime("%Y%m%d%H%M%S")
            assert id == f"{type_}_{time_created_str}"

    assert len(list(db_manager.get("sleep"))) == 1
