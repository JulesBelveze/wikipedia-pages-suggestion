import requests
import re
from collections import Counter


# function that outputs all the Wikipedia links in a given page
# if countable is True returns a list and the occurence of each link
def wikiPagesFinder(url, countable=False):
    response = requests.get(url)
    wikilinks = re.findall(r'\[\[(.*?)[\]\]|\]\]]', response.text)

    return Counter(wikilinks) if countable is True else list(set(wikilinks))
