#!/usr/bin/env node
/* Checks site/assets/runner/explain.js against messages the browser runners really print (captured from Pyodide,
   xcc and TeaVM javac), including errors that fall in the test code appended after a reader's answer. */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

const source = readFileSync(process.env.EXPLAIN_FILE || fileURLToPath(new URL('../site/assets/runner/explain.js', import.meta.url)), 'utf8');
const { explain } = await import(`data:text/javascript,${encodeURIComponent(source)}`);
const all = (e) => [e.where, e.title, e.what, ...e.notes, e.fix].join(' ');
const results = [];
const check = (name, fn) => { try { fn(); results.push(`ok   ${name}`); } catch (error) { results.push(`FAIL ${name}: ${error.message.split('\n')[0]}`); } };

const py = (stderr, status = 'error') => ({ status, stdout: '', stderr });
const NAME = 'Traceback (most recent call last):\n  File "main.py", line 2, in <module>\n    pirnt(x)\n    ^^^^^\nNameError: name \'pirnt\' is not defined. Did you mean: \'print\'?\n';

check('Python typo: Chinese, with the line, the name and the likely fix', () => {
  const e = explain(py(NAME), { language: 'python', lang: 'zh' });
  assert.equal(e.line, 2);
  assert.match(all(e), /第 2 行/);
  assert.match(all(e), /pirnt/);
  assert.match(all(e), /拼写/);
  assert.match(e.fix, /print/);
});
check('Python: an assert failing in the tests says the code ran and a test disagreed', () => {
  const e = explain(py('Traceback (most recent call last):\n  File "main.py", line 12, in <module>\n    assert f(3) == 9\nAssertionError\n'), { language: 'python', lang: 'en', ownLines: 5 });
  assert.equal(e.line, null);
  assert.match(all(e), /your code ran/);
});
check('Python: a syntax error reported past the reader\'s code does not claim the code ran', () => {
  const e = explain(py('  File "main.py", line 7\n    print(f(2))\n    ^\nSyntaxError: \'(\' was never closed\n'), { language: 'python', lang: 'en', ownLines: 5 });
  assert.doesNotMatch(all(e), /your code ran/);
  assert.match(all(e), /did not compile|nothing ran/);
});
check('Python: AttributeError on None explains a missing return', () => {
  const e = explain(py('Traceback (most recent call last):\n  File "main.py", line 3, in <module>\n    x.append(1)\nAttributeError: \'NoneType\' object has no attribute \'append\'\n'), { language: 'python', lang: 'en' });
  assert.match(e.what, /returned nothing|no return/);
});
check('C: a missing semicolon names the line and says it is often on the line before', () => {
  const e = explain({ status: 'compile', stdout: '', stderr: "/home/main.c(4): `;' expected\n  printf(\"%d\\n\", x);\n  ^~~~~~\n" }, { language: 'c', lang: 'en' });
  assert.equal(e.line, 4);
  assert.match(all(e), /semicolon/);
  assert.match(all(e), /line before/);
});
check('C: a compile error in the appended tests says nothing ran (review P0)', () => {
  const e = explain({ status: 'compile', stdout: '', stderr: "main.c(9): `text_len' undeclared\n" }, { language: 'c', lang: 'en', ownLines: 6 });
  assert.doesNotMatch(all(e), /your code ran/);
  assert.match(all(e), /did not compile/);
  const z = explain({ status: 'compile', stdout: '', stderr: "main.c(9): `}' expected\n" }, { language: 'c', lang: 'zh', ownLines: 6 });
  assert.doesNotMatch(all(z), /你的代码运行了/);
  assert.match(all(z), /没有通过编译/);
});
check('C: library names point to their header', () => {
  for (const [name, header] of [['printf', 'stdio.h'], ['getchar', 'stdio.h'], ['malloc', 'stdlib.h'], ['rand', 'stdlib.h'], ['strchr', 'string.h'], ['isdigit', 'ctype.h'], ['sqrt', 'math.h'], ['bool', 'stdbool.h'], ['INT_MAX', 'limits.h'], ['assert', 'assert.h'], ['NULL', 'stddef.h']]) {
    const e = explain({ status: 'compile', stdout: '', stderr: `main.c(3): \`${name}' undeclared\n` }, { language: 'c', lang: 'en' });
    assert.match(e.title, new RegExp(header.replace('.', '\\.')), `${name} should point to ${header}`);
  }
  const other = explain({ status: 'compile', stdout: '', stderr: "main.c(3): `totl' undeclared\n" }, { language: 'c', lang: 'en' });
  assert.match(other.what, /#include for its header/);
});
check('C: a missing closing bracket does not blame the line before', () => {
  const e = explain({ status: 'compile', stdout: '', stderr: "main.c(8): `}' expected\n" }, { language: 'c', lang: 'en' });
  assert.equal(e.notes.length, 0);
});
check('Java: a name the tests call but the class lacks is blamed on the test call, not a line of the answer', () => {
  const e = explain({ status: 'compile', stdout: '', stderr: 'Tests.java:3: cannot find symbol\n  symbol:   method plus(int,int)\n  location: class Main\n' }, { language: 'java', lang: 'en', ownLines: 4 });
  assert.equal(e.line, null);
  assert.equal(e.where, '');
  assert.match(e.what, /test code calls `plus`/);
});
check('Java: a missing class suggests an import', () => {
  const e = explain({ status: 'compile', stdout: '', stderr: 'Main.java:3: cannot find symbol\n  symbol:   class Scanner\n  location: class Main\n' }, { language: 'java', lang: 'zh' });
  assert.equal(e.line, 3);
  assert.match(e.what, /import java\.util\.Scanner/);
});
check('Java: an uncaught exception names only causes the browser runner reports this way', () => {
  const e = explain({ status: 'error', stdout: '', stderr: 'Uncaught exception: (could not fetch message)\n' }, { language: 'java', lang: 'en' });
  assert.doesNotMatch(e.what, /division by zero/);
});
check('an unknown error with no line does not point at a line', () => {
  const e = explain({ status: 'error', stdout: '', stderr: 'something odd happened\n' }, { language: 'c', lang: 'en' });
  assert.doesNotMatch(e.what, /line it names/);
});
check('a clean run, a timeout or a missing runtime gets no explanation', () => {
  for (const status of ['ok', 'timeout', 'unavailable']) assert.equal(explain({ status, stdout: '', stderr: '' }, { language: 'python' }), null);
});

console.log(results.join('\n'));
if (results.some((r) => r.startsWith('FAIL'))) process.exit(1);
console.log(`PASS: ${results.length} error-explanation checks`);
