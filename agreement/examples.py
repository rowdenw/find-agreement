from agreement.bible_api import get_chapter
from agreement.color_scheme import ColorScheme, GoodacreColorScheme
from agreement.synoptic_table_model import SynopticTableModel, ParallelTuple
from agreement.synoptic_table_rich_text import SynopticTableRichText
import tests.config


def run_example(table_title: str, passages, report_filename, color_scheme=None):
    synopsis_model: SynopticTableModel = SynopticTableModel.build_synoptic_table(table_title, passages)
    
    rich_table_view = SynopticTableRichText(
        synopsis_model,
        color_scheme=color_scheme
    )
    rich_table_view.print_to_console()


def main():
    run_example(
        "14 John's Preaching of Repentance",
        [
            ParallelTuple(title="Matt. 3:7-10", text=get_chapter("grc-byz1904", "καταματθαιον", 3, 7, 10)),
            ParallelTuple(title="Luke 3:7-9", text=get_chapter("grc-byz1904", "καταλουκαν", 3, 7, 9))
        ],
        "014-Matt+Luke.html",
        color_scheme = ColorScheme({1: "blue", 2: "yellow", 3: "green"})

    )

    run_example(
        "68 On Judging (Log and Speck)",
        [
            ParallelTuple(title="Matt. 7:3-5", text=get_chapter("grc-byz1904", "καταματθαιον", 7, 3, 5)),
            ParallelTuple(title="Luke 6:41-43", text=get_chapter("grc-byz1904", "καταλουκαν", 6, 41, 43))
        ],
        "068-Matt+Luke.html"
    )

    run_example(
        "128 The Parable of the Mustard Seed (First Verse)",
        [
            ParallelTuple(title="Mark 4:30", text=tests.config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30),
            ParallelTuple(title="Matt. 13:31", text=tests.config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31),
            ParallelTuple(title="Luke 13:18-19", text=tests.config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19)
        ],
        "128-Mark+Matt+Luke.html",
        color_scheme = ColorScheme({3: "yellow", 6: "green"})
    )

    run_example(
        "128 The Parable of the Mustard Seed (First Verse)",
        [
            ParallelTuple(title="Matt. 13:31", text=tests.config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31),
            ParallelTuple(title="Mark 4:30", text=tests.config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30),
            ParallelTuple(title="Luke 13:18-19", text=tests.config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19)
        ],
        "128-Matt+Mark+Luke.html",
        color_scheme = GoodacreColorScheme(column_Matthew=0, column_Mark=1, column_Luke=2)
    )

    run_example(
        "291 False Christs and False Prophets",
        [
            ParallelTuple(title="Mark 13:21-23", text=get_chapter("grc-byz1904", "καταμαρκον", 13, 21, 23)),
            ParallelTuple(title="Matt. 24:23-25", text=get_chapter("grc-byz1904", "καταματθαιον", 24, 23, 25))
         ],
        "291-Mark+Matt.svg"
    )

if __name__ == "__main__":
    main()
