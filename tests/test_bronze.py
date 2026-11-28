from leviathan.bronze.load import decode, parse


def test_decode_utf8_with_bom():
    assert decode("﻿Div,HomeTeam".encode("utf-8")) == ("Div,HomeTeam", "utf-8-sig")


def test_decode_falls_back_to_cp1252():
    text, encoding = decode("Malmö".encode("cp1252"))
    assert (text, encoding) == ("Malmö", "cp1252")


def test_parse_keeps_values_as_text():
    records, bad = parse("Div,HomeTeam,FTHG\nE0,Arsenal,2\n")
    assert records == [(1, {"Div": "E0", "HomeTeam": "Arsenal", "FTHG": "2"})]
    assert bad == []


def test_parse_skips_blank_rows_and_trailing_commas():
    records, _ = parse("Div,HomeTeam,,\nE0,Arsenal,,\n,,,\n")
    assert records == [(1, {"Div": "E0", "HomeTeam": "Arsenal"})]


def test_parse_quarantines_rows_wider_than_header():
    records, bad = parse("Div,HomeTeam\nE0,Arsenal\nE0,Chelsea,extra\n")
    assert records == [(1, {"Div": "E0", "HomeTeam": "Arsenal"})]
    assert bad == [(2, "E0,Chelsea,extra", "more fields than header")]


def test_parse_keeps_repeated_column_names():
    records, _ = parse("LB,LB\n1.5,2.0\n")
    assert records == [(1, {"LB": "1.5", "LB#2": "2.0"})]
