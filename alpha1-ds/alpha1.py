#!/usr/bin/env python3

#Alma Mater

import urllib.request
import sys
import bs4
import itertools
from collections import Counter
import json
import time

faculty = [] #List to store name of the faculty
degree = [] #List to store name of the degree
school = [] #List to store name of the school

def get_so_page(url):
    try:
        connection = urllib.request.urlopen(url)
    except urllib.request.HTTPError:
        return {}
    except:
        print("Error")
        sys.exit()
    soup = bs4.BeautifulSoup(connection, "lxml")
    fs = soup.findAll('div', class_='question-summary')
    return {f['id']: 
            [tag.string for tag in f.findAll(class_='post-tag')] 
     for f in fs}
    
BASE = "https://www.umb.edu/academics/cla/faculty"
TAGS = "University of Massachusetts", "PhD", "Faculty"

n = 1

faculty = {}

while True:
    URL = f'{BASE}/{"+".join(TAGS)}?tab=newest&pagesize=50&page={n}'
    doq = get_so_page(URL)
    if not doq:
        break
    print(f"Page {n}")
    faculty.update(doq)
    n += 1
    time.sleep(1) # Give it a break!

counts = Counter(itertools.chain.from_iterable(faculty.values()))
with open(f'{"+".join(TAGS)}.json', "w") as jfile:
    json.dump(counts.most_common(22)[2:], jfile)

df = pd.DataFrame({'Faculty':faculty,'PhD':degree,'University':school}) 
df.to_csv('faculty.csv', index=False, encoding='utf-8')