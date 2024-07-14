from agreement.cltk import Greek
from agreement.synopsis import get_highlight

Matt_3_7_start = "ἰδὼν δὲ πολλοὺς τῶν Φαρισαίων καὶ Σαδδουκαίων ἐρχομένους \
ἐπὶ τὸ βάπτισμα αὐτοῦ εἶπεν αὐτοῖς· γεννήματα ἐχιδνῶν,"


def test_column_color():
    greek = Greek()

    doc = greek.NLP.analyze(text=Matt_3_7_start)
    a_matches_b = (
        [3]  # ὁ
        + [13]  # αὐτός
        + list(range(15, 17))  # γέννημα ἔχιδνα
    )
    assert (
        get_highlight(a_matches_b, doc.pos, doc.tokens, column="blue")
        == "[blue]ἰδὼν δὲ πολλοὺς[/blue] [yellow]τῶν[/yellow] [blue]Φαρισαίων \
καὶ Σαδδουκαίων ἐρχομένους ἐπὶ τὸ βάπτισμα αὐτοῦ εἶπεν[/blue] [yellow]αὐτοῖς\
[/yellow][blue]·[/blue] [yellow]γεννήματα ἐχιδνῶν[/yellow][blue],[/blue]"
    )


def test_default_highlight():
    greek = Greek()

    doc = greek.NLP.analyze(text=Matt_3_7_start)
    a_matches_b = (
        [3]  # ὁ
        + [13]  # αὐτός
        + list(range(15, 17))  # γέννημα ἔχιδνα
    )
    assert (
        get_highlight(a_matches_b, doc.pos, doc.tokens)
        == "ἰδὼν δὲ πολλοὺς [yellow]τῶν[/yellow] Φαρισαίων καὶ Σαδδουκαίων \
ἐρχομένους ἐπὶ τὸ βάπτισμα αὐτοῦ εἶπεν [yellow]αὐτοῖς[/yellow]· [yellow]\
γεννήματα ἐχιδνῶν[/yellow],"
    )


def test_green_highlight():
    greek = Greek()

    doc = greek.NLP.analyze(text=Matt_3_7_start)
    a_matches_b = (
        [3]  # ὁ
        + [13]  # αὐτός
        + list(range(15, 17))  # γέννημα ἔχιδνα
    )
    assert (
        get_highlight(a_matches_b, doc.pos, doc.tokens, agreement="green")
        == "ἰδὼν δὲ πολλοὺς [green]τῶν[/green] Φαρισαίων καὶ Σαδδουκαίων \
ἐρχομένους ἐπὶ τὸ βάπτισμα αὐτοῦ εἶπεν [green]αὐτοῖς[/green]· [green]\
γεννήματα ἐχιδνῶν[/green],"
    )


def test_left_justify():
    greek = Greek()
    doc = greek.NLP.analyze(text="ὀργῆς;\nποιήσατε")
    a_matches_b = [0, 3]
    assert (
        get_highlight(a_matches_b, doc.pos, doc.tokens)
        == "[yellow]ὀργῆς[/yellow];\n[yellow]ποιήσατε[/yellow]"
    )
