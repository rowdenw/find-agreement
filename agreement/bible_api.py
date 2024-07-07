import json
from urllib import parse
import urllib.request


def percent_encode(link):
    scheme, netloc, path, query, fragment = parse.urlsplit(link)
    path = parse.quote(path)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))


def get_verse(version, book, chapter, verse):
    endpoint = "https://cdn.jsdelivr.net/gh/wldeh/bible-api/bibles/${version}/books/${book}/chapters/${chapter}/verses/${verse}.json"
    endpoint = endpoint.replace("${version}", version)
    endpoint = endpoint.replace("${book}", book)
    endpoint = endpoint.replace("${chapter}", str(chapter))
    endpoint = endpoint.replace("${verse}", str(verse))
    with urllib.request.urlopen(percent_encode(endpoint)) as url:
        data = json.load(url)
    return data["text"]
