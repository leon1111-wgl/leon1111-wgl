# Learner walk (November 2026)

Four readers each try one real task on the built site, at desktop width and at 375 px, in the dark and the light theme. The walk is `scripts/learner_walk.mjs`. It runs in CI on every `teaching-*` branch and pull request, saves a screenshot of every step, and records timings. Each friction point it found is now a check in the same script, so the walk fails if that friction comes back.

| Reader | Language | Task |
| --- | --- | --- |
| Has never programmed | Chinese | Pick a goal, run the first program, make a typo and run it again, come back the next day |
| Exam in COMP2123 | Chinese | Sit the diagnostic paper, revise the weakest chapter, follow an algorithm step by step, look terms up, check progress |
| Writes C by hand | English | Answer a question by keyboard only, then type a written answer in and run its tests |
| At work | English | Look something up from the homepage and the hub, open the heaviest chapter on a phone, open a lab |

## What the walk found

Measured on the release before this one: CI run 43480146985, commit d8e9b13, which added the walk and nothing else. Each reader ran in all four width and theme combinations, so a friction point fails four times for each reader it affects.

| Check | Friction found | Readers whose walk hit it | Failing runs | Severity | Now |
| --- | --- | --- | --- | --- | --- |
| W2 | Search matched chapter titles and a few defined terms only. 18 of the 21 lookups the readers typed found nothing or the wrong chapter: "二分查找", "时间复杂度", "shortest path", "segfault" and "race condition" found nothing. "RAG" found the Java arrays chapter, because "storage" contains "rag". The homepage search found nothing for "race condition". | exam, engineer | 12 | High: a chapter that exists cannot be reached | Fixed |
| W5 | A failed run showed only the raw message. A beginner's typo in the first Python program gave an English traceback and no explanation. A C compile error in paper coding said "did not compile" and nothing more. | zero, paper | 8 | High for a beginner: it stops the first lesson | Fixed |
| W1 | Back on the hub the next day, the route's next step was three clicks away: enter, the route banner, then the step. | zero | 4 | Medium | Fixed |
| W3 | Chapters ask questions, but only as folded answers. Nothing marked an answer inside a chapter; marking happened only on the hub's practice pages. | exam | 4 | Medium | Fixed |
| W4 | All 136 trace tables were static. Only 9 chapters had step-through diagrams. | exam | 4 | Medium | Fixed |
| W7 | My learning listed last read, starred and recent courses. Route progress, review due and practice scores were on three other pages. | exam | 4 | Low to medium | Fixed |
| W6 | Keyboard: a multiple-choice question could be answered by keyboard alone, and focus moved to the mark, so it was announced. axe-core found one serious problem: in light, the "← All courses" chip on the guide pages was 4.10:1, under the AA level of 4.5:1. | engineer | 2 (light only) | Low | Fixed |
| W8 | The heaviest chapter page (COMP2017, about 30,700 elements and 1 MB of HTML) was readable, with its Run buttons in place, in 0.24 to 0.29 s at desktop and 1.09 to 1.26 s at 375 px with the CPU slowed 4 times. | engineer | 0 | Not a friction by this measure | Unchanged, timings recorded |

Ranking: by the number of readers whose walk hit the friction, then by severity. W2 and W5 each stopped two readers. The other five each affected one. The remaining candidate, slow heavy pages, was measured and not found.

## What changed for each

- **W2 search.** `scripts/build_search.py` writes `site/learn/data/search.json` (219 KB gzipped), which records what every chapter teaches in both languages: titles, defined terms, the opening sentence of its principle, the titles of its worked problems and programs, and its most distinctive terms. `site/assets/find.js` ranks chapters by where a word is found. Short words such as IoU and RAG must match a whole word. Plurals match. Chinese is matched as typed, or by its two-character pieces. Synonym groups map what readers type to what chapters say ("二分查找" to "二分搜索", "segfault" to "segmentation fault"). Each group holds only true synonyms. Nine chapters also carry the names readers use for them, such as "time complexity" for the chapter on growth and correctness, and each of those names was checked against the chapter's text. Each hit says where it matched: a defined term, the chapter's opening, or a worked problem. The hub and the homepage share the index. The file loads with the first search, and until it arrives the old title search still works.
- **W5 errors explained.** `site/assets/runner/explain.js` reads what the three browser runners print and explains the common errors in Chinese or English: the line, what usually causes the error, and what to try. Python has 20 rules, from NameError (with Python's own "did you mean") to IndentationError and AssertionError. C has 14, including a missing semicolon, which the compiler reports on the next line, and the header to `#include` for 66 library names. Java has 9. The Java runner now names the file an error is in, so a name the tests call but the answer lacks is reported as that, not as a line of the answer. When the runner cannot say which Java exception occurred, the explanation says so and names the usual two. The raw message stays below the explanation. In paper coding, an error in the appended tests says whether the reader's code ran or did not compile. `scripts/test_explain.mjs` checks these against messages captured from the real runners.
- **W1 resume.** The hub's front page shows the route's next step, one click away, and today's review count.
- **W3 in-chapter checks.** Every chapter of the five courses and the five AI guides (208 chapters) now asks one question in the middle of the chapter, after its first worked problem or program, and marks it at once.
  - 81 are authored multiple-choice questions. A wrong choice shows why that choice is wrong, as a hint, and the reader tries again.
  - 42 are numeric. A wrong answer shows the first step of the solution.
  - 60 ask the reader to predict a program's output before unfolding it. The first wrong line is pointed out.
  - 25 ask the reader to recall the answer to one of the chapter's questions.

  After a right answer, a second wrong one or "Show the answer", the full solution appears. A miss joins the review queue.
- **W4 trace stepper.** Every trace table with three or more rows (118 of 136) can be stepped through one row at a time, with buttons or the arrow keys. A counter tells a screen reader the step. The table shows every row until the reader asks to step.
- **W7 at a glance.** My learning opens with one panel showing the route (steps done), review (due today and in the queue), the practice score rate per course, and chapters read.
- **W6 contrast.** The chip uses a darker text colour in the light theme on every reading page.

## Limits

- The walk is a script, not a person. It follows the path its author chose. Each check proves one thing a reader can now do, not that every reader will find the page easy.
- The search lookups are 21 queries written for this walk, before the fix. Other wordings can still miss. Concepts the site does not teach, such as the pumping lemma or NP-completeness, correctly find nothing.
- Timings come from GitHub's Ubuntu runner with Chromium. CPU slowdown approximates a phone. It is not one.
- axe-core finds only what it can detect automatically.
- Real iOS Safari and screen readers were not used.
