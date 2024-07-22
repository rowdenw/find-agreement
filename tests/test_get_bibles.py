from agreement.bible_api import get_bibles
from tests import config


def test_get_bibles():
    # https://github.com/wldeh/bible-api/blob/main/bibles/bibles.json
    bibles = get_bibles()
    assert (
        bibles.loc[bibles["id"] == "grc-byz1904", "version"].to_string(index=False)[
            0: len(config.grc_byz1904_VERSION)
        ]
        == config.grc_byz1904_VERSION
    )
