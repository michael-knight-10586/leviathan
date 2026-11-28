from datetime import date

from leviathan.landing.manifest import LANDING_ROOT, classify, landed_path

DAY = date(2026, 11, 28)


def test_landed_path_main_league():
    url = "https://www.football-data.co.uk/mmz4281/2627/E0.csv"
    assert landed_path(url, DAY) == f"{LANDING_ROOT}/mmz4281/2627/E0/2026-11-28/E0.csv"


def test_landed_path_extra_league():
    url = "https://www.football-data.co.uk/new/ARG.csv"
    assert landed_path(url, DAY) == f"{LANDING_ROOT}/new/ARG/2026-11-28/ARG.csv"


def test_classify_all_four_statuses():
    previous = {"same": "h1", "edited": "h2", "gone": "h3"}
    current = {"same": "h1", "edited": "h9", "added": "h4"}
    assert classify(previous, current) == {
        "same": "unchanged",
        "edited": "changed",
        "gone": "missing",
        "added": "new",
    }


def test_classify_first_run_everything_new():
    assert classify({}, {"a": "h1", "b": "h2"}) == {"a": "new", "b": "new"}
