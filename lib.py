# Small helpers so each module's spec stays short: slide titles, coloured code, boxes, tables, quizzes.
import html as _h
import re

KW = ("const let var function return if else for while do switch case break continue new class extends super this "
      "import export from default async await try catch finally throw typeof instanceof in of null undefined true "
      "false interface type implements enum keyof readonly as public private protected static void yield delete").split()
_tok = re.compile(r'(//[^\n]*|/\*.*?\*/|`(?:\\.|[^`])*`|"(?:\\.|[^"])*"|\'(?:\\.|[^\'])*\'|\b\d+(?:\.\d+)?n?\b|\b[A-Za-z_$][\w$]*\b|<\/?[A-Za-z][\w.-]*|.)', re.S)


def color(src):
    out = []
    for m in _tok.finditer(src):
        t = m.group(0)
        e = _h.escape(t, quote=False)
        if t.startswith("//") or t.startswith("/*"):
            out.append(f'<span class="c">{e}</span>')
        elif t[0] in "\"'`":
            out.append(f'<span class="s">{e}</span>')
        elif t[0].isdigit():
            out.append(f'<span class="n">{e}</span>')
        elif t in KW:
            out.append(f'<span class="k">{e}</span>')
        elif t.startswith("<") and len(t) > 1:
            out.append(f'&lt;<span class="a">{_h.escape(t[1:])}</span>' if t[1] != "/" else f'&lt;/<span class="a">{_h.escape(t[2:])}</span>')
        elif t[:1].isupper() and t.isidentifier():
            out.append(f'<span class="t">{e}</span>')
        else:
            out.append(e)
    return "".join(out)


def code(src, size=34, step=None, style="", hl=None):
    """Code block. A line starting with '§n ' is highlighted at step n (several: '§1,3 ')."""
    lines = []
    for line in src.strip("\n").split("\n"):
        m = re.match(r"§([\d,]+) ?(.*)", line)
        if m:
            lines.append(f'<span data-hl="{m.group(1)}">{color(m.group(2))}</span>')
        else:
            lines.append(color(line))
    st = f' data-step="{step}"' if step is not None else ""
    return f'<pre class="code"{st} style="font-size:{size}px;{style}">' + "\n".join(lines) + "</pre>"


def H(*parts):
    """Title: H("Plain ", "underlined", " plain")."""
    s = "".join(f'<span class="u">{p}</span>' if i % 2 else p for i, p in enumerate(parts))
    return f"<h1>{s}</h1>"


def sub(text):
    return f'<p class="sub">{text}</p>'


def box(c, title, body="", step=None, style="", size=None):
    st = f' data-step="{step}"' if step is not None else ""
    fs = f' style="font-size:{size}px"' if size else ""
    b = f"<b>{title}</b>" if title else ""
    return f'<div class="box {c}"{st} style="{style}">{b}<small{fs}>{body}</small></div>'


def row(*items, gap=28, style="", top=False):
    return f'<div class="row{" top" if top else ""}" style="gap:{gap}px;{style}">' + "".join(items) + "</div>"


def col(*items, gap=20, style=""):
    return f'<div style="display:flex;flex-direction:column;gap:{gap}px;{style}">' + "".join(items) + "</div>"


def fill(*items, gap=30):
    return f'<div class="fill" style="gap:{gap}px">' + "".join(items) + "</div>"


def pts(items, size=38, style=""):
    """items: (html, step) or (html, step, cls)."""
    li = "".join(f'<li class="{it[2] if len(it) > 2 else ""}" data-step="{it[1]}">{it[0]}</li>' for it in items)
    return f'<ul class="pts" style="font-size:{size}px;margin-top:14px;{style}">{li}</ul>'


def table(head, rows, size=31):
    """rows: (cells, step)."""
    h = "".join(f"<th>{x}</th>" for x in head)
    r = "".join(f'<tr data-step="{s}">' + "".join(f"<td>{c}</td>" for c in cells) + "</tr>" for cells, s in rows)
    return f'<table class="t" style="font-size:{size}px;margin-top:10px"><tr>{h}</tr>{r}</table>'


def note(text, step=None, style=""):
    st = f' data-step="{step}"' if step is not None else ""
    return f'<p class="note center"{st} style="margin-top:30px;{style}">{text}</p>'


def title_slide(n, title, tagline, intro, more, pill=None):
    return {"html": f"""<div class="fill center">
  <div class="pill" style="align-self:center;margin-bottom:30px">{pill or f"FRONTEND · MODULE {n}"}</div>
  <h1 style="font-size:{112 if len(title) < 22 else 92}px"><span class="u">{title}</span></h1>
  <p class="sub" style="margin-top:26px;font-size:40px" data-step="1">{tagline}</p></div>""",
            "steps": [intro, more]}


def predict(title, cards, size=34):
    """cards: (question_html, answer_big, explanation, ask_narration, answer_narration). Steps: q0 a0 q1 a1 ..."""
    html, steps = [], []
    for i, (q, a, ex, askn, ansn) in enumerate(cards):
        html.append(f'<div class="box gray" style="width:820px" data-step="{2*i}"><b><code style="font-size:{size}px">{q}</code></b>'
                    f'<div data-step="{2*i+1}"><span class="big" style="font-size:64px;color:#16a34a">{a}</span>'
                    f'<small>{ex}</small></div></div>')
        steps += [(askn, 2.0), ansn]
    return {"html": H(*title) + '<div class="row top" style="gap:26px;margin-top:20px;flex-wrap:wrap">' + "".join(html) + "</div>",
            "steps": steps}


def quiz(cards):
    """cards: (question_html, answer_html, colour, ask_narration, answer_narration)."""
    html, steps = [], []
    for i, (q, a, c, askn, ansn) in enumerate(cards):
        html.append(f'<div class="row" data-step="{2*i}"><div class="box gray grow"><small style="font-size:34px;color:#1f2937">{q}</small></div>'
                    f'<div class="box {c}" style="width:760px" data-step="{2*i+1}"><small style="font-size:31px;color:#1f2937">{a}</small></div></div>')
        steps += [(askn, 1.5), ansn]
    return {"html": H("Quick ", "quiz") + fill(*html, gap=24), "steps": steps}


def recap(items, narration, size=35):
    return {"html": H("", "Recap") + pts([(x, 0) for x in items], size=size), "steps": [(narration, 1.5)]}
