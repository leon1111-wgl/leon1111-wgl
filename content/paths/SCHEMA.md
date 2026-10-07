# Bilingual teaching content contract

Each guide has `id`, `code`, `color`, `title`, `subtitle`, `description`, `coverage`, `prerequisites`, `outcomes`, `map`, `topics`, `references` and `review`.

The four subject guides contain 16 topics each. The separate beginner primer contains eight. Every subject guide has four learning stages. Every topic appears once in the knowledge map and has one review card. Keep existing topic IDs stable so bookmarks still work.

All prose is localized as `{"en":"…","zh":"…"}`. Prerequisites and outcomes contain a list for each language. Shared code and mathematical notation are not translated. Publisher names and reference kinds may remain in English.

A topic contains `id`, `title`, `level` (`foundation`, `core`, `applied`, `advanced`), `story`, `concept`, `application`, `practice`, `formula`, `symbols`, `calculation`, `limits`, `takeaway` and `sources`.

Every topic also contains:

- `glossary`: at least three `{term, meaning}` objects.
- `guided_questions`: at least three `{question, answer}` objects, with answers shown.
- `practice_cases`: at least two `{title, body}` applications.
- `code_examples`: at least one `{id, title, intro, code, output, explanation}` object. IDs are lowercase ASCII words separated by hyphens. Code runs without a network connection, using Python's standard library or NumPy. Output must match an actual run.

Teach as if the reader is a high school student. Start with a complete, original story. Define terms before using them. Explain each symbol, its units or shape, and the assumptions behind a formula. Work through small numbers. Explain the code and the output. Ask why a step works and what changes when an input changes. Use short sentences, but retain the reasoning. Word-count targets must not encourage padding.

References contain `id`, localized `title`, verified primary `url`, `publisher` and `kind`. Map every topic to its relevant references. Use at least eight substantive primary pages per guide. Distinguish a tiny mechanism example from a production system. Do not imply endorsement or present the notes as official translations. Stories, examples and commentary are original; do not copy source tutorials, assignments, exams or provider material. The renderer applies Leon branding.

Run `scripts/build.py`, `scripts/validate.py` and `scripts/verify_examples.py` after changes. Structural validation cannot judge teaching quality or prove mathematical correctness; review the prose, arithmetic and source support as well.
