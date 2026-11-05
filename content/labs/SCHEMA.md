# Engineering labs: content/labs/<id>/

A lab is a realistic small job with real tools. Layout: `lab.json`, `files/` (everything the lab starts from, copied to a temporary folder), and `captured.json`, written by `scripts/verify_labs.py --write` in CI. The page shows real captured output, so never type output by hand.

```json
{
  "id": "c-asan-overflow", "course": "comp2017", "minutes": 30, "tools": ["clang", "AddressSanitizer"],
  "title": {"en": "...", "zh": "..."}, "summary": {"en": "One line", "zh": "..."},
  "scenario": {"en": "The job, as a colleague would describe it. Paragraphs.", "zh": "..."},
  "show": ["copy_line.c"],
  "steps": [
    {"title": {"en": "...", "zh": "..."}, "body": {"en": "What to do and why; what to look for in the output.", "zh": "..."},
     "command": "clang -std=c11 -g -fsanitize=address copy_line.c -o demo && ./demo", "exit": 1,
     "contains": ["heap-buffer-overflow"], "lines": 30,
     "patch": {"file": "copy_line.c", "from": "text in the file", "to": "replacement"}}
  ],
  "review": [{"en": "A code review checklist line for this kind of change", "zh": "..."}],
  "tradeoffs": {"en": "Production trade-offs, with the cost of each choice. Paragraphs.", "zh": "..."},
  "done": [{"en": "Done when ...", "zh": "..."}]
}
```

- Steps run in order, in one temporary folder, with `bash -c`. `patch` is applied before the step's command (this is how the fix is shown); `command` is optional. `exit` is the expected exit code (default 0). `contains` lists strings that must appear in the combined stdout and stderr; choose stable text, since output is compared loosely. `lines` limits what the page shows (default 40).
- Output is normalised: hex addresses become 0xADDR, process ids in `==1234==` become `==PID==`, the temporary folder becomes `.`.
- Tools available in CI (Ubuntu 24.04): clang, gcc, make, gdb, valgrind; Java 8 `javac` and `java`, with `$LAB_TOOLS/junit.jar` (JUnit 5 console standalone), `$LAB_TOOLS/jacocoagent.jar`, `$LAB_TOOLS/jacococli.jar`; python3 with pytest, ruff, numpy, scipy, pandas, scikit-learn. No network in steps. Anything else must be written into `files/`.
- The lab must be deterministic: fixed seeds, fabricated small data. Timings vary, so never assert on exact times; state ratios qualitatively and let `contains` check structure only.
- Reader text is bilingual, plain and specific. Explain each tool option the first time it appears. Treat the reader as a working engineer: no toy framing, name real trade-offs, say what the tool cannot catch.
- All code and data are original and fabricated. No real companies; names are Leon, Mia, Emma, Jack, Iris, Noah.
