# https://en.wikipedia.org/wiki/Greek_orthography#In_printing
def print_Greek_token(token, pos, previous, scripta_continua=False):
    # https://www.billmounce.com/greekalphabet/greek-punctuation-syllabification
    # https://blog.greek-language.com/2022/02/14/punctuation-in-ancient-greek-texts-part-i/
    # https://www.opoudjis.net/unicode/punctuation.html
    # https://en.wikipedia.org/wiki/Ancient_Greek_grammar#Alphabet
    if pos == "PUNCT":  # token in "·,;."
        # https://library.biblicalarchaeology.org/article/punctuationinthenewtestament/
        # https://en.wikipedia.org/wiki/Scriptio_continua
        if scripta_continua:
            return ""
        else:
            return token
    else:
        if previous is None or previous == "\n" or scripta_continua:
            return token
        else:
            return " " + token


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
