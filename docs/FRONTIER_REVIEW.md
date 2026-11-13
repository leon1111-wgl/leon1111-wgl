# Teaching: frontier review (November 2026)

What current research and leading tools suggest for this learning site, what was adopted, what was skipped and why. Written for the four readers the site now serves: someone who has never programmed, a student cramming for an exam, someone who must write code by hand, and a working engineer.

Each adopted item has a check that fails without it. Where I read only an abstract or a secondary summary, the entry says so.

## Decisions

| Candidate | Decision | Why | How it is checked |
| --- | --- | --- | --- |
| Spaced review with a modern scheduler (FSRS-6) | **Adopt** | Spaced practice and practice testing lead both major reviews of study techniques. FSRS is the open reference scheduler. | `scripts/verify_fsrs.py` compares every stability, difficulty and interval with py-fsrs 6.3.2 |
| Attempt before seeing the answer | **Adopt** | Generating an answer first helps later learning, and rereading is among the weakest strategies. The audit found 509 answers printed beside their questions. | Answers fold by default; `scripts/test_study.mjs` asserts they start closed |
| Read and trace before writing | **Adopt** | A controlled study of an explicit sequence (read semantics, write semantics, read templates, write templates) improved completion and post-test results. | Predict-the-output drills check against outputs from `scripts/verify_examples.py`; trace tables must equal the output of an instrumented program (`scripts/verify_practice.py`) |
| Marked practice with rubrics and timed mock papers | **Adopt** | Testing with feedback transfers better than rereading, and rubrics show a moderate effect on performance. | `scripts/validate_study.py` adds up rubric marks; `scripts/verify_practice.py` runs every model answer against its tests and checks those tests fail on a wrong answer |
| C and Java running in the browser | **Adopt** xcc's wcc and TeaVM's javac | A free, self-hosted route exists: under 0.5 MB for C and about 7 MB for Java, with nothing sent to a server. | `scripts/verify_browser_runners.mjs` runs every example through the real runner; a Run button appears only on those that match |
| A chapter at a time on phones | **Adopt** | One course page measured 424 screens at 375 px. Long unbroken pages lose the reader's place. | `scripts/test_study.mjs` asserts one visible chapter and no sideways scroll at 375 px |
| Faded Parsons problems | **Skip for now** | Good evidence as a scaffold for writing, and students like them. But paper coding is the skill at stake here, and tracing plus rubric-marked writing already covers it. Worth revisiting. | n/a |
| Knowledge tracing (BKT, DKT) | **Skip** | These need many learners' data and a server. A score rate per chapter gives this site's reader the same decision: what to revise next. | n/a |
| A tutor running on a small browser model | **Skip** | Trust is the blocker. See below. | n/a |
| Full LLVM in the browser, CheerpJ, remote judges | **Skip** | See below. | n/a |

## Added after the learner walk (November 2026)

The walk in `docs/LEARNER_WALK.md` found where real tasks stalled. Four changes rest on evidence, so they are recorded here.

| Change | Decision | Evidence and its limits | How it is checked |
| --- | --- | --- | --- |
| Failed runs explained in plain words | **Adopt, with the raw message kept** | The evidence is mixed. Becker (SIGCSE 2016) gave CS1 students enhanced Java compiler messages and found fewer errors and fewer repeated errors overall, with eight specific messages showing a significant effect. Denny, Luxton-Reilly and Carpenter (ITiCSE 2014) ran a controlled study of enhanced syntax-error messages and found no significant effect. So the explanations stay short and name the line, the original message stays visible beside them, and the site does not claim they speed learning. | Learner walk W5 |
| A marked question in the middle of each chapter, with a hint before the answer | **Adopt** | This is practice testing with feedback, the technique the reviews above rate highest, plus attempt-first. The hint is the reason a chosen wrong option is wrong, so the reader tries again before seeing the solution. | Learner walk W3; `scripts/validate_study.py` requires a check for every chapter |
| Step-through for every trace table | **Adopt** | Step-by-step execution, as in Python Tutor and the site's own diagrams, now reaches the 118 trace tables with three or more rows, which were static. No new research claim. | Learner walk W4 |
| Search by what a chapter teaches | **Adopt** | Not a learning-science claim. It is a usability fix, measured on 21 lookups the walk's readers typed. | Learner walk W2 |
| A tutor running on a small browser model | **Still skipped** | The reasons below are unchanged. | n/a |

## Learning science

**Spacing and testing.** Dunlosky et al. (2013) rated practice testing and distributed practice the only two high-utility techniques of ten, and rated rereading, highlighting and summarising low. Donoghue and Hattie's 2021 meta-analysis of the same ten techniques (242 studies, 169,179 participants) again found distributed practice and practice testing most effective. A 2024 field study of spaced quizzing across nine STEM courses is a useful caution: the benefit was not uniform, and the pooled spacing effect disappeared once calculus was excluded (read as an abstract). So the queue is offered as a habit, and the site does not promise exam gains.

**Attempt first.** Sinha and Kapur's 2021 meta-analysis (53 studies) found problem solving before instruction gave a moderate advantage over instruction first (g = 0.36), with weaker or reversed results for young children and general skills. I read the abstract and summaries. This supports folding answers rather than removing explanations: the reader tries, then reads.

**Worked examples and novices.** Worked examples beat problem solving for novices and lose that edge as expertise grows (the expertise reversal effect; Sweller and Cooper 1985; Kalyuga and colleagues). So beginners get the plain explanation and worked example first and try afterwards. Engineers can skip to labs. One 2013 study of less structured legal reasoning did not find the reversal, so this is a default, not a law.

**Reading before writing.** Xie et al. (2019) taught four skills in order: reading semantics (tracing), writing semantics, reading templates and writing templates. Teaching them explicitly raised exercise completion and lowered post-test errors. This is the order of the paper-coding route. Evidence on Parsons problems is similar in direction: Weinman et al. (CHI 2021) found faded Parsons problems improved writing about as much as writing practice.

**Rubrics.** Panadero et al.'s 2023 meta-analysis found rubrics have a moderate effect on performance after correcting for publication bias (g = 0.45, k = 21). Effects on self-regulation and self-efficacy were small, with intervals including zero. Self-marking therefore uses concrete rubric lines rather than a general "how did you do?".

## Scheduler

FSRS-6 is the version implemented by the reference scheduler py-fsrs (v6.3.2, August 2026) and by ts-fsrs 6. The srs-benchmark project evaluates schedulers on about 727 million reviews from 10,000 Anki users, and lists FSRS-6 with 21 parameters. It also lists a newer FSRS-7 built for fractional intervals. I stayed on FSRS-6 because a day-level queue does not need fractional intervals and a stable reference scheduler exists to test against. The default parameters are medians over that dataset, not fitted to one reader. Personal optimisation would need thousands of a reader's own reviews, which this site will rarely have.

Learning steps are off: a forgotten card returns once in the same round and is then scheduled by the algorithm. This keeps the behaviour identical to py-fsrs with empty learning steps.

## Running C and Java in the browser

| Option | Size | Result on this site's programs | Decision |
| --- | --- | --- | --- |
| xcc's `wcc`, self-hosted as WebAssembly (MIT) | 0.46 MB uncompressed | 50 of 77 C programs, each compiled and run in milliseconds. Most of the rest use processes, threads, signals or sockets, which a browser cannot provide; two need library parts this libc lacks | **Adopted** |
| `@yowasp/clang` (ISC) | 105 MB | Not tested; too heavy for a Run button on a phone | Skipped |
| teavm-javac, self-hosted (Apache-2.0, with OpenJDK javac under GPLv2+CE) | about 7 MB | 65 of 67 Java programs after building from the current source. The public playground build got 43 of the first 49: `getMessage` was missing and bounds errors were uncatchable | **Adopted** |
| CheerpJ | Hosted runtime | A full JVM, and free for personal and educational use, but the runtime is only served by its vendor and it requires a much larger first load | Skipped; the best fallback if TeaVM's reduced library becomes a problem |
| Remote judges (Judge0, Piston, Compiler Explorer) | None | Learners' code would leave the browser, and these depend on third-party rate limits | Skipped |

**Limits the site states next to the button:**
- Browser C does not catch memory errors. Out-of-bounds access and null pointers often go unnoticed, so the C caution points to `-fsanitize=address` on a real machine.
- Browser Java uses a reduced library. Integer division by zero and array store errors stop the program rather than throwing a catchable exception. `Scanner` and `StringJoiner` are small original stand-ins (`scripts/java_shims`).

## A browser-model tutor

Considered and skipped.

- **Evidence on tutors:** Kestin et al. (Scientific Reports, 2025) found an AI tutor beat in-class active learning in one Harvard physics course, but that tutor was given expert step-by-step solutions to prevent errors. Bastani et al. (PNAS, 2025) found that students with unrestricted GPT-4 scored 17% lower once it was removed. A guardrailed tutor avoided that harm but did not improve exam results.
- **Evidence on small models:** Free-form generation from a 0.6B model made unsupported claims in this portfolio's Career Atlas project, so it was restricted there to choosing evidence under a schema. A tutor must explain and correct, which is exactly the free-form task it cannot be trusted with.
- **Cost to a learner:** about 350 MB, about 1.4 GB of GPU memory, and no phones.

Real outputs, verified answers and rubrics are more honest. If a tutor is revisited, it should have a larger model, pre-written solutions as its ground truth, and a measured error rate.

## Leading platforms: what was borrowed

- **Khan Academy:** a clear next step and mastery by skill. Borrowed: route steps and the per-chapter score rate. Not borrowed: accounts.
- **Runestone Academy:** interactive ebooks with code runners, tracing and Parsons problems. Borrowed: tracing and running code inside the text.
- **Python Tutor:** step-by-step visual execution. The site already had step-through diagrams; memory diagrams are now practised, not only shown.
- **Exercism:** tests as the feedback loop for written code. Borrowed: "type it in and run the tests" after paper marking.
- **Anki:** a daily review habit. Borrowed: the rating buttons and FSRS.

## Sources

- Dunlosky et al. 2013, Psychological Science in the Public Interest: [AFT reprint](https://es.aft.org/sites/default/files/dunlosky_0.pdf)
- Donoghue and Hattie 2021, Frontiers in Education: [doi:10.3389/feduc.2021.581216](https://www.doi.org/10.3389/feduc.2021.581216)
- Spaced quizzing across STEM courses, 2024, International Journal of STEM Education: [article](https://link.springer.com/article/10.1186/s40594-024-00468-5)
- Sinha and Kapur 2021, Review of Educational Research: [doi:10.3102/00346543211019105](https://doi.org/10.3102/00346543211019105)
- Xie et al. 2019, Computer Science Education: [PDF](https://faculty.washington.edu/ajko/papers/Xie2019IntroCSTheoryOfInstruction.pdf)
- Weinman et al. 2021, CHI: [PDF](https://acelab.berkeley.edu/wp-content/papercite-data/pdf/parsons-chi2021.pdf)
- Worked-example and expertise reversal, legal reasoning study: [Utrecht University record](https://research-portal.uu.nl/en/publications/the-worked-example-and-expertise-reversal-effect-in-less-structur/)
- Panadero et al. 2023, Educational Psychology Review: [record](https://portalcientifico.uned.es/documentos/657f1b373ea324404509cf90)
- Kestin et al. 2025, Scientific Reports: [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)
- Bastani et al. 2025, PNAS: [abstract](https://econpapers.repec.org/RePEc:nas:journl:v:122:y:2025:p:e2422633122)
- FSRS: [py-fsrs](https://github.com/open-spaced-repetition/py-fsrs), [srs-benchmark](https://github.com/open-spaced-repetition/srs-benchmark), Ye, Su and Cao, KDD 2022 ([record](https://dblp1.uni-trier.de/rec/conf/kdd/YeSC22.html))
- Becker 2016, SIGCSE: [doi:10.1145/2839509.2844584](https://doi.org/10.1145/2839509.2844584)
- Denny, Luxton-Reilly and Carpenter 2014, ITiCSE: [doi:10.1145/2591708.2591748](https://doi.org/10.1145/2591708.2591748)
- Browser compilers: [xcc](https://github.com/tyfkda/xcc), [teavm-javac](https://github.com/konsoletyper/teavm-javac), [CheerpJ licensing](https://cheerpj.com/docs/licensing), [@yowasp/clang](https://github.com/YoWASP/clang)
