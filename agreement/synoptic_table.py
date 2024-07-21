import rich
from rich.table import Table

from agreement.agreement import calculate_agreement_types
from agreement.color_scheme import ColorScheme
from agreement.greek_text import GreekText


class SynopticTable:
    """
    A synopsis of passages and text.

    Attributes
    ----------
    rich.table
        table with one column per passage and rows of text and analysis,
        suitable for printing to console or SVG
    """

    def __init__(self, title, parallels,
                 color_scheme=ColorScheme(None, None, None, "yellow")):
        self.table = Table(show_footer=True)
        self.table.title = title
        passages, texts = list(zip(*parallels))
        greekTexts = []
        for text in texts:
            greekTexts.append(GreekText(text))
        agreement_types = calculate_agreement_types(greekTexts)
        cells = []
        descriptions = []
        for index, agreement_type in enumerate(agreement_types):
            cells.append(get_color_text(color_scheme,
                                        zip(greekTexts[index].pos,
                                            greekTexts[index].tokens,
                                            agreement_type)))
            descriptions.append(str(len(greekTexts[index].clean)) + " words")
        for index, passage in enumerate(passages):
            self.table.add_column(header=passage, footer=descriptions[index])
        self.table.add_row(*cells)

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
