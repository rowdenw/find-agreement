import rich
from rich.table import Table
from collections import namedtuple
from typing import List, Optional
from agreement.synoptic_table_model import SynopticTableModel, PreparedTokenTuple

from agreement.agreement import calculate_agreement_types
from agreement.color_scheme import ColorScheme

class SynopticTableRichText:
    def __init__(self, table_model: SynopticTableModel,
                 color_scheme=ColorScheme(None, None, None, "yellow")):
            self.table_model = table_model
            self.color_scheme = color_scheme

            self._table = Table(show_footer=True)
            self._table.title = table_model.table_title

            word_counts: List[int] = table_model.word_counts
            for index in range(len(table_model.column_headings)):
                column_header = table_model.column_headings[index]
                column_footer = f"{table_model.word_counts[index]} words"
                self._table.add_column(header=column_header, footer=column_footer)

            cells = [
                get_colorized_text_for_tokens(self.color_scheme, tokens)
                for tokens in self.table_model.prepared_texts
            ]
            self.table.add_row(*cells)


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

# def print_Greek_token(token: str, pos: str, previous: Optional[str], scripta_continua: bool = False):
#     # https://www.billmounce.com/greekalphabet/greek-punctuation-syllabification
#     # https://blog.greek-language.com/2022/02/14/punctuation-in-ancient-greek-texts-part-i/
#     # https://www.opoudjis.net/unicode/punctuation.html
#     # https://en.wikipedia.org/wiki/Ancient_Greek_grammar#Alphabet
#     if pos == "PUNCT":  # token in "·,;."
#         # https://library.biblicalarchaeology.org/article/punctuationinthenewtestament/
#         # https://en.wikipedia.org/wiki/Scriptio_continua
#         if scripta_continua:
#             return ""
#         else:
#             return token
#     else:
#         if previous is None or previous == "\n" or scripta_continua:
#             return token
#         else:
#             return " " + token

def get_colorized_text_for_tokens(colorScheme: ColorScheme, token_agreement: List[PreparedTokenTuple]) -> str:
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
    for token, agreement_type in token_agreement:
        style: Optional[str] = colorScheme.get_color(agreement_type)
        text.append(token, style=style)
    return text.markup
