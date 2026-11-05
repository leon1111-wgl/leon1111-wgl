/* FSRS-6 scheduling for the review queue, with the published default parameters and no learning steps.
   Checked in CI against the reference scheduler py-fsrs (see scripts/verify_fsrs.py).
   A card is { s: stability in days, d: difficulty 1-10, last: ms, due: ms, reps, lapses }; a new card is null. */
(() => {
  const W = [0.212, 1.2931, 2.3065, 8.2956, 6.4133, 0.8334, 3.0194, 0.001, 1.8722, 0.1666, 0.796, 1.4835, 0.0614, 0.2629, 1.6483, 0.6014, 1.8729, 0.5425, 0.0912, 0.0658, 0.1542];
  const DECAY = -W[20];
  const FACTOR = 0.9 ** (1 / DECAY) - 1;
  const DAY = 86400000;
  const AGAIN = 1, HARD = 2, GOOD = 3, EASY = 4;
  const clampD = (d) => Math.min(Math.max(d, 1), 10);
  const clampS = (s) => Math.max(s, 0.001);
  // Python's round(): exact halves go to the even neighbour
  const roundEven = (x) => { const r = Math.round(x); return Math.abs(x - Math.trunc(x)) === 0.5 && r % 2 !== 0 ? r - 1 : r; };
  const initialD = (rating, clamp) => { const d = W[4] - Math.E ** (W[5] * (rating - 1)) + 1; return clamp ? clampD(d) : d; };
  const retrievability = (card, now) => (1 + FACTOR * Math.max(0, Math.floor((now - card.last) / DAY)) / card.s) ** DECAY;
  const nextD = (d, rating) => {
    const delta = -(W[6] * (rating - 3));
    return clampD(W[7] * initialD(EASY, false) + (1 - W[7]) * (d + ((10 - d) * delta) / 9));
  };
  const shortTermS = (s, rating) => {
    let inc = Math.E ** (W[17] * (rating - 3 + W[18])) * s ** -W[19];
    if (rating >= HARD) inc = Math.max(inc, 1);
    return clampS(s * inc);
  };
  const forgetS = (d, s, r) => Math.min(
    W[11] * d ** -W[12] * ((s + 1) ** W[13] - 1) * Math.E ** ((1 - r) * W[14]),
    s / Math.E ** (W[17] * W[18]),
  );
  const recallS = (d, s, r, rating) => s * (1 + Math.E ** W[8] * (11 - d) * s ** -W[9] * (Math.E ** ((1 - r) * W[10]) - 1)
    * (rating === HARD ? W[15] : 1) * (rating === EASY ? W[16] : 1));
  const intervalDays = (s, retention, maximum) => {
    const days = roundEven((s / FACTOR) * (retention ** (1 / DECAY) - 1));
    return Math.min(Math.max(days, 1), maximum);
  };
  function review(card, rating, now, { retention = 0.9, maximum = 36500 } = {}) {
    let s; let d;
    if (!card) {
      s = clampS(W[rating - 1]);
      d = initialD(rating, true);
    } else {
      const days = Math.floor((now - card.last) / DAY);
      s = days < 1 ? shortTermS(card.s, rating)
        : clampS(rating === AGAIN ? forgetS(card.d, card.s, retrievability(card, now)) : recallS(card.d, card.s, retrievability(card, now), rating));
      d = nextD(card.d, rating);
    }
    const days = intervalDays(s, retention, maximum);
    return { s, d, last: now, due: now + days * DAY, reps: (card?.reps || 0) + 1, lapses: (card?.lapses || 0) + (rating === AGAIN ? 1 : 0), days };
  }
  globalThis.LeonFSRS = { review, retrievability, AGAIN, HARD, GOOD, EASY, DAY };
})();
