from datetime import datetime, timedelta


def test_read_activities(testclient):
    response = testclient.get("/activities")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_read_activities_from_date(testclient):
    today_date: datetime = datetime.now()
    from_date: datetime = datetime(
        today_date.year, today_date.month, today_date.day,
        0, 0, 0
    ) - timedelta(days=2)

    response = testclient.get(f"/activities/?from_date={from_date}")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_read_activities_to_date(testclient):
    today_date: datetime = datetime.now()
    to_date: datetime = datetime(
        today_date.year, today_date.month, today_date.day,
        0, 0, 0
    ) - timedelta(days=2)

    response = testclient.get(f"/activities/?to_date={to_date}")
    assert response.status_code == 200
    assert len(response.json()) == 7


def test_read_activities_from_date_to_date(testclient):
    today_date: datetime = datetime.now()
    from_date: datetime = datetime(
        today_date.year, today_date.month, today_date.day,
        0, 0, 0
    ) - timedelta(days=4)
    to_date: datetime = datetime(
        today_date.year, today_date.month, today_date.day,
        23, 59, 59
    ) - timedelta(days=3)

    response = testclient.get(f"/activities/?from_date={from_date}&to_date={to_date}")
    assert response.status_code == 200
    assert len(response.json()) == 2
