from rich.console import Console

from agreement.bible_api import get_chapter
from agreement.color_scheme import ColorScheme
from agreement.config import get_report_path
from agreement.synoptic_table import SynopticTable


def main():
    synopticTable = SynopticTable(
        "291 False Christs and False Prophets",
        [
            ["Mark 13:21-23",
             get_chapter("grc-byz1904", "καταμαρκον", 13, 21, 23)],
            ["Matt. 24:23-25",
             get_chapter("grc-byz1904", "καταματθαιον", 24, 23, 25)],
        ],
    )
    table = synopticTable.table
    console = Console(record=True)
    console.print(table)

    svg_path = get_report_path("291-Mark+Matt.svg")
    console.save_svg(svg_path)

    synopticTable = SynopticTable(
        "14 John's Preaching of Repentance",
        [
            ["Matt. 3:7-10",
             get_chapter("grc-byz1904", "καταματθαιον", 3, 7, 10)],
            ["Luke 3:7-9",
             get_chapter("grc-byz1904", "καταλουκαν", 3, 7, 9)],
        ],
        color_scheme=ColorScheme(None, "blue", "yellow", "green"),
    )
    table = synopticTable.table
    console = Console(record=True)
    console.print(table)

    html_path = get_report_path("014-Matt+Luke.html")
    console.save_html(html_path)

    synopticTable = SynopticTable(
        "68 On Judging (Log and Speck)",
        [["Matt. 7:3-5", get_chapter("grc-byz1904", "καταματθαιον", 7, 3, 5)],
         ["Luke 6:41-43", get_chapter("grc-byz1904", "καταλουκαν", 6, 41, 43)]]
    )
    table = synopticTable.table
    console = Console(record=True)
    console.print(table)

    html_path = get_report_path("068-Matt+Luke.html")
    console.save_html(html_path)


if __name__ == "__main__":
    main()
