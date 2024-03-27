from datetime import datetime, timedelta


def assert_needed_activity_data(ld: list[dict]):
    for d in ld:
        assert "id" in d
        assert "username" in d
        assert "fit_file_path" in d
        assert "file_id" in d
        assert "zone_info" in d
        assert "session" in d


def test_read_activities(testclient):
    response = testclient.get("/activities")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 10
    assert response.json()["count"] == 10
    assert_needed_activity_data(response.json()["data"])


def test_read_activities_from_date(testclient):
    today_date: datetime = datetime.now()
    from_date: datetime = datetime(
        today_date.year, today_date.month, today_date.day,
        0, 0, 0
    ) - timedelta(days=2)

    response = testclient.get(f"/activities/?from_date={from_date}")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 3
    assert response.json()["count"] == 3
    assert_needed_activity_data(response.json()["data"])


def test_read_activities_to_date(testclient):
    today_date: datetime = datetime.now()
    to_date: datetime = datetime(
        today_date.year, today_date.month, today_date.day,
        0, 0, 0
    ) - timedelta(days=2)

    response = testclient.get(f"/activities/?to_date={to_date}")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 7
    assert response.json()["count"] == 7
    assert_needed_activity_data(response.json()["data"])


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
    assert len(response.json()["data"]) == 2
    assert response.json()["count"] == 2
    assert_needed_activity_data(response.json()["data"])
