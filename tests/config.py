import json

import pandas as pd


grc_byz1904_VERSION = "1904 Patriarchal Greek New Testament"


def grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_3_7_10():
    with open("tests/grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_3.json") as read:
        data = json.load(read)
    df = pd.json_normalize(data["data"])
    text = df["text"]
    return " ".join(text[7 - 1: 10])


grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23 = (
    "τότε ἐάν τις ὑμῖν εἴπῃ, ἰδοὺ ὧδε ὁ Χριστὸς ἢ ὧδε, μὴ πιστεύσητε·"
)
grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21 = (
    "καὶ τότε ἐάν τις ὑμῖν εἴπῃ, ἰδοὺ ὧδε ὁ Χριστός, ἰδοὺ ἐκεῖ, μὴ πιστεύετε."
)


def grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_3_7_9():
    with open("tests/grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_3.json") as read:
        data = json.load(read)
    df = pd.json_normalize(data["data"])
    text = df["text"]
    return " ".join(text[7 - 1: 9])
