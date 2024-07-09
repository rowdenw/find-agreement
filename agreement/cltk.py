from cltk import NLP
import difflib


def match_lemmata(left_text, right_text):
    cltk_nlp = NLP(language="grc", suppress_banner=True)

    common_count = 0

    left_count = 0
    left_doc = cltk_nlp.analyze(text=left_text)
    left_lemmata = left_doc.lemmata
    left_POS = left_doc.pos
    left_tokens = left_doc.tokens

    longest = 0

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
                (increment, left_result) = process_token(
                    left_POS[i], left_tokens[i], left_result, i)
                left_count += increment
        if prev.b + prev.size != match.b:
            for i in range(prev.b + prev.size, match.b):
                (increment, right_result) = process_token(
                    right_POS[i], right_tokens[i], right_result, i)
                right_count += increment
        if (
            match.a < len(left_lemmata)
            or match.b < len(right_lemmata)
            or match.size > 0
        ):
            left_result += "[yellow]"
            for i in range(match.a, match.a + match.size):
                (increment, left_result) = process_token(
                    left_POS[i], left_tokens[i], left_result, i)
                common_count += increment
                contiguous += increment
                left_count += increment
            left_result += "[/yellow]"
            right_result += "[yellow]"
            for i in range(match.b, match.b + match.size):
                (increment, right_result) = process_token(
                    right_POS[i], right_tokens[i], right_result, i)
                right_count += increment
            right_result += "[/yellow]"
            if contiguous > longest:
                longest = contiguous
            prev = match
    return (common_count, longest, left_count, left_result,
            right_count, right_result)


def process_token(part_of_speech, token, text, position):
    increment = 0
    if part_of_speech == "PUNCT":
        text += token
    else:
        increment = 1
        if position == 0:
            text += token
        else:
            text += " " + token
    return increment, text
