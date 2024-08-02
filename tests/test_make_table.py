import tests.config as config
from agreement.synoptic_table import SynopticTable, Parallel

def test_one_title_header():

    TABLE_TITLE = "291 False Christs and False Prophets"
    PASSAGES = [
        Parallel(title="Mark 13:21", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21, footer="14 words")
    ]

    synopsis = SynopticTable(TABLE_TITLE, PASSAGES)
    synopsis.process_synopsis()
    table = synopsis.table
    assert table.title == TABLE_TITLE
    for index in range(len(PASSAGES)):
        assert table.columns[index].header == PASSAGES[index].title
        assert table.columns[index].footer == PASSAGES[index].footer
    assert table.row_count == 1


def test_two_title_header():
    TABLE_TITLE = "291 False Christs and False Prophets"
    PASSAGES = [
        Parallel(title="Mark 13:21", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21, footer="14 words"),
        Parallel(title="Matt. 24:23", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23, footer="13 words")
    ]

    synopsis = SynopticTable(TABLE_TITLE, PASSAGES)
    synopsis.process_synopsis()
    table = synopsis.table
    assert table.title == TABLE_TITLE
    for index in range(len(PASSAGES)):
        assert table.columns[index].header == PASSAGES[index].title
        assert table.columns[index].footer == PASSAGES[index].footer
    assert table.row_count == 1

def test_three_title_header():
    TABLE_TITLE = "128 The Parable of the Mustard Seed (First Verse)"
    PASSAGES = [
        Parallel(title="Matt. 13:31", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31, footer="21 words"),
        Parallel(title="Mark 4:30", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30, footer="14 words"),
        Parallel(title="Luke 13:18-19", text=config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19, footer="13 words"),
    ]

    synopsis = SynopticTable(TABLE_TITLE, PASSAGES)
    synopsis.process_synopsis()
    table = synopsis.table
    assert table.title == TABLE_TITLE
    for index in range(len(PASSAGES)):
        assert table.columns[index].header == PASSAGES[index].title
        assert table.columns[index].footer == PASSAGES[index].footer
    assert table.row_count == 1
