# https://en.wikipedia.org/wiki/Greek_orthography#In_printing
from agreement.synopsis_table import print_Greek_token


def test_print_scripta_continua():
    assert print_Greek_token("·", "PUNCT", "λέγων",
                             scripta_continua=True) == ""
    assert print_Greek_token(",", "PUNCT", "σινάπεως",
                             scripta_continua=True) == ""
    assert print_Greek_token(";", "PUNCT", "Θεοῦ",
                             scripta_continua=True) == ""
    assert print_Greek_token(".", "PUNCT", "Θεοῦ",
                             scripta_continua=True) == ""


def test_print_punctuation():
    assert print_Greek_token("·", "PUNCT", "λέγων",
                             scripta_continua=False) == "·"
    assert print_Greek_token(",", "PUNCT", "σινάπεως",
                             scripta_continua=False) == ","
    assert print_Greek_token(";", "PUNCT", "Θεοῦ",
                             scripta_continua=False) == ";"
    assert print_Greek_token(".", "PUNCT", "Θεοῦ",
                             scripta_continua=False) == "."


def test_print_word_without_space():
    assert print_Greek_token("Ἄλλην", "", None,
                             scripta_continua=True) == "Ἄλλην"
    assert print_Greek_token("Ἄλλην", "", None,
                             scripta_continua=False) == "Ἄλλην"
    assert print_Greek_token("Ἄλλην", "", "\n",
                             scripta_continua=True) == "Ἄλλην"
    assert print_Greek_token("Ἄλλην", "", "\n",
                             scripta_continua=False) == "Ἄλλην"


def test_print_space():
    assert print_Greek_token("παραβολὴν", "", "Ἄλλην",
                             scripta_continua=False) == " παραβολὴν"


def test_default_modern():
    assert print_Greek_token("·", "PUNCT", "λέγων") == "·"
    assert print_Greek_token(",", "PUNCT", "σινάπεως") == ","
    assert print_Greek_token(";", "PUNCT", "Θεοῦ") == ";"
    assert print_Greek_token(".", "PUNCT", "Θεοῦ") == "."
