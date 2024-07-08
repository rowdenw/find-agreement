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
        table = synopsis.makeTable()
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
        table = synopsis.makeTable()
        self.assertEqual(table.title, "291 False Christs and False Prophets")
        self.assertEqual(table.columns[0].header, "Mark 13:21")
        self.assertEqual(table.columns[1].header, "Matt. 24:23")
        self.assertEqual(table.row_count, 1)

    def test_two_data(self):
        synopsis = Synopsis(
            "291 False Christs and False Prophets",
            left_passage="Mark 13:21",
            right_passage="Matt. 24:23",
            left_text=config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21,
            right_text=config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23,
        )
        data = synopsis.getData()
        left_highlighted = " καὶ[yellow] τότε ἐάν τις ὑμῖν εἴπῃ, ἰδοὺ ὧδε ὁ Χριστός[/yellow], ἰδοὺ ἐκεῖ[yellow], μὴ πιστεύετε[/yellow]."
        self.assertEqual(data.iat[0, 0], left_highlighted)
        self.assertEqual(data.iloc[0]["Mark 13:21"], left_highlighted)
        right_highlighted = "[yellow] τότε ἐάν τις ὑμῖν εἴπῃ, ἰδοὺ ὧδε ὁ Χριστὸς[/yellow] ἢ ὧδε[yellow], μὴ πιστεύσητε[/yellow]·"
        self.assertEqual(data.iat[0, 1], right_highlighted)
        self.assertEqual(data.iloc[0]["Matt. 24:23"], right_highlighted)
        #TODO: summary = synopsis.getSummary()
        #TODO: self.assertEqual(summary.iloc["count"]["Mark 13:21"], 14)


if __name__ == "__main__":
    unittest.main()
