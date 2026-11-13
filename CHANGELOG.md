# Changelog

One entry per release. Main is the release: a push to it deploys the public site.

## 2026-11 · Learner walk: search, feedback and full Chinese

A scripted walk of four readers through real tasks found where the hub got in the way. This release fixes what it found and closes the content gaps the teaching release left open. `docs/LEARNER_WALK.md` has the walk, its findings and their ranking.

**What changed**
- Learner walk: `scripts/learner_walk.mjs` takes four readers through a real task each, at desktop and 375 px, in dark and light. The readers are someone who has never programmed, an exam taker, someone writing C by hand, and an engineer. CI saves every step as a screenshot. Each friction point it found is a check, so it fails if that friction returns.
- Search finds chapters by what they teach, on the hub and the homepage. On the walk's 21 lookups, 18 had found nothing or the wrong chapter. Examples: 二分查找, 时间复杂度, segfault, race condition, and RAG, which found the Java arrays chapter. Each hit says where it matched.
- A failed run is explained in plain Chinese or English: the line, the usual cause, and what to try, above the raw message. This covers Python, C and Java in reading pages and paper coding. The Java runner now says whether an error is in the reader's code or in the tests.
- Every chapter of the five courses and five AI guides (208) asks one question in the middle, marked at once. A wrong choice gets a hint (why that choice is wrong) and another try; the full answer comes after. The mix is 81 multiple choice, 42 numeric, 60 predict-the-output and 25 recall. A miss joins the review queue.
- Trace tables (118 of the 136 have three or more rows) can be stepped through one row at a time, by button or arrow key.
- The hub's front page shows the next step of your route, one click away, and today's review. My learning opens with route, review, practice score and chapters read in one panel.
- In light, the "← All courses" chip on guide pages had too little contrast. axe-core found it; it is fixed.
- Chinese: every chapter of COMP2022, COMP2123, COMP3308, COMP2017 and INFO1113 (136) now carries the full English text, in full sentences. 121 chapters were rewritten. Measured as Chinese characters over English characters of reader prose, the course means rose from 0.28–0.34 to 0.40–0.41. `scripts/zh_depth.py check` now fails any chapter below 0.37.
- AI guides: 93 authored questions with worked answers across machine learning, deep learning, vision and multimodal, covering all 64 chapters. There are two papers per guide, a diagnostic and a mock, so their exam route now opens.
- The repeated "use the original calculation" filler in 16 vision and multimodal chapters is replaced. Each one now says what its linked primary source documents and works a fresh example with numbers.
- Corrected 12 stale references in the guides: names not in the story, and analogies that had been removed. Also corrected the Adam "first moments" wording, one Dijkstra trace row that left out a step, and a garbled English sentence in the Dijkstra notes.

**What was checked**
- In CI on the branch: every program, practice answer, guide example, lab and Run button, as before. Also the new checks:
  - `scripts/zh_depth.py check`;
  - `scripts/test_explain.mjs` (13 checks against messages captured from the real runners);
  - the learner walk (80 checks across the four width and theme combinations, including axe-core);
  - the 112 end-to-end checks, now including the four AI exam routes.
- Fails first: the walk ran in CI on a commit that added only the walk (run 43480146985). It failed on all seven friction points it then fixed, and passed on its timing check for heavy pages.
- The 93 new questions run: model answers, verify code and intermediate numbers were compared line by line. Every number in the 16 new practice sections was recomputed with a script.
- One independent read-only review (Fable). It sampled 13 rewritten chapters, 6 new practice sections, the machine-learning pack in full, the vision and multimodal question packs, and the error explanations. It found one P0: the "error is in the tests" note said the code ran when it had not compiled. It found eight P1s: four translation and term problems, three gaps in the error explanations and one unlinked source. All are fixed, the explanations with tests that fail on the old logic. Of fifteen P2s, thirteen were fixed in full and two in part; what remains is listed below.
- By eye, from the walk's screenshots: the quick check, trace stepper, explained errors, resume link, search reasons and at-a-glance panel at desktop and 375 px.

**What was left out**
- Heavy pages were measured, not changed. The heaviest chapter was readable in 0.24–0.29 s at desktop and 1.09–1.26 s with the CPU slowed four times. Its page still has about 30,700 elements.
- The Chinese prose of the four AI guides was not measured or deepened. Parts of the multimodal guide read as notes, not sentences.
- From the review: its note on comma placement in the COMP2123 and COMP3308 Chinese was not applied. The MuRAG "top 4" claim in one multimodal practice section was taken from the paper but not rechecked. One multimodal topic still lists a source its text does not use.
- C programs that crash at run time get the general explanation, not a specific one.
- Search is measured on 21 lookups written for the walk. Other wordings can still miss. Topics the site does not teach, such as the pumping lemma, find nothing.
- Not tested: real iOS Safari, real phones, and screen readers. Keyboard paths and announcements are checked by script only.

## 2026-11 · Both themes at both widths

**What changed**
- The reader flows now run in dark and light at desktop and 375 px. Each flow fails on a page error, a console error, sideways scroll or the wrong theme.
- A new check measures text contrast on the main pages in those four combinations.
- Fixed what these and a look at the pages found. On phones, the "What to revise" heading was squeezed onto three lines, and page text showed faintly through the top bar, tab bar and paper timer. In light, the ✕ on marked answers, the "Watch out." label and the counts on the homepage filters were below the WCAG AA contrast levels.
- Route checks now run in English and Chinese. They had been running in Chinese by accident.
- Corrected the "By hand" line in the teaching entry below, which claimed more than was done.

**What was checked**
- Automated in dark and light at desktop and 375 px: every reader flow in `scripts/test_study.mjs`, in Chromium. That covers routes, labs, guides, defined words, backup, predict-the-output, multiple choice, trace tables, paper coding, a whole mock paper, review, search, reading pages with C and Java runs, the homepage search and failed loads.
- Contrast, in the same four combinations: goal picker, route, practice, an answered question, a mock paper and its result, review and a review card, a lab, a reading page with a Run result, a guide and the homepage, with chapters revealed and answers open.
- Automated in fewer combinations: the phone chapter view and phone layouts at 375 px in both themes; blocked storage at 375 px in dark; homepage links at desktop in dark.
- By hand, from screenshots of the route, practice, an answered question, a mock paper and its result, review, a review card and a reading page with a Run result: dark at desktop and 375 px, and light at 375 px.

**What was left out**
- Text over a gradient or image is not measured, so it was only looked at where those pages show it.
- Light at desktop was checked by the automated flows and contrast only, not by eye.
- Real iOS Safari and other real phones are still not tested.

## 2026-11 · Phone fixes

**What changed**
- Icons on the goal picker and course lists stay square on phones.
- Score rows on mock paper results and "What to revise" now read the same way on phones: chapter and score, then the bar, then the links, with each link's text inside its button.
- The Python practice page now says 42 review cards, matching the review page. Its 42 practice questions are its deck, and adding them gives 42 cards, so the "0" was the mistake.

**What was checked:** new checks at 375 px in `scripts/test_study.mjs` for all three, each seen failing before the fix; the full CI gate on the branch; the live site after deploy.

**What was left out:** nothing from this list.

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
- Themes at this release: the end-to-end checks ran in dark at desktop and 375 px, and only the hub intro also ran in light. The "Both themes at both widths" entry above extends them.
- By hand at this release: the goal route and a paper question at desktop in dark; a memory question, a lab and a guide at 375 px in light; the live goal picker at desktop. An independent reader sampled questions, guides, chapters and labs in both languages.

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
