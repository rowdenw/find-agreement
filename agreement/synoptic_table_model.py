from collections import namedtuple
from typing import List, Tuple, NamedTuple, Optional

from agreement.agreement import calculate_agreement_types
from agreement.greek_text import GreekText

class ParallelTuple(NamedTuple):
    title: str # Title of a column in an agreement table
    text: str # Body text for one column in agreement table

class PreparedTokenTuple(NamedTuple):
    token: str # greek word
    agreement_type: int # numeric code for agreement type, which is translated to color

class TokenAgreementTuple(NamedTuple):
    pos: str # part of speech
    token: str # greek word
    agreement_type: int # numeric code for agreement type, which is translated to color

class SynopticTableModel:
    """
    A synopsis of passages and text.

    Attributes
    ----------
    """
    def __init__(self, title: str, parallels: List[ParallelTuple]):
        self.parallels: List[ParallelTuple] = parallels
        self._table_title = title
        self._column_headings: List[str] = [passage.title for passage in self.parallels]
        self._prepared_texts: List[List[PreparedTokenTuple]]
        self._word_counts: List[int]

    def process_synopsis(self):
        processed_greek_texts: List[GreekText] = [GreekText(passage.text) for passage in self.parallels]
        passage_agreement_types: List[List[int]] = calculate_agreement_types(processed_greek_texts)

        token_agreements: List[List[TokenAgreementTuple]] = []
        for index in range(len(passage_agreement_types)):
            ta_tuples = zip(
                processed_greek_texts[index].pos, # part of speech
                processed_greek_texts[index].tokens, # greek word
                passage_agreement_types[index] # numeric code for agreement type, which is translated to color
            )
            token_agreements.append([TokenAgreementTuple(*z) for z in ta_tuples])

        self._prepared_texts: List[List[PreparedTokenTuple]] = [
            self.prepare_tokens(ta) for ta in token_agreements
        ]

        self._word_counts: List[int] = [len(gt.clean) for gt in processed_greek_texts]

    @property
    def table_title(self) -> str:
        return self._table_title

    @property
    def column_headings(self) -> List[str]:
        return self._column_headings

    @property
    def prepared_texts(self) -> List[List[PreparedTokenTuple]]:
        return self._prepared_texts

    @property
    def word_counts(self) -> List[int]:
        return self._word_counts

    def prepare_tokens(self, token_agreement: List[TokenAgreementTuple]) -> List[PreparedTokenTuple]:
        prev: Optional[str] = None
        # text = rich.text.Text()
        prepared_tokens: List[PreparedTokenTuple] = []
        for pos, token, agreement_type in token_agreement:
            to_print = print_Greek_token(token, pos, prev)
            prepared_tokens.append(PreparedTokenTuple(to_print, agreement_type))
            prev = token
        return prepared_tokens

def print_Greek_token(token: str, pos: str, previous: Optional[str], scripta_continua: bool = False) -> str:
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


