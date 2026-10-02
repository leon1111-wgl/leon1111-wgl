# Maintaining the profile and learning library

The homepage and five original course guides are English. Four AI field guides provide complete English and Chinese editions with a language switch. The five original learning paths are INFO1113, COMP2017, COMP2123, COMP2022 and COMP3308. Business courses, raw slides, examinations and assignment solutions are excluded. The notes explain concepts using independently written stories and examples.

## Files

- `README.md`: GitHub profile, with working links to readable Markdown notes and PDF references.
- `site/`: complete static website; upload only this directory as the Pages artifact.
- `content/profile.json`: factual biography and GitHub URL.
- `content/COURSE.json`: reviewed course text, knowledge map and compact reference content.
- `content/paths/*.json`: eight bilingual topics, a framework, a review and primary references for each AI guide.
- `scripts/build_paths.py`: generate the bilingual pages and complete Markdown downloads.
- `notes/`: readable Markdown versions for GitHub.
- `profile/bio.txt`: concise GitHub account biography.
- `scripts/build.py`: generate HTML, Markdown and the profile README.
- `scripts/build_pdfs.py`: generate watermarked one-page PDFs and the five-page collection.
- `scripts/validate.py`: validate local navigation, course scope and PDF structure.

The supplied source PDFs and extraction audit remain outside this project. Do not copy the parent directory into a public repository.

## Preview

Run `python3 -m http.server 8765 --directory site` from this project, then open `http://localhost:8765`.
The built website is plain HTML, CSS and JavaScript. It has no analytics, account system, build service dependency, remote fonts, or browser framework. Course content and navigation remain available without JavaScript.

## Rebuild

Use Python 3 with the packages in `requirements.txt`:

```sh
python3 scripts/build.py
python3 scripts/build_pdfs.py
python3 scripts/validate.py
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
