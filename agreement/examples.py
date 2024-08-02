from rich.console import Console

from agreement.bible_api import get_chapter
from agreement.color_scheme import ColorScheme, GoodacreColorScheme
from agreement.config import get_report_path
from agreement.synoptic_table import SynopticTable, Parallel
import tests.config

def run_example(table_title, passages, report_filename, **kwargs):
    synoptic_table = SynopticTable(
        table_title, passages,
        **kwargs
    )

    synoptic_table.process_synopsis()
    table = synoptic_table.table
    print(table)
    console = Console(record=True)
    console.print(table)
    html_path = get_report_path(report_filename)
    console.save_html(html_path)

def main():
    run_example(
        "14 John's Preaching of Repentance",
        [
            Parallel(title="Matt. 3:7-10", text=get_chapter("grc-byz1904", "καταματθαιον", 3, 7, 10), footer=""),
            Parallel(title="Luke 3:7-9", text=get_chapter("grc-byz1904", "καταλουκαν", 3, 7, 9), footer="")
        ],
        "014-Matt+Luke.html",
        color_scheme = ColorScheme(None, "blue", "yellow", "green")

    )


    run_example(
        "68 On Judging (Log and Speck)",
        [
            Parallel(title="Matt. 7:3-5", text=get_chapter("grc-byz1904", "καταματθαιον", 7, 3, 5), footer=""),
            Parallel(title="Luke 6:41-43", text=get_chapter("grc-byz1904", "καταλουκαν", 6, 41, 43), footer="")
        ],
        "068-Matt+Luke.html"
    )

    run_example(
        "128 The Parable of the Mustard Seed (First Verse)",
        [
            Parallel(title="Mark 4:30", text=tests.config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30, footer=""),
            Parallel(title="Matt. 13:31", text=tests.config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31, footer=""),
            Parallel(title="Luke 13:18-19", text=tests.config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19, footer="")
        ],
        "128-Mark+Matt+Luke.html",
        color_scheme = ColorScheme(None, None, None, "yellow", None, None, "green")
    )

    run_example(
        "128 The Parable of the Mustard Seed (First Verse)",
        [
            Parallel(title="Matt. 13:31", text=tests.config.grc_byz1904_ΚΑΤΑ_ΜΑΤΘΑΙΟΝ_13_31, footer=""),
            Parallel(title="Mark 4:30", text=tests.config.grc_byz1904_ΚΑΤΑ_ΜΑΡΚΟΝ_4_30, footer=""),
            Parallel(title="Luke 13:18-19", text=tests.config.grc_byz1904_ΚΑΤΑ_ΛΟΥΚΑΝ_13_18_19, footer="")
        ],
        "128-Matt+Mark+Luke.html",
        color_scheme = GoodacreColorScheme(0, 1, 2)
    )

    run_example(
        "291 False Christs and False Prophets",
        [
            Parallel(title="Mark 13:21-23", text=get_chapter("grc-byz1904", "καταμαρκον", 13, 21, 23), footer=""),
            Parallel(title="Matt. 24:23-25", text=get_chapter("grc-byz1904", "καταματθαιον", 24, 23, 25), footer="")
         ],
        "291-Mark+Matt.svg"
    )

if __name__ == "__main__":
    main()
