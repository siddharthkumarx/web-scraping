# Phase 1 — Static Web Scraping · Revision Notes

**Stack:** `requests` + `BeautifulSoup` + `csv`
**Practice sites:** quotes.toscrape.com, books.toscrape.com

---

## 1. The shape of every scraper

Every scraper you will ever write is these 5 steps.

| # | Step | Code |
|---|---|---|
| 1 | Fetch the page | `requests.get(url)` |
| 2 | Sort the mess | `BeautifulSoup(response.text, "html.parser")` |
| 3 | Find the containers | `soup.select("div.quote")` |
| 4 | Reach inside each one | `block.select_one("span.text").text` |
| 5 | Save | `csv.writer(f)` |

**Golden rule:** grab the container first, then look inside it.
Searching the whole page gives you pieces that don't belong together.

---

## 2. Programs

### P1 — Is the site alive?

```python
import requests

response = requests.get("https://quotes.toscrape.com")
print(response.status_code)
```

`200` OK · `403` blocked (you look like a bot) · `404` page missing

### P2 — See the raw HTML

```python
print(response.text[:300])
```

### P3 — One item

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, "html.parser")
print(soup.select_one("span.text").text)
```

### P4 — All items

```python
for quote in soup.select("span.text"):
    print(quote.text)
```

`select_one` → one thing · `select` → a list

### P5 — Container + several fields

```python
for block in soup.select("div.quote"):
    quote = block.select_one("span.text").text
    author = block.select_one("small.author").text
    print(quote, "—", author)
```

### P6 — Save to CSV

```python
import csv, os
import requests
from bs4 import BeautifulSoup

os.makedirs("data", exist_ok=True)

response = requests.get("https://quotes.toscrape.com")
soup = BeautifulSoup(response.text, "html.parser")

rows = []
for block in soup.select("div.quote"):
    quote = block.select_one("span.text").text
    author = block.select_one("small.author").text
    tags = ", ".join(t.text for t in block.select("div.tags a.tag"))
    rows.append([quote, author, tags])

with open("data/quotes.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["quote", "author", "tags"])
    writer.writerows(rows)

print("Saved", len(rows), "quotes")
```

**Shape matters:** `rows = []` outside the loop, file written after it.
Write inside the loop and each page erases the last.

### P7 — Pagination (100 quotes)

```python
import csv, os, time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

os.makedirs("data", exist_ok=True)

url = "https://quotes.toscrape.com"
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
    url = urljoin(url, next_link["href"]) if next_link else None

    time.sleep(1)

with open("data/quotes.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["quote", "author", "tags"])
    writer.writerows(rows)

print("Saved", len(rows), "quotes")
```

`while` not `for` — you don't know the page count. The site tells you as you go.
**No Next button = the signal to stop.** Not an error.

### P8 — Unseen site, full job (1000 books)

```python
import csv, os, time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

RATINGS = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

os.makedirs("data", exist_ok=True)

url = "https://books.toscrape.com/"
rows = []

while url:
    print("Scraping", url)
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")

    for block in soup.select("article.product_pod"):
        title = block.select_one("h3 a")["title"]
        price = block.select_one("p.price_color").text.strip()
        availability = block.select_one("p.instock.availability").text.strip()
        rating = RATINGS[block.select_one("p.star-rating")["class"][1]]
        rows.append([title, price, availability, rating])

    next_link = soup.select_one("li.next a")
    url = urljoin(url, next_link["href"]) if next_link else None

    time.sleep(1)

with open("data/books.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["TITLE", "PRICE", "AVAILABILITY", "RATING"])
    writer.writerows(rows)

print("Saved", len(rows), "books")
```

---

## 3. Selectors

**The dot always means class. Only class. Nothing else.**

| HTML | Selector |
|---|---|
| `class="quote"` on a div | `div.quote` |
| `class="instock availability"` (two classes) | `p.instock.availability` |
| `title="..."` — an attribute, NOT a class | cannot use a dot |
| link inside an h3 | `h3 a` (space = go inside) |

- No `class=` in the HTML → no dot in the selector.
- Space between two parts = "inside".
- `soup.select_one("a")` searches the **whole page**. `block.select_one("a")` searches **one container**.
- Be specific enough to be unambiguous — **not one step more**. Longer selectors break sooner.
- Put the **stable** part in the selector, read the **changing** part afterwards.

### Finding a selector on an unknown site — 4 steps

1. Right-click the exact thing → Inspect
2. Has a `class`? → use `tag.class`, done
3. No class? → look at the **parent**, keep going up until you find a class or a rare tag
4. Write the path down from there

Don't use Chrome's "Copy selector". Long, ugly, breaks on any redesign.

---

## 4. Text vs attribute

```html
<a href="/author/Albert-Einstein" title="A Light in the Attic">A Light in the ...</a>
```

| Want | Use | Returns |
|---|---|---|
| what you see on the page | `.text` | string |
| `href`, `title`, `src` | `["href"]` | string |
| `class` | `["class"]` | **LIST** |

- `["class"]` returns a list because HTML allows many classes on one tag. Take `[1]`, `[0]`, etc.
- `["href"]` goes **outside** the quotes: `select_one("li.next a")["href"]`
- **Not everything useful is text.** Truncated titles (`A Light in the ...`) are real characters in the page — the full title lives in the `title` attribute.
- The question is never *"which one is real"*. It is **"which one is usable by the client"**.

---

## 5. Traps

| Error / symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | never installed | `pip install` once, `import` every file |
| `MissingSchema` | no `https://` | browsers add it silently, Python never guesses |
| `unicodeescape` error in a path | `\U`, `\n`, `\1` are magic | use `/` or `r"..."` |
| `'NoneType' object is not subscriptable` | `select_one` found nothing | check `if thing:` before reaching inside |
| Excel shows `â€œ` or `Â£` | wrong alphabet assumed | `encoding="utf-8-sig"` · `response.encoding = "utf-8"` |
| Text full of `\n` and spaces | HTML indentation is real | `.strip()` (cleans ends only, not the middle) |
| Only last page saved | file written inside the loop | collect first, write once at the end |
| Old file gone | `"w"` overwrites | **no undo**, ever — use timestamps if data matters |
| Page 2 works, page 3 dies | relative link changed shape | `urljoin(url, href)` — never `BASE + href` |
| Some items silently missing | hardcoded a changing class (`p.star-rating.Three`) | selector = stable part only |

### Reading a traceback

1. **Bottom line first** — that's *what* went wrong
2. **Find your own filename** — that's *where*
3. **Ignore everything else** — library internals, not your code

---

## 6. URLs

- **Relative link** = directions from where you are standing, not a full address.
- `page-3.html` means "same folder as me" — which changes as you move.
- `BASE + href` only works if the link shape never changes. On books.toscrape.com it changes at page 2.
- **Always use `urljoin(current_url, href)`.** Same effort, never surprises you.

---

## 7. Copy-forever settings

Don't memorise these. Know why they exist.

| Setting | Why |
|---|---|
| `newline=""` | stops blank rows between lines on Windows |
| `encoding="utf-8-sig"` | Excel reads it correctly (use plain `utf-8` for code/databases) |
| `exist_ok=True` | "make sure folder exists" — safe to run 100 times |
| `time.sleep(1)` | polite; without it you look like an attack |
| `response.encoding = "utf-8"` | only when the site doesn't declare its alphabet |

**Idea vs setting:** ideas transfer to new problems — understand them deeply. Settings never change — copy them.

---

## 8. File modes

| Mode | Meaning | Effect |
|---|---|---|
| `"w"` | write | erases everything first — **whiteboard** |
| `"a"` | append | adds to the bottom — **notebook** |
| `"x"` | exclusive | refuses if the file exists — safety lock |
| `"r"` | read | looks only |

Overwritten data is **not** in the Recycle Bin. It is gone.
Data that matters → put the date in the filename:

```python
from datetime import datetime
stamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
filename = f"data/quotes_{stamp}.csv"
```

Year first so files sort correctly.

---

## 9. Confusions cleared

- **Git Bash is not a language.** It's a terminal brand, like PowerShell. Not needed.
- **`urllib` needs no install.** It ships with Python — like `csv`, `os`, `time`. Only `requests` and `beautifulsoup4` were extras.
- **Python saves where the terminal is standing**, not next to your `.py` file. Always open the project folder with File → Open Folder.
- **One default output folder is wrong.** One folder per project, `data/` inside it. Projects must travel whole.
- **Git doesn't save empty folders** — so `os.makedirs` is required for your repo to work on any other machine.
- **Nobody knows all the libraries.** The skill is thinking *"this is common, someone solved it"* and searching.

---

## 10. Delivery checklist

Before handing data to anyone:

- [ ] Full values, not truncated (`...`)
- [ ] Whitespace stripped
- [ ] Numbers as numbers, not words (`3`, not `Three`)
- [ ] Opens cleanly in Excel — no `â€œ`, no `Â£`
- [ ] Header row present
- [ ] Row count matches expectation (100 quotes · 1000 books)
- [ ] `time.sleep()` present — no site hammered

---

## Phase 1 — done

Can scrape any **static** website end to end, alone.

**Next:** Phase 2 — the Network tab. Most "JavaScript-heavy" sites are just fetching JSON from a hidden API. Find that endpoint and you skip the browser entirely.
