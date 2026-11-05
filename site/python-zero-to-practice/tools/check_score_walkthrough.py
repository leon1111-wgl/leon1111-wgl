"""检查项目分步参考：精确输出、函数边界、原项目等价性和迁移规则。"""
import contextlib
import copy
import csv
import importlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def raises(error_type, action, message=None):
    try:
        action()
    except error_type as error:
        if message is not None:
            assert str(error) == message, (str(error), message)
    else:
        raise AssertionError(f'预期 {error_type.__name__}，但没有报错')


def check(project_dir=None):
    project_dir = project_dir or ROOT / 'projects/02_score_report'
    guided = project_dir / 'guided'
    manifest = json.loads((ROOT / 'tools/score_walkthrough.json').read_text(encoding='utf-8'))
    # 每个脚本从无关目录独立启动；只让临时目录承接意外输出。
    env = dict(os.environ, PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='Python 分步验证 ') as td:
        temp = Path(td)
        for case in manifest:
            result = subprocess.run([sys.executable, '-X', 'utf8', str(guided / case['file'])],
                cwd=temp, env=env, capture_output=True, text=True, encoding='utf-8', timeout=5)
            assert result.returncode == 0, (case['file'], result.stderr)
            assert result.stdout == case['output'], (case['file'], result.stdout, case['output'])
            assert not result.stderr, (case['file'], result.stderr)
        assert not list(temp.iterdir()), '分步示例应只打印，不生成结果文件'

        names = [Path(c['file']).stem for c in manifest]
        old_modules = {name: sys.modules.get(name) for name in names}
        sys.path.insert(0, str(guided))
        try:
            for name in names:
                sys.modules.pop(name, None)
            quiet = io.StringIO()
            with contextlib.redirect_stdout(quiet):
                first, second, third, fourth, transfer = [importlib.import_module(name) for name in names]
            assert quiet.getvalue() == '', '导入阶段文件不应执行演示'
            raw = {'student_id': ' s1 ', 'name': ' A ', 'score': '0'}
            original = copy.deepcopy(raw)
            assert first.parse_row(raw) == {'student_id': 's1', 'name': 'A', 'score': 0}
            assert raw == original, '清洗应返回新字典，不改调用者原始行'
            for score in ['0', '60', '100', ' 60 ', '+60']:
                assert first.parse_row(dict(raw, score=score))['score'] == int(score)
            for score in ['abc', '', None, '60.5']:
                raises(ValueError, lambda score=score: first.parse_row(dict(raw, score=score)), '分数不是整数')
            for score in ['-1', '101']:
                raises(ValueError, lambda score=score: first.parse_row(dict(raw, score=score)), '分数超出 0 到 100')
            for key in ['student_id', 'name']:
                raises(ValueError, lambda key=key: first.parse_row(dict(raw, **{key: ' '})), 'ID 或姓名为空')
            raises(ValueError, lambda: first.parse_row({**raw, None: ['extra']}), '字段数超过表头列数')
            sample = second.sample_rows()
            original = copy.deepcopy(sample)
            valid, errors = second.collect_rows(sample)
            assert sample == original
            assert [r['score'] for r in valid] == [60, 0, 90]
            assert errors == [{'record': 2, 'reason': '分数不是整数'}, {'record': 4, 'reason': '重复 ID'}]
            assert second.collect_rows(iter(sample)) == (valid, errors)
            assert second.collect_rows([]) == ([], [])
            assert second.collect_rows(sample) == (valid, errors), '多次调用的 seen 不能共享'
            invalid_only = [dict(raw, score='bad')]
            assert second.collect_rows(invalid_only)[0] == []
            before = copy.deepcopy(valid)
            summary = third.summarize(valid)
            assert summary['valid_count'] == 3 and summary['total'] == 150
            assert summary['mean'] == 50.0 and summary['pass_rate'] == 2 / 3
            assert valid == before, '排名不能原地改变有效记录顺序'
            empty = third.summarize([])
            assert empty == {'valid_count': 0, 'total': 0, 'mean': None, 'pass_rate': None, 'ranking': []}
            tied = [dict(raw, student_id='b', score=60), dict(raw, student_id='a', score=60)]
            assert [r['student_id'] for r in third.summarize(tied)['ranking']] == ['a', 'b']
            assert third.summarize([{'student_id':'x','name':'X','score':59}])['pass_rate'] == 0
            assert third.summarize([{'student_id':'x','name':'X','score':60}])['pass_rate'] == 1
            spec = importlib.util.spec_from_file_location('original_score_project', project_dir / 'app.py')
            complete = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(complete)
            assert fourth.analyze(project_dir / 'data/scores.csv') == complete.analyze(project_dir / 'data/scores.csv')
            fixtures = [
                'student_id,name,score\n',
                'student_id,name,score\ns1,A,bad\ns1,A,0\ns1,A,100\ns2,B,60\n',
                'student_id,name,score\ns1,"A, B",100\ns2,"两行\n姓名",x\ns3,C,60\n',
                '\ufeffstudent_id,name,score\ns1,A,0\n\ns2,B\ns3,C,60,extra\n',
                'student_id,name,score,comment\ns1,A,90,已声明的额外列\n',
            ]
            for content in fixtures:
                file = temp / 'scores.csv'
                file.write_text(content, encoding='utf-8', newline='')
                actual = fourth.analyze(file)
                assert actual == complete.analyze(file), (content, actual)
            file.write_text('student_id,name,score\ns1,"两行\n姓名",bad\n', encoding='utf-8')
            assert fourth.analyze(file)['errors'][0]['record'] == 1, '使用逻辑记录号，不是物理行号'
            file.write_text('wrong\n', encoding='utf-8')
            raises(ValueError, lambda: fourth.analyze(file), '缺少必需列 student_id、name、score')
            raises(FileNotFoundError, lambda: fourth.analyze(temp / 'not-found.csv'))
            limit = csv.field_size_limit()
            try:
                csv.field_size_limit(30)
                file.write_text('student_id,name,score\ns1,'+'x'*31+',60\n', encoding='utf-8')
                raises(csv.Error, lambda: fourth.analyze(file))
            finally:
                csv.field_size_limit(limit)
            log = transfer.sample_logs()
            before = copy.deepcopy(log)
            rows, failures = transfer.clean_tool_rows(log)
            assert log == before and [r['ms'] for r in rows] == [0, 250, 30]
            assert sum(r['ms'] for r in rows) == 280
            assert failures == [{'record':3,'reason':'耗时不是整数'}, {'record':5,'reason':'重复 ID'}]
            assert transfer.clean_tool_rows([]) == ([], [])
            edge_rows = [{'id':'x','tool':'search','ms':'-1'}, {'id':'x','tool':'search','ms':'1000'}]
            clean, bad = transfer.clean_tool_rows(edge_rows)
            assert clean == [{'id':'x','tool':'search','ms':1000}]
            assert bad == [{'record':1,'reason':'耗时不能为负数'}]
            for changes in [{'id':''}, {'tool':' '}, {'ms':None}, {None:['extra']}]:
                dirty = {'id':'x','tool':'search','ms':'0'}
                dirty.update(changes)
                clean, bad = transfer.clean_tool_rows([dirty])
                assert not clean and len(bad) == 1
        finally:
            sys.path.remove(str(guided))
            for name, old in old_modules.items():
                if old is None:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = old
    print('成绩项目分步验收：5/5 脚本输出通过；边界、输入保留、导入静默、完整项目等价与工具日志迁移通过。')


if __name__ == '__main__':
    check()
