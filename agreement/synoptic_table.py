import rich
from rich.table import Table
from collections import namedtuple
from typing import List

from agreement.agreement import calculate_agreement_types
from agreement.color_scheme import ColorScheme
from agreement.greek_text import GreekText

Parallel = namedtuple('Parallel', [
    'title', # Title of a column in an agreement table
    'text', # Body text for one column in agreement table
    'footer' # Footer text for column showing count of matching words
])

TokenAgreement = namedtuple('TokenAgreement', [
    'pos', # part of speech
    'token', # greek word
    'agreement_type' # numeric code for agreement type, which is translated to color
])

class SynopticTable:
    """
    A synopsis of passages and text.

    Attributes
    ----------
    rich.table
        table with one column per passage and rows of text and analysis,
        suitable for printing to console or SVG
    """

    def __init__(self, title, parallels: List[Parallel],
                 color_scheme=ColorScheme(None, None, None, "yellow")):
        self.parallels = parallels
        self._table = Table(show_footer=True)
        self.table.title = title
        self.color_scheme = color_scheme


    def process_synopsis(self):
        passage_titles = [passage.title for passage in self.parallels]
        greek_texts = [GreekText(passage.text) for passage in self.parallels]
        agreement_types = calculate_agreement_types(greek_texts)

        cells = [
            get_colorized_text_for_tokens(
                self.color_scheme,
                [TokenAgreement(*t) for t in zip(
                    greek_texts[index].pos, # part of speech
                    greek_texts[index].tokens, # greek word
                    agreement_type # numeric code for agreement type, which is translated to color
                )]
            )
            for index, agreement_type in enumerate(agreement_types)
        ]

        descriptions = [
            f"{len(greek_texts[index].clean)} words"
            for index in range(len(greek_texts))
        ]

        for index, passage in enumerate(passage_titles):
            self.table.add_column(header=passage, footer=descriptions[index])

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


def get_colorized_text_for_tokens(colorScheme: ColorScheme, token_agreement: List[TokenAgreement]) -> str:
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

    See Also
    --------
    Synopsis.getData : individual analysis results that are transposed for
    the table
    """
    prev = None
    text = rich.text.Text()
    for pos, token, agreement_type in token_agreement:
        to_print = print_Greek_token(token, pos, prev)
        style = colorScheme.get_color(agreement_type)
        text.append(to_print, style=style)
        prev = token
    return text.markup
