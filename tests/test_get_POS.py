import unittest

from cltk import NLP

from tests import config


class TestGetPOS(unittest.TestCase):
    def test_POS_Mark_13_21(self):
        text = config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21 + "\n"
        cltk_nlp = NLP(language="grc", suppress_banner=True)
        cltk_doc = cltk_nlp.analyze(text=text)
        self.assertEqual(
            cltk_doc.pos,
            [
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
            ],
        )
