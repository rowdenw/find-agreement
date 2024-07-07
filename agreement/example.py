from agreement.bible_api import get_verse
from rich.console import Console
from agreement.synopsis import Synopsis


def main():
    synopsis = Synopsis(
        "291 False Christs and False Prophets",
        left_passage="Mark 13:21",
        right_passage="Matt. 24:23",
        left_text=get_verse("grc-byz1904", "καταμαρκον", 13, 21),
        right_text=get_verse("grc-byz1904", "καταματθαιον", 24, 23),
    )
    table = synopsis.table
    console = Console(record=True)
    console.print(table)
    console.save_svg("example.svg")


if __name__ == "__main__":
    main()
