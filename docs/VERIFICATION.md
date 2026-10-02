# Delivery verification

Checked on 3 October 2026.

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

Only the reviewed project and `site/` deployment artifact are public. Supplied slides, assignments, examinations, solutions, the original CV and the private source audit remain outside this repository. Published material uses Guoliang branding. The HKU qualification is MSc, with AI interests; no Computer Science MSc claim is introduced.

The authenticated publishing account is leon1111-wgl. Release verification checks the deployed Git commit and publicly served files after deployment. Current release identifiers are kept in the private release audit, avoiding a self-referential commit hash inside this document.
