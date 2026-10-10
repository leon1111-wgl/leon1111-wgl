# Delivery verification

## Guided teaching extensions — 11 October 2026

This release adds 23 original guided cases in English and Chinese: three each for INFO1113, COMP2017, COMP2123, COMP2022 and COMP3308, plus two each for machine learning, deep learning, computer vision and multimodal learning. Each case includes a story, complete executable source, expected output, execution guidance, explained assumptions and an answered question. Nine new worked problems add explicit calculations and checks. Clickable case routes appear after the opening learning map, with separate prerequisite links; the homepage and GitHub profile expose the new index. Downloaded Markdown includes the same case anchors.

The existing 121 foundational topics and 72 bilingual AI/primer topics retain their original explanations and examples. The foundation totals are now 171 programs, 131 worked problems and 242 instructor insights. All 251 exported standalone programs passed fresh isolated compilation or execution and exact-output checks: 145 Python, 49 Java and 57 C. All 502 rendered code blocks and both example ZIP archives preserve source content. Navigation, bilingual case targets, opening roadmaps and publication-scope checks pass for all 38 HTML pages. Execution used Python 3.12.14, JDK 8 and Apple Clang on macOS.

Independent author checks compare 210 knapsack cases with exhaustive subsets, 120 Bellman–Ford graphs with Floyd–Warshall, 50 obstacle grids with distance relaxation, and 50 DFA pairs with word enumeration. Further checks cover 13 Catalan values, explicit parse trees, all 64 small finite relations, 100 A* cases against all-pairs distances, classification counts, log-space Bayes, validation costs, cross-entropy shift invariance and gradient finite differences. Vision checks include 100 coordinate round trips and 50 segmentation masks compared with set operations. Multimodal checks include 100 timestamp matches against linear search and retrieval edge cases. The three new C examples also passed ASan/UBSan with the shown inputs. These are finite checks, not proofs over arbitrary inputs; no Linux run or leak-detection coverage is claimed.

Source-preservation checks confirm that previous topic IDs, core explanations, program source/output, worked problems and references remain intact. The COMP2017 coverage summary updates its program count from 54 to 57. The biography, beginner primer, original C project sources, supplied Python handbook, handbook ZIP and all compact PDFs are unchanged. Primary references were added for the relevant concepts; the stories, synthetic fixtures and teaching implementations are independently written.

Desktop and actual 390-pixel browser checks cover the new course route, Chinese case text, 18px body text and 16px code, without page-level horizontal overflow in the checked views. Same-case language switching was checked after the anchor navigation settled. Nested reading anchors prefer the visible example when it and its parent chapter cover equal viewport areas. Earlier-release evidence below is historical and retains its original counts and dates.

Python handbook and display-name update checked on 7 October 2026. Earlier course execution and editorial evidence below was recorded on 3 October 2026 unless stated otherwise.

## Python handbook and display name

The Chinese Python — Zero to Practice handbook has 19 units, 91 runnable examples, 100 self-study exercises and four complete projects. Its generated portable ZIP contains 329 files. Fresh isolated execution from that ZIP passed 91/91 examples, 100/100 reference solutions and 4/4 project checks. Tests used the bundled Python runtime on macOS in a temporary path containing spaces and Chinese characters. These finite checks do not establish behavior on every Python version or operating system.

The source validator checks all handbook Python files against Python 3.10 syntax, chapter counts, manifests, homepage/profile entries and byte equality between every ZIP entry and the published source. The complete website now has 38 validated HTML pages. The supplied exercise, example and project files remain unchanged; adaptation is limited to the book builder, style and generated presentation files.

The public name is Leon Wang. The site, profile artwork, Markdown, learning maps, code signatures and PDF watermarks were rebuilt with Leon branding and the LW monogram. Existing account URLs, download routes and saved browser preference keys remain stable. All five individual references still contain one page, and their collection contains five pages.

Fresh checks also passed all three existing C workshops and all 456 rendered source comparisons after the branding changes. An archive scan confirmed the new name throughout public text, PDF metadata and downloadable ZIP contents. The Python ZIP rebuild is deterministic. Desktop browser checks confirmed handbook search and deep links, an interactive alias demonstration, progress persistence after reload, light/dark themes and the new homepage entry. All five rebuilt PDF pages were rendered and inspected. The browser did not apply the requested narrow viewport override in this run, so no new phone-sized visual verification is claimed for the imported handbook.

## Teaching coverage

The five computer-science courses preserve all 121 original topic IDs: INFO1113 (23), COMP2017 (24), COMP2123 (26), COMP2022 (24), and COMP3308 (24). Every course has a complete English and Chinese edition. Together they contain 156 standalone programs, 122 original worked problems and 242 topic-specific teaching notes. Every topic includes a glossary and answered guiding questions. The code, expected output and topic anchors agree across languages.

COMP2123 is presented as Algorithm Design and Analysis. Data structures support the algorithms, whose explanations distinguish correctness, time, space and modeling assumptions. Its 52 Python examples preserve all 36 previous code/output pairs and add contrasting methods, traces and boundary cases. INFO1113 has 46 complete Java programs; COMP2017 has 54 C programs. COMP2022 and COMP3308 each have 48 worked problems, with four additional Python demonstrations between them.

The four AI guides each contain 16 topics in English and Chinese, organized into four learning stages. The separate bilingual beginner primer has eight lessons. All 72 bilingual topics have an original story, concept, application, documented practice, formula, symbol explanation, numerical walkthrough, glossary, answered guiding questions, runnable Python with expected output and explanation, two application cases, limitations, takeaway and mapped primary references. Language editions share stable topic anchors.

All 228 exported programs passed compilation or execution with matching output: 128 Python, 46 Java and 54 C. The example checker runs each program in an isolated temporary directory. Python uses Python 3.12.14 and NumPy 2.3.5. Java uses JDK 8; C uses Apple Clang 16 with C11, POSIX thread support and warnings treated as errors. Text comparisons permit one optional final newline; all other whitespace must agree. The five additional named Java illustrations were separately compiled and run.

Independent algorithm checks compare selection with sorted ranks, sorting with Python's reference result, multiplication with integer arithmetic, and range reports with direct filtering. They cover empty inputs, duplicate values, invalid ranks and endpoint cases. These finite checks support the examples; they do not prove correctness for every possible input or make them production implementations.

The previous release independently reviewed its 48 C programs. The six new bridge programs also passed independent strict compilation, AddressSanitizer/UndefinedBehaviorSanitizer and output checks. Additional local checks passed for 24 memory-focused programs under AddressSanitizer/UndefinedBehaviorSanitizer and all 12 pthread programs under ThreadSanitizer. These checks used the fixed tutorial inputs on macOS; ASan leak detection was disabled. They do not establish correctness for all schedules, resource failures or platforms.

## COMP2017 engineering workshops

The course now provides a six-pass plan, 24 chapter-specific coaches and three complete bilingual workshops: streaming log analysis, bounded process-output capture and threaded file statistics. They contain 15 guided milestones and 36 source, build, test, fixture and README files. Each milestone explains the goal, reasoning, actual code extract and answered checkpoint. The guides cover requirements, architecture, ownership, actual runs, debugging, tests, tradeoffs and extensions.

All three projects passed isolated Clang builds with C11, POSIX threads and `-Wall -Wextra -Werror -pedantic`. The log analyzer's 16 tests and process runner's 14 tests pass. The pipeline suite passes its boundary, error, close/drain, startup-failure and repeated-schedule checks, including 48 runs of 37 jobs. All 14 documented run commands match stdout and exit status. Additional author checks passed for the log analyzer under ASan/UBSan and for the pipeline under ThreadSanitizer. All executions were on macOS with Apple Clang 16; no separate Linux execution is claimed. Finite tests do not cover every operating-system failure or thread schedule.

The project validator checks full bilingual fields, source manifests, rendered source and all four project archives. Exported files and ZIP entries preserve raw original bytes, including CRLF and whitespace-only fixtures. Exact source copies appear in both language editions. Original topics, their 48 existing C programs and expected outputs remain intact; six bridge examples precede harder concepts.

Independent integration review identified duplicate milestone anchors, source-section language-switch ambiguity, whitespace normalization in fixtures, and missing Markdown setup guidance. These were corrected. Milestones use a reserved prefix; source files have their own reading anchors; fixture bytes are preserved; both HTML and Markdown provide archive links and explicit Clang, make and Python 3 prerequisites.

## Rendering and navigation

The static validator passed for 37 HTML pages, local links and anchors, Markdown download links, knowledge-map coverage, complete bilingual teaching fields, allowed publication scope and biography wording. Each course and AI guide starts with a clickable learning route. The corresponding Markdown notes use 26 English/Chinese SVG maps, including the new workshop routes. All 456 rendered standalone-code blocks match the original source. Both standalone-example ZIP archives and all four new project ZIP archives match their source files byte for byte.

Five individual PDFs still have one page each; the collection has five pages. Every PDF starts with a compact learning route. All five pages of the rebuilt collection were rendered and visually inspected for clipping, overlap, missing symbols and watermark placement. PDF references remain English; the full web references and notes have both languages.

Browser checks cover desktop and 390-pixel layouts, English and Chinese, dark and light themes, 18px default body text, 21px larger text, 16px/18px code, saved reading preference, same-chapter language switching, copy-button feedback, the collapsible run instructions and chapter navigation. Long code lines scroll within their code panel. No page-level horizontal overflow was observed in the tested views. CSS and JavaScript URLs carry content hashes to refresh changed assets.

GitHub's Markdown rendering API preserves the profile cover, course cards, primer/download links and collapsible catalogue. It also confirms that the generated state-trace tables render as tables. Course counts use native text below the images. Local profile previews are previews of rendered content, not screenshots of the public GitHub page.

## Editorial review and publication boundary

The mathematical review checked the assumptions, intermediate calculations and answers in the new algorithms, computation and AI problems. Examples explain why a method applies and how to check its result. Further-thinking notes discuss alternatives, changed assumptions and links between topics.

Independent integration review found and corrected blank lines that broke Markdown trace tables and overly broad whitespace trimming in output verification. Final link checks also exclude code blocks and code spans, so C function-pointer calls are not mistaken for Markdown links. Earlier reviewed ML, DL, vision, multimodal and primer source content is preserved unchanged in this release.

Primary references include official Python, Java, POSIX, NumPy, Google, scikit-learn, PyTorch, OpenCV, Hugging Face and original research sources. These are independent teaching notes, not official translations or endorsed courses.

Only the reviewed project and `site/` deployment artifact are public. Supplied university slides, assignments, examinations and assessment solutions, the original CV and the private source audit remain outside this repository. The explicitly requested Python handbook includes its own self-study exercises and reference solutions. Published material uses Leon branding. The HKU qualification is MSc, with AI interests; no Computer Science MSc claim is introduced.

The authenticated publishing account is leon1111-wgl. Release verification checks the deployed Git commit and publicly served files after deployment. Current release identifiers are kept in the private release audit, avoiding a self-referential commit hash inside this document.
