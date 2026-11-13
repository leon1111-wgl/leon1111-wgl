"""Write site/learn/data/search.json: what every chapter teaches, in both languages, for the hub and homepage search.

Each chapter keeps five fields; site/assets/find.js ranks a match by the field it is found in:
  t  titles in English and Chinese                                   10
  k  defined terms (glossary, both languages), functions its programs call   6
  l  the first sentences of its principle: what the chapter says it teaches  5
  h  its worked problems, programs and notes, by title                 3
  b  its most distinctive words, phrases and Chinese pieces, best first  1 to 2
Text is folded to lower case so the browser only has to look things up.

The body is not stored whole (2.7 MB). It is cut to the terms that set a chapter apart (tf-idf), and every term a
reader is likely to type is kept wherever it occurs: all glossary terms on the site and the synonym words below.

`syn` maps what readers type to what chapters say. Each group holds names for one idea only: a word joins a group
only when a chapter teaches that exact idea under the other name.
"""
import gzip
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from build_learn import PYTHON_EN  # noqa: E402
CONTENT = ROOT / 'content'
OUT = ROOT / 'site' / 'learn' / 'data' / 'search.json'
COURSES = ['INFO1113', 'COMP2017', 'COMP2123', 'COMP2022', 'COMP3308']
GUIDES = {'start': 'primer.json', 'ml': 'paths/ml.json', 'dl': 'paths/dl.json', 'vision': 'paths/vision.json', 'multimodal': 'paths/multimodal.json'}

SYNONYMS = [
    ['binary search', '二分查找', '二分搜索', '二分法'],
    ['big-o', 'big o', 'time complexity', 'asymptotic', '时间复杂度', '渐近', '大 o 记号'],
    ['hash table', 'hash map', 'hashing', '哈希表', '散列表', '哈希'],
    ['segmentation fault', 'segfault', '段错误'],
    ['race condition', 'data race', '竞态条件', '竞态', '竞争条件', '数据竞争'],
    ['memory leak', 'memory leaks', '内存泄漏', '内存泄露'],
    ['cross-validation', 'cross validation', '交叉验证'],
    ['shortest path', 'shortest paths', 'shortest-path', '最短路径', '最短路'],
    ['comprehension', 'list comprehension', '列表推导式', '列表推导', '推导式'],
    ['gradient descent', 'gd', '梯度下降'],
    ['stochastic gradient descent', 'sgd', '随机梯度下降'],
    ['overfitting', 'overfit', '过拟合'],
    ['retrieval-augmented generation', 'rag', '检索增强生成', '检索增强'],
    ['intersection over union', 'iou', '交并比'],
    ['null pointer', '空指针'],
    ['deadlock', '死锁'],
    ['dynamic allocation', 'malloc', '动态分配', '动态内存'],
    # abbreviations and Chinese names students type; each idea is taught under its full name in the chapters found
    ['k-nearest neighbours', 'k-nearest neighbors', 'k nearest neighbours', 'k nearest neighbors', 'knn', 'k-nn', 'k 近邻', 'k近邻'],
    ['dynamic programming', 'dp', '动态规划'],
    ['undefined behaviour', 'undefined behavior', 'ub', '未定义行为'],
    ['batch normalization', 'batch normalisation', 'batch norm', 'batchnorm', '批归一化', '批量归一化'],
    ['principal component analysis', 'principal components', 'pca', '主成分分析', '主成分'],
    ['object-oriented programming', 'object-oriented', 'object oriented', 'oop', '面向对象编程', '面向对象'],
    ['convolutional neural network', 'convolutional network', 'cnn', '卷积神经网络', '卷积网络'],
    ['multilayer perceptron', 'multi-layer perceptron', 'mlp', '多层感知机', '多层感知器'],
    ['breadth-first search', 'breadth first search', 'bfs', '广度优先搜索', '广度优先'],
    ['depth-first search', 'depth first search', 'dfs', '深度优先搜索', '深度优先'],
    ['minimum spanning tree', 'minimum spanning trees', 'mst', '最小生成树'],
    ['non-maximum suppression', 'nms', '非极大值抑制'],
    # "=" marks a word matched with its capitals: "mAP" is mean average precision, "map" stays Java's Map
    ['mean average precision', '=mAP', '平均精度均值'],
    ['vision transformer', 'vit', '视觉 transformer'],
    ['large language model', 'llm', '大语言模型'],
]

# What readers call a chapter when its own title and terms use other words. Each entry was checked against the
# chapter's text: the chapter teaches that idea, by that name or the one in its title.
ALIASES = {
    'comp2123/analysis-correctness': ['big-o notation', 'asymptotic notation', 'time complexity', '时间复杂度', '大 o 记号', '渐近记号'],
    'comp2123/trees-traversal': ['binary tree', '二叉树'],
    'comp3308/support-vector-machines': ['svm', 'support vector machine', '支持向量机'],
    'ml/logistic-thresholds': ['logistic regression', '逻辑回归'],
    'vision/detection-overlap': ['object detection', '目标检测', 'non-maximum suppression', 'nms', '非极大值抑制'],
    'info1113/exceptions': ['exception handling', 'try catch', '异常处理'],
    'info1113/testing-contracts': ['unit test', 'junit', '单元测试'],
    'comp2017/memory-layout': ['segmentation fault', 'segfault', '段错误', 'stack overflow', '栈溢出'],
    'comp2017/parallel-performance': ['thread pool', 'worker pool', '线程池'],
    # the four parts of object-oriented programming: objects and encapsulation, inheritance, overriding, abstraction
    'info1113/classes-invariants': ['object-oriented programming', '面向对象编程'],
    'info1113/inheritance-composition': ['object-oriented programming', '面向对象编程'],
    'info1113/overload-override': ['object-oriented programming', '面向对象编程'],
    'info1113/abstractions': ['object-oriented programming', '面向对象编程'],
    # the parts a large language model is built from (embeddings, attention, the Transformer block) and the chapter that
    # connects one to images; a chapter that only says it is "not a language model" is left out
    'dl/dl-token-embeddings': ['large language model', '大语言模型'],
    'dl/dl-attention': ['large language model', '大语言模型'],
    'dl/dl-transformer-block': ['large language model', '大语言模型'],
    'multimodal/visual-instruction-tuning': ['large language model', '大语言模型'],
    # COCO's AP, which this chapter teaches, is averaged over classes: what readers call mAP
    'vision/detection-average-precision': ['mean average precision', '平均精度均值'],
}

STOP = set('''about above after again against also although among another anything around because been before being
below both cannot could does doing down during each either else enough even every example first from further given gives
have having here into itself just keep keeps later least less like made make makes many might more most much must need
needs never next often only other others over same second should shows since some still such than that their them then
there these they thing things third this those though three through thus together under until upon used uses using very
want what when where whether which while whole will with within without would write your the and for are but not you
its can one two was his her has had may all any our out who how why use new now see way'''.split())
EN_WORD = re.compile(r"[a-z][a-z0-9+#*'-]*[a-z0-9+#*]|[a-z]")
HAN_RUN = re.compile('[一-鿿]+')
EN_KEEP, ZH_KEEP = 70, 70


def clean(text):
    """Readable text for the reasons shown under a hit: code marks dropped, space collapsed, case kept."""
    text = re.sub(r'`([^`]*)`', r'\1', str(text))
    text = text.replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', ' ')
    return re.sub(r'\s+', ' ', text).strip()


def fold(text):
    text = re.sub(r'`([^`]*)`', r'\1', str(text))
    text = text.replace('‑', '-').replace('–', '-').replace('—', ' ')
    return re.sub(r'\s+', ' ', text).strip().lower()


def gather(value, keys=None):
    """All strings under value; with keys, only under those dict keys (and anything below them)."""
    out = []
    if isinstance(value, str):
        out.append(value)
    elif isinstance(value, list):
        for v in value:
            out += gather(v)
    elif isinstance(value, dict):
        for k, v in value.items():
            if k in ('code', 'output', 'id', 'language', 'url', 'trace', 'sources', 'rows', 'formula'):
                continue
            if keys is None or k in keys:
                out += gather(v)
    return out


def lead(text, sentences=1):
    """The first sentences of a paragraph: what the chapter says it is about."""
    first = str(text).split('\n\n')[0]
    parts = re.split(r'(?<=[.!?。！？])\s*', first)
    return ' '.join(parts[:sentences])


def course_chapters(code, keywords):
    en = json.loads((CONTENT / f'{code}.json').read_text())
    zh = json.loads((CONTENT / 'translations' / f'{code}.zh.json').read_text())
    cid = code.lower()
    for n, (a, b) in enumerate(zip(en['topics'], zh['topics']), 1):
        both = (a, b)
        yield {
            'c': cid, 'i': a['id'], 'n': n,
            't': fold(f"{a['title']} | {b['title']}"),
            'k': clean(' · '.join(g['term'] for t in both for g in t.get('glossary', [])) + ' · ' + keywords.get(cid, {}).get(a['id'], '')),
            'l': clean(f"{lead(a['principle'])} {lead(b['principle'])}"),
            'h': clean(' · '.join([p['title'] for t in both for p in t.get('worked_problems', [])]
                                 + [x['title'] for t in both for x in t.get('code_examples', [])]
                                 + [x['title'] for t in both for x in t.get('instructor_notes', [])])),
            'b': fold(' '.join(gather(list(both)))),
        }


def guide_chapters(cid, name):
    guide = json.loads((CONTENT / name).read_text())
    for n, t in enumerate(guide['topics'], 1):
        yield {
            'c': cid, 'i': t['id'], 'n': n,
            't': fold(' | '.join(gather(t['title']))),
            'k': clean(' · '.join(v for g in t.get('glossary', []) for v in gather(g.get('term')))),
            'l': clean(' '.join(lead(v) for v in gather(t['concept']))),
            'h': clean(' · '.join(gather([p.get('title') for p in t.get('practice_cases', [])] + [x.get('title') for x in t.get('code_examples', [])]))),
            'b': fold(' '.join(gather(t))),
        }


def handbook_chapters():
    """The Chinese Python handbook: one chapter per '# NN title' section of its textbook, prose without code."""
    text = (ROOT / 'site' / 'python-zero-to-practice' / 'textbook.md').read_text()
    text = re.sub(r'```.*?```', ' ', text, flags=re.S)
    parts = re.split(r'^# (\d\d) (.+)$', text, flags=re.M)
    for k in range(1, len(parts), 3):
        num, title, body = parts[k], parts[k + 1], parts[k + 2]
        goals = re.search(r'^## 学习目标\s*\n(.*?)(?=^## )', body, flags=re.M | re.S)
        yield {'c': 'python', 'i': f'c{num}', 'n': int(num) + 1, 't': fold(f'{PYTHON_EN[int(num)]} | {title}'), 'k': '',
               'l': clean(goals.group(1) if goals else '')[:300], 'h': clean(' · '.join(re.findall(r'^## (.+)$', body, flags=re.M))),
               'b': fold(re.sub(r'^#+ .*$', ' ', body, flags=re.M))}


def latin_terms(text):
    words = [w.strip("'-") for w in EN_WORD.findall(text)]
    out = [w for w in words if len(w) >= 3 and w not in STOP]
    # two-word phrases of content words, joined by _ so they stay one term ("shortest_path")
    out += [f'{a}_{b}' for a, b in zip(words, words[1:]) if a not in STOP and b not in STOP and len(a) >= 3 and len(b) >= 3]
    return out


def han_terms(text):
    out = []
    for run in HAN_RUN.findall(text):
        for n in (2, 3):
            out += [run[i:i + n] for i in range(len(run) - n + 1)]
    return out


def vocabulary():
    """Terms readers type: every glossary term on the site and every synonym word."""
    vocab = {fold(w) for group in SYNONYMS for w in group if not w.startswith('=')}
    for code in COURSES:
        for path in (CONTENT / f'{code}.json', CONTENT / 'translations' / f'{code}.zh.json'):
            vocab |= {fold(g['term']) for t in json.loads(path.read_text())['topics'] for g in t.get('glossary', [])}
    for name in GUIDES.values():
        for t in json.loads((CONTENT / name).read_text())['topics']:
            vocab |= {fold(v) for g in t.get('glossary', []) for v in gather(g.get('term'))}
    vocab = {re.sub(r'[（(].*?[)）]', '', v).strip() for v in vocab}
    return sorted(v for v in vocab if len(v) >= 2)


WORDS = re.compile(r"[a-z0-9][a-z0-9+#*'.-]*[a-z0-9+#*]|[a-z0-9]")


def word_runs(text, longest=4):
    """Every run of up to four consecutive Latin words, so a glossary term is found by a set lookup."""
    words = WORDS.findall(text)
    return {' '.join(words[i:i + n]) for n in range(1, longest + 1) for i in range(len(words) - n + 1)}


def contains(term, text, runs):
    if HAN_RUN.search(term):
        return term in text
    return ' '.join(WORDS.findall(term)) in runs


def distinctive(chapters):
    """Cut each chapter's body to its most distinctive terms (tf-idf), keeping every vocabulary term it contains."""
    vocab = vocabulary()
    docs = [(Counter(latin_terms(ch['b'])), Counter(han_terms(ch['b']))) for ch in chapters]
    df_en, df_zh = Counter(), Counter()
    for en, zh in docs:
        df_en.update(en.keys())
        df_zh.update(zh.keys())
    found = []
    for ch in chapters:
        runs = word_runs(ch['b'])
        found.append([v for v in vocab if contains(v, ch['b'], runs)])
    df_v = Counter(v for f in found for v in f)
    n = len(docs)
    for ch, (en, zh), vs in zip(chapters, docs, found):
        def weight(term, counts, df):
            return (1 + math.log(counts[term])) * math.log(n / df[term])
        en_top = sorted(en, key=lambda w: -weight(w, en, df_en))[:EN_KEEP]
        zh_top = sorted(zh, key=lambda g: -weight(g, zh, df_zh))[:ZH_KEEP]
        scored = {w: weight(w, en, df_en) for w in en_top}
        scored.update({g: weight(g, zh, df_zh) for g in zh_top})
        body = ch['b']
        for v in vs:
            key = v.replace(' ', '_')
            if key not in scored:
                scored[key] = (1 + math.log(max(1, body.count(v)))) * math.log(n / df_v[v])
        ch['b'] = ' '.join(sorted(scored, key=lambda w: -scored[w]))


def build():
    keywords = json.loads((ROOT / 'site' / 'learn' / 'data' / 'keywords.json').read_text())
    chapters = list(handbook_chapters())
    for code in COURSES:
        chapters += list(course_chapters(code, keywords))
    for cid, name in GUIDES.items():
        chapters += list(guide_chapters(cid, name))
    distinctive(chapters)
    for ch in chapters:
        extra = ALIASES.get(f"{ch['c']}/{ch['i']}")
        if extra:
            ch['k'] = clean(f"{ch['k']} · {' · '.join(extra)}")
    data = {'v': 2, 'syn': SYNONYMS, 'chapters': chapters}
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    return data


if __name__ == '__main__':
    d = build()
    raw = OUT.read_bytes()
    print(f"search index: {len(d['chapters'])} chapters, {len(raw) // 1024} KB, {len(gzip.compress(raw)) // 1024} KB gzipped")
