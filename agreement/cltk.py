from cltk import NLP
import difflib


class Greek:
    def __init__(self):
        self.NLP = NLP(language="grc", suppress_banner=True)


def get_n_gram_Jaccard_index(lemmata_a, lemmata_b, n):
    n_grams_a = []
    for i in range(len(lemmata_a) - (n - 1)):
        n_gram = [lemmata_a[i]]
        for j in range(1, n):
            n_gram.append(lemmata_a[i + j])
        n_grams_a.append(n_gram)

    intersection = 0

    n_grams_b = []
    for i in range(len(lemmata_b) - (n - 1)):
        n_gram = [lemmata_b[i]]
        for j in range(1, n):
            n_gram.append(lemmata_b[i + j])
        n_grams_b.append(n_gram)
        if n_gram in n_grams_a:
            intersection += 1

    # Jaccard index = intersection / union
    J = intersection / (len(n_grams_a) + len(n_grams_b) - intersection)
    return J


def get_sequence(doc):
    return [
        i for i, pos in enumerate(doc.pos)
        if pos != "PUNCT" and doc.tokens[i] != "\n"
    ]


def match_sequences(doc_a, sequence_a, doc_b, sequence_b):
    agreement = {}
    lemmata_a = [doc_a.lemmata[i] for i in sequence_a]
    lemmata_b = [doc_b.lemmata[i] for i in sequence_b]
    sequence_a_matches_b = []
    sequence_b_matches_a = []
    prev = difflib.Match(0, 0, 0)
    matcher = difflib.SequenceMatcher(a=lemmata_a, b=lemmata_b)
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
        [pos for i, pos in enumerate(sequence_a) if sequence_a_matches_b[i]],
        [pos for i, pos in enumerate(sequence_b) if sequence_b_matches_a[i]],
    )
