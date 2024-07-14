from agreement.cltk import Greek
from agreement.synopsis import get_highlight


def test_highlight():
    greek = Greek()
    doc = greek.NLP.analyze(
        text="ἰδὼν δὲ πολλοὺς τῶν Φαρισαίων καὶ Σαδδουκαίων ἐρχομένους ἐπὶ τὸ βάπτισμα αὐτοῦ εἶπεν αὐτοῖς· γεννήματα ἐχιδνῶν,"
    )
    a_matches_b = (
        [3]  # ὁ
        + [13]  # αὐτός
        + list(range(15, 17))  # γέννημα ἔχιδνα
    )
    assert (
        get_highlight(a_matches_b, doc.pos, doc.tokens)
        == "ἰδὼν δὲ πολλοὺς [yellow]τῶν[/yellow] Φαρισαίων καὶ Σαδδουκαίων ἐρχομένους ἐπὶ τὸ βάπτισμα αὐτοῦ εἶπεν [yellow]αὐτοῖς[/yellow]· [yellow]γεννήματα ἐχιδνῶν[/yellow],"
    )
