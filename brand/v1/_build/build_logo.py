"""Builds the outlined logo files in brand/v1/logo/ from the brand fonts.

    python3 brand/v1/_build/build_logo.py
"""

from pathlib import Path

from glyphs import archivo

OUT = Path(__file__).resolve().parent.parent / "logo"
INK, PAPER, CUT = "#191917", "#f3f2ee", "#ff4f00"


def wordmark(fill):
    face = archivo(wght=600, wdth=100)
    size, pad = 100, 4
    letters, width = face.text_path("ronson", x=pad, y=0, size=size, tracking=-0.02)
    dot, dot_w = face.text_path(".", x=pad + width - 0.02 * size, y=0, size=size)
    _, _, _, top = face.bounds(face.gname("o"))
    asc = top * size / face.upm
    w = pad * 2 + width + dot_w
    h = asc + pad * 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 {-asc - pad:.1f} {w:.1f} {h:.1f}" '
        f'width="{w:.0f}" height="{h:.0f}" role="img" aria-label="ronson.">'
        f'<path fill="{fill}" d="{letters}"/><path fill="{CUT}" d="{dot}"/></svg>\n'
    )


def favicon():
    # drawn on the 32 grid, not from the outline, so it stays crisp at 16px
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        f'<rect width="32" height="32" fill="{INK}"/>'
        f'<path fill="{PAPER}" d="M9 9h4v2.2c1-1.6 2.6-2.4 4.8-2.4H19v3.8h-1.6c-2.9 0-4.4 1.4-4.4 4.4V23H9z"/>'
        f'<rect x="20" y="19" width="4" height="4" fill="{CUT}"/></svg>\n'
    )


OUT.mkdir(exist_ok=True)
(OUT / "wordmark.svg").write_text(wordmark(INK))
(OUT / "wordmark-inverse.svg").write_text(wordmark(PAPER))
(OUT / "favicon.svg").write_text(favicon())
print("wrote", *sorted(p.name for p in OUT.iterdir()))
