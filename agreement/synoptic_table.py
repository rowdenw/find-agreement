import rich
from rich.table import Table
from collections import namedtuple
from typing import List

from agreement.agreement import calculate_agreement_types
from agreement.color_scheme import ColorScheme
from agreement.greek_text import GreekText

Parallel = namedtuple('Parallel', ['title', 'text', 'footer'])


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
            get_color_text(
                self.color_scheme,
                zip(
                    greek_texts[index].pos, # part of speech
                    greek_texts[index].tokens, # greek word
                    agreement_type # numeric code for agreement type, which is translated to color
                )
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


def get_color_text(colorScheme, token_agreement):
    prev = None
    text = rich.text.Text()
    for pos, token, type in token_agreement:
        to_print = print_Greek_token(token, pos, prev)
        style = colorScheme.get_color(type)
        text.append(to_print, style=style)
        prev = token
    return text.markup
