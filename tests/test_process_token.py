import unittest

from agreement.cltk import process_token


class TestProcessToken(unittest.TestCase):
    def test_punctuation(self):
        token = ","
        (increment, new_text) = process_token("PUNCT", token, 6)
        self.assertEqual(increment, 0,
                         "Punctuation is not part of word count.")
        self.assertEqual(new_text, token, "Punction is included in output.")

    def test_newline(self):
        token = "\n"
        (increment, new_text) = process_token("ADP", token, 18)
        self.assertEqual(increment, 0, "Newline is not part of word count.")
        self.assertEqual(new_text, token, "Newline is included in output.")

    def test_first_word(self):
        token = "καί"
        (increment, new_text) = process_token("CCONJ", token, 0)
        self.assertEqual(increment, 1, "Word increments count.")
        self.assertEqual(new_text, token, "First word is unmodified.")

    def test_second_word(self):
        token = "τότε"
        (increment, new_text) = process_token("ADV", token, 1)
        self.assertEqual(increment, 1, "Word increments count.")
        self.assertEqual(new_text, ' ' + token, "Second word is after space.")
