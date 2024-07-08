from rich.table import Table
import pandas as pd

from agreement.cltk import match_lemmata


class Synopsis:
    def __init__(self, title, **kwargs):
        self.data = pd.DataFrame()

        self.table = Table()
        self.table.title = title
        if kwargs.get("left_passage"):
            self.table.add_column(kwargs["left_passage"])
        if kwargs.get("right_passage"):
            self.table.add_column(kwargs["right_passage"])
        # TODO: Write tests to produce empty string if passage provided but no text.
        if kwargs.get("left_text") and kwargs.get("right_text"):
            self.data["passage"] = [
                kwargs.get("left_passage"),
                kwargs.get("right_passage"),
            ]
            left_text = kwargs["left_text"]
            right_text = kwargs["right_text"]
            self.data["raw text"] = [kwargs["left_text"], kwargs["right_text"]]
            # TODO: This could produce an error if there is text but no passage. Write test to raise error.
            left_data, right_data = match_lemmata(left_text, right_text)
            self.data["highlighted text"] = [left_data, right_data]
            self.table.add_row(left_data, right_data)
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
            tabular data with one column per analysis result and one row per passage

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
            table with one column per passage and rows of text and analysis, suitable for printing to console or SVG

        See Also
        --------
        Synopsis.getData : individual analysis results that are transposed for the table
        """
        return self.table
