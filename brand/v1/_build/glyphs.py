"""Outline text from the brand's variable fonts.

Instances a variable woff2 at fixed axes (fontTools.varLib.instancer), reads
GPOS pair kerning (lookup type 2, formats 1 and 2) and returns SVG path data in
a y-down coordinate system with the baseline at y=0. Units are font units
(1000/em) unless a size is given.
"""

from functools import lru_cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONTS = Path(__file__).resolve().parent.parent / "fonts"
ARCHIVO = FONTS / "archivo-latin.woff2"
MARTIAN = FONTS / "martian-mono-latin.woff2"


def _fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Face:
    def __init__(self, path, **axes):
        font = TTFont(str(path))
        self.font = instancer.instantiateVariableFont(font, axes)
        self.upm = self.font["head"].unitsPerEm
        self.cmap = self.font.getBestCmap()
        self.glyphset = self.font.getGlyphSet()
        self.hmtx = self.font["hmtx"]
        self._kern = self._read_kern()

    # -- kerning -------------------------------------------------------
    def _read_kern(self):
        pairs, classes = {}, []
        if "GPOS" not in self.font:
            return pairs, classes
        gpos = self.font["GPOS"].table
        idx = set()
        for fr in gpos.FeatureList.FeatureRecord:
            if fr.FeatureTag == "kern":
                idx.update(fr.Feature.LookupListIndex)
        for i in sorted(idx):
            lookup = gpos.LookupList.Lookup[i]
            for st in lookup.SubTable:
                if lookup.LookupType == 9:
                    st = st.ExtSubTable
                if getattr(st, "LookupType", 2) != 2:
                    continue
                cov = st.Coverage.glyphs
                if st.Format == 1:
                    for g1, ps in zip(cov, st.PairSet):
                        for pvr in ps.PairValueRecord:
                            v = getattr(pvr.Value1, "XAdvance", 0) if pvr.Value1 else 0
                            pairs.setdefault((g1, pvr.SecondGlyph), v)
                elif st.Format == 2:
                    classes.append((set(cov), st.ClassDef1.classDefs,
                                    st.ClassDef2.classDefs, st.Class1Record))
        return pairs, classes

    def kern(self, a, b):
        pairs, classes = self._kern
        if (a, b) in pairs:
            return pairs[(a, b)]
        for cov, cd1, cd2, recs in classes:
            if a not in cov:
                continue
            c1, c2 = cd1.get(a, 0), cd2.get(b, 0)
            v = recs[c1].Class2Record[c2].Value1
            return getattr(v, "XAdvance", 0) if v else 0
        return 0

    # -- glyphs --------------------------------------------------------
    def gname(self, ch):
        return self.cmap[ord(ch)]

    def advance(self, name):
        return self.hmtx[name][0]

    def bounds(self, name):
        bp = BoundsPen(self.glyphset)
        self.glyphset[name].draw(bp)
        return bp.bounds  # y-up font units

    def glyph_path(self, name, x=0.0, y=0.0, scale=1.0):
        pen = SVGPathPen(self.glyphset, ntos=_fmt)
        tp = TransformPen(pen, (scale, 0, 0, -scale, x, y))
        self.glyphset[name].draw(tp)
        return pen.getCommands()

    def layout(self, text, tracking=0.0, adjust=None):
        """Return [(glyph_name, x_font_units)] and total advance.
        tracking is in em; adjust maps pair index -> extra units after glyph i."""
        names = [self.gname(c) for c in text]
        out, x = [], 0.0
        track = tracking * self.upm
        for i, n in enumerate(names):
            out.append((n, x))
            x += self.advance(n)
            if i + 1 < len(names):
                x += self.kern(n, names[i + 1]) + track
                if adjust and i in adjust:
                    x += adjust[i]
        return out, x

    def text_path(self, text, x=0.0, y=0.0, size=None, tracking=0.0,
                  adjust=None):
        """Single SVG path 'd' for text, baseline at y, origin x."""
        s = (size / self.upm) if size else 1.0
        lay, w = self.layout(text, tracking, adjust)
        d = "".join(self.glyph_path(n, x + gx * s, y, s) for n, gx in lay if n != "space")
        return d, w * s


@lru_cache(maxsize=None)
def archivo(wght=800, wdth=125):
    return Face(ARCHIVO, wght=wght, wdth=wdth)


@lru_cache(maxsize=None)
def martian(wght=500, wdth=87.5):
    return Face(MARTIAN, wght=wght, wdth=wdth)
