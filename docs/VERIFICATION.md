# Delivery verification

Checked on 3 October 2026.

## Teaching coverage

Five English courses retain their 121 topic IDs: INFO1113 (23), COMP2017 (24), COMP2123 (26), COMP2022 (24), and COMP3308 (24). Their knowledge maps and five one-page PDF references remain available. COMP2123 now has 36 runnable Python examples across all 26 topics, plus 78 defined terms and 78 answered guiding questions. Ten topics have two examples.

The four AI guides each contain 16 topics in English and Chinese, organized into four learning stages. The separate bilingual beginner primer has eight lessons. All 72 bilingual topics have an original story, concept, application, documented practice, formula, symbol explanation, numerical walkthrough, glossary, answered guiding questions, runnable Python with expected output and explanation, two application cases, limitations, takeaway and mapped primary references. Language editions share stable topic anchors.

The 108 exported Python examples run with Python 3.12.14 and NumPy 2.3.5. Every file was executed in an isolated temporary working directory and its printed output matched the lesson. The standard-library examples need no additional packages. No example downloads a dataset or model weights. Data-structure review also checked representative empty inputs, repeated values, missing targets, graph boundaries, AVL subtree preservation, prefix codes and arithmetic against independent results. Passing these checks does not prove correctness for every possible input or make the examples production implementations.

## Rendering and navigation

The static validator checks 21 HTML pages, local links and anchors, Markdown download links, knowledge-map coverage, complete bilingual teaching fields, allowed publication scope and biography wording. Five individual PDFs still have one page each; the collection has five pages. The PDF content is unchanged from the previously rendered and visually inspected edition.

Browser checks cover desktop and 390-pixel layouts, English and Chinese, dark and light themes, 18px default body text, 21px larger text, 16px/18px code, saved reading preference, same-chapter language switching, Python-copy feedback, the collapsible run instructions and chapter navigation. Long code lines scroll within their code panel. No page-level horizontal overflow was observed in the tested views. CSS and JavaScript URLs carry content hashes to refresh changed assets.

GitHub's Markdown rendering API preserves the profile cover, course cards, primer/download links and collapsible catalogue. The cover now uses fewer, larger labels. Course counts use native text below the images. Local profile previews are previews of rendered content, not screenshots of the public GitHub page.

## Editorial review and publication boundary

Independent review checked ML, DL, vision, multimodal, the primer and the rendering/export code. Corrections included a chapter-local residual-sign convention, bird-call translation consistency, a conditional-probability explanation, a matrix example that hid a reset error, attention-dimension wording the scope of a document-row demo, and the identity-matrix definition in the Transformer example. Primary references include official Python, NumPy, Google, scikit-learn, PyTorch, OpenCV, Hugging Face and original research sources. These are independent teaching notes, not official translations or endorsed courses.

Only the reviewed project and `site/` deployment artifact are public. Supplied slides, assignments, examinations, solutions, the original CV and the private source audit remain outside this repository. Published material uses Guoliang branding. The HKU qualification is MSc, with AI interests; no Computer Science MSc claim is introduced.

The authenticated publishing account is leon1111-wgl. Release verification checks the deployed Git commit and publicly served files after deployment. Current release identifiers are kept in the private release audit, avoiding a self-referential commit hash inside this document.
