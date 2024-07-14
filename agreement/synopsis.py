from rich.table import Table

from agreement.cltk import Greek, get_sequence, match_sequences


class Synopsis:
    """
    A synopsis of passages and text.

    Attributes
    ----------
    pandas.DataFrame
        tabular data with one row per passage
        and one column per analysis result:

        longest sequence: longest common subsequence
            https://en.wikipedia.org/wiki/Longest_common_subsequence
        longest string: longest string of verbatim agreement
            or common substring
            https://en.wikipedia.org/wiki/Longest_common_substring
    rich.table
        table with one column per passage and rows of text and analysis,
        suitable for printing to console or SVG
    """

    def __init__(self, title, **kwargs):
        self.table = Table(show_footer=True)
        self.table.title = title
        if kwargs.get("left_passage"):
            self.table.add_column(kwargs["left_passage"])
        if kwargs.get("right_passage"):
            self.table.add_column(kwargs["right_passage"])
        if kwargs.get("left_text") and kwargs.get("right_text"):
            greek = Greek()
            doc_a = greek.NLP.analyze(text=kwargs.get("left_text"))
            sequence_a = get_sequence(doc_a)
            doc_b = greek.NLP.analyze(text=kwargs.get("right_text"))
            sequence_b = get_sequence(doc_b)
            (agreement, a_matches_b, b_matches_a) = match_sequences(
                doc_a, sequence_a, doc_b, sequence_b
            )
            self.table.add_row(
                get_highlight(a_matches_b, doc_a.pos, doc_a.tokens),
                get_highlight(b_matches_a, doc_b.pos, doc_b.tokens),
            )
            self.table.add_row(str(len(sequence_a)) + " words",
                               str(len(sequence_b)) + " words")
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


def get_highlight(matches, pos, tokens):
    highlight = ""
    prev_match = False
    for i, token in enumerate(tokens):
        current_match = i in matches
        if current_match and not prev_match:
            if i > 0 and pos[i] != "PUNCT":
                highlight += " "
            highlight += "[yellow]" + token
        elif not current_match and prev_match:
            highlight += "[/yellow]"
            if i > 0 and pos[i] != "PUNCT":
                highlight += " "
            highlight += token
        else:
            if i > 0 and pos[i] != "PUNCT":
                highlight += " "
            highlight += token
        prev_match = current_match
    return highlight
