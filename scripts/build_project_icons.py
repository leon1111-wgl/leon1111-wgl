"""Write the small project icons used in the README Projects table (site/assets/icons/*.svg)."""
from pathlib import Path

LINE = 'fill="none" stroke="#60c9ce" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
MARK = 'fill="none" stroke="#b8ee91" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'

GLYPHS = {
    # a support chat bubble with an approval check
    "loopdesk": f'<path {LINE} d="M9 10h10a3 3 0 0 1 3 3v5a3 3 0 0 1-3 3h-5l-4 3v-3H9a3 3 0 0 1-3-3v-5a3 3 0 0 1 3-3z"/>'
                f'<circle cx="11" cy="15.5" r="1" fill="#60c9ce"/><circle cx="14" cy="15.5" r="1" fill="#60c9ce"/><circle cx="17" cy="15.5" r="1" fill="#60c9ce"/>'
                f'<path {MARK} d="M21.5 8.5l1.6 1.6 3-3.3"/>',
    # a bar chart whose numbers are checked
    "proofbi": f'<path {LINE} d="M7 24h18M9 24v-6h3.5v6M14.3 24V14h3.5v10M19.6 24V10h3.5v14"/>'
               f'<path {MARK} d="M7.5 9.5l2 2 3.5-4"/>',
    # a shield with a check: copy that passes review
    "adproof": f'<path {LINE} d="M16 6l8 3v6c0 5-3.5 8.5-8 10-4.5-1.5-8-5-8-10V9z"/>'
               f'<path {MARK} d="M12.5 15.5l2.5 2.5 4.5-5"/>',
    # a document under a lens
    "creditlens": f'<path {LINE} d="M10 6h8l4 4v6M10 6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h5M11.5 12h6M11.5 16h4"/>'
                  f'<circle {MARK} cx="20.5" cy="20.5" r="4"/><path {MARK} d="M23.4 23.4l2.6 2.6"/>',
    # a home inside a detection box
    "estateguard": f'<path {LINE} d="M10.5 16.5l5.5-5 5.5 5V22h-11z"/>'
                   f'<path {MARK} d="M6 10V6h4M22 6h4v4M26 22v4h-4M10 26H6v-4"/>',
    # an open book, for the tutorials
    "tutorials": f'<path {LINE} d="M16 10c-2.5-2-6-2.5-9-2v15c3-.5 6.5 0 9 2 2.5-2 6-2.5 9-2V8c-3-.5-6.5 0-9 2zM16 10v15"/>'
                 f'<path {MARK} d="M10 13h3M10 16.5h3M19 13h3"/>',
    # an earnings line under a scope
    "finscope": f'<path {LINE} d="M6.5 23l5-5.5 4 2.5 5-7.5 5 3"/>'
                f'<circle {MARK} cx="20.5" cy="12.5" r="4"/><path {MARK} d="M20.5 6.5v2M20.5 16.5v2M14.5 12.5h2M24.5 12.5h2"/>',
}


def build():
    out = Path(__file__).resolve().parents[1] / "site" / "assets" / "icons"
    out.mkdir(parents=True, exist_ok=True)
    for name, glyph in GLYPHS.items():
        (out / f"{name}.svg").write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">'
            f'<rect x=".5" y=".5" width="31" height="31" rx="8" fill="#0f1824" stroke="#24384a"/>{glyph}</svg>\n',
            encoding="utf-8")
    print(", ".join(GLYPHS))


if __name__ == "__main__":
    build()
