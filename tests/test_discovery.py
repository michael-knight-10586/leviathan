from leviathan.landing.discovery import _LinkParser, compare_pages


def test_link_parser_collects_address_and_text():
    parser = _LinkParser()
    parser.feed('<a href="englandm.php">England Football Results</a>'
                '<a href="mmz4281/2627/E0.csv">Premier League</a>')
    assert parser.links == [
        ("englandm.php", "England Football Results"),
        ("mmz4281/2627/E0.csv", "Premier League"),
    ]


def test_compare_pages_finds_added_and_removed():
    added, removed = compare_pages(["a.php", "b.php"], ["b.php", "c.php"])
    assert added == ["c.php"]
    assert removed == ["a.php"]
