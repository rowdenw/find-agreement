import difflib


# Test whether difflib continues counterintuitive behavior.
def test_Mark_Matt_agreement():
    mark = [
        "καί",
        "τότε",
        "ἐάν",
        "τὶς",
        "ὑμεῖς",
        "εἶπον",
        ",",
        "ἰδοὺ",
        "ὧδε",
        "ὁ",
        "χριστός",
        ",",
        "ἰδοὺ",
        "ἐκεῖ",
        ",",
        "μή",
        "πιστεύω",
        ".",
    ]
    matt = [
        "τότε",
        "ἐάν",
        "τὶς",
        "ὑμεῖς",
        "εἶπον",
        ",",
        "ἰδοὺ",
        "ὧδε",
        "ὁ",
        "χριστός",
        "ἤ",
        "ὧδε",
        ",",
        "μή",
        "πιστεύω",
        "·",
    ]
    # "If isjunk was provided, first the longest matching block is
    # determined as above, but with the additional restriction that no
    # junk element appears in the block. Then that block is extended as
    # far as possible by matching (only) junk elements on both sides. So
    # the resulting block never matches on junk except as identical junk
    # happens to be adjacent to an interesting match."
    # ~ https://docs.python.org/3/library/difflib.html
    longest_match_adjacent_junk = ["τότε", "ἐάν", "τὶς", "ὑμεῖς", "εἶπον", ","]

    matcher = difflib.SequenceMatcher(lambda x: x in ",.·", mark, matt)
    longest_match = matcher.find_longest_match()
    assert longest_match.a == 1
    assert longest_match.b == 0
    assert longest_match.size == 6
    assert (
        mark[longest_match.a: longest_match.a + longest_match.size]
        == longest_match_adjacent_junk
    )
    assert (
        matt[longest_match.b: longest_match.b + longest_match.size]
        == longest_match_adjacent_junk
    )

    matches = matcher.get_matching_blocks()

    # get_matching_blocks(), in contrast, will include junk:
    longest_match_including_junk = [
        "τότε",
        "ἐάν",
        "τὶς",
        "ὑμεῖς",
        "εἶπον",
        ",",
        "ἰδοὺ",
        "ὧδε",
        "ὁ",
        "χριστός",
    ]
    assert matches[0].a == 1
    assert matches[0].b == 0
    assert matches[0].size == 10
    assert (
        mark[matches[0].a: matches[0].a + matches[0].size]
        == longest_match_including_junk
    )
    assert (
        matt[matches[0].b: matches[0].b + matches[0].size]
        == longest_match_including_junk
    )

    assert matches[1].a == 14
    assert matches[1].b == 12
    assert matches[1].size == 3
    assert mark[matches[1].a: matches[1].a + matches[1].size] == [",", "μή",
                                                                  "πιστεύω"]
    assert matt[matches[1].b: matches[1].b + matches[1].size] == [",", "μή",
                                                                  "πιστεύω"]

    # “The last triple is a dummy, and has the value (len(a), len(b), 0).”
    assert matches[2].a == len(mark)
    assert matches[2].b == len(matt)
    assert matches[2].size == 0
