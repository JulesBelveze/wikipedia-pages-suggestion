import requests
import re
from collections import Counter


# function that outputs all the Wikipedia links in a given page
# if countable is True returns a list and the occurence of each link
def wikiPagesFinder(url, countable=False):
    response = requests.get(url)
    wikilinks = re.findall(r'\[\[(.*?)[\]\]|\]\]]', response.text)
    return Counter(wikilinks) if countable is True else list(set(wikilinks))


def urlWikiPagesConstructor(page_name):
    baseurl = "http://en.wikipedia.org/w/api.php/?"
    action = "action=query"
    content = "prop=revisions"
    rvprop = "rvprop=timestamp|content"
    dataformat = "format=json"
    limit = "rvlimit=1"  # consider only the first revision
    title = "titles=" + page_name
    query = "%s%s&%s&%s&%s&%s&%s" % (baseurl, action, title, content, rvprop, dataformat, limit)
    return query

print(wikiPagesFinder("http://en.wikipedia.org/w/api.php/?action=query&titles=John_Lennon&prop=revisions&rvprop=timestamp|content&format=json&rvlimit=1"))