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
    console.save_svg("example.svg")


if __name__ == "__main__":
    main()
