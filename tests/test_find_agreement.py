import difflib
import unittest


# Test whether difflib continues counterintuitive behavior.
class TestFindAgreement(unittest.TestCase):
    def test_Mark_Matt_agreement(self):
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
        # "If isjunk was provided, first the longest matching block is determined
        # as above, but with the additional restriction that no junk element
        # appears in the block. Then that block is extended as far as possible by
        # matching (only) junk elements on both sides. So the resulting block never
        # matches on junk except as identical junk happens to be adjacent to an
        # interesting match." ~ https://docs.python.org/3/library/difflib.html
        longest_match_adjacent_junk = ["τότε", "ἐάν", "τὶς", "ὑμεῖς", "εἶπον", ","]

        matcher = difflib.SequenceMatcher(lambda x: x in ",.·", mark, matt)
        longest_match = matcher.find_longest_match()
        self.assertEqual(longest_match.a, 1)
        self.assertEqual(longest_match.b, 0)
        self.assertEqual(longest_match.size, 6)
        self.assertEqual(
            mark[longest_match.a : longest_match.a + longest_match.size],
            longest_match_adjacent_junk,
        )
        self.assertEqual(
            matt[longest_match.b : longest_match.b + longest_match.size],
            longest_match_adjacent_junk,
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
        self.assertEqual(matches[0].a, 1)
        self.assertEqual(matches[0].b, 0)
        self.assertEqual(matches[0].size, 10)
        self.assertEqual(
            mark[matches[0].a : matches[0].a + matches[0].size],
            longest_match_including_junk,
        )
        self.assertEqual(
            matt[matches[0].b : matches[0].b + matches[0].size],
            longest_match_including_junk,
        )

        self.assertEqual(matches[1].a, 14)
        self.assertEqual(matches[1].b, 12)
        self.assertEqual(matches[1].size, 3)
        self.assertEqual(
            mark[matches[1].a : matches[1].a + matches[1].size],
            [",", "μή", "πιστεύω"],
        )
        self.assertEqual(
            matt[matches[1].b : matches[1].b + matches[1].size],
            [",", "μή", "πιστεύω"],
        )

        # “The last triple is a dummy, and has the value (len(a), len(b), 0).”
        self.assertEqual(matches[2].a, len(mark))
        self.assertEqual(matches[2].b, len(matt))
        self.assertEqual(matches[2].size, 0)


if __name__ == "__main__":
    unittest.main()
