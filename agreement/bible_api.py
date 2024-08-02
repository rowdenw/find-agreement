from urllib import parse
import json
import pandas as pd
import urllib.request


def percent_encode(link):
    scheme, netloc, path, query, fragment = parse.urlsplit(link)
    path = parse.quote(path)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))


def get_verse(version, book, chapter, verse):
    endpoint = (
        "https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles"
        f"/{version}"
        f"/books/{book}"
        f"/chapters/{chapter}"
        f"/verses/{verse}.json"
    )

    with urllib.request.urlopen(percent_encode(endpoint)) as url:
        data = json.load(url)
    return data["text"]


def get_chapter(version, book, chapter, start_verse, end_verse):
    endpoint = (
        "https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles"
        f"/{version}"
        f"/books/{book}"
        f"/chapters/{chapter}.json"
    )

    with urllib.request.urlopen(percent_encode(endpoint)) as url:
        data = json.load(url)
    df = pd.json_normalize(data["data"])
    text = df["text"]
    return "\n".join(text[start_verse - 1: end_verse])


def get_bibles():
    endpoint = "\
https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/bibles.json\
"
    with urllib.request.urlopen(percent_encode(endpoint)) as url:
        df = pd.read_json(url)
    return df
