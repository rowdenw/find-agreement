import unittest

import tests.config as config
from agreement.synopsis import Synopsis


class TestMakeTable(unittest.TestCase):
    def test_one_title_header(self):
        synopsis = Synopsis(
            "291 False Christs and False Prophets",
            left_passage="Mark 13:21",
            left_text=config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21,
        )
        table = synopsis.getTable()
        self.assertEqual(table.title, "291 False Christs and False Prophets")
        self.assertEqual(table.columns[0].header, "Mark 13:21")
        self.assertEqual(table.row_count, 1)

    def test_two_title_header(self):
        synopsis = Synopsis(
            "291 False Christs and False Prophets",
            left_passage="Mark 13:21",
            right_passage="Matt. 24:23",
            left_text=config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21,
            right_text=config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23,
        )
        table = synopsis.getTable()
        self.assertEqual(table.title, "291 False Christs and False Prophets")
        self.assertEqual(table.columns[0].header, "Mark 13:21")
        self.assertEqual(table.columns[1].header, "Matt. 24:23")
        self.assertEqual(table.row_count, 2)


if __name__ == "__main__":
    unittest.main()
