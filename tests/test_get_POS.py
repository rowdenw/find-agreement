from agreement.greek_text import GreekText
from tests import config


def test_POS_Mark_13_21():
    passage = GreekText(config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21 + "\n")
    assert passage.pos == [
        "CCONJ",
        "ADV",
        "SCONJ",
        "ADJ",
        "PRON",
        "VERB",
        "PUNCT",
        "INTJ",
        "ADV",
        "DET",
        "NOUN",
        "PUNCT",
        "INTJ",
        "ADV",
        "PUNCT",
        "CCONJ",
        "VERB",
        "PUNCT",
        "ADP",
        ]
