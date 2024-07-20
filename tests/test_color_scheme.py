import rich
from agreement.color_scheme import ColorScheme
from agreement.color_scheme import GoodacreColorScheme
from agreement.passage import GreekPassage
from agreement.color_scheme import get_agreement_type
from tests import config
from tests.config import grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19
from agreement.synopsis_table import print_Greek_token


def test_agreement_type():
    assert get_agreement_type([]) == 0  # e.g., punctuation
    assert get_agreement_type([0]) == 1  # only in passage 0
    assert get_agreement_type([1]) == 2  # only in passage 1
    assert get_agreement_type([0, 1]) == 3  # in passages 0 and 1
    assert get_agreement_type([2]) == 4  # only in passage 2
    assert get_agreement_type([0, 2]) == 5  # in passages 0 and 2
    assert get_agreement_type([1, 2]) == 6  # in passages 1 and 2
    assert get_agreement_type([0, 1, 2]) == 7  # e.g., in all Synoptic Gospels


def test_color_scheme():
    colorScheme = ColorScheme(None, None, None, "yellow")
    assert colorScheme.get_color(3) == "yellow"
    colorScheme.set_color(get_agreement_type([1, 2]), "green")
    assert colorScheme.get_color(6) == "green"


def get_color_text(colorScheme, token_agreement):
    prev = None
    text = rich.text.Text()
    for pos, token, type in token_agreement:
        to_print = print_Greek_token(token, pos, prev)
        style = colorScheme.get_color(type)
        text.append(to_print, style=style)
        prev = token
    return text.markup


agreement_type_Matt_13_31 = [1, 1, 1, 1, 7, 0, 5, 5, 7, 7, 7, 1, 1, 1, 0, 1,
                             1, 1, 1, 3, 1, 1, 7, 0]


def test_color_Matt_13_31():
    color_text = "Ἄλλην παραβολὴν παρέθηκεν αὐτοῖς[blue] λέγων[/blue]·\
[orange] ὁμοία[orange][/orange] ἐστὶν[blue][/orange] ἡ[blue][/blue] βασιλεία\
[blue][/blue] τῶν[/blue] οὐρανῶν κόκκῳ σινάπεως, ὃν λαβὼν ἄνθρωπος ἔσπειρεν\
[purple] ἐν[/purple] τῷ ἀγρῷ[blue] αὐτοῦ[/blue]·"
    column_Matthew = 0
    column_Mark = 1
    column_Luke = 2
    colorScheme = ColorScheme()
    # https://www.facebook.com/groups/212992206399733/posts/1194217374943873/
    # Triple Trad in Blue
    # https://en.wikipedia.org/wiki/Synoptic_Gospels#Triple_tradition
    colorScheme.set_color(get_agreement_type([column_Matthew, column_Mark,
                                              column_Luke]), "blue")
    # Matt-Mark in Purple...
    colorScheme.set_color(get_agreement_type([column_Matthew, column_Mark]),
                          "purple")
    # Mark-Luke in Green...
    colorScheme.set_color(get_agreement_type([column_Mark, column_Luke]),
                          "green")
    # Double Trad in orange...
    # https://en.wikipedia.org/wiki/Synoptic_Gospels#Double_tradition
    colorScheme.set_color(get_agreement_type([column_Matthew, column_Luke]),
                          "orange")
    passage = GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31)
    pos = passage.pos
    tokens = passage.tokens
    row = get_color_text(colorScheme, zip(pos, tokens,
                                          agreement_type_Matt_13_31))
    assert row == color_text


agreement_type_Mark_4_30_32 = [1, 7, 0, 1, 1, 7, 7, 7, 5, 0, 1, 3, 5, 1, 1,
                               7, 0]


def test_color_Mark_4_30_32():
    color_text = "[blue]Καὶ[black on white][/blue] ἔλεγε[/black on white]·\
[blue] πῶς[blue][/blue] ὁμοιώσωμεν[black on white][/blue] τὴν[black on white]\
[/black on white] βασιλείαν[black on white][/black on white] τοῦ\
[/black on white] Θεοῦ;[blue] ἢ[purple][/blue] ἐν[/purple] τίνι[blue] παραβολῇ\
[blue][/blue] παραβάλωμεν[black on white][/blue] αὐτήν[/black on white];"
    # http://www.hypotyposeis.org/synoptic-problem/2004/10/johns-imprisonment.html
    colorScheme = ColorScheme(None, "blue", "red", "purple",
                              "green", None, None, "black on white")
    passage = GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30)
    pos = passage.pos
    tokens = passage.tokens
    assert (
        get_color_text(colorScheme, zip(pos, tokens,
                       agreement_type_Mark_4_30_32)) == color_text
    )


agreement_type_Luke_13_18 = [7, 4, 0, 4, 6, 6, 7, 7, 7, 5, 0, 4, 5, 4, 7, 0]


def test_color_Luke_13_18():
    color_text = "[brown]Ἔλεγε[yellow][/brown] δέ[/yellow]·[yellow] τίνι\
[orange][/yellow] ὁμοία[orange][/orange] ἐστὶν[brown][/orange] ἡ[brown]\
[/brown] βασιλεία[brown][/brown] τοῦ[green][/brown] Θεοῦ[/green],[yellow] καὶ\
[green][/yellow] τίνι[yellow][/green] ὁμοιώσω[brown][/yellow] αὐτήν[/brown];"
    column_Matthew = 0
    column_Mark = 1
    column_Luke = 2
    colorScheme = GoodacreColorScheme(column_Matthew, column_Mark, column_Luke)
    passage = GreekPassage(grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19)
    pos = passage.pos
    tokens = passage.tokens
    assert get_color_text(colorScheme, zip(pos, tokens,
                          agreement_type_Luke_13_18)) == color_text
