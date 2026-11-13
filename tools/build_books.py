"""Rebuild the Books section of index.html from tools/books.json.
Only editions marked live are linked; a book with no live edition is left out."""
import json, html, os, re
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
data = json.load(open(os.path.join(here, 'books.json'), encoding='utf-8'))
cards = []
for b in data['books']:
    live = [e for e in b['editions'] if e['live']]
    if not live:
        continue
    t = html.escape(b['title'])
    w, h = (116, 180) if b.get('tall') else (180, 180)
    links = '\n'.join(
        f'              <a class="book-buy" href="https://www.amazon.co.uk/dp/{e["isbn10"]}" rel="noopener" target="_blank">'
        f'{html.escape(e["lang"]) if e["lang"] != "Paperback" else "Buy on Amazon UK"}</a>' for e in live)
    langs = '' if b.get('tall') else '<p class="book-note">Amazon UK, by edition:</p>\n'
    cards.append(f'''        <article class="book-card" role="listitem">
          <img src="assets/books/{b['img']}" alt="Cover of {t}" width="{w}" height="{h}" loading="lazy" />
          <div>
            <h3>{t}</h3>
            <p>{html.escape(b['format'])}</p>
            {langs}            <div class="book-links">
{links}
            </div>
          </div>
        </article>''')
block = '<!-- BOOKS:START -->\n' + '\n'.join(cards) + '\n        <!-- BOOKS:END -->'
p = os.path.join(root, 'index.html')
s = open(p, encoding='utf-8').read()
s2 = re.sub(r'<!-- BOOKS:START -->.*?<!-- BOOKS:END -->', lambda m: block, s, flags=re.S)
assert s2.count('BOOKS:START') == 1
if s2 != s:
    open(p, 'w', encoding='utf-8').write(s2)
    print('updated', len(cards), 'books')
else:
    print('no change')
