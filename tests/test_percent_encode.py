from agreement.bible_api import percent_encode


def test_encode_Mark_13_21():
    link = "\
https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/grc-byz1904/books/καταμαρκον/chapters/13/verses/21.json\
"
    encoded = percent_encode(link)
    assert encoded == "\
https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/grc-byz1904/books/%CE%BA%CE%B1%CF%84%CE%B1%CE%BC%CE%B1%CF%81%CE%BA%CE%BF%CE%BD/chapters/13/verses/21.json\
"


def test_encode_Matt_24_23():
    link = "\
https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/grc-byz1904/books/καταματθαιον/chapters/24/verses/23.json\
"
    encoded = percent_encode(link)
    assert encoded == "\
https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/grc-byz1904/books/%CE%BA%CE%B1%CF%84%CE%B1%CE%BC%CE%B1%CF%84%CE%B8%CE%B1%CE%B9%CE%BF%CE%BD/chapters/24/verses/23.json\
"
