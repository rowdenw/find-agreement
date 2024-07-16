from agreement.passage import GreekPassage
from agreement.synopsis import get_highlight

Matt_3_7_start = "ἰδὼν δὲ πολλοὺς τῶν Φαρισαίων καὶ Σαδδουκαίων ἐρχομένους \
ἐπὶ τὸ βάπτισμα αὐτοῦ εἶπεν αὐτοῖς· γεννήματα ἐχιδνῶν,"


def test_column_color():
    passage = GreekPassage(Matt_3_7_start)
    matches = (
        [3]  # ὁ
        + [13]  # αὐτός
        + list(range(15, 17))  # γέννημα ἔχιδνα
    )
    assert (
        get_highlight(matches, passage.pos, passage.tokens, column="blue")
        == "[blue]ἰδὼν δὲ πολλοὺς[/blue] [yellow]τῶν[/yellow] [blue]Φαρισαίων \
καὶ Σαδδουκαίων ἐρχομένους ἐπὶ τὸ βάπτισμα αὐτοῦ εἶπεν[/blue] [yellow]αὐτοῖς\
[/yellow][blue]·[/blue] [yellow]γεννήματα ἐχιδνῶν[/yellow][blue],[/blue]"
    )


def test_default_highlight():
    passage = GreekPassage(Matt_3_7_start)
    matches = (
        [3]  # ὁ
        + [13]  # αὐτός
        + list(range(15, 17))  # γέννημα ἔχιδνα
    )
    assert (
        get_highlight(matches, passage.pos, passage.tokens)
        == "ἰδὼν δὲ πολλοὺς [yellow]τῶν[/yellow] Φαρισαίων καὶ Σαδδουκαίων \
ἐρχομένους ἐπὶ τὸ βάπτισμα αὐτοῦ εἶπεν [yellow]αὐτοῖς[/yellow]· [yellow]\
γεννήματα ἐχιδνῶν[/yellow],"
    )


def test_green_highlight():
    passage = GreekPassage(Matt_3_7_start)
    matches = (
        [3]  # ὁ
        + [13]  # αὐτός
        + list(range(15, 17))  # γέννημα ἔχιδνα
    )
    assert (
        get_highlight(matches, passage.pos, passage.tokens, agreement="green")
        == "ἰδὼν δὲ πολλοὺς [green]τῶν[/green] Φαρισαίων καὶ Σαδδουκαίων \
ἐρχομένους ἐπὶ τὸ βάπτισμα αὐτοῦ εἶπεν [green]αὐτοῖς[/green]· [green]\
γεννήματα ἐχιδνῶν[/green],"
    )


def test_left_justify():
    passage = GreekPassage("ὀργῆς;\nποιήσατε")
    matches = [0, 3]
    assert (
        get_highlight(matches, passage.pos, passage.tokens)
        == "[yellow]ὀργῆς[/yellow];\n[yellow]ποιήσατε[/yellow]"
    )
