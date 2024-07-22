from agreement.bible_api import get_verse
import tests.config as config


def test_get_Mark_13_21():
    # https://github.com/wldeh/bible-api/blob/main/bibles/grc-byz1904/books/καταμαρκον/chapters/13/verses/21.json
    text = get_verse("grc-byz1904", "καταμαρκον", 13, 21)
    assert text == config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21


def test_get_Matt_24_23():
    # https://github.com/wldeh/bible-api/blob/main/bibles/grc-byz1904/books/καταματθαιον/chapters/24/verses/23.json
    text = get_verse("grc-byz1904", "καταματθαιον", 24, 23)
    assert text == config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23
