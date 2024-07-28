import difflib

from agreement.find_agreement import AgreementFinder


class LCSAgreementFinder(AgreementFinder):
    def __init__(self):
        super().__init__()

    def agreement(self, lemmata_a, sequence_a, lemmata_b, sequence_b):
        agreement = {}
        match_a = [lemmata_a[i] for i in sequence_a]
        match_b = [lemmata_b[i] for i in sequence_b]
        sequence_a_matches_b = []
        sequence_b_matches_a = []
        prev = difflib.Match(0, 0, 0)
        matcher = difflib.SequenceMatcher(a=match_a, b=match_b)
        for match in matcher.get_matching_blocks():
            agreement[match.size] = agreement.get(match.size, 0) + 1
            if prev.a + prev.size != match.a:
                sequence_a_matches_b[prev.a + prev.size: match.a] = [False] * (
                    match.a - prev.size - prev.a
                )
            if prev.b + prev.size != match.b:
                sequence_b_matches_a[prev.b + prev.size: match.b] = [False] * (
                    match.b - prev.size - prev.b
                )
            sequence_a_matches_b[match.a:
                                 match.a + match.size] = [True] * match.size
            sequence_b_matches_a[match.b:
                                 match.b + match.size] = [True] * match.size
            prev = match
        return (
            agreement,
            [
                position
                for i, position in enumerate(sequence_a)
                if sequence_a_matches_b[i]
            ],
            [
                position
                for i, position in enumerate(sequence_b)
                if sequence_b_matches_a[i]
            ],
        )


def calculate_agreement(passages):
    agreements = []
    matches = [[[] for i in range(len(passages))]
               for j in range(len(passages))]
    agreementFinder = LCSAgreementFinder()

    for left in range(len(passages)):
        for right in range(left + 1, len(passages)):
            (agreement,
             matches[left][right],
             matches[right][left]) = agreementFinder.agreement(passages[left].lemmata,
                                                               passages[left].clean,
                                                               passages[right].lemmata,
                                                               passages[right].clean,
                                                               )
            agreements.append(agreement)
    return agreements, matches


def calculate_agreement_types(texts):
    agreements, matches = calculate_agreement(texts)
    agreement_types = []
    for column in range(len(texts)):
        agreement_types.append(
            [
                2**column if j in texts[column].clean else 0
                for j in range(len(texts[column].tokens))
            ]
        )
    for left in range(len(agreement_types)):
        for right in range(left + 1, len(agreement_types)):
            agreement_types[left] = [
                agreement_types[left][position] + 2**right
                if position in matches[left][right]
                else agreement_types[left][position]
                for position in range(len(agreement_types[left]))
            ]
            agreement_types[right] = [
                agreement_types[right][position] + 2**left
                if position in matches[right][left]
                else agreement_types[right][position]
                for position in range(len(agreement_types[right]))
            ]
    return agreement_types
