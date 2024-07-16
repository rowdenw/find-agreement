from agreement.agreement import match_sequences
from agreement.passage import GreekPassage
from tests import config


def test_calculate_agreement():
    passageA = GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_3_7_10())
    passageB = GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_3_7_9())
    assert len(passageA.clean) == 78
    assert len(passageB.clean) == 72
    (agreement, a_matches_b, b_matches_a) = match_sequences(
        passageA.lemmata, passageA.clean, passageB.lemmata, passageB.clean
    )
    assert max(agreement.keys()) == 45
    assert agreement[1] == 1
    assert agreement[19] == 1
    assert agreement[45] == 1
    assert sum(list(agreement.keys())) == 65
