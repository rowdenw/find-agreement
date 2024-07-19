import json

import pandas as pd


grc_byz1904_VERSION = "1904 Patriarchal Greek New Testament"

# https://www.bible-researcher.com/parallels.html


# 014 John's Preaching of Repentance
def grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_3_7_10():
    with open("tests/grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_3.json") as read:
        data = json.load(read)
    df = pd.json_normalize(data["data"])
    text = df["text"]
    return " ".join(text[7 - 1: 10])


def grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_3_7_9():
    with open("tests/grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_3.json") as read:
        data = json.load(read)
    df = pd.json_normalize(data["data"])
    text = df["text"]
    return " ".join(text[7 - 1: 9])


# 128 The Parable of the Mustard Seed (First Verse)
grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31 = "Ἄλλην παραβολὴν παρέθηκεν αὐτοῖς λέγων· \
ὁμοία ἐστὶν ἡ βασιλεία τῶν οὐρανῶν κόκκῳ σινάπεως, ὃν λαβὼν ἄνθρωπος ἔσπειρεν \
ἐν τῷ ἀγρῷ αὐτοῦ·"
grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30 = "Καὶ ἔλεγε· πῶς ὁμοιώσωμεν τὴν βασιλείαν τοῦ \
Θεοῦ; ἢ ἐν τίνι παραβολῇ παραβάλωμεν αὐτήν;"
grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19 = "Ἔλεγε δέ· τίνι ὁμοία ἐστὶν ἡ βασιλεία \
τοῦ Θεοῦ, καὶ τίνι ὁμοιώσω αὐτήν;"

# 235 The Day of the Son of Man (One Verse)
grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_24_23 = (
    "τότε ἐάν τις ὑμῖν εἴπῃ, ἰδοὺ ὧδε ὁ Χριστὸς ἢ ὧδε, μὴ πιστεύσητε·"
)
grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_13_21 = (
    "καὶ τότε ἐάν τις ὑμῖν εἴπῃ, ἰδοὺ ὧδε ὁ Χριστός, ἰδοὺ ἐκεῖ, μὴ πιστεύετε."
)
