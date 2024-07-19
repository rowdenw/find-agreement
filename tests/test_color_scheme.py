import rich
from agreement.passage import GreekPassage
from tests import config
from tests.config import grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19
from tests.test_print_Greek import print_Greek_token


agreement_type_Matt_13_31 = [2, 3, 2, 2, 2, 0, 6, 6, 6, 6, 2, 2, 6, 6, 0, 6,
                             6, 6, 2, 2, 2, 2, 2, 0, ]


agreement_type_Mark_4_30_32 = [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 3, 1,
                               0, ]


agreement_type_Luke_13_18 = [4, 4, 0, 4, 6, 6, 6, 6, 4, 4, 0, 4, 4, 4, 4, 0, ]


def get_agreement_type(in_passage):
    agreement_type = 0
    for passage in in_passage:
        agreement_type += 2**passage
    return agreement_type


def test_agreement_type():
    assert get_agreement_type([]) == 0  # e.g., punctuation
    assert get_agreement_type([0]) == 1  # only in passage 0
    assert get_agreement_type([1]) == 2  # only in passage 1
    assert get_agreement_type([0, 1]) == 3  # in passages 0 and 1
    assert get_agreement_type([2]) == 4  # only in passage 2
    assert get_agreement_type([0, 2]) == 5  # in passages 0 and 2
    assert get_agreement_type([1, 2]) == 6  # in passages 1 and 2
    assert get_agreement_type([0, 1, 2]) == 7  # e.g., in all Synoptic Gospels


class ColorScheme:
    def __init__(self, *colors):
        self._color = {}
        for index, color in enumerate(colors):
            self._color[index] = color

    def get_color(self, index):
        return self._color[index]

    def set_color(self, index, color):
        self._color[index] = color


def test_color_scheme():
    colorScheme = ColorScheme(None, None, None, "yellow")
    assert colorScheme.get_color(3) == "yellow"
    colorScheme.set_color(get_agreement_type([1, 2]), "green")
    assert colorScheme.get_color(6) == "green"


def get_color_text(colorScheme, token_agreement):
    prev = None
    styles = []
    tokens = []
    text = rich.text.Text()
    for pos, token, type in token_agreement:
        tokens.append(print_Greek_token(token, pos, prev))
        styles.append(colorScheme.get_color(type))
        prev = token
    text.append_tokens(zip(tokens, styles))
    return text.markup


def test_color_Matt_13_31():
    color_text = "Ἄλλην[yellow] παραβολὴν[/yellow] παρέθηκεν αὐτοῖς λέγων·\
[green] ὁμοία[green][/green] ἐστὶν[green][/green] ἡ[green][/green] βασιλεία\
[/green] τῶν οὐρανῶν[green] κόκκῳ[green][/green] σινάπεως[/green],[green] ὃν\
[green][/green] λαβὼν[green][/green] ἄνθρωπος[/green] ἔσπειρεν ἐν τῷ ἀγρῷ \
αὐτοῦ·"
    colorScheme = ColorScheme(None, None, None, "yellow", None, None, "green")
    passage = GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31)
    pos = passage.pos
    tokens = passage.tokens
    row = get_color_text(colorScheme, zip(pos, tokens,
                                          agreement_type_Matt_13_31))
    assert row == color_text


def test_color_Mark_4_30_32():
    # TODO: Test and fix spacing algorithm. Or does Rich have something?
    color_text = "Καὶ ἔλεγε· πῶς ὁμοιώσωμεν τὴν βασιλείαν τοῦ Θεοῦ; ἢ ἐν τίνι\
[yellow] παραβολῇ[/yellow] παραβάλωμεν αὐτήν"
    colorScheme = ColorScheme(None, None, None, "yellow", None, None, "green")
    passage = GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30)
    pos = passage.pos
    tokens = passage.tokens
    assert (
        get_color_text(colorScheme, zip(pos, tokens,
                       agreement_type_Mark_4_30_32)) == color_text
    )


def test_color_Luke_13_18():
    color_text = "Ἔλεγε δέ· τίνι[green] ὁμοία[green][/green] ἐστὶν[green]\
[/green] ἡ[green][/green] βασιλεία[/green] τοῦ Θεοῦ, καὶ τίνι ὁμοιώσω αὐτήν;"
    colorScheme = ColorScheme(None, None, None, "yellow", None, None, "green")
    passage = GreekPassage(grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19)
    pos = passage.pos
    tokens = passage.tokens
    assert get_color_text(colorScheme, zip(pos, tokens,
                          agreement_type_Luke_13_18)) == color_text
