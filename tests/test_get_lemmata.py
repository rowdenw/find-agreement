from agreement.passage import GreekPassage
import tests.config as config


def test_lemmatize_Mark_13_21():
    greekPassage = GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21)
    assert greekPassage.lemmata == [
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
    ]


def test_lemmatize_Matt_24_23():
    greekPassage = GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23)
    assert greekPassage.lemmata == [
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
    ]
