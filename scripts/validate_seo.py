"""Check the search and sharing tags: canonical URLs, language alternates, share images, JSON-LD and the sitemap."""
from pathlib import Path
from xml.etree import ElementTree
import json
import re
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from seo import SITE_URL

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
PAGES = ['index.html', 'learn/index.html', 'python-zero-to-practice/index.html',
         *[p.relative_to(SITE).as_posix() for folder in ('courses', 'cheatsheets', 'ai', 'projects') for p in sorted((SITE / folder).glob('*.html'))]]


def local(url):
    """The file in site/ that an absolute site URL points at."""
    assert url.startswith(SITE_URL), url
    path = url[len(SITE_URL):].split('#')[0]
    return SITE / (path + 'index.html' if path.endswith('/') or not path else path)


def png_size(path):
    head = path.read_bytes()[:24]
    return struct.unpack('>II', head[16:24])


def validate():
    errors = []
    canonicals = set()
    for name in PAGES:
        page = (SITE / name).read_text()
        where = f'{name}:'
        canonical = re.search(r'<link rel="canonical" href="([^"]+)"', page)
        own = SITE_URL + {'index.html': '', 'learn/index.html': 'learn/'}.get(name, name)
        if not canonical or canonical.group(1) != own:
            errors.append(f'{where} canonical should be {own}')
        else:
            canonicals.add(canonical.group(1))
        for tag in ['<title>', '<meta name="description"', '<meta property="og:title"', '<meta property="og:description"',
                    '<meta property="og:url"', '<meta name="twitter:card" content="summary_large_image"']:
            if tag not in page:
                errors.append(f'{where} missing {tag}')
        image = re.search(r'<meta property="og:image" content="([^"]+)"', page)
        if not image or not local(image.group(1)).is_file():
            errors.append(f'{where} og:image missing or not in site/')
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)
        if not blocks:
            errors.append(f'{where} no JSON-LD')
        for block in blocks:
            try:
                if json.loads(block).get('@context') != 'https://schema.org':
                    errors.append(f'{where} JSON-LD without the schema.org context')
            except json.JSONDecodeError as error:
                errors.append(f'{where} JSON-LD does not parse: {error}')
        alternates = dict(re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)"', page))
        for lang, url in alternates.items():
            if not local(url).is_file():
                errors.append(f'{where} hreflang {lang} points at a missing page')
            elif lang != 'x-default' and canonical and canonical.group(1) not in local(url).read_text():
                errors.append(f'{where} hreflang {lang} page does not point back')
        if alternates and 'x-default' not in alternates:
            errors.append(f'{where} alternates without x-default')
    tree = ElementTree.parse(SITE / 'sitemap.xml')
    locs = [e.text for e in tree.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if len(locs) != len(set(locs)):
        errors.append('sitemap: duplicate URLs')
    for url in locs:
        if not local(url).is_file():
            errors.append(f'sitemap: {url} has no page')
    for url in canonicals - set(locs):
        errors.append(f'sitemap: missing {url}')
    if f'Sitemap: {SITE_URL}sitemap.xml' not in (SITE / 'robots.txt').read_text():
        errors.append('robots.txt: no sitemap line')
    for path in sorted((SITE / 'assets' / 'og').glob('*.png')):
        expected = (1280, 640) if path.name.startswith('repo-') else (1200, 630)
        if png_size(path) != expected:
            errors.append(f'{path.name}: {png_size(path)} instead of {expected}')
        if path.stat().st_size > 1_000_000:
            errors.append(f'{path.name}: over the 1 MB GitHub social preview limit')
    return errors, len(PAGES), len(locs)


if __name__ == '__main__':
    errors, pages, urls = validate()
    if errors:
        print('\n'.join(errors))
        sys.exit(1)
    print(f'SEO tags valid on {pages} pages; sitemap lists {urls} URLs.')
