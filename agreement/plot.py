import matplotlib.pyplot as plt

from agreement.agreement import match_sequences
from agreement.bible_api import get_chapter
from agreement.config import get_report_path
from agreement.passage import GreekPassage


def main():
    passageA = GreekPassage(get_chapter("grc-byz1904", "καταμαρκον",
                                        13, 21, 23))
    passageB = GreekPassage(get_chapter("grc-byz1904", "καταματθαιον",
                                        24, 23, 25))
    (agreement, a_matches_b, b_matches_a) = match_sequences(
        passageA.lemmata, passageA.clean,
        passageB.lemmata, passageB.clean
        )

    length = list(agreement.keys())
    length.sort()
    max_SVA = max(agreement.keys()) + 1
    data = {i: agreement.get(i, 0) * i for i in range(1, max_SVA)}

    fig, ax = plt.subplots()
    # fig.suptitle('Figure')
    y_pos = range(1, max_SVA)
    ax.barh(y_pos, data.values(), align='center')
    ax.set_title("Mark 13:21-23 & Matt. 24:23-25 Agreement")
    ax.set_xlabel("Total Words (length of SVA x number of instances)")
    ax.set_ylabel("Lengths of String of Verbatim Agreement (SVA)")
    ax.set_yticks(y_pos)

    fig_path = get_report_path('291-Mark+Matt.png')
    fig.savefig(fig_path)

    plt.show()


if __name__ == "__main__":
    main()
