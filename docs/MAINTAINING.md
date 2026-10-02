# Maintaining the profile and learning library

The personal homepage is English. All five foundational courses, four AI field guides and the eight-lesson beginner primer provide complete English and Chinese editions with a language switch. The five original learning paths are INFO1113, COMP2017, COMP2123, COMP2022 and COMP3308. Business courses, raw slides, examinations and assignment solutions are excluded. The notes explain concepts using independently written stories and examples.

## Files

- `README.md`: personal-first GitHub profile with a clickable website cover, course portals and a collapsible catalogue of direct teaching-page links.
- `site/`: complete static website; upload only this directory as the Pages artifact.
- `content/profile.json`: factual biography and GitHub URL.
- `content/COURSE.json`: complete English course text, knowledge map and compact reference.
- `content/translations/COURSE.zh.json`: complete Chinese edition with the same topic IDs and runnable source.
- `scripts/build_courses.py`: render both course editions, web references and Markdown.
- `scripts/roadmaps.py`: opening HTML route diagrams and SVG maps for downloaded notes.
- `content/paths/*.json`: 16 bilingual topics, a framework, a review and primary references for each AI guide.
- `content/primer.json`: beginner lessons in Python and the mathematics used by the guides.
- `scripts/teaching.py`: glossary, guided questions, runnable examples, download archive and asset versioning.
- `scripts/verify_examples.py`: compile/run every exported Python, Java and C file and compare its actual output.
- `scripts/validate_exports.py`: check that HTML copy text and both ZIP archives match the source.
- `scripts/build_paths.py`: generate the bilingual pages and complete Markdown downloads.
- `notes/`: readable Markdown versions for GitHub.
- `profile/bio.txt`: concise GitHub account biography.
- `scripts/build.py`: generate HTML, Markdown and the profile README.
- `scripts/build_profile.py`: generate the GitHub-compatible profile artwork and README; rebuild after editing.
- `scripts/build_pdfs.py`: generate watermarked one-page PDFs and the five-page collection.
- `scripts/validate.py`: validate local navigation, course scope and PDF structure.

The supplied source PDFs and extraction audit remain outside this project. Do not copy the parent directory into a public repository.

## Preview

Run `python3 -m http.server 8765 --directory site` from this project, then open `http://localhost:8765`.
The built website is plain HTML, CSS and JavaScript. It has no analytics, account system, build service dependency, remote fonts, or browser framework. Course content and navigation remain available without JavaScript.

## Rebuild

Use Python 3 with the packages in `requirements.txt`. Pygments performs syntax highlighting during the build; the website needs no external scripts. Full example verification also needs a JDK 8+ and a C11 compiler on a POSIX system:

```sh
python3 scripts/build.py
python3 scripts/build_pdfs.py
python3 scripts/validate.py
python3 scripts/verify_examples.py
python3 scripts/validate_exports.py
```

Portable fonts are bundled in `scripts/fonts/` with their license. PDF generation stops if the text cannot fit at a readable size. Edit overly long reference blocks instead of shrinking them indefinitely.

## Publish on GitHub

1. Set `github` in `content/profile.json` to the verified account URL and rebuild.
2. To display the README on the personal profile, use a public repository whose name exactly matches that account's username.
3. Upload this project directory's contents, preserving the `site/`, `notes/`, and `.github/` directory structure. Do not upload the supplied slides or the parent directory.
4. In repository Settings → Pages, choose GitHub Actions. The included workflow publishes `site/` after a push to `main` or a manual run.
5. Verify the actual Pages URL, then update the README website link if GitHub assigns a different URL. Set the account Website field to the published URL and use `profile/bio.txt` for the optional biography.

GitHub documentation: https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme

## Updating the teaching material

Keep each course topic’s story, principle, formula, symbol explanation and example. In each bilingual AI topic retain both complete language versions of the story, concept, application, documented practice, formula explanation, worked calculation, limits and takeaway. Explain every symbol and state the assumptions of complexity bounds or probability models. Use fresh illustrative problems. Retain links to primary references. Check each knowledge-map link and PDF after rebuilding.

The default screen body size is 18px. A saved larger-text preference uses 21px. Code uses 16px or 18px with horizontal scrolling to preserve indentation. Do not reduce teaching text to fit a card. CSS and JavaScript URLs include a content hash so updates do not depend on an old browser cache expiring. The GitHub cover uses short large text; course counts stay in native Markdown text.

Python, Java and C programs and their ZIP archives are generated into `site/examples/` and `site/downloads/`. Edit their JSON source, then rebuild. Most snippets use the standard library; some need NumPy. Examples have no model-weight or dataset downloads. A successful run checks the shown output, not every possible input.

Output and rendered-code comparisons allow one optional final newline because a displayed text block may omit it. All other whitespace is significant, including indentation, trailing spaces and extra blank lines.

Every foundational topic includes original instructor insights. Programming topics contrast complete examples. Theory topics explain method choice, intermediate steps, the answer and a sanity check. COMP2123 is Algorithm Design and Analysis; data structures are tools used to implement algorithms.

Original course URLs keep the English `.html` route. Chinese editions use `.zh.html`; both share topic anchors. Keep these anchors stable when renaming a title. Single-page PDFs remain English; web cheatsheets have both languages.
