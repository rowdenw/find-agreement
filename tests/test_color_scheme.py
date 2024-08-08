from typing import List

from agreement.color_scheme import ColorScheme
from agreement.color_scheme import GoodacreColorScheme
from agreement.greek_text import GreekText
from agreement.color_scheme import get_agreement_type
from agreement.synoptic_table_rich_text import get_colorized_text_for_tokens
from agreement.synoptic_table_model import TokenAgreementTuple
from tests import config
from tests.config import grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19


def assert_color_scheme(passage: GreekText, agreement_types: List[int], color_scheme: ColorScheme, color_text: str):
    pos = passage.pos
    tokens = passage.tokens
    token_agreements = [TokenAgreementTuple(*t) for t in zip(pos, tokens, agreement_types)]
    row = get_colorized_text_for_tokens(color_scheme, token_agreements)
    assert row == color_text

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

    # Here we have a bit of a challenge, because this would be where, in 
    # SynopticTableModel, we take all three columns of text, and
    # compute the agreement types. The output of SynopticTableModel
    # is a list of TokenAgreementTuples, each of which has 
    # the token, part of speech, and agreement type for that token
    #
    # The GreekText class is the tokenized text, exposing two lists, 
    # one "lemmata" (the lemmatized words), the other "clean", a list
    # of indices into the tokens. If an index is in the list, then
    # that token is an actual lemmatized word, not punctuation or newline
    #
    passage = GreekText(config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31)

    # Here we cheat a bit. passage (a GreekText) doesn't properly expose pos or tokens.
    # Need to figure out if that's needed or not

    # It looks like what we're doing here is first building the list of tuples that
    # needs to be passed to get_colorized_text_for_tokens, bypassing the normal
    # processing of agreement types. 
    # I really don't think this belongs in this test, but we'll have to give it
    # another look.
    # pos = passage.pos  # the list of parts of speech
    # tokens = passage.tokens  # the list of raw tokens
    # token_agreements = [TokenAgreementTuple(*t) for t in zip(pos, tokens, agreement_type_Matt_13_31)]
    # row = get_colorized_text_for_tokens(colorScheme, token_agreements)
    # assert row == color_text
    assert_color_scheme(passage, agreement_type_Matt_13_31, colorScheme, color_text)


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
    passage = GreekText(config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30)

    assert_color_scheme(passage, agreement_type_Mark_4_30_32, colorScheme, color_text)

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
    passage = GreekText(grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19)
    pos = passage.pos
    tokens = passage.tokens

    assert_color_scheme(passage, agreement_type_Luke_13_18, colorScheme, color_text)
