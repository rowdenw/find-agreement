from rich.table import Table

from agreement.agreement import get_n_gram_Jaccard_index, match_sequences
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

    def __init__(self, title, **kwargs):
        self.table = Table(show_footer=True)
        self.table.title = title
        if kwargs.get("left_passage"):
            self.table.add_column(kwargs["left_passage"])
            if kwargs.get("left_column"):
                left_column = kwargs.get("left_column")
            else:
                left_column = ""
        if kwargs.get("right_passage"):
            self.table.add_column(kwargs["right_passage"])
            if kwargs.get("right_column"):
                right_column = kwargs.get("right_column")
            else:
                right_column = ""
        if kwargs.get("left_text") and kwargs.get("right_text"):
            if kwargs.get("agreement"):
                highlight = kwargs["agreement"]
            else:
                highlight = "yellow"
            passageA = GreekPassage(kwargs.get("left_text"))
            passageB = GreekPassage(kwargs.get("right_text"))
            (agreement, a_matches_b, b_matches_a) = match_sequences(
                passageA.lemmata, passageA.clean,
                passageB.lemmata, passageB.clean
            )
            self.table.add_row(
                get_highlight(
                    a_matches_b,
                    passageA.pos,
                    passageA.tokens,
                    agreement=highlight,
                    column=left_column,
                ),
                get_highlight(
                    b_matches_a,
                    passageB.pos,
                    passageB.tokens,
                    agreement=highlight,
                    column=right_column,
                ),
            )
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


def get_highlight(matches, pos, tokens, agreement="yellow", column=""):
    if len(column) > 0:
        column_start = "[" + column + "]"
        column_stop = "[/" + column + "]"
    else:
        column_start = ""
        column_stop = ""
    prev_match = False
    span_start = "[" + agreement + "]"
    span_stop = "[/" + agreement + "]"
    start_of_line = True
    text = ""
    for i, token in enumerate(tokens):
        current_match = i in matches
        if current_match and not prev_match:
            if i > 0:
                text += column_stop
            text += get_spacing(pos[i],
                                start_of_line, token) + span_start + token
        elif not current_match and prev_match:
            text += span_stop
            text += get_spacing(pos[i],
                                start_of_line, token) + column_start + token
        else:
            if i == 0:
                text = column_start
            else:
                text += get_spacing(pos[i], start_of_line, token)
            text += token
        prev_match = current_match
        start_of_line = token == "\n"
    if current_match:
        text += span_stop
    else:
        text += column_stop
    return text


def get_spacing(pos, start_of_line, token):
    if pos != "PUNCT" and not start_of_line and not token == "\n":
        return " "
    else:
        return ""


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
