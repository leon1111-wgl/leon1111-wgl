/* Chapter search shared by the learning hub and the homepage. The index is learn/data/search.json (scripts/build_search.py).
   A chapter matches when every word of the query is found in it. Where a word is found decides the rank: title 10,
   defined term 6, the chapter's opening sentence 5, a worked problem or program title 3, its distinctive terms 1 to 2
   (more for the terms that set it apart most). Words typed side by side that appear side by side count extra.
   Short Latin words such as IoU or RAG must match a whole word, so "rag" never matches "storage"; plurals match their
   singular. Chinese is matched as typed, or by its two-character pieces when two thirds of them occur in one field.
   Synonym groups map what readers type to what chapters call it. */
(function (root) {
  const WEIGHT = { t: 10, k: 6, l: 5, h: 3, b: 1 };
  const FIELDS = ['t', 'k', 'l', 'h', 'b'];
  const HAN = /[一-鿿]/;
  const STOP = new Set(['a', 'an', 'the', 'of', 'for', 'to', 'in', 'on', 'and', 'or', 'is', 'are', 'how', 'what', 'why', 'with', 'do', 'does', 'i', 'my', 'vs', '的', '是', '怎么', '什么', '如何']);
  const fold = (s) => String(s || '').normalize('NFKC').toLowerCase().replace(/[‐-—_]/g, '-').replace(/\s+/g, ' ').trim();
  const escapeRe = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const cache = new Map();
  /* a Latin word: whole word when short, a word start when long ("overfit" finds "overfitting"), plural or not */
  const latinRe = (word) => {
    let re = cache.get(word);
    if (!re) {
      const stem = word.length >= 5 && /[^s]s$/.test(word) ? word.replace(/(ies|es|s)$/, (m) => (m === 'ies' ? 'y' : '')) : word;
      // "dictionary" finds "dictionaries", and "dictionaries" finds "dictionary"
      const body = stem.length >= 5 && stem.endsWith('y') ? `${escapeRe(stem.slice(0, -1))}(?:y|ies)` : escapeRe(stem);
      re = new RegExp(`(?:^|[^a-z0-9])(${body}${stem.length <= 4 ? '(?:s|es)?(?![a-z0-9])' : ''})`);
      cache.set(word, re);
    }
    return re;
  };
  const pieces = (s) => { const out = []; for (let i = 0; i + 2 <= s.length; i += 1) out.push(s.slice(i, i + 2)); return out; };
  /* how well one unit is found in one field: 0 (not found) to 1, and where (0 = start of the field) */
  const found = (u, text) => {
    if (HAN.test(u)) {
      const at = text.indexOf(u);
      if (at >= 0) return [1, at];
      if (u.length < 3) return [0, 0];
      const ps = pieces(u);
      const got = ps.filter((p) => text.includes(p)).length / ps.length;
      return got >= 2 / 3 ? [got * 0.6, text.indexOf(ps.find((p) => text.includes(p)))] : [0, 0];
    }
    const m = latinRe(u).exec(text);
    return m ? [1, m.index] : [0, 0];
  };
  const units = (q) => {
    const all = (q.match(/[一-鿿]+|[a-z0-9*+#][a-z0-9+#*.'-]*/g) || []).map((u) => u.replace(/[.'-]+$/, '')).filter(Boolean);
    const kept = all.filter((u) => !STOP.has(u) && (u.length > 1 || HAN.test(u) || all.length === 1));
    return kept.length ? kept : all;
  };
  function scoreUnit(u, ch) {
    let best = 0; let where = '';
    for (const k of FIELDS) {
      const [hit, at] = found(u, ch[k]);
      if (!hit) continue;
      // distinctive terms are stored best first: earlier ones count up to twice as much
      const s = WEIGHT[k] * hit * (k === 'b' ? 2 - at / Math.max(1, ch.b.length) : 1);
      if (s > best) { best = s; where = k; }
    }
    return [best, where];
  }
  /* a group of alternatives (synonyms): the best-scoring alternative counts */
  function scoreAlternatives(alts, ch, synonym) {
    let best = 0; let where = '';
    for (const alt of alts) {
      const us = units(alt);
      if (!us.length) continue;
      // a several-word synonym counts only as a phrase: "language model" is not "regular language" plus "model"
      if (synonym && us.length > 1) {
        const phrase = us.join(' ');
        const k = ['t', 'k', 'l', 'h'].find((x) => ch[x].includes(phrase));
        const s = k ? WEIGHT[k] * 2 : (` ${ch.b} `.includes(` ${us.join('_')} `) ? 2 : 0);
        if (s > best) { best = s; where = k || 'b'; }
        continue;
      }
      let total = 0; let field = '';
      for (const u of us) {
        const [s, f] = scoreUnit(u, ch);
        if (!s) { total = 0; break; }
        total += s; field = field || f;
      }
      if (us.length > 1 && total) {
        // the words side by side, as typed
        const phrase = us.join(' ');
        const k = ['t', 'k', 'l', 'h'].find((x) => ch[x].includes(phrase));
        if (k) { total += WEIGHT[k]; field = k; } else if (` ${ch.b} `.includes(` ${us.join('_')} `)) total += 2;
      }
      if (total > best) { best = total; where = field; }
    }
    return [best, where];
  }
  function expand(query, syn) {
    let rest = ` ${fold(query)} `;
    const raw = ` ${String(query || '').normalize('NFKC')} `;
    const groups = [];
    // every group the query names, longest match first, so "随机梯度下降" is stochastic gradient descent and not
    // gradient descent with "随机" left over
    const found = [];
    for (const group of syn || []) {
      // an entry starting with "=" matches only with its own capitals ("mAP", not "map")
      const exact = group.filter((w) => w.startsWith('=')).map((w) => w.slice(1));
      const words = group.filter((w) => !w.startsWith('=')).map(fold).sort((a, b) => b.length - a.length);
      const cased = exact.find((w) => new RegExp(`(?:^|[^A-Za-z0-9])${escapeRe(w)}(?![A-Za-z0-9])`).test(raw));
      const hit = cased ? fold(cased) : words.find((w) => (HAN.test(w) ? rest.includes(w) : latinRe(w).test(rest)));
      if (hit) found.push({ words, hit });
    }
    found.sort((a, b) => b.hit.length - a.hit.length);
    for (const { words, hit } of found) {
      const present = HAN.test(hit) ? rest.includes(hit) : latinRe(hit).test(rest);
      if (!present) continue;
      groups.push({ alts: words, synonym: true });
      rest = rest.replace(HAN.test(hit) ? hit : latinRe(hit), ' ');
    }
    for (const u of units(rest.trim())) groups.push({ alts: [u], synonym: false });
    return groups;
  }
  /* titles and bodies are stored folded; terms, openings and headings keep their case for display, so they are
     folded once here and searched through this copy */
  const folded = (index) => {
    if (!index.folded) index.folded = index.chapters.map((ch) => ({ ...ch, k: fold(ch.k), l: fold(ch.l), h: fold(ch.h) }));
    return index.folded;
  };
  function search(index, query, limit = 40) {
    const groups = expand(query, index.syn);
    if (!groups.length) return [];
    // the whole query, as typed, found side by side counts extra too ("try catch", "for loop")
    const whole = units(fold(query));
    const phrase = whole.length > 1 ? whole.join(' ') : '';
    const hits = [];
    folded(index).forEach((ch, order) => {
      let score = 0; let where = '';
      for (const g of groups) {
        const [s, w] = scoreAlternatives(g.alts, ch, g.synonym);
        if (!s) return;
        score += s; where = where || w;
      }
      if (phrase) {
        const k = ['t', 'k', 'l', 'h'].find((x) => ch[x].includes(phrase));
        if (k) score += WEIGHT[k]; else if (` ${ch.b} `.includes(` ${whole.join('_')} `)) score += 2;
      }
      hits.push({ c: ch.c, i: ch.i, n: ch.n, score, where, order });
    });
    return hits.sort((a, b) => b.score - a.score || a.order - b.order).slice(0, limit);
  }
  /* a short reason to show under a hit: the defined term, heading or opening words where the query was found */
  function snippet(index, hit, query, lang) {
    const ch = index.chapters.find((x) => x.c === hit.c && x.i === hit.i);
    if (!ch || !hit.where || hit.where === 't' || hit.where === 'b') return '';
    const alts = expand(query, index.syn).flatMap((g) => g.alts);
    const parts = hit.where === 'l' ? ch.l.split(/(?<=[.。!?！？])\s*/) : ch[hit.where].split(' · ');
    const inLang = (p) => (lang === 'zh' ? HAN.test(p) : !HAN.test(p));
    const has = (p) => alts.some((a) => units(a).every((u) => found(u, p)[0]));
    const best = parts.find((p) => has(fold(p)) && inLang(p)) || parts.find((p) => has(fold(p))) || '';
    return best.length > 90 ? `${best.slice(0, 88)}…` : best;
  }
  root.LeonFind = { search, snippet, fold };
  if (typeof module === 'object' && module.exports) module.exports = root.LeonFind;
})(typeof window !== 'undefined' ? window : globalThis);
