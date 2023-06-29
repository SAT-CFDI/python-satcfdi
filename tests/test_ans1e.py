from datetime import datetime, timezone

from satcfdi.ans1e import to_utc_time


def test_date_time():
    d = datetime(2023, 6, 28, 19, 28, 1, tzinfo=timezone.utc)
    assert to_utc_time(d) == '230628192801Z'
    