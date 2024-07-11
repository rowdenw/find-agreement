from cltk import NLP
import difflib


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
        if prev.a + prev.size != match.a:
            for i in range(prev.a + prev.size, match.a):
                (increment, new_text) = process_token(
                    left_POS[i], left_tokens[i], i)
                left_count += increment
                left_result += new_text
        if prev.b + prev.size != match.b:
            for i in range(prev.b + prev.size, match.b):
                (increment, new_text) = process_token(
                    right_POS[i], right_tokens[i], i)
                right_count += increment
                right_result += new_text
        if (
            match.a < len(left_lemmata)
            or match.b < len(right_lemmata)
            or match.size > 0
        ):
            left_result += "[yellow]"
            for i in range(match.a, match.a + match.size):
                (increment, new_text) = process_token(
                    left_POS[i], left_tokens[i], i)
                left_count += increment
                left_result += new_text
            left_result += "[/yellow]"
            right_result += "[yellow]"
            for i in range(match.b, match.b + match.size):
                (increment, new_text) = process_token(
                    right_POS[i], right_tokens[i], i)
                contiguous += increment
                longest_sequence += increment
                right_count += increment
                right_result += new_text
            right_result += "[/yellow]"
            if contiguous > longest_string:
                longest_string = contiguous
            prev = match
    return (longest_sequence, longest_string, left_count, left_result,
            right_count, right_result)


def process_token(part_of_speech, token, position):
    increment = 0
    if part_of_speech == "PUNCT" or token == "\n":
        new_text = token
    else:
        increment = 1
        if position == 0:
            new_text = token
        else:
            new_text = " " + token
    return increment, new_text
