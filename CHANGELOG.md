# Changelog

One entry per release. Main is the release: a push to it deploys the public site.

## 2026-11 · Teaching for four readers


**What changed**
- Pick a goal (never programmed, exam coming, writing by hand, at work) and get a route of steps that stay ticked.
- Practice for every course: original questions with marks, solutions and rubrics, plus drills drawn from the lessons. Timed mock papers survive a refresh and mark what can be marked automatically.
- Paper-coding mode: attempt first with no running or autocomplete, self-mark against a rubric, then type it in and run the tests.
- Review queue scheduled by FSRS-6. Missed questions join it. Progress can be backed up to a file.
- Python, Java and C run on reading pages where they really work, and a note says when a program needs a real machine.
- First-steps guides for Python, Java, C, algorithms and computation, and writing-by-hand guides for C, Java and Python.
- 15 new chapters closing coverage gaps, including memory diagrams, reductions, topological order and strongly connected components.
- Engineering labs with real tools and the output CI captured from running them.
- Answers fold until asked for. Phones read one chapter at a time. Reading pages offer to resume. Tapping a defined word shows its meaning. Search finds chapters by what they teach.
- Python handbook v1.5 to v1.10 merged from the local working copy.

**What was checked**
- In CI before release: all 285 course programs compile, run and match their pages; 258 authored questions run (model answers pass their tests, wrong answers fail them, trace tables match instrumented programs, calculations match); 48 guide examples; 14 labs with their real tools (ASan, TSan, gdb, valgrind, make, JUnit, JaCoCo, pytest, ruff, scikit-learn); FSRS against py-fsrs on every review; every Run button in Chromium; 47 end-to-end checks at desktop and 375 px, including a whole mock paper across a refresh, blocked storage, failed loads, every route's links, and homepage links.
- By hand: reader flows at desktop and 375 px in both themes. An independent reader sampled questions, guides, chapters and labs in both languages.

**What was left out, and why**
- Older chapters of COMP2022, COMP2123 and COMP3308 are still thin in Chinese. New chapters and practice are full length. This needs its own pass.
- The AI guides have review cards and predict-the-output drills, but no authored questions or mock papers yet. Their exam route is hidden.
- 27 of 77 C programs and 2 of 67 Java programs have no Run button, because they need processes, threads, signals or a library part the browser version lacks. Each says so.
- Browser Java cannot catch division by zero or array store errors, and browser C does not catch memory errors. The pages say so next to the button.
- No browser-model tutor: see `docs/FRONTIER_REVIEW.md`.
- Not tested: real iOS Safari, and the setup steps on real Windows machines. Gradle is not covered by the labs.

## 2026-11 · Homepage (611d4c9)

**What changed:** search across projects and chapters, a start-here panel, project filters, a "Try" line and last-pushed date on each card, DOI link, and a README project grid.

**What was checked:** live site at desktop and 375 px in both themes, README as GitHub renders it.

**What was left out:** the paper's year stays "AAAI 2025" as the owner chose, though the publisher's record says Vol. 40, published March 2026. Pinning repos and social-preview images need the owner.
