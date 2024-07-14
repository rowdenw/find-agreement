from agreement.bible_api import get_chapter
from rich.console import Console
from agreement.synopsis import Synopsis


def main():
    synopsis = Synopsis(
        "291 False Christs and False Prophets",
        left_passage="Mark 13:21-23",
        right_passage="Matt. 24:23-25",
        left_text=get_chapter("grc-byz1904", "καταμαρκον", 13, 21, 23),
        right_text=get_chapter("grc-byz1904", "καταματθαιον", 24, 23, 25),
    )
    table = synopsis.table
    console = Console(record=True)
    console.print(table)
    console.save_svg("docs/_static/291-Mark+Matt.svg")

    synopsis = Synopsis(
        "14 John's Preaching of Repentance",
        left_passage="Matt. 3:7-10",
        right_passage="Luke 3:7-9",
        left_text=get_chapter("grc-byz1904", "καταματθαιον", 3, 7, 10),
        right_text=get_chapter("grc-byz1904", "καταλουκαν", 3, 7, 9),
    )
    table = synopsis.table
    console = Console(record=True)
    console.print(table)
    console.save_html("docs/_static/014-Matt+Luke.html")

    synopsis = Synopsis(
        "68 On Judging (Log and Speck)",
        left_passage="Matt. 7:3-5",
        right_passage="Luke 6:41-43",
        left_text=get_chapter("grc-byz1904", "καταματθαιον", 7, 3, 5),
        right_text=get_chapter("grc-byz1904", "καταλουκαν", 6, 41, 43),
    )
    table = synopsis.table
    console = Console(record=True)
    console.print(table)
    console.save_html("docs/_static/068-Matt+Luke.html")


if __name__ == "__main__":
    main()
