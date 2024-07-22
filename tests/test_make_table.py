import tests.config as config
from agreement.synoptic_table import SynopticTable


def test_one_title_header():
    synopsis = SynopticTable(
        "291 False Christs and False Prophets",
        [["Mark 13:21", config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21]])
    table = synopsis.getTable()
    assert table.title == "291 False Christs and False Prophets"
    assert table.columns[0].header == "Mark 13:21"
    assert table.columns[0].footer == "14 words"
    assert table.row_count == 1


def test_two_title_header():
    synopsis = SynopticTable(
        "291 False Christs and False Prophets",
        [["Mark 13:21", config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21],
         ["Matt. 24:23", config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23]])
    table = synopsis.getTable()
    assert table.title == "291 False Christs and False Prophets"
    assert table.columns[0].header == "Mark 13:21"
    assert table.columns[0].footer == "14 words"
    assert table.columns[1].header == "Matt. 24:23"
    assert table.columns[1].footer == "13 words"
    assert table.row_count == 1
