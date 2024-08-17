import rich
from rich.table import Table
from rich.console import Console
from typing import List, Optional

from agreement.color_scheme import ColorScheme
from agreement.synoptic_table_model import SynopticTableModel, TokenAgreementTuple


class SynopticTableRichText:
    """
    A synopsis of passages and text.

    Attributes
    ----------
    rich.table
        table with one column per passage and rows of text and analysis,
        suitable for printing to console or SVG
    """
    _default_color_scheme=ColorScheme({3: "yellow"})

    def __init__(self, table_model: SynopticTableModel, color_scheme: Optional[ColorScheme]=None):
        self._table_model = table_model
        self._rich_console = None

        self._color_scheme: Optional[ColorScheme]
        if (color_scheme == None):
                self._color_scheme = self._default_color_scheme
        else:
                self._color_scheme = color_scheme
        assert self._color_scheme is not None

        self._table = Table(show_footer=True)
        self._table.title = table_model.table_title
        token_agreements = self._table_model.token_agreements
        cells = [
            get_colorized_text_for_tokens(
                self._color_scheme,
                token_agreement_list
            )
            for token_agreement_list in token_agreements
        ]

        descriptions = [
            f"{count} words"
            for count in self._table_model.word_counts
        ]

        for index in range(len(self._table_model.column_headings)):
            self._table.add_column(
                header=self._table_model.column_headings[index],
                footer=descriptions[index]
            )

        self._table.add_row(*cells)


    def print_to_console(self):
        if self._rich_console is None:
            self._rich_console = Console(record=True)
        self._rich_console.print(self._table)


    # Leaving here for testing, but no longer intended to be used.
    # Call print_to_console.
    @property
    def table(self):
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
        return self._table


def get_colorized_text_for_tokens(colorScheme: ColorScheme, token_agreements: List[TokenAgreementTuple]) -> str:
    """
    Get a string of text marked up with colors showing agreement type, for a 
    single column of an agreements table.

    Parameters:
    -----------
    colorScheme (ColorScheme): Maps agreement type code to display color.
    token_agreement (List[TokenAgreement]): List of tuples, each of which
        has a part of speech (pos), a text token, and the encoded agreement
        type for that token in that column.

    Returns:
    --------
    str:
        A string of (Greek) text, interspersed with Rich markup giving each
        word a color indicating the type of agreement. This string becomes
        the content of a cell in an agreement table.

        Example output:
        '[brown]Ἔλεγε[yellow][/brown] δέ[/yellow]·[yellow] τίνι[orange][/yellow]
        ὁμοία[orange][/orange] ἐστὶν[brown][/orange] ἡ[brown][/brown] βασιλεία[brown][/brown]
        τοῦ[green][/brown] Θεοῦ[/green],[yellow] καὶ[green][/yellow] τίνι[yellow][/green]
        ὁμοιώσω[brown][/yellow] αὐτήν[/brown];"
    """
    text = rich.text.Text()
    for pos, token, agreement_type, printable_text in token_agreements:
        style = colorScheme.get_color(agreement_type)
        text.append(printable_text, style=style)
    return text.markup
