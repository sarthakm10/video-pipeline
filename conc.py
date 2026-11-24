"""Helpers for the concept videos (DSA, Java, Spring)."""
from lib import *


def cells(values, lo=None, hi=None, step=None, label="", size=44, mark=None, style=""):
    """A row of array cells; [lo, hi] is the highlighted window, mark = {index: colour} for single cells."""
    out = []
    for i, v in enumerate(values):
        inside = lo is not None and lo <= i <= hi
        bg = (mark or {}).get(i, "#fde68a" if inside else "#fff")
        border = "#d97706" if inside else "#9ca3af"
        out.append(f'<div style="width:{size + 40}px;height:{size + 40}px;border:4px solid {border};border-radius:12px;'
                   f'background:{bg};display:flex;align-items:center;justify-content:center;'
                   f'font:700 {size}px Cascadia Code,Consolas,monospace">{v}</div>')
    st = f' data-step="{step}"' if step is not None else ""
    lab = f'<div style="font-size:32px;min-width:330px;color:#374151">{label}</div>' if label else ""
    return f'<div class="row" style="gap:10px;align-items:center;{style}"{st}>{lab}{"".join(out)}</div>'


def graph(nodes, edges, colors=None, w=640, h=380, directed=False, step=None, labels=None, r=34):
    """Small SVG graph. nodes: {name: (x, y)}; edges: [(a, b)]; colors: {name: (fill, stroke)}; labels: {name: text below}."""
    colors = colors or {}
    st = f' data-step="{step}"' if step is not None else ""
    parts = [f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"{st} style="overflow:visible;flex-shrink:0;width:{w}px;height:{h}px">',
             '<defs><marker id="ah" markerUnits="userSpaceOnUse" markerWidth="22" markerHeight="22" refX="20" refY="11" orient="auto">'
             '<path d="M0,0 L22,11 L0,22 z" fill="#374151"/></marker></defs>']
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        if directed:
            d = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            x2, y2 = x2 - (x2 - x1) * (r + 6) / d, y2 - (y2 - y1) * (r + 6) / d
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#374151" stroke-width="4"'
                     f'{" marker-end=\"url(#ah)\"" if directed else ""}/>')
    for n, (x, y) in nodes.items():
        fill, stroke = colors.get(n, ("#fff", "#374151"))
        fs = min(32, 2 * r * 0.82 / (0.58 * len(n)))
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="4"/>'
                     f'<text x="{x}" y="{y + fs * 0.34:.0f}" text-anchor="middle" font-size="{fs:.0f}" font-weight="700" '
                     f'font-family="Segoe UI">{n}</text>')
        if labels and n in labels:
            parts.append(f'<text x="{x}" y="{y + r + 32}" text-anchor="middle" font-size="26" fill="#4b5563" '
                         f'font-family="Segoe UI">{labels[n]}</text>')
    return "".join(parts) + "</svg>"
