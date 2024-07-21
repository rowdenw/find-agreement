import rich
from rich.table import Table

from agreement.agreement import calculate_agreement_type
from agreement.agreement import get_n_gram_Jaccard_index
from agreement.agreement import match_sequences
from agreement.color_scheme import ColorScheme
from agreement.passage import GreekPassage


class SynopsisTable:
    """
    A synopsis of passages and text.

    Attributes
    ----------
    rich.table
        table with one column per passage and rows of text and analysis,
        suitable for printing to console or SVG
    """

    def __init__(self, title, color_scheme=ColorScheme(None, None, None,
                                                       "yellow"), **kwargs):
        self.table = Table(show_footer=True)
        self.table.title = title
        if kwargs.get("left_passage"):
            self.table.add_column(kwargs["left_passage"])
        if kwargs.get("right_passage"):
            self.table.add_column(kwargs["right_passage"])
        if kwargs.get("left_text") and kwargs.get("right_text"):
            passageA = GreekPassage(kwargs.get("left_text"))
            passageB = GreekPassage(kwargs.get("right_text"))
            (agreement, a_matches_b, b_matches_a) = match_sequences(
                passageA.lemmata, passageA.clean,
                passageB.lemmata, passageB.clean
            )
            agreement_type = calculate_agreement_type([passageA, passageB])
            textA = get_color_text(color_scheme,
                                   zip(passageA.pos, passageA.tokens,
                                       agreement_type[0]))
            textB = get_color_text(color_scheme,
                                   zip(passageB.pos, passageB.tokens,
                                       agreement_type[1]))
            self.table.add_row(textA, textB)
            words_a = str(len(passageA.clean))
            words_b = str(len(passageB.clean))
            self.table.add_row(
                words_a + " words",
                words_b + " words"
            )
            J = get_n_gram_Jaccard_index(
                    [passageA.lemmata[i] for i in passageA.clean],
                    [passageB.lemmata[i] for i in passageB.clean],
                    3,
                )

            subsequence = sum(list(agreement.keys()))
            self.table.columns[0].footer = (
                "longest common subsequence: "
                + str(subsequence)
                + " words\n"
                + "longest common substring: "
                + str(max(agreement.keys()))
                + " words\n"
                + "trigram Jaccard index: "
                + "{:.2f}".format(J)
            )
        elif kwargs.get("left_text"):
            self.table.add_row(kwargs["left_text"])
        elif kwargs.get("right_text"):
            self.table.add_row(kwargs["right_text"])

    def getTable(self):
        """
        Get table showing text analysis.

        Returns
        -------
        rich.table
            table with one column per passage and rows of text and analysis,
            suitable for printing to console or SVG

        See Also
        --------
        Synopsis.getData : individual analysis results that are transposed for
        the table
        """
        return self.table


def print_Greek_token(token, pos, previous, scripta_continua=False):
    # https://www.billmounce.com/greekalphabet/greek-punctuation-syllabification
    # https://blog.greek-language.com/2022/02/14/punctuation-in-ancient-greek-texts-part-i/
    # https://www.opoudjis.net/unicode/punctuation.html
    # https://en.wikipedia.org/wiki/Ancient_Greek_grammar#Alphabet
    if pos == "PUNCT":  # token in "·,;."
        # https://library.biblicalarchaeology.org/article/punctuationinthenewtestament/
        # https://en.wikipedia.org/wiki/Scriptio_continua
        if scripta_continua:
            return ""
        else:
            return token
    else:
        if previous is None or previous == "\n" or scripta_continua:
            return token
        else:
            return " " + token


def get_color_text(colorScheme, token_agreement):
    prev = None
    text = rich.text.Text()
    for pos, token, type in token_agreement:
        to_print = print_Greek_token(token, pos, prev)
        style = colorScheme.get_color(type)
        text.append(to_print, style=style)
        prev = token
    return text.markup
