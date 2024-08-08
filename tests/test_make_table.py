import tests.config as config
from agreement.synoptic_table_model import SynopticTableModel, ParallelTuple
from agreement.synoptic_table_rich_text import SynopticTableRichText

def render_table(table_title, passages, footers, color_scheme=None):
    synopsis_model = SynopticTableModel(table_title, passages)
    synopsis_model.process_synopsis()
    rich_synoptic_table = SynopticTableRichText(synopsis_model, color_scheme=color_scheme)
    table = rich_synoptic_table.table
    return table
    
def assert_table(table, table_title, passages, footers):
    assert table.title == table_title
    for index in range(len(passages)):
        assert table.columns[index].header == passages[index].title
        assert table.columns[index].footer == footers[index]
    assert table.row_count == 1

def test_one_title_header():

    TABLE_TITLE = "291 False Christs and False Prophets"
    PASSAGES = [
        ParallelTuple(title="Mark 13:21", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21)
    ]
    FOOTERS = ["14 words"]

    table = render_table(TABLE_TITLE, PASSAGES, FOOTERS)
    assert_table(table, TABLE_TITLE, PASSAGES, FOOTERS)


def test_two_title_header():
    TABLE_TITLE = "291 False Christs and False Prophets"
    PASSAGES = [
        ParallelTuple(title="Mark 13:21", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21),
        ParallelTuple(title="Matt. 24:23", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23)
    ]
    FOOTERS = ["14 words", "13 words"]

    table = render_table(TABLE_TITLE, PASSAGES, FOOTERS)
    assert_table(table, TABLE_TITLE, PASSAGES, FOOTERS)


def test_three_title_header():
    TABLE_TITLE = "128 The Parable of the Mustard Seed (First Verse)"
    PASSAGES = [
        ParallelTuple(title="Matt. 13:31", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31),
        ParallelTuple(title="Mark 4:30", text=config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30),
        ParallelTuple(title="Luke 13:18-19", text=config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19),
    ]
    FOOTERS = ["21 words", "14 words", "13 words"]

    table = render_table(TABLE_TITLE, PASSAGES, FOOTERS)
    assert_table(table, TABLE_TITLE, PASSAGES, FOOTERS)
