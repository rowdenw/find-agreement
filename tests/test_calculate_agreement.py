from agreement.agreement import match_sequences
from agreement.passage import GreekPassage
from tests import config


def test_calculate_agreement_014():
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


def test_calculate_agreement_128():
    passages = [
        GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30),
        GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31),
        GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19),
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


def calculate_agreement(passages):
    agreements = []
    matches = [
        [[] for i in range(len(passages))] for ji in range(len(passages))
        ]

    for left in range(len(passages)):
        for right in range(left + 1, len(passages)):
            (agreement,
             matches[left][right],
             matches[right][left]) = match_sequences(passages[left].lemmata,
                                                     passages[left].clean,
                                                     passages[right].lemmata,
                                                     passages[right].clean,
                                                     )
            agreements.append(agreement)
    return agreements, matches


def test_calculate_agreement_type_128():
    passages = [
        GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30),
        GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31),
        GreekPassage(config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19),
    ]
    agreements, matches = calculate_agreement(passages)
    agreement_type = []
    for column in range(len(passages)):
        agreement_type.append(
            [
                2**column if j in passages[column].clean else 0
                for j in range(len(passages[column].tokens))
                ]
                )
    for left in range(len(agreement_type)):
        for right in range(left+1, len(agreement_type)):
            agreement_type[left] = [
                agreement_type[left][position] + 2**right
                if position in matches[left][right]
                else agreement_type[left][position]
                for position in range(len(agreement_type[left]))
            ]
            agreement_type[right] = [
                agreement_type[right][position] + 2**left
                if position in matches[right][left]
                else agreement_type[right][position]
                for position in range(len(agreement_type[right]))
            ]
    print(agreement_type)
    assert 1 == 0
