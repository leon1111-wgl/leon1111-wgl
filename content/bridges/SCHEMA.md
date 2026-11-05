# First-steps and writing-by-hand guides: content/bridges/<id>.json

Short bilingual guides. `scripts/build_bridges.py` renders `site/bridges/<id>.html` and `<id>.zh.html`; `scripts/verify_bridges.py` compiles and runs every example.

The reader may have never programmed. Define every term the first time it appears. No skipped steps. One idea per lesson. Every lesson keeps the same order: plain explanation, worked example, common mistakes, self-check.

```json
{
  "id": "c-first-steps", "course": "comp2017", "kind": "first-steps",
  "title": {"en": "...", "zh": "..."}, "summary": {"en": "...", "zh": "..."},
  "needs": [{"en": "What you need before this: be honest and specific", "zh": "..."}],
  "setup": {
    "intro": {"en": "...", "zh": "..."},
    "systems": [{"name": {"en": "Windows", "zh": "Windows"}, "steps": [{"en": "...", "zh": "..."}], "verify": "gcc --version", "expect": {"en": "what you should see", "zh": "..."}}],
    "errors": [{"symptom": "exact error text", "fix": {"en": "...", "zh": "..."}}]
  },
  "lessons": [{
    "id": "first-program", "title": {"en": "...", "zh": "..."}, "goal": {"en": "After this you can ...", "zh": "..."},
    "plain": {"en": "Plain explanation. Paragraphs separated by blank lines.", "zh": "..."},
    "terms": [{"term": {"en": "compiler", "zh": "编译器"}, "meaning": {"en": "...", "zh": "..."}}],
    "example": {"language": "c", "code": "...", "output": "exact stdout", "walk": {"en": ["..."], "zh": ["..."]}},
    "mistakes": [{"wrong": "code or a command", "why": {"en": "what happens and why", "zh": "..."}, "right": "the fix"}],
    "check": [{"q": {"en": "A question that asks the reader to produce something", "zh": "..."}, "a": {"en": "...", "zh": "..."}}]
  }],
  "next": {"text": {"en": "What to read next", "zh": "..."}, "href": "courses/comp2017.html", "hrefZh": "courses/comp2017.zh.html"}
}
```

- `kind`: `first-steps` or `by-hand`. `setup` is optional; first-steps guides that need a tool should have it, and they should say that examples also run on the page with nothing installed.
- `example` is required in first-steps lessons and optional in by-hand lessons. For C use only `<stdio.h> <stdlib.h> <string.h> <stdint.h> <stdbool.h> <ctype.h> <limits.h> <math.h>`, and for Java a standalone `public class Main` using java.lang and java.util without `printf` or `String.format`, so the Run button works. Code must compile with `clang -std=c11 -Wall -Wextra -Werror -pedantic` or `javac -Xlint:all`.
- `mistakes`: 2 to 4 per lesson, real ones beginners make. `check`: 2 or 3, folded on the page. Prefer "write", "predict", "fix" over "explain".
- Chinese is a full edition: natural complete sentences, not a gloss, same content as English. Keep English sentences short. Use fixed terms.
- Original wording only. Do not copy coursework, slides, textbooks or past papers, and never say what a real exam contains. No real companies; names are Leon, Mia, Emma, Jack, Iris, Noah.
