"""核对图谱的实际课程锚点、关系方向和场景手算；不运行学习者代码。"""
from html.parser import HTMLParser
from pathlib import Path
import importlib.util
import json
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'source'))
from knowledge_map import DATA, map_markdown


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.links = []
        self.payload = ''
        self.capture = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag == 'script' and attrs.get('id') == 'knowledge-data':
            self.capture = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self.capture = False

    def handle_data(self, data):
        if self.capture:
            self.payload += data


def check():
    page = Page()
    page.feed((ROOT / 'index.html').read_text(encoding='utf-8'))
    assert len(page.ids) == len(set(page.ids)), '重复 HTML id'
    assert json.loads(page.payload) == json.loads(json.dumps(DATA)), '嵌入数据不是当前图谱源稿'
    nodes = {n['id']: n for n in DATA['nodes']}
    assert len(nodes) == len(DATA['nodes']) == 24
    assert len(DATA['routes']) == 5
    assert set(n['chapter'] for n in nodes.values()) == set(range(1, 19))
    for n in nodes.values():
        assert n['target'] in page.ids and n['example'] in page.ids, n
        assert all(n[k] for k in ['idea', 'memory', 'question', 'answer', 'pitfall'])
        assert '#c00-map-' + n['id'] in page.links
    edges = DATA['edges']
    assert len({(e['source'], e['target'], e['kind']) for e in edges}) == len(edges)
    for e in edges:
        assert e['source'] in nodes and e['target'] in nodes and e['source'] != e['target']
        assert e['kind'] in ('learn', 'connect') and e['why']
    # 建议先学的联系不能形成循环要求；联想边允许跨主题双向阅读。
    pending = set(nodes)
    while pending:
        ready = {n for n in pending if not any(e['kind'] == 'learn' and e['target'] == n and e['source'] in pending for e in edges)}
        assert ready, '建议先学关系形成循环'
        pending -= ready
    for route in DATA['routes']:
        assert len(set(route['nodes'])) == len(route['nodes'])
        assert all(key in nodes for key in route['nodes'])
    for scene in DATA['scenarios']:
        assert scene['target'] in page.ids
        assert len(scene['steps']) == 5
        for title, inp, action, out, keys in scene['steps']:
            assert title and inp and action and out and keys
            assert all(key in nodes for key in keys)
    for link in page.links:
        if link.startswith('#c00-map-'):
            assert link[len('#c00-map-'):] in nodes, link
        elif link.startswith('#'):
            assert link[1:] in page.ids, link
    assert (ROOT / '知识图谱.md').read_text(encoding='utf-8') == map_markdown()
    # 场景表里的手算规则要与实际参考项目一致，文件只写入临时目录。
    spec = importlib.util.spec_from_file_location('score_project', ROOT / 'projects/02_score_report/app.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as td:
        path = Path(td) / 'scores.csv'
        path.write_text('student_id,name,score\nS1, 小林 ,60\nS2,小安,abc\nS2,小安,0\nS3,小周,90\n', encoding='utf-8')
        report = module.analyze(path)
        assert report['valid_count'] == 3 and report['invalid_count'] == 1
        assert report['total'] == 150 and report['mean'] == 50.0
        assert report['pass_rate'] == 2 / 3
        assert [r['score'] for r in report['ranking']] == [90, 60, 0]
        assert report['ranking'][1]['name'] == '小林'
        with path.open('a', encoding='utf-8') as f:
            f.write('S2,小安,99\n')
        assert module.analyze(path)['total'] == 150, '应保留第一条有效学号记录'
        path.write_text('student_id,name,score\n', encoding='utf-8')
        empty = module.analyze(path)
        assert empty['mean'] is None and empty['pass_rate'] is None
    print(f'知识图谱：{len(nodes)} 个节点、{len(edges)} 条有说明的关系、5 条路线、2 条场景链路通过；成绩手算与原项目一致。')


if __name__ == '__main__':
    check()
