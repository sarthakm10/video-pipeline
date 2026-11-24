TAG = "Frontend 4 · CSS Layout and Responsive Design"
FILE = "Frontend 4 CSS Layout and Responsive Design.mp4"

def flexrow(jc, ai="center", h=170, direction="row"):
    items = "".join(f'<div style="background:{c};border-radius:10px;width:{w}px;height:{hh}px;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:700;color:#fff">{t}</div>'
                    for t, c, w, hh in [("1", "#2563eb", 120, 70), ("2", "#ea580c", 160, 100), ("3", "#16a34a", 110, 60)])
    return (f'<div style="display:flex;flex-direction:{direction};justify-content:{jc};align-items:{ai};gap:14px;height:{h}px;'
            f'border:4px dashed #94a3b8;border-radius:16px;padding:12px;background:#fff">{items}</div>')

SLIDES = [
{"html": """
<div class="fill center">
  <div class="pill" style="align-self:center;margin-bottom:30px">FRONTEND · MODULE 4</div>
  <h1 style="font-size:112px"><span class="u">CSS Layout</span></h1>
  <h1 style="font-size:84px;color:#0d9488">&amp; Responsive Design</h1>
  <p class="sub" style="margin-top:26px;font-size:40px" data-step="1">Flexbox · Grid · media queries · and the last CSS before JavaScript</p>
</div>""",
 "steps": [
  "Welcome to module four: CSS layout and responsive design.",
  "Two tools do almost all modern layout: flexbox and grid. Learn which one fits which job, add a few media queries, and your pages will look right on everything from a phone to a wide monitor. This is the last piece of CSS you need before JavaScript.",
 ]},

{"html": f"""
<h1><span class="u">Flexbox</span>: one direction</h1>
<div class="row top" style="gap:40px;margin-top:10px">
  <pre class="code" style="font-size:30px;width:760px;flex-shrink:0"><span class="t">.navbar</span> {{
  display: flex;
  <span data-hl="2">justify-content: space-between;</span>
  <span data-hl="3">align-items: center;</span>
  gap: <span class="n">16px</span>;
}}</pre>
  <div class="grow" style="display:flex;flex-direction:column;gap:16px">
    <div data-step="1" class="nohl"><div style="font-size:26px;color:#2563eb;font-weight:700">main axis →</div>{flexrow("flex-start","flex-start")}</div>
    <div data-step="2" class="nohl"><div style="font-size:26px;color:#6b7280">justify-content: space-between</div>{flexrow("space-between","flex-start")}</div>
    <div data-step="3" class="nohl"><div style="font-size:26px;color:#6b7280">+ align-items: center (cross axis ↕)</div>{flexrow("space-between","center")}</div>
  </div>
</div>""",
 "steps": [
  "Let's start with flexbox. Flexbox lays out children in one direction, either a row or a column. You turn it on by putting display flex on the parent. Like a navbar, with a logo, some links, and a login button.",
  "The key idea is the two axes. In a row, the main axis runs left to right. Items start at the beginning, lined up along it.",
  "Justify content works along the main axis. Space between pushes the first item to the start, the last to the end, and spreads the rest evenly.",
  "Align items works along the cross axis. Here, that's up and down. Center lines all the items up in the middle. Main axis, justify content. Cross axis, align items.",
 ]},

{"html": f"""
<h1>Flex <span class="u">children</span>, and centring</h1>
<div class="row top" style="gap:30px;margin-top:10px">
  <pre class="code grow" style="font-size:29px"><span data-hl="0"><span class="t">.search</span>  {{ flex: <span class="n">1</span>; }}           <span class="c">/* take the leftover */</span></span>
<span data-hl="0"><span class="t">.sidebar</span> {{ flex: <span class="n">0 0 250px</span>; }}   <span class="c">/* fixed 250px */</span></span>
<span data-hl="1"><span class="t">.push</span>    {{ margin-left: auto; }}  <span class="c">/* to the far end */</span></span></pre>
</div>
<div class="row" style="gap:30px;margin-top:30px">
  <pre class="code grow" style="font-size:30px" data-step="2"><span class="t">.center-me</span> {{
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: <span class="n">100vh</span>;
}}</pre>
  <div class="nohl" data-step="2" style="width:520px">{flexrow("center","center",220)}</div>
</div>
<div class="box yellow" style="margin-top:24px" data-step="3"><small style="font-size:30px;color:#1f2937">🤔 With <code>flex-direction: column</code>, which one centres <u>horizontally</u>? → <b style="display:inline;font-size:30px">align-items</b>, because the axes swap</small></div>""",
 "steps": [
  "You can also control the children. Flex one tells an item to take all the leftover space, perfect for a search box. And flex zero zero two fifty means don't grow, don't shrink, stay two hundred and fifty pixels wide.",
  "And margin left auto is a neat trick. It pushes an item, and everything after it, all the way to the far end.",
  "Here's the famous interview answer for centring something both ways. Display flex, justify content center, align items center. Done.",
  ("Now a quick question. If flex direction is column, which property centres items horizontally? Pause and think. It's align items. In a column, the main axis is vertical, so the two properties swap jobs.", 0.8),
 ]},

{"html": """
<h1><span class="u">Grid</span>: two directions</h1>
<div class="row top" style="gap:40px;margin-top:10px">
  <pre class="code" style="font-size:29px;width:880px;flex-shrink:0"><span data-hl="0"><span class="t">.cards</span> {
  display: grid;
  grid-template-columns: repeat(<span class="n">3</span>, <span class="n">1fr</span>);
  gap: <span class="n">20px</span>;
}</span>

<span data-hl="1"><span class="t">.cards</span> {
  grid-template-columns:
    repeat(auto-fill, minmax(<span class="n">260px</span>, <span class="n">1fr</span>));
}</span></pre>
  <div class="grow" style="display:flex;flex-direction:column;gap:18px">
    <div data-step="0" class="nohl" style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px">
      <div class="pill" style="background:#bfdbfe;text-align:center">1fr</div><div class="pill" style="background:#bfdbfe;text-align:center">1fr</div><div class="pill" style="background:#bfdbfe;text-align:center">1fr</div></div>
    <div data-step="1" class="nohl" style="font-size:28px;line-height:1.9">💻 laptop → <b>4</b> columns<br>📱 tablet → <b>2</b> columns<br>📱 phone → <b>1</b> column</div>
    <p class="note" data-step="1">no media queries needed!</p>
  </div>
</div>""",
 "steps": [
  "Grid lays out children in two dimensions, rows and columns at the same time. Repeat three, one F R, gives you three equal columns. F R means a fraction of the free space. So one F R and two F R would make the second column twice as wide.",
  "And here's the single most useful grid line. Repeat, auto fill, min max two sixty pixels, one F R. It fits as many columns as there's room for, each at least two hundred and sixty pixels wide, and stretches them to fill the row. Four columns on a laptop, two on a tablet, one on a phone. With no media queries at all.",
 ]},

{"html": """
<h1>Grid <span class="u">areas</span></h1>
<div class="row top" style="gap:40px;margin-top:10px">
  <pre class="code" style="font-size:28px;width:860px;flex-shrink:0"><span class="t">.page</span> {
  display: grid;
  grid-template-columns: <span class="n">240px 1fr</span>;
  grid-template-areas:
    <span class="s">"header  header"</span>
    <span class="s">"sidebar main"</span>
    <span class="s">"footer  footer"</span>;
}
<span class="t">.page &gt; header</span> { grid-area: header; }</pre>
  <div class="grow" data-step="1" style="display:grid;grid-template-columns:1fr 2.4fr;grid-template-rows:90px 280px 90px;gap:10px;font-size:30px;font-weight:700">
    <div style="grid-column:span 2;background:#bfdbfe;border-radius:12px;display:flex;align-items:center;justify-content:center">header</div>
    <div style="background:#e9d5ff;border-radius:12px;display:flex;align-items:center;justify-content:center">sidebar</div>
    <div style="background:#bbf7d0;border-radius:12px;display:flex;align-items:center;justify-content:center">main</div>
    <div style="grid-column:span 2;background:#e2e8f0;border-radius:12px;display:flex;align-items:center;justify-content:center">footer</div>
  </div>
</div>""",
 "steps": [
  "Grid can also name areas. You draw the layout right in the CSS, as text. Header across the top, sidebar and main in the middle, footer across the bottom. Then each element just says which area it belongs in.",
  "And there it is: the classic holy grail page layout. Header, sidebar, main, and footer. One grid container, no hacks.",
 ]},

{"html": """
<h1>Flexbox or <span class="u">Grid?</span></h1>
<div class="row top" style="gap:30px;margin-top:20px">
  <div class="box blue grow" data-step="0"><b>Flexbox</b><small style="font-size:30px">one dimension · items size themselves<br>→ navbars, toolbars, button rows, centring, inside a card</small></div>
  <div class="box green grow" data-step="1"><b>Grid</b><small style="font-size:30px">two dimensions · the container sets the tracks<br>→ page layouts, card grids, dashboards, aligned forms</small></div>
</div>
<p class="note center" style="margin-top:36px" data-step="2">They work together: Grid for the page, flexbox inside each card</p>
<div class="box yellow" style="margin-top:30px" data-step="3"><small style="font-size:30px;color:#1f2937">🤔 A row of tags that wraps onto new lines? → <b style="display:inline;font-size:30px">Flexbox</b> with <code>flex-wrap: wrap</code> and a <code>gap</code></small></div>""",
 "steps": [
  "So which one do you use? Flexbox is one dimensional, and the items decide their own size from their content. Use it for navbars, toolbars, rows of buttons, centring, and the insides of a card.",
  "Grid is two dimensional, and the container defines the rows and columns. Use it for page layouts, card grids, dashboards, and forms where labels need to line up.",
  "And they work together. Grid for the page and the list of cards, flexbox inside each card to line up its icon, title and button.",
  ("Quick check. You need a row of tags that wraps onto new lines. Flexbox or grid? It's flexbox, with flex wrap and a gap. Each tag is as wide as its text, and they don't need to line up in columns.", 0.8),
 ]},

{"html": """
<h1><span class="u">Responsive</span> design</h1>
<div class="row top" style="gap:22px;margin-top:6px">
  <div class="box orange grow" data-step="0"><b>1 · viewport tag</b><small>phones use their real width</small></div>
  <div class="box blue grow" data-step="0"><b>2 · fluid sizes</b><small><code>%</code> <code>fr</code> <code>minmax()</code> <code>max-width</code></small></div>
  <div class="box green grow" data-step="0"><b>3 · media queries</b><small>CSS only when a condition is true</small></div>
</div>
<pre class="code" style="font-size:29px;margin-top:26px" data-step="1"><span data-hl="1"><span class="t">.layout</span> { display: flex; flex-direction: column; }   <span class="c">/* 📱 phone: stacked */</span></span>

<span data-hl="2">@media (min-width: <span class="n">768px</span>) {                           <span class="c">/* tablet and up */</span>
  <span class="t">.layout</span> { flex-direction: row; }
}</span>
<span data-hl="3"><span class="t">img</span> { max-width: <span class="n">100%</span>; height: auto; }              <span class="c">/* never overflow */</span></span></pre>""",
 "steps": [
  "A responsive page adapts to the screen. It needs three ingredients. The viewport meta tag from module two. Fluid sizes, like percent, F R, min max, and max width, instead of fixed widths. And media queries, which apply CSS only when a condition is true.",
  "Write it mobile first. The base styles are for small screens. Here, the layout is a stacked column on a phone.",
  "Then a media query with min width adds changes as the screen gets bigger. From seven sixty eight pixels and up, the layout switches to a row. The honest rule for breakpoints: add one where your design breaks, not for specific devices.",
  "And one line keeps images from ever overflowing their container. Max width one hundred percent, height auto.",
 ]},

{"html": """
<h1>Variables, transitions, <span class="u">animations</span></h1>
<div class="row top" style="gap:26px;margin-top:6px">
  <pre class="code grow" style="font-size:26px" data-step="0"><span class="t">:root</span> {
  --brand: <span class="n">#0d9488</span>;
  --radius: <span class="n">10px</span>;
}
<span class="t">.btn</span> { background: var(--brand); }

<span class="t">[data-theme="dark"]</span> {
  --brand: <span class="n">#2dd4bf</span>;   <span class="c">/* dark mode! */</span>
}</pre>
  <pre class="code grow" style="font-size:26px" data-step="1"><span class="t">.card</span> {
  transition: transform <span class="n">0.2s</span> ease;
}
<span class="t">.card:hover</span> {
  transform: translateY(<span class="n">-4px</span>);
}</pre>
</div>
<div class="row" style="gap:30px;margin-top:26px" data-step="2">
  <div class="box green grow"><b>✓ animate</b><small style="font-size:32px"><code>transform</code> and <code>opacity</code>: no layout work, smooth</small></div>
  <div class="box red grow"><b>✗ avoid animating</b><small style="font-size:32px"><code>width</code> <code>top</code> <code>margin</code>: layout every frame, stutters</small></div>
</div>""",
 "steps": [
  "CSS variables keep values in one place. Define them on root, like a brand colour and a radius, and use them with var. Then dark mode is easy: just change the variables. In fact, this very site switches themes exactly like that.",
  "Transitions animate a change between two states. Here, hovering a card lifts it up four pixels, smoothly, over a fifth of a second.",
  "And for smooth animations, animate only transform and opacity. The browser can handle those without redoing the layout. Animating width, top, or margin makes the browser recalculate layout on every single frame, and that's when things start to stutter.",
 ]},

{"html": """
<h1>How teams write CSS <span class="u">today</span></h1>
<table class="t" style="margin-top:10px;font-size:30px">
<tr><th>Approach</th><th>Idea</th></tr>
<tr data-step="0"><td><b>Tailwind CSS</b></td><td>small utility classes in the markup: <code>px-4 py-2 rounded-lg bg-teal-600</code></td></tr>
<tr data-step="0"><td><b>CSS Modules</b></td><td>normal CSS, class names local to one component</td></tr>
<tr data-step="1"><td>Sass / SCSS</td><td>nesting, mixins, compiled to CSS</td></tr>
<tr data-step="1"><td>CSS-in-JS</td><td>styles in JavaScript next to the component</td></tr>
<tr data-step="1"><td>Component libraries</td><td>MUI, Chakra, shadcn/ui: ready-made accessible parts</td></tr>
</table>
<p class="note center" style="margin-top:30px" data-step="2">It all ends up as the CSS you just learned</p>""",
 "steps": [
  "In big apps, plain CSS files get hard to manage. Names clash, and nobody dares delete old styles. The two answers you'll meet most in React jobs are Tailwind, where you compose small utility classes right in the markup, and CSS Modules, where class names are automatically made unique to each component.",
  "You'll also see Sass, CSS in JS libraries, and component libraries like MUI and shadcn.",
  "But whatever the tool, it all ends up as the plain CSS you've learned in these two modules. So these fundamentals keep paying off.",
 ]},

{"html": """
<h1><span class="u">Recap</span></h1>
<ul class="pts" style="margin-top:14px;font-size:35px">
  <li data-step="0">Flexbox = one dimension · justify = main axis, align = cross axis</li>
  <li data-step="0">Centre: <code>flex</code> + <code>justify-content</code> + <code>align-items: center</code></li>
  <li data-step="0">Grid = two dimensions · <code>repeat(auto-fill, minmax(260px, 1fr))</code></li>
  <li data-step="0">Grid for the page, flexbox inside the pieces</li>
  <li data-step="0">Mobile-first: base styles, then <code>min-width</code> media queries</li>
  <li data-step="0">Animate <code>transform</code> and <code>opacity</code></li>
</ul>""",
 "steps": [
  ("Let's recap. Flexbox is one dimensional. Justify content works along the main axis, align items along the cross axis. To centre anything, use flex with both set to center. Grid is two dimensional, and repeat auto fill min max gives you a responsive card grid for free. Use grid for the page, and flexbox inside the pieces. Write mobile first, then add min width media queries. And animate only transform and opacity. That's the CSS you need. Next up: JavaScript! See you there.", 1.5),
 ]},
]
