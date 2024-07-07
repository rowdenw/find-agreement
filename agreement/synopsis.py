from cltk import NLP

from rich.table import Table
import difflib
import pandas as pd


def highlight_matching_lemmata(left_text, right_text):
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
                if left_POS[i] == "PUNCT":
                    left_result += left_tokens[i]
                elif match.a == 0:
                    left_result += left_tokens[i]
                else:
                    left_result += " " + left_tokens[i]
        if prev.b + prev.size != match.b:
            for i in range(prev.b + prev.size, match.b):
                if right_POS[i] == "PUNCT":
                    right_result += right_tokens[i]
                elif match.b == 0:
                    right_result += right_tokens[i]
                else:
                    right_result += " " + right_tokens[i]
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


class Synopsis:
    def __init__(self, title, **kwargs):
        self.df = pd.DataFrame()
        self.table = Table()
        self.table.title = title
        if kwargs.get("left_passage"):
            self.table.add_column(kwargs["left_passage"])
        if kwargs.get("right_passage"):
            self.table.add_column(kwargs["right_passage"])
        # TODO: Write tests to produce empty string if passage provided but no text.
        if kwargs.get("left_text") and kwargs.get("right_text"):
            left_text = kwargs["left_text"]
            right_text = kwargs["right_text"]
            # TODO: This could produce an error if there is text but no passage. Write test to raise error.
            left_data, right_data = highlight_matching_lemmata(left_text, right_text)
            self.df[kwargs["left_passage"]] = [left_data]
            self.df[kwargs["right_passage"]] = [right_data]
            self.table.add_row(left_data, right_data)
        elif kwargs.get("left_text"):
            self.table.add_row(kwargs["left_text"])
        elif kwargs.get("right_text"):
            self.table.add_row(kwargs["right_text"])

    def getDataFrame(self):
        return self.df

    def makeTable(self):
        return self.table
