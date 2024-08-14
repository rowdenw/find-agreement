from typing import List, NamedTuple

from agreement.agreement import calculate_agreement_types
from agreement.greek_text import GreekText
import json

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
    def __init__(self, table_title: str, column_headings: List[str], word_counts: List[int], token_agreements: List[List[TokenAgreementTuple]]):
        self._table_title: str = table_title
        self._column_headings: List[str] = column_headings
        self._word_counts: List[int] = word_counts
        self._token_agreements: List[List[TokenAgreementTuple]] = token_agreements

    def to_json(self):
        # Convert the data to a dictionary, explicitly handling TokenAgreementTuple
        data = {
            'table_title': self._table_title,
            'column_headings': self._column_headings,
            'word_counts': self._word_counts,
            'token_agreements': [
                [list(agreement) for agreement in column]
                for column in self._token_agreements
            ]
        }
        return json.dumps(data, ensure_ascii=False, indent=4)

    @classmethod
    def from_json(cls, json_str):
        # Load JSON data and convert lists back into TokenAgreementTuple
        data = json.loads(json_str)
        token_agreements = [
            [TokenAgreementTuple(*token) for token in row]
            for row in data['token_agreements']
        ]
        return cls(
            data['table_title'],
            data['column_headings'],
            data['word_counts'],
            token_agreements
        )

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

    @classmethod
    def build_synoptic_table(cls, table_title: str, parallels: List[ParallelTuple]) -> "SynopticTableModel":
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

        return cls(
            table_title,
            column_headings,
            word_counts,
            token_agreements
        )
