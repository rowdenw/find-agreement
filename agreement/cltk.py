from cltk import NLP
import difflib


def match_lemmata(left_text, right_text):
    cltk_nlp = NLP(language="grc", suppress_banner=True)

    left_doc = cltk_nlp.analyze(text=left_text)
    left_lemmata = left_doc.lemmata
    left_POS = left_doc.pos
    left_tokens = left_doc.tokens

    right_doc = cltk_nlp.analyze(text=right_text)
    right_lemmata = right_doc.lemmata
    right_POS = right_doc.pos
    right_tokens = right_doc.tokens

    left_result = ""
    right_result = ""
    prev = difflib.Match(0, 0, 0)
    matcher = difflib.SequenceMatcher(a=left_lemmata, b=right_lemmata)
    for match in matcher.get_matching_blocks():
        if prev.a + prev.size != match.a:
            for i in range(prev.a + prev.size, match.a):
                if left_POS[i] == "PUNCT" or match.a == 0:
                    left_result += left_tokens[i]
                else:
                    left_result += " " + left_tokens[i]
        if prev.b + prev.size != match.b:
            for i in range(prev.b + prev.size, match.b):
                if right_POS[i] == "PUNCT" or match.b == 0:
                    right_result += right_tokens[i]
                else:
                    right_result += " " + right_tokens[i]
        if (
            match.a < len(left_lemmata)
            or match.b < len(right_lemmata)
            or match.size > 0
        ):
            left_result += "[yellow]"
            for i in range(match.a, match.a + match.size):
                if left_POS[i] == "PUNCT":
                    left_result += left_tokens[i]
                else:
                    left_result += " " + left_tokens[i]
            left_result += "[/yellow]"
            right_result += "[yellow]"
            for i in range(match.b, match.b + match.size):
                if right_POS[i] == "PUNCT":
                    right_result += right_tokens[i]
                else:
                    right_result += " " + right_tokens[i]
            right_result += "[/yellow]"
            prev = match
    return left_result, right_result
