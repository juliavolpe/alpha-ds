#!/usr/bin/env python3

import urllib.request
import sys
import bs4
import itertools
from collections import Counter
import json
import time

def get_so_page(url):
    try:
        connection = urllib.request.urlopen(url)
    except urllib.request.HTTPError:
        return {}
    except:
        print("Error")
        sys.exit()
    soup = bs4.BeautifulSoup(connection, "lxml")
    qs = soup.findAll('div', class_='question-summary')
    return {q['id']: 
            [tag.string for tag in q.findAll(class_='post-tag')] 
     for q in qs}
    
BASE = "https://stackoverflow.com/questions/tagged"
TAGS = "go", "python"

n = 1

questions = {}

while True:
    URL = f'{BASE}/{"+".join(TAGS)}?tab=newest&pagesize=50&page={n}'
    doq = get_so_page(URL)
    if not doq:
        break
    print(f"Page {n}")
    questions.update(doq)
    n += 1
    time.sleep(1) # Give it a break!

counts = Counter(itertools.chain.from_iterable(questions.values()))
with open(f'{"+".join(TAGS)}.json', "w") as jfile:
    json.dump(counts.most_common(22)[2:], jfile)