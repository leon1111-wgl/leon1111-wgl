"""Search and sharing tags for the static pages: canonical, language alternates, Open Graph, Twitter and JSON-LD.

Every URL is absolute: crawlers and link previews ignore relative canonical, hreflang and og:image links.
"""
from html import escape
import json

SITE_URL = 'https://leon1111-wgl.github.io/leon1111-wgl/'
GITHUB = 'https://github.com/leon1111-wgl'
OG_HOME = 'assets/og/home.png'
OG_LEARN = 'assets/og/learn.png'
ISO = {'en': 'en', 'zh': 'zh-Hans'}
LOCALE = {'en': 'en_US', 'zh': 'zh_CN'}
AUTHOR = {'@type': 'Person', 'name': 'Leon Wang', 'url': SITE_URL}


def url(path=''):
    return SITE_URL + path


def jsonld(data):
    text = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return f'<script type="application/ld+json">{text}</script>'


def head(path, title, description, lang='en', alternates=None, image=OG_LEARN, image_alt='', data=None,
         site_name='Leon Learn', kind='website'):
    """The tags for one page. alternates maps 'en'/'zh' to the paths of the editions; English is the x-default."""
    E = lambda x: escape(str(x), quote=True)
    tags = [f'<link rel="canonical" href="{url(path)}">']
    if alternates:
        tags += [f'<link rel="alternate" hreflang="{ISO[l]}" href="{url(p)}">' for l, p in alternates.items()]
        tags.append(f'<link rel="alternate" hreflang="x-default" href="{url(alternates.get("en", path))}">')
    tags += [
        f'<meta property="og:type" content="{kind}">', f'<meta property="og:site_name" content="{E(site_name)}">',
        f'<meta property="og:title" content="{E(title)}">', f'<meta property="og:description" content="{E(description)}">',
        f'<meta property="og:url" content="{url(path)}">', f'<meta property="og:image" content="{url(image)}">',
        '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{E(image_alt or title)}">', f'<meta property="og:locale" content="{LOCALE[lang]}">',
    ]
    tags += [f'<meta property="og:locale:alternate" content="{LOCALE[l]}">' for l in (alternates or {}) if l != lang]
    tags += [
        '<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:title" content="{E(title)}">',
        f'<meta name="twitter:description" content="{E(description)}">', f'<meta name="twitter:image" content="{url(image)}">',
    ]
    if data:
        tags.append(jsonld(data))
    return ''.join(tags)


def course_data(name, description, path, lang, prerequisites=None, outcomes=None, kind='Course'):
    """schema.org Course for a course or guide edition. Free study notes by one author, not an official course."""
    data = {'@context': 'https://schema.org', '@type': kind, 'name': name, 'description': description, 'url': url(path),
            'inLanguage': ISO[lang], 'isAccessibleForFree': True, 'provider': AUTHOR, 'author': AUTHOR}
    if prerequisites:
        data['coursePrerequisites'] = list(prerequisites)
    if outcomes:
        data['teaches'] = list(outcomes)
    return data


def sheet_data(name, description, path, lang, course_name, course_path):
    """schema.org LearningResource for a one-page review sheet that belongs to a course."""
    return {'@context': 'https://schema.org', '@type': 'LearningResource', 'name': name, 'description': description,
            'url': url(path), 'inLanguage': ISO[lang], 'learningResourceType': 'Cheat sheet', 'isAccessibleForFree': True,
            'author': AUTHOR, 'isPartOf': {'@type': 'Course', 'name': course_name, 'url': url(course_path)}}
