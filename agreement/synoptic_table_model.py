from typing import List, NamedTuple

from agreement.agreement import calculate_agreement_types
from agreement.greek_text import GreekText

class ParallelTuple(NamedTuple):
    title: str # Title of a column in an agreement table
    text: str # Body text for one column in agreement table

class TokenAgreementTuple(NamedTuple):
    pos: str # part of speech
    token: str # greek word
    agreement_type: int # numeric code for agreement type, which is translated to color
    printable_text: str # Greek token ready for display (but without color).

class SynopticTableModel:
    """
    A synopsis of passages and text.

    Attributes
    ----------
    """
    def __init__(self, table_title: str, column_headings: List[str], token_agreements: List[List[TokenAgreementTuple]], word_counts: List[int]):
        self._table_title: str = table_title
        self._column_headings: List[str] = column_headings
        self._token_agreements: List[List[TokenAgreementTuple]] = token_agreements
        self._word_counts: List[int] = word_counts

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


def build_synoptic_table(table_title: str, parallels: List[ParallelTuple]):
    column_headings: List[str] = [passage.title for passage in parallels]
    
    processed_greek_texts: List[GreekText] = [GreekText(passage.text) for passage in parallels]
    passage_agreement_types: List[List[int]] = calculate_agreement_types(processed_greek_texts)
    token_agreements: List[List[TokenAgreementTuple]] = [
        [
            TokenAgreementTuple(pos, token, agreement_type, printable_token)
            for pos, token, agreement_type, printable_token in zip(
                gt.pos,
                gt.tokens,
                passage_agreement_types[col_index],
                gt.printable_tokens
            )
        ]
        for col_index, gt in enumerate(processed_greek_texts)
    ]

    word_counts: List[int] = [len(gt.clean) for gt in processed_greek_texts]

    return SynopticTableModel(
        table_title,
        column_headings,
        token_agreements,
        word_counts
    )
