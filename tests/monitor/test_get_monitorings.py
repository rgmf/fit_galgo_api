from datetime import datetime, timedelta

from app.database.models import Monitor


def test_read_monitorings_steps(testclient):
    response = testclient.get("/monitorings/steps")
    assert response.status_code == 200

    assert len(response.json()) == 5

    for d in response.json():
        monitor: Monitor = Monitor(**d)
        assert monitor.total_steps > 0


def test_read_monitorings_steps_from_date(testclient):
    from_date: datetime = datetime(2020, 1, 5, 0, 0, 0)
    response = testclient.get(f"/monitorings/steps/?from_date={from_date}")
    assert response.status_code == 200

    assert len(response.json()) == 3

    for d in response.json():
        monitor: Monitor = Monitor(**d)
        assert monitor.total_steps > 0


def test_read_monitorings_steps_to_date(testclient):
    to_date: datetime = datetime(2020, 1, 7, 23, 59, 59)
    response = testclient.get(f"/monitorings/steps/?to_date={to_date}")
    assert response.status_code == 200

    assert len(response.json()) == 4

    for d in response.json():
        monitor: Monitor = Monitor(**d)
        assert monitor.total_steps > 0


def test_read_monitorings_steps_from_date_to_date(testclient):
    from_date: datetime = datetime(2020, 1, 5, 0, 0, 0)
    to_date: datetime = datetime(2020, 1, 7, 23, 59, 59)
    response = testclient.get(f"/monitorings/steps/?from_date={from_date}&to_date={to_date}")
    assert response.status_code == 200

    assert len(response.json()) == 2

    for d in response.json():
        monitor: Monitor = Monitor(**d)
        assert monitor.total_steps > 0
