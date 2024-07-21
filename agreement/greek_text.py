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
        self._lemmata = self.doc.lemmata
        # TODO: Remove if not needed by rewritten synopsis. Otherwise document.
        self.pos = self.doc.pos
        # TODO: Remove if not needed by rewritten synopsis. Otherwise document.
        self.tokens = self.doc.tokens

    @property
    def clean(self):
        """
        List of indices (no text) of Greek words without newlines or
        punctuation
        """
        return self._clean

    @property
    def lemmata(self):
        """
        List of canonical forms of each token in text
        """
        return self._lemmata
