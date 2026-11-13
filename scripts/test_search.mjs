#!/usr/bin/env node
/* Checks the chapter search (site/assets/find.js over site/learn/data/search.json) on what readers type: the learner
   walk's lookups, the abbreviations and Chinese names students use, and words that must not land on the wrong chapter.
   A lookup passes when one of the chapters that teach the idea is among the first three hits. */
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

const require = createRequire(import.meta.url);
const find = require('../site/assets/find.js');
const index = JSON.parse(readFileSync(fileURLToPath(new URL('../site/learn/data/search.json', import.meta.url)), 'utf8'));
const top = (q, n = 3) => find.search(index, q, n).map((h) => `${h.c}/${h.i}`);

const KNN = ['comp3308/learning-neighbors', 'comp3308/knn-practice', 'ml/nearest-neighbours'];
const DP = ['comp2022/cyk-parsing', 'comp2022/chomsky-normal-form', 'comp2123/trees-traversal', 'info1113/recursion-memoization'];
const GD = ['ml/gradient-descent-scaling', 'start/slopes-gradients', 'comp3308/neural-training'];
const UB = ['comp2017/representation-control', 'comp2017/data-races-mutexes', 'comp2017/memory-layout', 'comp2017/callbacks', 'comp2017/preprocessing', 'comp2017/debugging-evidence'];
const OOP = ['info1113/classes-invariants', 'info1113/inheritance-composition', 'info1113/overload-override', 'info1113/abstractions'];
const CNN = ['comp3308/convolutional-networks', 'dl/dl-convolution'];
const MLP = ['dl/dl-representations', 'comp3308/backpropagation'];
const LLM = ['dl/dl-transformer-block', 'multimodal/visual-instruction-tuning', 'dl/dl-attention', 'dl/dl-token-embeddings'];
const LOOKUPS = [
  // the learner walk's lookups (scripts/learner_walk.mjs)
  ['二分查找', ['comp2123/recurrences-merge-sort', 'comp2123/bst-range-queries']], ['binary search', ['comp2123/recurrences-merge-sort', 'comp2123/bst-range-queries']],
  ['时间复杂度', ['comp2123/analysis-correctness']], ['big O', ['comp2123/analysis-correctness']],
  ['最短路径', ['comp2123/dijkstra-relaxation', 'comp2123/bfs-distance']], ['shortest path', ['comp2123/dijkstra-relaxation', 'comp2123/bfs-distance']],
  ['哈希表', ['comp2123/hashing-collisions', 'info1113/equality-hashing']], ['hash table', ['comp2123/hashing-collisions', 'info1113/equality-hashing']],
  ['梯度下降', GD], ['gradient descent', GD],
  ['内存泄漏', ['info1113/memory-diagrams', 'comp2017/memory-layout', 'comp2017/allocation-ownership', 'comp2017/debugging-evidence']],
  ['memory leak', ['info1113/memory-diagrams', 'comp2017/memory-layout', 'comp2017/allocation-ownership', 'comp2017/debugging-evidence']],
  ['段错误', ['comp2017/memory-layout']], ['segfault', ['comp2017/memory-layout']],
  ['竞态条件', ['comp2017/data-races-mutexes']], ['race condition', ['comp2017/data-races-mutexes']],
  ['过拟合', ['ml/validation-regularization-shift', 'comp3308/tree-generalization', 'ml/trees-ensembles']],
  ['列表推导式', ['python/c10']], ['cross validation', ['comp3308/evaluation-design', 'ml/validation-regularization-shift']],
  ['IoU', ['vision/detection-overlap', 'vision/detection-average-precision']], ['RAG', ['multimodal/multimodal-rag']],
  // abbreviations and Chinese names students type for ideas the chapters teach under their full names
  ['KNN', KNN], ['k-NN', KNN], ['k 近邻', KNN], ['最近邻', KNN],
  ['DP', DP], ['动态规划', DP], ['dynamic programming', DP],
  ['GD', GD], ['SGD', ['dl/dl-optimization']], ['随机梯度下降', ['dl/dl-optimization']],
  ['UB', UB], ['undefined behavior', UB], ['未定义行为', UB],
  ['batch norm', ['dl/dl-normalization']], ['batch normalization', ['dl/dl-normalization']], ['批归一化', ['dl/dl-normalization']],
  ['PCA', ['ml/clustering-pca']], ['主成分分析', ['ml/clustering-pca']], ['principal component analysis', ['ml/clustering-pca']],
  ['OOP', OOP], ['面向对象', OOP], ['object-oriented programming', OOP],
  ['CNN', CNN], ['卷积神经网络', CNN], ['MLP', MLP], ['多层感知机', MLP],
  ['BFS', ['comp2123/bfs-distance', 'comp3308/search-models']], ['广度优先搜索', ['comp2123/bfs-distance', 'comp3308/search-models']],
  ['DFS', ['comp2123/dfs-bridges', 'comp2123/topological-scc', 'comp3308/search-models']], ['深度优先搜索', ['comp2123/dfs-bridges', 'comp2123/topological-scc', 'comp3308/search-models']],
  ['MST', ['comp2123/minimum-spanning-trees']], ['最小生成树', ['comp2123/minimum-spanning-trees']],
  ['NMS', ['vision/detection-overlap']], ['非极大值抑制', ['vision/detection-overlap']],
  ['mAP', ['vision/detection-average-precision']], ['mean average precision', ['vision/detection-average-precision']],
  ['ViT', ['vision/visual-tokens']], ['vision transformer', ['vision/visual-tokens']],
  ['LLM', LLM], ['大语言模型', LLM], ['large language model', LLM],
];

const results = [];
const check = (name, fn) => { try { fn(); results.push(`ok   ${name}`); } catch (error) { results.push(`FAIL ${name}: ${error.message.split('\n')[0]}`); } };
for (const [query, right] of LOOKUPS) {
  check(`"${query}" finds a chapter that teaches it`, () => {
    const hits = top(query);
    assert.ok(hits.some((h) => right.includes(h)), `first three: ${hits.join(', ') || 'nothing'}`);
  });
}
check('"map" in lower case is Java\'s Map, not mean average precision', () => assert.match(top('map', 1)[0] || '', /^info1113\//));
check('"rag" never matches inside "storage"', () => assert.ok(!top('rag').some((h) => h.startsWith('info1113/'))));
check('a topic no chapter teaches finds nothing rather than something wrong', () => assert.deepEqual(top('pumping lemma'), []));
check('"LLM" does not lead to a chapter that only says it is not a language model', () => assert.ok(!top('LLM').includes('ml/text-naive-bayes')));

console.log(results.join('\n'));
const failed = results.filter((r) => r.startsWith('FAIL'));
if (failed.length) { console.log(`${failed.length} of ${results.length} search checks failed`); process.exit(1); }
console.log(`PASS: ${results.length} search checks`);
