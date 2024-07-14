from agreement.cltk import Greek, get_sequence, match_sequences
from tests import config


def test_calculate_agreement():
    greek = Greek()
    doc_a = greek.NLP.analyze(text=config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_3_7_10())
    doc_b = greek.NLP.analyze(text=config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_3_7_9())
    sequence_a = get_sequence(doc_a)
    sequence_b = get_sequence(doc_b)
    assert len(sequence_a) == 78
    assert len(sequence_b) == 72
    (agreement,
     a_matches_b, b_matches_a) = match_sequences(doc_a, sequence_a,
                                                 doc_b, sequence_b)
    assert agreement[1] == 1
    assert agreement[19] == 1
    assert agreement[45] == 1
    assert sum(list(agreement.keys())) == 65
