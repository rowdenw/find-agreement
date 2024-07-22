from agreement.bible_api import get_chapter


def test_get_Mark_13_21_23():
    # https://github.com/wldeh/bible-api/blob/main/bibles/grc-byz1904/books/καταμαρκον/chapters/13.json
    text = get_chapter("grc-byz1904", "καταμαρκον", 13, 21, 23)
    assert len(text.splitlines()) == 3
