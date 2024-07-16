from agreement.cltk import Greek, get_n_gram_Jaccard_index
from tests.config import grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23
from tests.config import grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21


def test_answer():
    greek = Greek()

    doc_a = greek.NLP.analyze(text=grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23)
    doc_b = greek.NLP.analyze(text=grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21)
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

    # τότε ἐάν τὶς ὑμεῖς εἶπον ἰδοὺ ὧδε ὁ χριστός ἤ ὧδε μή πιστεύω
    # has 4 unique trigrams:
    # ὁ χριστός ἤ
    # χριστός ἤ ὧδε
    # ἤ ὧδε μή πιστεύω
    # ὧδε μή πιστεύω
    lemmata_a = [doc_a.lemmata[i] for i in sequence_a]
    print(lemmata_a)

    # καί τότε ἐάν τὶς ὑμεῖς εἶπον ἰδοὺ ὧδε ὁ χριστός ἰδοὺ ἐκεῖ μή πιστεύω
    # has 5 unique trigrams:
    # καί τότε ἐάν
    # ὁ χριστός ἰδοὺ
    # χριστός ἰδοὺ ἐκεῖ
    # ἰδοὺ ἐκεῖ μή
    # ἐκεῖ μή πιστεύω
    lemmata_b = [doc_b.lemmata[i] for i in sequence_b]

    # 7 common trigrams:
    # τότε ἐάν τὶς
    # ἐάν τὶς ὑμεῖς
    # τὶς ὑμεῖς εἶπον
    # ὑμεῖς εἶπον ἰδοὺ
    # εἶπον ἰδοὺ ὧδε
    # ἰδοὺ ὧδε ὁ
    # ὧδε ὁ χριστός
    assert get_n_gram_Jaccard_index(lemmata_a, lemmata_b, 3) == 7 / (
        (4 + 7) + (5 + 7) - 7
    )
