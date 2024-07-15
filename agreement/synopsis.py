from rich.table import Table

from agreement.cltk import Greek, get_sequence, match_sequences


class Synopsis:
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
            greek = Greek()
            doc_a = greek.NLP.analyze(text=kwargs.get("left_text"))
            sequence_a = get_sequence(doc_a)
            doc_b = greek.NLP.analyze(text=kwargs.get("right_text"))
            sequence_b = get_sequence(doc_b)
            (agreement, a_matches_b, b_matches_a) = match_sequences(
                doc_a, sequence_a, doc_b, sequence_b
            )
            self.table.add_row(
                get_highlight(
                    a_matches_b, doc_a.pos, doc_a.tokens,
                    agreement=highlight, column=left_column
                ),
                get_highlight(
                    b_matches_a, doc_b.pos, doc_b.tokens,
                    agreement=highlight, column=right_column
                ),
            )
            self.table.add_row(
                str(len(sequence_a)) + " words",
                str(len(sequence_b)) + " words"
            )
            self.table.columns[0].footer = (
                "longest common subsequence: "
                + str(sum(list(agreement.keys())))
                + " words"
                + "\nlongest common substring: "
                + str(max(agreement.keys()))
                + " words"
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
