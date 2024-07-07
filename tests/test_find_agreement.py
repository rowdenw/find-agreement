import difflib
import unittest

#TODO: Can this be changed to run the code? If not, delete.
class TestFindAgreement(unittest.TestCase):
    def test_Mark_Matt_agreement(self):
        mark = ['καί', 'τότε', 'ἐάν', 'τὶς', 'ὑμεῖς', 'εἶπον', ',', 'ἰδοὺ', 'ὧδε',
                'ὁ', 'χριστός', ',', 'ἰδοὺ', 'ἐκεῖ', ',', 'μή', 'πιστεύω', '.']
        matt = ['τότε', 'ἐάν', 'τὶς', 'ὑμεῖς', 'εἶπον', ',', 'ἰδοὺ', 'ὧδε', 'ὁ',
                'χριστός', 'ἤ', 'ὧδε', ',', 'μή', 'πιστεύω', '·']
        matcher = difflib.SequenceMatcher(lambda x: x in ",.·", mark, matt)
        match = matcher.find_longest_match()
        self.assertEqual(match.a, 1)
        self.assertEqual(match.b, 0)
        # Skipping junk means match size is 6 rather than 10?
        self.assertEqual(match.size, 6)
        for match in matcher.get_matching_blocks():
            print("Match             : {}".format(match))
            print("Matching Sequence : {}".format(mark[match.a:match.a+match.size]))

if __name__ == "__main__":
    unittest.main()
