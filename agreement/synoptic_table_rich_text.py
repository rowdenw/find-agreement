import rich
from rich.table import Table
from collections import namedtuple
from typing import List, Optional

from agreement.agreement import calculate_agreement_types
from agreement.color_scheme import ColorScheme
from agreement.greek_text import GreekText
from agreement.synoptic_table_model import SynopticTableModel, TokenAgreementTuple

# TokenAgreement = namedtuple('TokenAgreement', [
#     'pos', # part of speech
#     'token', # greek word
#     'agreement_type' # numeric code for agreement type, which is translated to color
# ])

class SynopticTableRichText:
    """
    A synopsis of passages and text.

    Attributes
    ----------
    rich.table
        table with one column per passage and rows of text and analysis,
        suitable for printing to console or SVG
    """
    _default_color_scheme=ColorScheme(None, None, None, "yellow")

    def __init__(self, table_model: SynopticTableModel, color_scheme: Optional[ColorScheme]=None):
        self._table_model = table_model
        # self._color_scheme = color_scheme
        self._color_scheme: Optional[ColorScheme]
        if (color_scheme == None):
                self._color_scheme = self._default_color_scheme
        else:
                self._color_scheme = color_scheme
        assert self._color_scheme is not None

        # self.parallels = parallels
        self._parallels = table_model.parallels

        self._table = Table(show_footer=True)
        # self.table.title = title
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

    # def process_synopsis(self):
    #     passage_titles = [passage.title for passage in self.parallels]
    #     agreement_types = calculate_agreement_types(greek_texts)
    #     greek_texts = [GreekText(passage.text) for passage in self.parallels]

    #     cells = [
    #         get_colorized_text_for_tokens(
    #             self._color_scheme,
    #             [TokenAgreementTuple(*t) for t in zip(
    #                 greek_texts[index].pos, # part of speech
    #                 greek_texts[index].tokens, # greek word
    #                 agreement_type # numeric code for agreement type, which is translated to color
    #             )]
    #         )
    #         for index, agreement_type in enumerate(agreement_types)
    #     ]

    #     descriptions = [
    #         f"{len(greek_texts[index].clean)} words"
    #         for index in range(len(greek_texts))
    #     ]

    #     for index, passage in enumerate(passage_titles):
    #         self.table.add_column(header=passage, footer=descriptions[index])

    #     self.table.add_row(*cells)

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


def get_colorized_text_for_tokens(colorScheme: ColorScheme, token_agreement: List[TokenAgreementTuple]) -> str:
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
    prev = None
    text = rich.text.Text()
    for pos, token, agreement_type in token_agreement:
        to_print = print_Greek_token(token, pos, prev)
        style = colorScheme.get_color(agreement_type)
        text.append(to_print, style=style)
        prev = token
    return text.markup
