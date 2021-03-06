import requests
import re
from collections import Counter


def wikiPagesFinder(url, countable=False):
    """function that outputs all the Wikipedia links in a given page
    if countable is True returns a list and the occurence of each link"""
    response = requests.get(url)
    wikilinks = re.findall(r'\[\[(.*?)[\]\]|\]\]]', response.text)
    #    wikilinks = [link.replace(' ', "_") for link in wikilinks]
    wikilinks = [urlWikiPagesConstructor(link) for link in wikilinks]
    return Counter(wikilinks) if countable is True else list(set(wikilinks))


def urlWikiPagesConstructor(page_name):
    """function constructing the URL to request the Wikipedia API given a page title"""
    baseurl = "http://en.wikipedia.org/w/api.php/?"
    action = "action=query"
    content = "prop=revisions"
    rvprop = "rvprop=timestamp|content"
    dataformat = "format=json"
    limit = "rvlimit=1"  # consider only the first revision
    title = "titles=" + page_name
    query = "%s%s&%s&%s&%s&%s&%s" % (baseurl, action, title, content, rvprop, dataformat, limit)
    return query