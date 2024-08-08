from collections import namedtuple
from typing import List, Tuple, NamedTuple, Optional

from agreement.agreement import calculate_agreement_types
from agreement.greek_text import GreekText

class ParallelTuple(NamedTuple):
    title: str # Title of a column in an agreement table
    text: str # Body text for one column in agreement table

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
        self._prepared_texts: List[List[TokenAgreementTuple]]
        self._word_counts: List[int]

    def process_synopsis(self):
        processed_greek_texts: List[GreekText] = [GreekText(passage.text) for passage in self.parallels]
        passage_agreement_types: List[List[int]] = calculate_agreement_types(processed_greek_texts)

        self._token_agreements: List[List[TokenAgreementTuple]] = []
        for index in range(len(passage_agreement_types)):
            ta_tuples = zip(
                processed_greek_texts[index].pos, # part of speech
                processed_greek_texts[index].tokens, # greek word
                passage_agreement_types[index] # numeric code for agreement type, which is translated to color
            )
            self._token_agreements.append([TokenAgreementTuple(*z) for z in ta_tuples])

        self._word_counts: List[int] = [len(gt.clean) for gt in processed_greek_texts]

    @property
    def table_title(self) -> str:
        return self._table_title

    @property
    def column_headings(self) -> List[str]:
        return self._column_headings

    @property
    def token_agreements(self) -> List[List[TokenAgreementTuple]]:
        return self._token_agreements

    @property
    def word_counts(self) -> List[int]:
        return self._word_counts

