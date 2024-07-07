import unittest

from cltk import NLP

import tests.config as config


class TestGetLemmata(unittest.TestCase):
    def test_lemmatize_Mark_13_21(self):
        text = config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21
        cltk_nlp = NLP(language="grc", suppress_banner=True)
        cltk_doc = cltk_nlp.analyze(text=text)
        self.assertEqual(
            cltk_doc.lemmata,
            [
                "καί",
                "τότε",
                "ἐάν",
                "τὶς",
                "ὑμεῖς",
                "εἶπον",
                ",",
                "ἰδοὺ",
                "ὧδε",
                "ὁ",
                "χριστός",
                ",",
                "ἰδοὺ",
                "ἐκεῖ",
                ",",
                "μή",
                "πιστεύω",
                ".",
            ],
        )

    def test_lemmatize_Matt_24_23(self):
        text = config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23
        cltk_nlp = NLP(language="grc", suppress_banner=True)
        cltk_doc = cltk_nlp.analyze(text=text)
        self.assertEqual(
            cltk_doc.lemmata,
            [
                "τότε",
                "ἐάν",
                "τὶς",
                "ὑμεῖς",
                "εἶπον",
                ",",
                "ἰδοὺ",
                "ὧδε",
                "ὁ",
                "χριστός",
                "ἤ",
                "ὧδε",
                ",",
                "μή",
                "πιστεύω",
                "·",
            ],
        )


if __name__ == "__main__":
    unittest.main()
