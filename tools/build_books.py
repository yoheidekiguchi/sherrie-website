"""Rebuild the Books section of index.html from tools/books.json.
Only editions marked live are linked; a book with no live edition is left out."""
import json, html, os, re
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
data = json.load(open(os.path.join(here, 'books.json'), encoding='utf-8'))
FLAG = {"Japanese": "jp", "Spanish": "es", "French": "fr"}
def amz(e): return f'https://www.amazon.co.uk/dp/{e["isbn10"]}'
def flag(c): return f'<img class="flag" src="assets/flags/{c}.svg" alt="" width="18" height="12" />'
def links(b, live):
    if b.get('tall'):
        return '\n'.join(f'              <a class="book-buy" href="{amz(e)}" rel="noopener" target="_blank">Buy on Amazon UK</a>' for e in live)
    out = []
    en = [e for e in live if e['lang'] == 'English']
    bi = [e for e in live if e['lang'].startswith('English–')]
    for e in en:
        out.append(f'              <a class="book-buy book-en" href="{amz(e)}" rel="noopener" target="_blank" aria-label="English edition on Amazon UK">{flag("gb")}English</a>')
    if bi:
        out.append('              <p class="book-bi-label">' + flag("gb") + 'Bilingual: English +</p>')
        out.append('              <div class="book-bi">')
        for e in bi:
            other = e['lang'].split('–', 1)[1]
            out.append(f'                <a class="book-buy" href="{amz(e)}" rel="noopener" target="_blank" aria-label="English and {other} edition on Amazon UK">{flag(FLAG[other])}{html.escape(other)}</a>')
        out.append('              </div>')
    return '\n'.join(out)
series, other = [], []
for b in data['books']:
    live = [e for e in b['editions'] if e['live']]
    if not live:
        continue
    t = html.escape(b['title'])
    if b.get('tall'):
        other.append(f'''        <article class="book-wide" role="listitem">
          <img src="assets/books/{b['img']}" alt="Cover of {t}" width="116" height="180" loading="lazy" />
          <div>
            <h3>{t}</h3>
            <p>{html.escape(b['format'])}</p>
            <div class="book-links">
{links(b, live)}
            </div>
          </div>
        </article>''')
        continue
    short = t.replace('Lovely Lon and ', '', 1) if t.startswith('Lovely Lon and ') else t
    series.append(f'''        <article class="book-card" role="listitem">
          <img src="assets/books/{b['img']}" alt="Cover of {t}" width="400" height="400" loading="lazy" />
          <div class="book-body">
            <h3><span class="book-series">Lovely Lon and</span> {short[0].upper() + short[1:]}</h3>
            <div class="book-links">
{links(b, live)}
            </div>
          </div>
        </article>''')
cards = ['        <div class="books-head"><h3>Lovely Lon picture books</h3><p>Hardcover picture books for young children, in English and in bilingual editions. Links go to Amazon UK.</p></div>',
         '        <div class="books" role="list">'] + series + ['        </div>']
if other:
    cards += ['        <div class="books-other" role="list">'] + other + ['        </div>']
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
