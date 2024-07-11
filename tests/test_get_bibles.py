from agreement.bible_api import get_bibles
import unittest

from tests import config


class TestGetBibles(unittest.TestCase):
    def test_get_bibles(self):
        # https://github.com/wldeh/bible-api/blob/main/bibles/bibles.json
        bibles = get_bibles()
        self.assertEqual(
            bibles.loc[bibles["id"] == "grc-byz1904",
                       "version"].to_string(
                           index=False)[0:len(config.grc_byz1904_VERSION)],
            config.grc_byz1904_VERSION
        )
