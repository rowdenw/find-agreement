from abc import ABC, abstractmethod


class AgreementFinder(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def agreement(self, lemmata_a, sequence_a, lemmata_b, sequence_b):
        raise NotImplementedError(
            "Agreement Finders must implement \
agreement."
        )


class CommonAgreementFinder(AgreementFinder):
    def __init__(self):
        super().__init__()


class NGramAgreementFinder(AgreementFinder):
    def __init__(self, n=3):
        super().__init__()
        self.n = n

    def agreement(self, lemmata_a, sequence_a, lemmata_b, sequence_b):
        match_a = [lemmata_a[i] for i in sequence_a]
        match_b = [lemmata_b[i] for i in sequence_b]
        n_grams_a = [tuple(match_a[i: i + self.n])
                     for i in range(len(match_a) - self.n + 1)]
        n_grams_b = [tuple(match_b[i: i + self.n])
                     for i in range(len(match_b) - self.n + 1)]
        intersection = len(set(n_grams_a).intersection(n_grams_b))
        union = (len(n_grams_a) + len(n_grams_b)) - intersection
        score = intersection / union if union != 0 else 0.0
        sequence_a_matches_b = [
            i for i in range(len(match_a))
            if tuple(match_a[i: i + self.n]) in n_grams_b
        ]
        sequence_b_matches_a = [
            i for i in range(len(match_b))
            if tuple(match_b[i: i + self.n]) in n_grams_a
        ]
        return (
            score,
            [
                position
                for i, position in enumerate(sequence_a)
                if i in sequence_a_matches_b
            ],
            [
                position
                for i, position in enumerate(sequence_b)
                if i in sequence_b_matches_a
            ],
        )
