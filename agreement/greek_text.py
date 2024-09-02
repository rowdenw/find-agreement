from typing import List, Optional

"""
Use Classical Language Toolkit for natural language processing (NLP) with a
general-purpose pipeline for Ancient Greek.

CLASS
-----
GreekPassage
    NLP analysis of a passage of Greek text
"""

from cltk import NLP

# TODO: How can this avoid warning "Model for 'grc' / 'txt' already present"?
NLP = NLP(language="grc", suppress_banner=True)


class GreekText:
    """
    NLP analysis of a passage of Greek text

    Attributes
    ----------
    clean : list
        Indices of Greek words in text, without newlines or punctuation
    lemmata : list
        canonical forms of each token in text
    """

    def __init__(self, text):
        self.doc = NLP.analyze(text=text)
        self._clean = [
            i
            for i, pos in enumerate(self.doc.pos)
            if pos != "PUNCT" and self.doc.tokens[i] != "\n"
        ]
        self._lemmata: List[str] = self.doc.lemmata
        # TODO: Remove if not needed by rewritten synopsis. Otherwise document.
        self._pos: List[str] = self.doc.pos
        # TODO: Remove if not needed by rewritten synopsis. Otherwise document.
        self._tokens: List[str] = self.doc.tokens

        self._printable_tokens: List[str] = get_printable_tokens(self._tokens, self._pos)

    @property
    def clean(self) -> List[int]:
        """
        List of indices (no text) of Greek words without newlines or
        punctuation
        """
        return self._clean

    @property
    def lemmata(self) -> List[str]:
        """
        List of canonical forms of each token in text
        """
        return self._lemmata

    @property
    def pos(self) -> List[str]:
        """
        List of parts of speech for each token in text
        """
        return self._pos

    @property
    def tokens(self) -> List[str]:
        """
        List of unprocessed (input) tokens
        """
        return self._tokens

    @property
    def printable_tokens(self) -> List[str]:
        """
        List of tokens processed for display
        """
        return self._printable_tokens


def print_Greek_token(token: str, pos: str, previous: Optional[str], scripta_continua: bool=False) -> str:
    # https://www.billmounce.com/greekalphabet/greek-punctuation-syllabification
    # https://blog.greek-language.com/2022/02/14/punctuation-in-ancient-greek-texts-part-i/
    # https://www.opoudjis.net/unicode/punctuation.html
    # https://en.wikipedia.org/wiki/Ancient_Greek_grammar#Alphabet
    retval: str
    if pos == "PUNCT":  # token in "·,;."
        # https://library.biblicalarchaeology.org/article/punctuationinthenewtestament/
        # https://en.wikipedia.org/wiki/Scriptio_continua
        if scripta_continua:
            retval = ""
        else:
            retval = token
    else:
        if previous is None or previous == "\n" or scripta_continua:
            retval = token
        else:
            retval = f" {token}"

    return retval


# Goes through the list of tokens, and based on their context in the passage, 
# modifies each token if necessary so it can be directly printed out.
def get_printable_tokens(tokens: List[str], pos: List[str]) -> List[str]:
    """
    """
    printable_text_list: List[str] = []
    prev_token: Optional[str] = None
    for idx in range(len(tokens)):
        ps=pos[idx]
        token=tokens[idx]
        printable = print_Greek_token(token, ps, prev_token)
        printable_text_list.append(printable)
        prev_token=token
    return printable_text_list
