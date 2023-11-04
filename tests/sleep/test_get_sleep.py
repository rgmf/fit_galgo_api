from datetime import datetime, timedelta


def test_read_sleep(testclient):
    response = testclient.get("/monitorings/sleep")
    assert response.status_code == 200
    assert len(response.json()) == 11


def test_read_sleep_from_date(testclient):
    today_date: datetime = datetime.now()
    from_date: datetime = datetime(
        today_date.year, today_date.month, today_date.day,
        0, 0, 0
    ) - timedelta(days=2)

    response = testclient.get(f"/monitorings/sleep/?from_date={from_date}")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_read_sleep_to_date(testclient):
    today_date: datetime = datetime.now()
    to_date: datetime = datetime(
        today_date.year, today_date.month, today_date.day,
        0, 0, 0
    ) - timedelta(days=2)

    response = testclient.get(f"/monitorings/sleep/?to_date={to_date}")
    assert response.status_code == 200
    assert len(response.json()) == 9


def test_read_sleep_from_date_to_date(testclient):
    today_date: datetime = datetime.now()
    from_date: datetime = datetime(
        today_date.year, today_date.month, today_date.day,
        0, 0, 0
    ) - timedelta(days=4)
    to_date: datetime = datetime(
        today_date.year, today_date.month, today_date.day,
        23, 59, 59
    ) - timedelta(days=3)

    response = testclient.get(
        f"/monitorings/sleep/?from_date={from_date}&to_date={to_date}"
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_read_sleep_two_dates_from_date_1(testclient):
    from_date: datetime = datetime(2010, 10, 10, 0, 0, 0)
    response = testclient.get(f"/monitorings/sleep/?from_date={from_date}")
    assert response.status_code == 200
    assert len(response.json()) == 11


def test_read_sleep_two_dates_from_date_2(testclient):
    from_date: datetime = datetime(2010, 10, 11, 0, 0, 0)
    response = testclient.get(f"/monitorings/sleep/?from_date={from_date}")
    assert response.status_code == 200
    assert len(response.json()) == 11


def test_read_sleep_two_dates_from_date_out(testclient):
    from_date: datetime = datetime(2010, 10, 12, 0, 0, 0)
    response = testclient.get(f"/monitorings/sleep/?from_date={from_date}")
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_read_sleep_two_dates_to_date_1(testclient):
    to_date: datetime = datetime(2010, 10, 10, 0, 0, 0)
    response = testclient.get(f"/monitorings/sleep/?to_date={to_date}")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_read_sleep_two_dates_to_date_2(testclient):
    to_date: datetime = datetime(2010, 10, 11, 0, 0, 0)
    response = testclient.get(f"/monitorings/sleep/?to_date={to_date}")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_read_sleep_two_dates_to_date_out(testclient):
    to_date: datetime = datetime(2010, 10, 9, 0, 0, 0)
    response = testclient.get(f"/monitorings/sleep/?to_date={to_date}")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_read_sleep_two_dates_from_and_to_date_out_below(testclient):
    from_date: datetime = datetime(2010, 10, 8, 0, 0, 0)
    to_date: datetime = datetime(2010, 10, 9, 0, 0, 0)
    response = testclient.get(
        f"/monitorings/sleep/?from_date={from_date}&to_date={to_date}"
    )
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_read_sleep_two_dates_from_and_to_date_in_below(testclient):
    from_date: datetime = datetime(2010, 10, 9, 0, 0, 0)
    to_date: datetime = datetime(2010, 10, 10, 0, 0, 0)
    response = testclient.get(
        f"/monitorings/sleep/?from_date={from_date}&to_date={to_date}"
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_read_sleep_two_dates_from_and_to_date_same_dates(testclient):
    from_date: datetime = datetime(2010, 10, 10, 0, 0, 0)
    to_date: datetime = datetime(2010, 10, 11, 0, 0, 0)
    response = testclient.get(
        f"/monitorings/sleep/?from_date={from_date}&to_date={to_date}"
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_read_sleep_two_dates_from_and_to_date_in_above(testclient):
    from_date: datetime = datetime(2010, 10, 11, 0, 0, 0)
    to_date: datetime = datetime(2010, 10, 12, 0, 0, 0)
    response = testclient.get(
        f"/monitorings/sleep/?from_date={from_date}&to_date={to_date}"
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_read_sleep_two_dates_from_and_to_date_out_above(testclient):
    from_date: datetime = datetime(2010, 10, 12, 0, 0, 0)
    to_date: datetime = datetime(2010, 10, 13, 0, 0, 0)
    response = testclient.get(
        f"/monitorings/sleep/?from_date={from_date}&to_date={to_date}"
    )
    assert response.status_code == 200
    assert len(response.json()) == 0
