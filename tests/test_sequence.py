from agreement.cltk import Greek, get_sequence, match_sequences
import tests.config as config


def grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_3_7_10_sequence():
    return (
        list(range(0, 14))  # token 14 is ·
        + list(range(15, 17))  # token 17 is ,
        + list(range(18, 26))  # token 26 is ;
        + list(range(27, 33))  # token 33 is ,
        + list(range(34, 40))  # token 40 is ,
        + list(range(41, 45))  # token 45 is .
        + list(range(46, 61))  # token 61 is .
        + list(range(62, 73))  # token 73 is ·
        + list(range(74, 86))  # token 86 is .
    )


def grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_3_7_9_sequence():
    return (
        list(range(0, 7))  # token 7 is ᾽
        + list(range(8, 9))  # token 9 is ·
        + list(range(10, 12))  # token 12 is ,
        + list(range(13, 21))  # token 21 is ;
        + list(range(22, 28))  # token 28 is ,
        + list(range(29, 35))  # token 35 is ,
        + list(range(36, 40))  # token 40 is ·
        + list(range(41, 56))  # token 56 is .
        + list(range(57, 68))  # token 68 is ·
        + list(range(69, 81))  # token 81 is ·
    )


def test_match_sequences():
    greek = Greek()
    doc_a = greek.NLP.analyze(text=config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_3_7_10())
    sequence_a = get_sequence(doc_a)
    doc_b = greek.NLP.analyze(text=config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_3_7_9())
    sequence_b = get_sequence(doc_b)
    (agreement, a_matches_b, b_matches_a) = match_sequences(doc_a, sequence_a,
                                                 doc_b, sequence_b)
    assert a_matches_b[0:23] == (
        [3]  # ὁ
        + [13]  # αὐτός
        + list(range(15, 17))  # γέννημα ἔχιδνα
        + list(range(18, 26))  # τίς ὑπέδειξεν ὑμῖν φυγεῖν ἀπὸ τῆς μελλούσης ὀργῆς
        + list(range(27, 33))  # ποιήσατε οὖν καρπὸν ἄξιον τῆς μετανοίας
        + list(range(34, 36))  # καὶ μὴ
        + list(range(37, 40))  # λέγειν ἐν ἑαυτοῖς
    )
    assert b_matches_a[0:23] == (
        [2]  # τοῖς
        + [8]  # αὐτοῦ
        + list(range(10, 12))  # γεννήματα ἐχιδνῶν
        + list(range(13, 21))  # τίς ὑπέδειξεν ὑμῖν φυγεῖν ἀπὸ τῆς μελλούσης ὀργῆς
        + list(range(22, 28))  # ποιήσατε οὖν καρποὺς ἀξίους τῆς μετανοίας
        + list(range(29, 31))  # καὶ μὴ
        + list(range(32, 35))  # λέγειν ἐν ἑαυτοῖς
    )


def test_Matt_3_7_10_sequence():
    greek = Greek()
    doc = greek.NLP.analyze(text=config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_3_7_10())
    sequence = get_sequence(doc)
    assert sequence == grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_3_7_10_sequence()


def test_Luke_3_7_9_sequence():
    greek = Greek()
    doc = greek.NLP.analyze(text=config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_3_7_9())
    sequence = get_sequence(doc)
    assert sequence == grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_3_7_9_sequence()
