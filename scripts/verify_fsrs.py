#!/usr/bin/env python3
"""Compare site/learn/fsrs.js with the reference FSRS scheduler (py-fsrs), rating by rating.

Needs the `fsrs` package and node on PATH, so it runs in CI. The review queue is only as good as this match.
"""
from datetime import datetime, timedelta, timezone
from pathlib import Path
import json
import random
import subprocess
import tempfile

from fsrs import Card, Rating, Scheduler

ROOT = Path(__file__).resolve().parents[1]
RUNNER = '''
const fs = require('fs');
require(process.argv[2]);
const { review } = globalThis.LeonFSRS;
const seqs = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
console.log(JSON.stringify(seqs.map((seq) => {
  let card = null;
  return seq.map(([rating, at]) => { card = review(card, rating, at); return [card.s, card.d, card.days]; });
})));
'''


def main():
    rng = random.Random(20261105)
    scheduler = Scheduler(learning_steps=(), relearning_steps=(), enable_fuzzing=False)
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    sequences, expected = [], []
    for _ in range(400):
        card = Card()
        now = start
        seq, exp = [], []
        for step in range(rng.randint(1, 12)):
            rating = rng.choice([1, 2, 3, 3, 3, 4])
            # mostly on the due date, sometimes early (same day) or late
            if step:
                now = card.due + timedelta(days=rng.choice([0, 0, 0, -1, 2, 7]), hours=rng.randint(0, 5))
                now = max(now, card.last_review + timedelta(hours=rng.randint(1, 3)))
            card, _ = scheduler.review_card(card, Rating(rating), review_datetime=now)
            seq.append([rating, int(now.timestamp() * 1000)])
            exp.append([card.stability, card.difficulty, (card.due - now).days])
        sequences.append(seq)
        expected.append(exp)
    with tempfile.TemporaryDirectory() as tmp:
        data = Path(tmp) / 'seqs.json'
        data.write_text(json.dumps(sequences))
        script = Path(tmp) / 'run.js'
        script.write_text(RUNNER)
        out = subprocess.run(['node', str(script), str(ROOT / 'site/learn/fsrs.js'), str(data)], capture_output=True, text=True, check=True).stdout
    actual = json.loads(out)
    checked = 0
    for i, (want_seq, got_seq) in enumerate(zip(expected, actual)):
        for j, (want, got) in enumerate(zip(want_seq, got_seq)):
            checked += 1
            if abs(want[0] - got[0]) > 1e-6 * max(1, abs(want[0])) or abs(want[1] - got[1]) > 1e-6 or want[2] != got[2]:
                raise SystemExit(f'sequence {i} step {j}: reference {want}, site {got}, ratings {sequences[i][:j + 1]}')
    print(f'PASS: FSRS matches py-fsrs on {checked} reviews in {len(expected)} sequences')


if __name__ == '__main__':
    main()
