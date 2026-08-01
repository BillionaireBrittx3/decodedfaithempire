#!/usr/bin/env python3
"""Render the rebuilt manuscript to a 6x9 KDP PDF using Noto Serif,
reproducing the source's exact page breaks (from pagemap.json)."""
import json, sys, docx
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from xml.sax.saxutils import escape

FONTS = {
 ("N"): ("NotoSerif", "fonts/NotoSerif-Regular.ttf"),
 ("B"): ("NotoSerif-Bold", "fonts/NotoSerif-Bold.ttf"),
 ("I"): ("NotoSerif-Italic", "fonts/NotoSerif-Italic.ttf"),
 ("BI"):("NotoSerif-BoldItalic", "fonts/NotoSerif-BoldItalic.ttf"),
}
for _k,(name,path) in FONTS.items():
    pdfmetrics.registerFont(TTFont(name, path))

def fontname(bold, ital):
    if bold and ital: return "NotoSerif-BoldItalic"
    if bold: return "NotoSerif-Bold"
    if ital: return "NotoSerif-Italic"
    return "NotoSerif"

PAGE_W, PAGE_H = 6*inch, 9*inch
M_T, M_B, M_L, M_R = 0.48*inch, 0.5*inch, 0.62*inch, 0.62*inch
FRAME_X = M_L
FRAME_Y = M_B
FRAME_W = PAGE_W - M_L - M_R
FRAME_H = PAGE_H - M_T - M_B
ALIGN = {"L":TA_LEFT,"C":TA_CENTER,"R":TA_RIGHT,"J":TA_JUSTIFY}

def build(docx_path, pagemap_path, out_path):
    d = docx.Document(docx_path); P = d.paragraphs
    pm = json.load(open(pagemap_path))["para_page"]
    # collect non-empty paragraphs grouped by page, preserving order
    from collections import defaultdict, OrderedDict
    pages = OrderedDict()
    # need specs: recompute size/bold/ital/align/spacing here from doc
    def spec_of(p):
        size=None
        for r in p.runs:
            if r.font.size: size=round(r.font.size.pt,1); break
        bset=[bool(r.bold) for r in p.runs if r.text.strip()]
        iset=[bool(r.italic) for r in p.runs if r.text.strip()]
        bold=len(bset)>0 and all(bset)
        ital=len(iset)>0 and all(iset)
        pf=p.paragraph_format
        al=pf.alignment
        align={None:"L",0:"L",1:"C",2:"R",3:"J"}.get(int(al) if al is not None else None,"L")
        sb=pf.space_before.pt if pf.space_before is not None else 0
        sa=pf.space_after.pt if pf.space_after is not None else 0
        if size is None: size=10.0
        F=1.362  # Noto Serif natural single-line height ((ascent-descent+lineGap)/upm)
        lsv=pf.line_spacing
        if lsv is None:
            leading=size*F
        elif isinstance(lsv,float):
            leading=size*F*lsv
        else:
            leading=lsv.pt
        return size,bold,ital,align,sb,sa,leading
    for i,p in enumerate(P):
        if not p.text.strip(): continue
        pg = pm.get(str(i))
        pages.setdefault(pg, []).append((i,p))

    c = canvas.Canvas(out_path, pagesize=(PAGE_W, PAGE_H))
    overflow_pages=[]
    for pg in sorted(pages.keys()):
        flow=[]
        for i,p in pages[pg]:
            size,bold,ital,align,sb,sa,leading = spec_of(p)
            st=ParagraphStyle(f"s{i}", fontName=fontname(bold,ital), fontSize=size,
                              leading=leading, alignment=ALIGN[align],
                              spaceBefore=sb, spaceAfter=sa)
            txt=escape(p.text).replace("\n","<br/>")
            flow.append(Paragraph(txt, st))
        f=Frame(FRAME_X, FRAME_Y, FRAME_W, FRAME_H, leftPadding=0,rightPadding=0,
                topPadding=0,bottomPadding=0)
        # suppress spaceBefore of very first flowable so page tops align
        if flow:
            flow[0].spaceBefore=0
        f.addFromList(flow, c)  # mutates flow: unplaced flowables remain
        if flow:
            overflow_pages.append((pg,len(flow)))
        # centered page-number footer (NotoSerif 9pt), matching source
        c.setFont("NotoSerif", 9)
        c.drawCentredString(PAGE_W/2.0, 24, str(pg))
        c.showPage()
    c.save()
    print(f"rendered {len(pages)} pages -> {out_path}")
    if overflow_pages:
        print("OVERFLOW on pages:", overflow_pages[:30], "total", len(overflow_pages))
    else:
        print("no overflow; pagination matches source")
    return len(pages), overflow_pages

if __name__=="__main__":
    dp=sys.argv[1] if len(sys.argv)>1 else "Man_rebuilt.docx"
    out=sys.argv[2] if len(sys.argv)>2 else "Man_rebuilt_render.pdf"
    build(dp,"pagemap.json",out)
