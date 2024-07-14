from cltk import NLP
import difflib


class Greek:
    def __init__(self):
        self.NLP = NLP(language="grc", suppress_banner=True)


def get_sequence(doc):
    return [i for i, pos in enumerate(doc.pos) if pos != "PUNCT"]


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
        sequence_a_matches_b[match.a: match.a + match.size] = [True] * match.size
        sequence_b_matches_a[match.b: match.b + match.size] = [True] * match.size
        prev = match
    return (
        agreement,
        [pos for i, pos in enumerate(sequence_a) if sequence_a_matches_b[i]],
        [pos for i, pos in enumerate(sequence_b) if sequence_b_matches_a[i]],
    )


def match_lemmata(left_text, right_text):
    cltk_nlp = NLP(language="grc", suppress_banner=True)

    longest_sequence = 0

    left_count = 0
    left_doc = cltk_nlp.analyze(text=left_text)
    left_lemmata = left_doc.lemmata
    left_POS = left_doc.pos
    left_tokens = left_doc.tokens

    longest_string = 0

    right_count = 0
    right_doc = cltk_nlp.analyze(text=right_text)
    right_lemmata = right_doc.lemmata
    right_POS = right_doc.pos
    right_tokens = right_doc.tokens

    left_result = ""
    right_result = ""
    prev = difflib.Match(0, 0, 0)
    matcher = difflib.SequenceMatcher(a=left_lemmata, b=right_lemmata)
    for match in matcher.get_matching_blocks():
        contiguous = 0
        (increment, new_text) = loop_match(
            left_POS, left_tokens, prev.a + prev.size, match.a
        )
        left_count += increment
        left_result += new_text
        (increment, new_text) = loop_match(
            right_POS, right_tokens, prev.b + prev.size, match.b
        )
        right_count += increment
        right_result += new_text
        if match.size == 0:
            break
        left_result += "[yellow]"
        (increment, new_text) = loop_match(
            left_POS, left_tokens, match.a, match.a + match.size
        )
        left_count += increment
        left_result += new_text
        left_result += "[/yellow]"
        right_result += "[yellow]"
        (increment, new_text) = loop_match(
            right_POS, right_tokens, match.b, match.b + match.size
        )
        right_count += increment
        right_result += new_text
        right_result += "[/yellow]"
        contiguous += increment
        longest_sequence += increment
        if contiguous > longest_string:
            longest_string = contiguous
        prev = match
    return (
        longest_sequence,
        longest_string,
        left_count,
        left_result,
        right_count,
        right_result,
    )


def loop_match(POS, tokens, range_start, range_stop):
    count = 0
    result = ""
    for i in range(range_start, range_stop):
        (increment, new_text) = process_token(POS[i], tokens[i], i)
        count += increment
        result += new_text
    return count, result


def process_token(part_of_speech, token, sentence_word):
    if part_of_speech == "PUNCT" or token == "\n":
        increment = 0
        new_text = token
    else:
        increment = 1
        if sentence_word == 0:
            new_text = token
        else:
            new_text = " " + token
    return increment, new_text
