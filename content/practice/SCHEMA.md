# Practice packs: content/practice/<course>.json

One file per course id (`comp2017`, `info1113`, `comp2123`, `comp2022`, `comp3308`, `python`, `start`, `ml`, `dl`, `vision`, `multimodal`). `scripts/build_study.py` merges it into `site/learn/data/<course>.json`; `scripts/validate_study.py` and `scripts/verify_practice.py` check it.

**Rules for every question**
- Original wording and original questions only. Never copy or paraphrase coursework, slides, past papers or textbooks. Never say or imply what a real exam contains.
- Reader text is `{ "en": ..., "zh": ... }`. Both complete. English: short sentences a beginner can follow. Chinese: natural, full sentences, not telegraphic, not a word-for-word gloss. Use fixed terms consistently.
- Fictional names only where a name is needed (Leon, Mia, Emma, Jack, Iris, Noah). No real companies.
- `topic` must be an existing chapter id of that course. `marks` is a positive integer. Marks should reflect the work: 1 to 2 for a quick choice, 4 to 6 for a short trace or a small function, 8 to 12 for a longer function or a proof.
- Code must print exactly what the question claims. Everything checkable is checked by `scripts/verify_practice.py`.

```json
{ "course": "comp2017", "questions": [ ], "papers": [ ], "labs": [ ] }
```

## Question kinds

All have `id` (lowercase, hyphens, unique, must not start with `p-` or `w-`), `kind`, `topic`, `title`, `marks`. Optional: `minutes`, `language` (`c`, `java`, `python`), `code` (shown as plain text, no highlighting), `prompt`.

**mcq**: `options`: 3 to 5 of `{ "text": {...}, "correct": true, "why": {...} }`. Exactly one correct. `why` on every option says why it is right or wrong. Optional `solution`. Wrong options should be real misconceptions. If the answer depends on running code, add `verify_code`, `verify_language` and `verify_output` (see below).

**numeric**: `prompt`, `answer` (a number), optional `tolerance`, `unit`, and `solution`. **Required:** `verify_code` in Python printing the answer. The checker compares it with `answer`.

**predict**: authored predict-the-output. `code`, `language`, `output` (exact stdout), `walk` `{ "en": [...], "zh": [...] }`. The checker runs `code`.

**trace**: a dry-run table. `code`, `language`, `columns` `{ "en": [...], "zh": [...] }`, `rows` (array of arrays of strings; column 0 is a step label always shown), `given` (optional list of `"row,col"` cells shown filled in), `solution`. Every other cell is a blank the reader fills in, compared after trimming and ignoring case. Keep cell values short and unambiguous: a number or a short token. **Required:** `verify_code`, `verify_language`: an instrumented copy of the program that prints each row as tab-separated cells, including column 0. The checker requires its stdout to equal `rows` exactly.

**write**: paper coding. `language`, `prompt`, `minutes`, `model_code`, `rubric`, `mistakes`, `tests`, `expected`, `wrong_code`, optional `starter`.
- `rubric`: list of `{ "marks": n, "text": {...} }`. Marks must add up to `marks`. Each line is something a reader can tick honestly: "Checks for NULL before dereferencing", not "good style".
- `mistakes`: 3 to 5 real handwriting mistakes in this language for this task, such as a missing semicolon after a struct, `=` for `==`, forgetting `\0`, `length` versus `length()`, off-by-one in `<=`. Bilingual.
- `tests` proves the model answer works, in this language:
  - C: appended to the same file as `model_code`, and contains `int main(void)`. Use only `<stdio.h> <stdlib.h> <string.h> <stdint.h> <stdbool.h> <ctype.h> <limits.h> <assert.h> <math.h>`. No threads, fork or signals. Must compile with `clang -std=c11 -Wall -Wextra -Werror -pedantic`. Put needed `#include`s in `model_code`.
  - Java: `model_code` is the whole `Main.java`, with `public class Main` and no `main` required. `tests` is `Tests.java`: `public class Tests { public static void main(String[] args) {...} }`, calling `Main`. Java 8 syntax. Use only java.lang and java.util; no streams needed; avoid `printf`, `String.format` and `Scanner`.
  - Python: appended to the same namespace. Print results or assert.
- `expected`: exact stdout of the tests with the model answer.
- `wrong_code`: a plausible wrong answer in the same form as `model_code`. The tests must not produce `expected` with it (a crash or failed assert also counts). This proves the tests can tell.
- `starter`: optional text placed in the box when the reader types it in (for Java, the class shell).

**memory**: draw a diagram at a marked line. `language`, `code` (with a comment such as `// HERE` at the moment asked about), `prompt`, `rubric`, `mistakes`, `memory`, and `verify_code`, `verify_output` where values can be shown by printing.
`memory`: `{ "stack": [ { "frame": "main", "vars": [ { "name": "p", "value": "H1", "points": "H1" } ] } ], "heap": [ { "id": "H1 (int[3])", "cells": [ { "name": "[0]", "value": "7" } ] } ], "data": [ { "name": "\"hi\"", "value": "read-only text" } ] }`. Use symbolic labels (H1, H2) rather than addresses.

**short**, **proof**, **design**: written answers, self-marked. `prompt`, optional `code`, `solution` (the full model answer), `rubric`, optional `mistakes`. `design` is: describe an algorithm, argue it is correct, and analyse its running time, and its rubric splits marks across those three.

**bug**: find and fix. `language`, `code` (the buggy program), `prompt`, `solution` (names the bug and why it fails), `rubric`, `mistakes`, `fixed_code`, `tests`, `expected`. Same conventions as write: tests run against `fixed_code` and must print `expected`; run against `code` they must not.

## verify_code

`verify_code` is a complete program in `verify_language` (default `python`). `verify_output` is its exact expected stdout. For numeric and trace, the expected value comes from the question itself instead.

## papers

`{ "id": "mock-a", "type": "diagnostic" | "mock" | "paper", "title": {...}, "minutes": 60, "questions": ["id", ...], "note": {...} }`
- `diagnostic`: about 20 minutes, spans the stages of the course, mostly self-marking kinds with low effort, used to find weak chapters.
- `mock`: a longer timed paper of mixed kinds.
- `paper`: only `trace`, `memory`, `write` and `bug`, for writing by hand.
Papers may use the derived questions too. Marks and minutes should be realistic: about 1 mark a minute. The `note` says plainly that it is an original practice paper and not a guide to any real exam's format.

Do not write `labs` here unless asked: they have their own schema.
