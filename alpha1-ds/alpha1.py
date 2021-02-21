#!/usr/bin/env python3

#Alma Mater by Edward Birch and Julia Volpe
#Overall, we struggled with this project. We understand what the project is asking
#us to do, but we are having a hard time excecuting it. 

import urllib.request
import sys
import bs4
import itertools
from collections import Counter
import json
import time
import pandas as pd

faculty = [] #List to store name of the faculty
degree = [] #List to store name of the degree
school = [] #List to store name of the school

def get_UMB_page(url):
    try:
        connection = urllib.request.urlopen(BASE1.join(BASE2))
        #We seperated the BASE into 2 parts, so that we could put the department 
        #name in between to make the URL
    except urllib.request.HTTPError:
        return {}
    except:
        print("Error!")
        sys.exit()
    soup = bs4.BeautifulSoup(connection, "lxml")
    depName = list(soup.a.stripped_strings)[0].lower() 
    #depName finds the department name and uses the first word so that we can
    #join it to make the URL. When you click on each department, the one
    #part of the URL that changes is the department name that goes 
    #https://www.umb.edu/academics/cla/HERE/faculty where the HERE is.
    #For most of the specific department links (but not all), the word that
    #goes in HERE is the first word of the link. Our method does not work for 
    #all the links but for the links that do not apply to this rule and were
    #not consistent, we didn't know what else to do.
    print(depName)
    fs = soup.findAll('div', class_='unit') 
    #when we were looking at the View Page Source for the first page, we were
    #trying to locate what included all the faculty links, and this was the 
    #div class that we believe includes everything, but we are not exactly sure.
    #The classes on the page would have the word "unit" followed by a dash and a number.
    #Ex "unit-30", "unit-70", "unit-50", and "unit-100", similar to how in stack overflow 
    #View Page Source how it would say "question-summary" followed by the specific ID number.
    return {f['id']: 
            [tag.string for tag in f.findAll(class_='content')] 
            #the id that paired with the class='unit' was titled 'content' so we used that
     for f in fs}


BASE1 = "https://www.umb.edu/academics/cla" 
BASE2 = "/faculty"
TAGS = "University of Massachusetts Boston, UMass, UMB, Beacons, U-Mass, Boston State College"
#We found these tags by looking in the View Source Page and found them under Meta Keywords.
#Unlike with the stack overflow example, we didn't include specific tags like "python" or "go",
#so we don't think we can use these TAGS in anyway...

n = 1

faculty = {}

while True:
    URLp1 = f'{BASE1}{"/".join(depName)}'
    #we defined depName when we defined get_UMB_page(url), but we don't know how to make it so 
    #that is defined here. We already returned the id for the get_UMB_page(url) so we can't 
    #return depName :( don't know what to do
    fullURL = f'{URLp1}{"/".join(BASE2)}'
    #We seperated the URL into two parts to join BASE1 and BASE2 so we can have the department
    #name in the middle of the URL
    dof = get_UMB_page(fullURL)
    if not dof:
        break
    print(f"Page {n}")
    faculty.update(dof)
    n += 1
    time.sleep(1) # Give it a break!

counts = Counter(itertools.chain.from_iterable(faculty.values()))
with open(f'{"+".join(TAGS)}.json', "w") as jfile:
    json.dump(counts.most_common(22)[2:], jfile)

df = pd.DataFrame({'Faculty':faculty,'PhD':degree,'University':school}) 
df.to_csv('faculty.csv', index=False, encoding='utf-8')