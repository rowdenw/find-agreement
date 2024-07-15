import matplotlib.pyplot as plt

from agreement.bible_api import get_chapter
from agreement.cltk import Greek, get_sequence, match_sequences


def main():
    greek = Greek()
    doc_a = greek.NLP.analyze(
        text=get_chapter("grc-byz1904", "καταμαρκον",
                         13, 21, 23))
    sequence_a = get_sequence(doc_a)
    doc_b = greek.NLP.analyze(
        text=get_chapter("grc-byz1904", "καταματθαιον",
                         24, 23, 25)
    )
    sequence_b = get_sequence(doc_b)
    (agreement, a_matches_b, b_matches_a) = match_sequences(
        doc_a, sequence_a, doc_b, sequence_b
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
    fig.savefig("docs/_static/291-Mark+Matt.png")
    plt.show()


if __name__ == "__main__":
    main()
