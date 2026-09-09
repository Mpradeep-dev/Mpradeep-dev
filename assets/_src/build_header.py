"""Regenerate assets/header-{dark,light}.svg with all text outlined to <path>.

Why outlined: GitHub renders the header via a plain <img>, so any <text> would
fall back to whatever font the viewer has. Outlining to vector paths makes the
banner pixel-identical everywhere and removes the font dependency entirely.

Requires: fontTools, and local Segoe UI (ships with Windows):
    segoeuib.ttf  (bold)     -> name
    seguisb.ttf   (semibold) -> eyebrow
    segoeui.ttf   (regular)  -> sub

Run from this directory:  python build_header.py
"""
import pathlib
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.transformPen import TransformPen

FONTS = {
    "regular":  r"C:/Windows/Fonts/segoeui.ttf",
    "semibold": r"C:/Windows/Fonts/seguisb.ttf",
    "bold":     r"C:/Windows/Fonts/segoeuib.ttf",
}
ASSETS = pathlib.Path(__file__).resolve().parents[1]
ARIA = "Pradeep Murugesan, AI Engineer. Computer Vision, GenAI / RAG, Backend, MLOps."


def _run(text, font_path, size, x, y, tracking, pen_factory):
    f = TTFont(font_path)
    scale = size / f["head"].unitsPerEm
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    pen = pen_factory(gs)
    penx = x
    for ch in text:
        gname = cmap.get(ord(ch), ".notdef")
        gs[gname].draw(TransformPen(pen, (scale, 0, 0, -scale, penx, y)))
        penx += hmtx[gname][0] * scale + tracking
    return pen


def path_d(*args):
    return _run(*args, SVGPathPen).getCommands()


def bounds(*args):
    return _run(*args, BoundsPen).bounds


BLOCKS = {
    "eyebrow": ("AI ENGINEER", FONTS["semibold"], 14, 74, 86, 5.0),
    "name":    ("Pradeep Murugesan", FONTS["bold"], 62, 72, 156, -1.5),
    "sub":     ("Computer Vision  \u00b7  GenAI / RAG  \u00b7  Backend  \u00b7  MLOps",
                FONTS["regular"], 18, 74, 226, 0.4),
}
d = {k: path_d(*v) for k, v in BLOCKS.items()}

for k, v in BLOCKS.items():
    x0, y0, x1, y1 = bounds(*v)
    assert x1 < 1010, f"{k} collides with the aperture motif ({x1:.0f})"
    assert 0 < y0 and y1 < 300, f"{k} overflows the canvas vertically"


def svg(defs, bg, grid, accent, name_fill, sub_fill):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 300" width="1280" height="300" role="img" aria-label="{ARIA}">
{defs}  <rect width="1280" height="300" fill="{bg}"/>

  <!-- faint baseline grid -->
  <line x1="72" y1="252" x2="1208" y2="252" stroke="{grid}" stroke-width="1"/>

  <!-- aperture / lens motif : computer-vision nod -->
  <g transform="translate(1108 150)" fill="none" stroke="{accent}">
    <circle r="92" stroke-opacity="0.12"/>
    <circle r="66" stroke-opacity="0.20"/>
    <circle r="40" stroke-opacity="0.34"/>
    <circle r="4" fill="{accent}" stroke="none"/>
    <path d="M0 -66 L23 -40 M57 33 L23 40 M-57 33 L-23 40" stroke-opacity="0.4" stroke-width="1.5"/>
  </g>

  <!-- eyebrow : "AI ENGINEER" (outlined) -->
  <path d="{d['eyebrow']}" fill="{accent}"/>

  <!-- name : "Pradeep Murugesan" (outlined) -->
  <path d="{d['name']}" fill="{name_fill}"/>

  <!-- accent rule -->
  <rect x="74" y="182" width="96" height="3" fill="{accent}"/>

  <!-- sub (outlined) -->
  <path d="{d['sub']}" fill="{sub_fill}"/>
</svg>
'''


DARK_DEFS = '''  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#0b0f14"/>
      <stop offset="1" stop-color="#0e141b"/>
    </linearGradient>
  </defs>
'''

(ASSETS / "header-dark.svg").write_text(
    svg(DARK_DEFS, "url(#bg)", "#1b2430", "#34d3c1", "#f4f6f8", "#8b98a5"), encoding="utf-8")
(ASSETS / "header-light.svg").write_text(
    svg("", "#f6f7f9", "#e3e6ea", "#0d9488", "#0d1117", "#57606a"), encoding="utf-8")
print("wrote header-dark.svg and header-light.svg")
