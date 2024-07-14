from rich.table import Table
import pandas as pd

from agreement.cltk import match_lemmata


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
        self.data = pd.DataFrame()

        self.table = Table(show_footer=True)
        self.table.title = title
        if kwargs.get("left_passage"):
            self.table.add_column(kwargs["left_passage"])
        if kwargs.get("right_passage"):
            self.table.add_column(kwargs["right_passage"])
        if kwargs.get("left_text") and kwargs.get("right_text"):
            self.data["passage"] = [
                kwargs.get("left_passage"),
                kwargs.get("right_passage"),
            ]
            left_text = kwargs["left_text"]
            right_text = kwargs["right_text"]
            self.data["raw text"] = [kwargs["left_text"], kwargs["right_text"]]
            (longest_sequence, longest_string, left_count, left_data,
             right_count, right_data) = (
                match_lemmata(left_text, right_text)
            )
            self.data["longest sequence"] = [longest_sequence,
                                             longest_sequence]
            self.data["highlighted text"] = [left_data, right_data]
            self.data["longest string"] = [longest_string, longest_string]
            self.data["word count"] = [left_count, right_count]
            self.table.add_row(left_data, right_data)
            self.table.add_row(str(left_count) + " words",
                               str(right_count) + " words")
            self.table.columns[0].footer = (
                "longest common subsequence: "
                + str(longest_sequence) + " words"
                + "\nlongest common substring: "
                + str(longest_string) + " words"
            )
        elif kwargs.get("left_text"):
            self.table.add_row(kwargs["left_text"])
        elif kwargs.get("right_text"):
            self.table.add_row(kwargs["right_text"])

    def getData(self):
        """
        Get data resulting from analysis, e.g., for testing.

        Returns
        -------
        pandas.DataFrame
            tabular data with one row per passage
            and one column per analysis result

        See Also
        --------
        Synopsis.getTable : transposed data in printable form
        """
        return self.data

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
    highlight = ''
    prev_match = False
    for i, token in enumerate(tokens):
        current_match = i in matches
        if current_match and not prev_match:
            if i > 0 and pos[i] != "PUNCT":
                highlight += ' '
            highlight += "[yellow]" + token
        elif not current_match and prev_match:
            highlight += "[/yellow]"
            if i > 0 and pos[i] != "PUNCT":
                highlight += ' '
            highlight += token
        else:
            if i > 0 and pos[i] != "PUNCT":
                highlight += ' '
            highlight += token
        prev_match = current_match
    return highlight
