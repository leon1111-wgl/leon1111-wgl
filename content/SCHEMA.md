# Leon teaching sources

The five public course codes are INFO1113, COMP2017, COMP2123, COMP2022 and COMP3308. All explanations, stories and worked problems are original. Do not publish supplied assignments, exams, answers, slides, provider branding or business teaching.

## Course editions

`content/CODE.json` is the complete English edition. `content/translations/CODE.zh.json` is the complete Chinese edition with the same structure. Preserve every existing topic ID, map membership, example ID, program source and expected output across editions. Translate all reader-facing prose (reference titles and code comments may remain English). Keep English sentences short and teach a high-school beginner carefully. Chinese is a full edition, not a summary.

Keep existing fields: code, title, subtitle, description, coverage, color, prerequisites, outcomes, map, topics, cheatsheet, references. Map stages may add a `purpose` sentence. A topic keeps id, title, story, principle, formula, symbols, example, pitfall, check. Keep previous good explanations; expand, do not thin them out. Existing checks are original teaching questions, not supplied coursework.

## Detailed teaching blocks

Every topic has at least three glossary entries `{term, meaning}`, three guided_questions `{question, answer}`, and two instructor_notes `{title, body}`. Instructor notes are topic-specific reasoning: why this approach, changed assumptions, alternatives, links to other concepts, or sanity checks. Avoid generic filler and unsupported claims of personal experience. Each body should explain a concrete consequence or example.

`code_examples` entries use:
- id: stable lowercase hyphenated ID
- title, intro, explanation: strings; explanation has multiple short paragraphs
- language: `python`, `java`, or `c` (default python)
- code: complete standalone program; no prompts, network, external files or nondeterministic stdout
- output: exact stdout, English, same in both editions
- walkthrough: at least three strings describing meaningful lines/blocks and their purpose
- trace: `{columns: [string, ...], rows: [[string, ...], ...]}` for a concrete variable/state/execution trace; optional for examples where not helpful
- syntax_notes: optional `[{syntax, meaning}]` for unfamiliar syntax

Java: Java 8 compatible, one standalone file, public class Main, helper classes nested or package-private. C: standalone C11/POSIX source, deterministic bounded execution, use standard headers and safe ownership. C compilation uses `clang -std=c11 -Wall -Wextra -Werror -pedantic -pthread file.c -o demo`. Add `_POSIX_C_SOURCE 200809L` before headers when necessary. Do not rely on Linux-only APIs without replacing them with portable examples. Each Java program downloads into a unique example directory as Main.java. Every new Python example uses standard library unless NumPy is necessary. Preserve old Python examples.

`worked_problems` entries use:
- title, question: strings, with all inputs/assumptions explicit
- strategy: explain how to choose an approach before calculating
- steps: at least three strings; show intermediate substitutions and the reason for each step
- answer: result with interpretation, not just a number
- sanity_check: independent check, boundary case, or condition under which answer changes

Programming courses: aim for at least two complete runnable examples per topic, contrast useful cases rather than tiny duplicates. COMP2123 is **Algorithm Design and Analysis**: algorithms lead, data structures support implementation. Include Python, invariants/proof ideas, complexity, and alternatives. Preserve all 26 IDs and existing 36 Python examples, add a second meaningful example where only one exists (at least 52 total).

COMP2022 and COMP3308: at least two worked_problems per topic, with fully worked original calculations or symbolic reasoning. Explain formulas and each symbol in accessible language. Add meaningful Python demonstrations where useful, without replacing the mathematics with code.

Cheatsheets remain compact. Preserve their existing English text except corrections or the COMP2123 course title/scope, so the existing single-page PDF layout is retained. Chinese cheatsheets translate the compact entries.

## Authoring and verification

Edit JSON sources, then regenerate HTML, Markdown, maps and downloadable programs. Keep source reviews and private authoring helpers outside this public project. Verify arithmetic and run every new program before publication. Use authoritative primary references for technical source checks.

The opening route uses each map stage's title, topic membership and short `purpose` sentence. Preserve the topic IDs so existing links and the language switch keep working. Run `scripts/validate.py`, `scripts/verify_examples.py` and `scripts/validate_exports.py` before publishing.

## Complete engineering workshops

`content/comp2017-path.json` has bilingual `title`/`intro`, six `sessions` (title, goal, existing topic IDs, readiness checkpoint, optional project ID), `deeper` topic IDs, and `coaches` keyed by every course topic. Each coach supplies a simple model, an engineering decision, and an answered checkpoint.

Each `content/projects/comp2017-*.json` describes one independently authored teaching project. Reader prose uses `{en, zh}`. Stable identifiers, source paths, commands, code, expected stdout and reference URLs remain shared. Required fields are id, number, title, summary, difficulty, story, prerequisites (topic/reason), outcomes, requirements (rule/why/check), architecture (nodes/flow/ownership), milestones, runs, debugging, test_plan, design_notes, files, extensions and references.

A milestone has id, title, goal, reasoning, at least three steps, a real source snippet (code/language), snippet_explanation and checkpoint (question/answer). Explain each phase's input, state and visible result. Snippets are labelled extracts; readers compile the complete files. Every file has path, role, unique read_order and at least three walkthrough steps. List all project files, including Makefile, tests, fixtures and both READMEs. No compiled artifacts belong in the manifest.

Runs contain a runtime-only command after the documented build, literal stdout, integer expected_exit, title and explanation. Describe stderr separately. A test case explains case/expected/reason; a debugging case explains symptom/hypothesis/inspection/fix. Design notes explain concrete tradeoffs and limits. Extensions include a plan and acceptance check. Preserve raw fixture bytes through export and archives. Prefer small deterministic fabricated inputs, documented bounds, explicit resource owners and cleanup paths. Never reuse supplied coursework as an example.

## Guided extensions

`learning-extensions.json` groups additions by course code (`INFO1113`, `COMP2017`, `COMP2123`, `COMP2022`, `COMP3308`) or AI guide code (`AI-ML`, `AI-DL`, `AI-CV`, `AI-MM`). Each case contains an existing `topic` ID, an existing code `example` ID, and complete `{en, zh}` values for `title` and `goal`. The manifest is navigation metadata; the lesson JSON remains the source of its teaching text and executable code. Generated case anchors use `lab-{topic}-{example}` in both language editions and their Markdown downloads. Run `scripts/validate_extensions.py` after rebuilding.
