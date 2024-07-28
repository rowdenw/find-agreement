import math
from agreement.find_agreement import NGramAgreementFinder
from agreement.greek_text import GreekText
from tests.config import grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23
from tests.config import grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21


def test_clean():
    passageA = GreekText(grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23)
    passageB = GreekText(grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21)
    sequence_a = (
        list(range(0, 5))  # τότε ἐάν τις ὑμῖν εἴπῃ
        + list(range(6, 12))  # ἰδοὺ ὧδε ὁ Χριστὸς ἢ ὧδε
        + list(range(13, 15))  # μὴ πιστεύσητε
    )
    sequence_b = (
        list(range(0, 6))  # καὶ τότε ἐάν τις ὑμῖν εἴπῃ
        + list(range(7, 11))  # ἰδοὺ ὧδε ὁ Χριστός
        + list(range(12, 14))  # ἰδοὺ ἐκεῖ
        + list(range(15, 17))  # μὴ πιστεύετε
    )
    assert passageA.clean == sequence_a
    assert passageB.clean == sequence_b


def test_answer():

    passageA = GreekText(grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23)
    # τότε ἐάν τις ὑμῖν εἴπῃ, ἰδοὺ ὧδε ὁ Χριστὸς ἢ ὧδε, μὴ πιστεύσητε·
    #    0   1   2    3    45    6   7 8       910  111213         1415
    # cleans to
    # τότε ἐάν τὶς ὑμεῖς εἶπον ἰδοὺ ὧδε ὁ χριστός ἤ ὧδε μή πιστεύω
    # which has 4 unique trigrams:
    # ὁ χριστός ἤ
    # χριστός ἤ ὧδε
    # ἤ ὧδε μή πιστεύω
    # ὧδε μή πιστεύω

    passageB = GreekText(grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21)
    # καὶ τότε ἐάν τις ὑμῖν εἴπῃ, ἰδοὺ ὧδε ὁ Χριστός, ἰδοὺ ἐκεῖ, μὴ πιστεύετε.
    #   0    1   2   3    4    56    7   8 9      1011  12   131415        1617
    # cleans to
    # καί τότε ἐάν τὶς ὑμεῖς εἶπον ἰδοὺ ὧδε ὁ χριστός ἰδοὺ ἐκεῖ μή πιστεύω
    # has 5 unique trigrams:
    # καί τότε ἐάν
    # ὁ χριστός ἰδοὺ
    # χριστός ἰδοὺ ἐκεῖ
    # ἰδοὺ ἐκεῖ μή
    # ἐκεῖ μή πιστεύω

    # 7 common trigrams:
    # τότε ἐάν τὶς
    # ἐάν τὶς ὑμεῖς
    # τὶς ὑμεῖς εἶπον
    # ὑμεῖς εἶπον ἰδοὺ
    # εἶπον ἰδοὺ ὧδε
    # ἰδοὺ ὧδε ὁ
    # ὧδε ὁ χριστός
    agreementFinder = NGramAgreementFinder(3)
    (score,
     a_matches_b,
     b_matches_a) = agreementFinder.agreement(passageA.lemmata, passageA.clean,
                                              passageB.lemmata, passageB.clean)
    # TODO: Also test a_matches_b and b_matches_a against lists above.
    assert math.isclose(score, 7 / ((4 + 7) + (5 + 7) - 7))
    # τότε ἐάν τις ὑμῖν εἴπῃ ἰδοὺ ὧδε
    assert a_matches_b == [0, 1, 2, 3, 4, 6, 7]
    # τότε ἐάν τις ὑμῖν εἴπῃ ἰδοὺ ὧδε
    assert b_matches_a == [1, 2, 3, 4, 5, 7, 8]
