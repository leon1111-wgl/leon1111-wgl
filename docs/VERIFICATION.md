# Delivery verification

Checked on 3 October 2026.

## Teaching coverage

The five computer-science courses preserve all 121 original topic IDs: INFO1113 (23), COMP2017 (24), COMP2123 (26), COMP2022 (24), and COMP3308 (24). Every course has a complete English and Chinese edition. Together they contain 150 standalone programs, 122 original worked problems and 242 topic-specific teaching notes. Every topic includes a glossary and answered guiding questions. The code, expected output and topic anchors agree across languages.

COMP2123 is presented as Algorithm Design and Analysis. Data structures support the algorithms, whose explanations distinguish correctness, time, space and modeling assumptions. Its 52 Python examples preserve all 36 previous code/output pairs and add contrasting methods, traces and boundary cases. INFO1113 has 46 complete Java programs; COMP2017 has 48 C programs. COMP2022 and COMP3308 each have 48 worked problems, with four additional Python demonstrations between them.

The four AI guides each contain 16 topics in English and Chinese, organized into four learning stages. The separate bilingual beginner primer has eight lessons. All 72 bilingual topics have an original story, concept, application, documented practice, formula, symbol explanation, numerical walkthrough, glossary, answered guiding questions, runnable Python with expected output and explanation, two application cases, limitations, takeaway and mapped primary references. Language editions share stable topic anchors.

All 222 exported programs passed compilation or execution with matching output: 128 Python, 46 Java and 48 C. The example checker runs each program in an isolated temporary directory. Python uses Python 3.12.14 and NumPy 2.3.5. Java uses JDK 8; C uses Apple Clang 16 with C11, POSIX thread support and warnings treated as errors. Text comparisons permit one optional final newline; all other whitespace must agree. The five additional named Java illustrations were separately compiled and run.

Independent algorithm checks compare selection with sorted ranks, sorting with Python's reference result, multiplication with integer arithmetic, and range reports with direct filtering. They cover empty inputs, duplicate values, invalid ranks and endpoint cases. These finite checks support the examples; they do not prove correctness for every possible input or make them production implementations.

Independent C review covered all 48 programs. Additional local checks passed for 24 memory-focused programs under AddressSanitizer/UndefinedBehaviorSanitizer and all 12 pthread programs under ThreadSanitizer. These checks used the fixed tutorial inputs on macOS; ASan leak detection was disabled. They do not establish correctness for all schedules, resource failures or platforms.

## Rendering and navigation

The static validator passed for 31 HTML pages, local links and anchors, Markdown download links, knowledge-map coverage, complete bilingual teaching fields, allowed publication scope and biography wording. Each course and AI guide starts with a clickable learning route. The corresponding Markdown notes use 20 English/Chinese SVG maps. All 444 rendered code blocks match the original source. Both downloadable code ZIP archives match their manifests and source files byte for byte.

Five individual PDFs still have one page each; the collection has five pages. Every PDF starts with a compact learning route. All five pages of the rebuilt collection were rendered and visually inspected for clipping, overlap, missing symbols and watermark placement. PDF references remain English; the full web references and notes have both languages.

Browser checks cover desktop and 390-pixel layouts, English and Chinese, dark and light themes, 18px default body text, 21px larger text, 16px/18px code, saved reading preference, same-chapter language switching, copy-button feedback, the collapsible run instructions and chapter navigation. Long code lines scroll within their code panel. No page-level horizontal overflow was observed in the tested views. CSS and JavaScript URLs carry content hashes to refresh changed assets.

GitHub's Markdown rendering API preserves the profile cover, course cards, primer/download links and collapsible catalogue. It also confirms that the generated state-trace tables render as tables. Course counts use native text below the images. Local profile previews are previews of rendered content, not screenshots of the public GitHub page.

## Editorial review and publication boundary

The mathematical review checked the assumptions, intermediate calculations and answers in the new algorithms, computation and AI problems. Examples explain why a method applies and how to check its result. Further-thinking notes discuss alternatives, changed assumptions and links between topics.

Independent integration review found and corrected blank lines that broke Markdown trace tables and overly broad whitespace trimming in output verification. Final link checks also exclude code blocks and code spans, so C function-pointer calls are not mistaken for Markdown links. Earlier reviewed ML, DL, vision, multimodal and primer source content is preserved unchanged in this release.

Primary references include official Python, Java, POSIX, NumPy, Google, scikit-learn, PyTorch, OpenCV, Hugging Face and original research sources. These are independent teaching notes, not official translations or endorsed courses.

Only the reviewed project and `site/` deployment artifact are public. Supplied slides, assignments, examinations, solutions, the original CV and the private source audit remain outside this repository. Published material uses Guoliang branding. The HKU qualification is MSc, with AI interests; no Computer Science MSc claim is introduced.

The authenticated publishing account is leon1111-wgl. Release verification checks the deployed Git commit and publicly served files after deployment. Current release identifiers are kept in the private release audit, avoiding a self-referential commit hash inside this document.
