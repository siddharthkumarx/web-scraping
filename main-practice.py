'''
1&2:    ##no of times:[1]

import requests

response = requests.get("https://quotes.toscrape.com")

print(response.status_code)
print(response.text[:300])
'''




'''
--------------------

3: ##no of times:[1]

import requests
from bs4 import BeautifulSoup

response = requests.get("https://quotes.toscrape.com")
soup = BeautifulSoup(response.text, "html.parser")

first_quote = soup.select_one("span.text")
print(first_quote.text)
'''




'''
-------------------
4:  ##no of times:[1]

import requests
from bs4 import BeautifulSoup

response = requests.get("https://quotes.toscrape.com")
soup = BeautifulSoup(response.text, "html.parser")

quotes = soup.select("span.text")

for quote in quotes:
    print(quote.text)
'''







'''    
------------------------
5:  ##no of times:[1]
import requests
from bs4 import BeautifulSoup

response = requests.get("https://quotes.toscrape.com")
soup = BeautifulSoup(response.text, "html.parser")

blocks = soup.select("div.quote")  #whole block code

for block in blocks:
	quote = block.select_one("span.text").text
	author = block.select_one("small.author").text
	link =block.select_one("a")["href"]     # we get link so we use [href], if we use .text, then comes (about) title 
	print(quote, "-", author, "->", link)

#for link getting of author
above attach
link = block.select_one("a)["href"]
'''








'''
6:  ##no of times:[3]
import csv
import requests
from bs4 import BeautifulSoup

response = requests.get("https://quotes.toscrape.com")
soup = BeautifulSoup(response.text, "html.parser")

rows = []

for block in soup.select("div.quote"):                          # you also use blocks = soup.select("div.quote")
    quote = block.select_one("span.text").text
    author = block.select_one("small.author").text
    tags = ", ".join(t.text for t in block.select("div.tags a.tag"))       #use tree mode : tree->branches->leaves
    rows.append([quote, author, tags])

import os   
os.makedirs("data", exist_ok=True)

with open("data/quotes.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["quote", "author", "tags"])           #FOR HEADING ON CSV
    writer.writerows(rows)                                 #FOR 1 ROW ADD USE WRITER.WRITEROW(anything), seperate rows by ","
                                                           # for many rows use writer.rows(anything)

print("Saved", len(rows), "quotes")
'''



'''
-------------------
7):            ##no of times:[3]
import csv
import os
import time
import requests
from bs4 import BeautifulSoup

BASE = "https://quotes.toscrape.com"

os.makedirs("data", exist_ok=True)

url = BASE
rows = []

while url:
    print("Scraping", url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for block in soup.select("div.quote"):
        quote = block.select_one("span.text").text
        author = block.select_one("small.author").text
        tags = ", ".join(t.text for t in block.select("div.tags a.tag"))
        rows.append([quote, author, tags])

    next_link = soup.select_one("li.next a")

    if next_link:
        url = BASE + next_link["href"]
    else:
        url = None

    time.sleep(1)

with open("data/quotes.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["quote", "author", "tags"])
    writer.writerows(rows)

print("Saved", len(rows), "quotes")
'''

'''
-------------DROP ALL EXERCISE: IT HARDER NOT MUCH USEFUL---------------
#EXERCISE A:    ##no of times:[3]
import csv                                                 

rows = [["hello", "world"], ["apple", "banana"]]

with open("test.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("done")
----------
writer.writerow(["col1", "col2"]) #Add a header row on top using
'''





'''
#EXERCISE B:    ##no of times:[3]
import requests
from bs4 import BeautifulSoup

response = requests.get("https://quotes.toscrape.com")
soup = BeautifulSoup(response.text, "html.parser")

for block in soup.select("div.quote"):
    quote = block.select_one("span.text").text
    author = block.select_one("small.author").text
    print(quote, "—", author)
'''







'''
#EXERCISE C: FINAL PROGRAM 6 :##no of times:[]
import csv
import os
import requests
from bs4 import BeautifulSoup

os.makedirs("data", exist_ok=True)

response = requests.get("https://quotes.toscrape.com")
soup = BeautifulSoup(response.text, "html.parser")

rows = []

for block in soup.select("div.quote"):
    quote = block.select_one("span.text").text
    author = block.select_one("small.author").text

    tag_list = []
    for t in block.select("div.tags a.tag"):
        tag_list.append(t.text)

    tags = ", ".join(tag_list)
    rows.append([quote, author, tags])

with open("data/quotes.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["quote", "author", "tags"])
    writer.writerows(rows)

print("Saved", len(rows), "quotes")
'''


























