from agreement.agreement import match_sequences
from agreement.agreement import calculate_agreement
from agreement.agreement import calculate_agreement_types
from agreement.greek_text import GreekText
from tests import config


def test_calculate_agreement_014():
    passageA = GreekText(config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_3_7_10())
    passageB = GreekText(config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_3_7_9())
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


def test_calculate_agreement_128():
    passages = [
        GreekText(config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30),
        GreekText(config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31),
        GreekText(config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19),
    ]
    assert len(passages[0].tokens) == 17  # words plus punctuation
    assert len(passages[0].clean) == 14  # words
    assert len(passages[1].tokens) == 24  # words plus punctuation
    assert len(passages[1].clean) == 21  # words
    assert len(passages[2].tokens) == 16  # words plus punctuation
    assert len(passages[2].clean) == 13  # words

    agreements, matches = calculate_agreement(passages)

    # ['ἔλεγε', 'τὴν', 'βασιλείαν', 'τοῦ', 'ἐν', 'αὐτήν']
    assert matches[0][1] == [1, 5, 6, 7, 11, 15]
    # ['λέγων', 'ἡ', 'βασιλεία', 'τῶν', 'ἐν', 'αὐτοῦ']
    assert matches[1][0] == [4, 8, 9, 10, 19, 22]
    # match of length 3: 5, 6, 7 matches 8, 9, 10
    assert max(agreements[0].keys()) == 3
    # 3 matches of length 1: 1 ~ 4, 11 ~ 19, and 15 ~ 22
    assert agreements[0][1] == 3

    # ['ἔλεγε', 'τὴν', 'βασιλείαν', 'τοῦ', 'Θεοῦ', 'τίνι', 'αὐτήν']
    assert matches[0][2] == [1, 5, 6, 7, 8, 12, 15]
    # ['Ἔλεγε', 'ἡ', 'βασιλεία', 'τοῦ', 'Θεοῦ', 'τίνι', 'αὐτήν']
    assert matches[2][0] == [0, 6, 7, 8, 9, 12, 14]
    # match of length 4: 5, 6, 7, 8 matches 6, 7, 8, 9
    assert max(agreements[1].keys()) == 4
    # 3 matches of length 1: 1 ~ 0, 12 ~ 12, 15~14
    assert agreements[1][1] == 3

    # ['λέγων', 'ὁμοία', 'ἐστὶν', 'ἡ', 'βασιλεία', 'τῶν', 'αὐτοῦ']
    assert matches[1][2] == [4, 6, 7, 8, 9, 10, 22]
    # ['Ἔλεγε', 'ὁμοία', 'ἐστὶν', 'ἡ', 'βασιλεία', 'τοῦ', 'αὐτήν']
    assert matches[2][1] == [0, 4, 5, 6, 7, 8, 14]
    # match of length 5: 6, 7, 8, 9, 10 matches 4, 5, 6, 7, 8
    assert max(agreements[2].keys()) == 5
    # 2 matches of length 1: 4 ~ 0, 22 ~ 14
    assert agreements[2][1] == 2


def test_calculate_agreement_type_128():
    texts = [
        GreekText(config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31),
        GreekText(config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30),
        GreekText(config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19),
    ]
    agreement_type = calculate_agreement_types(texts)
    assert agreement_type[0] == [1, 1, 1, 1, 7, 0, 5, 5, 7, 7, 7, 1, 1, 1, 0,
                                 1, 1, 1, 1, 3, 1, 1, 7, 0]
    assert agreement_type[1] == [2, 7, 0, 2, 2, 7, 7, 7, 6, 0, 2, 3, 6, 2, 2,
                                 7, 0]
    assert agreement_type[2] == [7, 4, 0, 4, 5, 5, 7, 7, 7, 6, 0, 4, 6, 4, 7,
                                 0]
