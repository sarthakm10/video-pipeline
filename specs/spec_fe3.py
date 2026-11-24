TAG = "Frontend 3 · CSS Essentials"
FILE = "Frontend 3 CSS Essentials.mp4"

SLIDES = [
{"html": """
<div class="fill center">
  <div class="pill" style="align-self:center;margin-bottom:30px">FRONTEND · MODULE 3</div>
  <h1 style="font-size:124px"><span class="u">CSS Essentials</span></h1>
  <p class="sub" style="margin-top:26px;font-size:40px" data-step="1">Which rule wins · and how boxes take up space</p>
</div>""",
 "steps": [
  "Welcome to module three: CSS essentials.",
  "CSS decides how everything looks. The language itself is simple. What trips people up is which rule wins, and how boxes take up space. Get those two right, and most of those, why does it look like that, moments simply disappear.",
 ]},

{"html": """
<h1>A rule, and <span class="u">three ways</span> to add it</h1>
<pre class="code" style="font-size:40px;margin-top:10px" data-step="0"><span class="t">h1</span> {                <span class="c">/* selector: what to style */</span>
  color: navy;       <span class="c">/* property: value; */</span>
  font-size: 2rem;
}</pre>
<div class="row top" style="gap:24px;margin-top:30px">
  <div class="box green grow" data-step="1"><b>1 · External ✓</b><small><code>&lt;link rel="stylesheet"&gt;</code><br>cached, shared by every page</small></div>
  <div class="box gray grow" data-step="2"><b>2 · Internal</b><small><code>&lt;style&gt;</code> in the head<br>one page only</small></div>
  <div class="box red grow" data-step="3"><b>3 · Inline</b><small><code>style="color:navy"</code><br>hard to maintain and override</small></div>
</div>""",
 "steps": [
  "A CSS rule has two parts. A selector, which says what to style, and a block of declarations, each one a property, a colon, a value, and a semicolon.",
  "There are three ways to attach CSS to a page. The one you should use is an external file, linked from the head. The browser caches it, and every page shares it.",
  "Second, an internal style block in the head. That only works for one page.",
  "And third, inline styles, right on one element. They're hard to maintain, and very hard to override. Keep them for values that JavaScript calculates, like the width of a progress bar.",
 ]},

{"html": """
<h1><span class="u">Selectors</span></h1>
<table class="t" style="margin-top:14px;font-size:31px">
<tr><th>Selector</th><th>Matches</th></tr>
<tr data-step="0"><td><code>p</code></td><td>every &lt;p&gt; element</td></tr>
<tr data-step="0"><td><code>.card</code></td><td>elements with class="card" ← use these most</td></tr>
<tr data-step="0"><td><code>#login</code></td><td>the one element with id="login" (too strong for styling)</td></tr>
<tr data-step="1"><td><code>.card p</code></td><td>a &lt;p&gt; anywhere inside a card</td></tr>
<tr data-step="1"><td><code>.menu &gt; li</code></td><td>an &lt;li&gt; <u>directly</u> inside .menu</td></tr>
<tr data-step="2"><td><code>a:hover</code> <code>li:nth-child(odd)</code></td><td>pseudo-classes: a state or position</td></tr>
<tr data-step="2"><td><code>.required::after</code></td><td>pseudo-element: a part of an element</td></tr>
</table>""",
 "steps": [
  "Selectors pick what to style. A plain tag name, like p, matches every paragraph. A dot and a name matches a class. That's the one you'll use most, because classes are reusable. And a hash matches an id. Avoid ids for styling. As you'll see in a moment, they're too strong.",
  "You can combine them. Dot card, space, p, matches a paragraph anywhere inside a card, however deep. But dot menu, greater than, li, only matches list items directly inside the menu.",
  "Pseudo-classes match a state, like hover when the mouse is over it, or every odd item in a list for zebra stripes. And pseudo-elements style a part of an element, like adding a star after a required field's label.",
 ]},

{"html": """
<h1>Which rule <span class="u">wins?</span></h1>
<div class="row" style="gap:20px;margin-top:10px;justify-content:center">
  <div class="box red center" style="width:400px" data-step="0"><b>1 · !important</b><small>jumps the queue</small></div>
  <div class="arrow" data-step="0">then</div>
  <div class="box orange center" style="width:400px" data-step="0"><b>2 · Specificity</b><small>more specific wins</small></div>
  <div class="arrow" data-step="0">then</div>
  <div class="box gray center" style="width:400px" data-step="0"><b>3 · Order</b><small>later rule wins</small></div>
</div>
<div class="row" style="gap:16px;margin-top:40px;justify-content:center" data-step="1">
  <div class="center"><div class="big" style="font-size:110px;color:#dc2626">0</div><div style="font-size:30px">ids</div></div>
  <div class="big" style="font-size:110px">,</div>
  <div class="center"><div class="big" style="font-size:110px;color:#2563eb">1</div><div style="font-size:30px">classes</div></div>
  <div class="big" style="font-size:110px">,</div>
  <div class="center"><div class="big" style="font-size:110px;color:#16a34a">1</div><div style="font-size:30px">elements</div></div>
  <div style="margin-left:60px;font-size:40px">← <code>p.intro</code></div>
</div>
<p class="note center" style="margin-top:26px" data-step="2">compare left to right · one id beats any number of classes</p>""",
 "steps": [
  "When two rules set the same property on the same element, the browser decides in three steps. First, importance: anything marked important wins. Then, specificity: the more specific selector wins. And if they're tied, order: the rule that comes later wins.",
  "Specificity is counted as three numbers. Ids, classes, and elements. P dot intro has zero ids, one class, and one element. So zero, one, one.",
  "You compare the numbers from left to right, like a version number. So a single id beats any number of classes.",
 ]},

{"html": """
<h1>Predict the <span class="u">colour</span> 🤔</h1>
<pre class="code" style="font-size:40px;margin-top:10px" data-step="0"><span class="t">#main p</span> { color: <span class="a">red</span>; }   <span class="c">/* (1, 0, 1) */</span>
<span class="t">.text</span>   { color: <span class="t">blue</span>; }  <span class="c">/* (0, 1, 0) */</span></pre>
<div class="row" style="gap:30px;margin-top:30px">
  <div class="box red grow" data-step="1"><b style="color:#dc2626">Red wins</b><small style="font-size:32px">the id makes it (1,0,1) · blue loses even though it comes later</small></div>
</div>
<div class="row" style="gap:30px;margin-top:30px">
  <div class="box gray grow" data-step="2"><small style="font-size:32px;color:#1f2937"><code>#nav a</code> (1,0,1) vs <code>.menu .link.active</code> (0,3,0)?</small></div>
  <div class="box green" style="width:520px" data-step="3"><small style="font-size:32px;color:#1f2937"><b style="display:inline;font-size:32px">#nav a</b>: one id beats three classes</small></div>
</div>
<div class="box teal" style="margin-top:30px" data-step="4"><small style="font-size:30px;color:#1f2937">🚀 Teams keep specificity <b style="display:inline;font-size:30px">low and flat</b>: single classes (BEM, Tailwind), so order decides. <code>!important</code> is a last resort.</small></div>""",
 "steps": [
  ("Let's try one. Hash main p sets the colour to red. Dot text sets it to blue, and comes later. The paragraph has both. Which colour wins? Pause and think.", 2.0),
  "Red. Hash main p has an id, so it's one, zero, one. Dot text is only zero, one, zero. Coming later doesn't help, because specificity is checked before order.",
  ("One more. Hash nav a, versus dot menu, dot link, dot active. Three classes against one id.", 1.5),
  "Hash nav a wins. One id beats any number of classes.",
  "And that's exactly why real teams avoid specificity wars. They style almost everything with single classes, using naming systems like BEM, or utility classes like Tailwind. Then every rule has the same specificity, and order decides. Treat important as a last resort, not a fix.",
 ]},

{"html": """
<h1>The <span class="u">box model</span></h1>
<div class="row" style="gap:50px;margin-top:10px">
  <div style="width:820px;flex-shrink:0">
    <div data-step="0" style="border:4px dashed #ea580c;background:#fff7ed;padding:56px 40px 40px;border-radius:12px;position:relative">
      <span style="position:absolute;top:10px;left:18px;font-size:28px;font-weight:700;color:#ea580c">margin</span>
      <div style="border:34px solid #374151;border-radius:6px;position:relative">
        <span style="position:absolute;top:-32px;left:10px;font-size:24px;font-weight:700;color:#fff">border</span>
        <div style="background:#bbf7d0;padding:52px 40px 40px;position:relative">
          <span style="position:absolute;top:10px;left:16px;font-size:28px;font-weight:700;color:#166534">padding</span>
          <div style="background:#bfdbfe;padding:34px;text-align:center;font-size:36px;font-weight:700">content</div>
        </div>
      </div>
    </div>
  </div>
  <div class="grow" style="display:flex;flex-direction:column;gap:20px">
    <pre class="code" style="font-size:28px" data-step="1"><span class="t">.card</span> {
  width: <span class="n">300px</span>;
  padding: <span class="n">16px</span>;
  border: <span class="n">2px</span> solid;
}</pre>
    <div class="box red" data-step="2"><small style="font-size:30px;color:#1f2937">content-box: <b style="display:inline;font-size:30px">300 + 32 + 4 = 336px</b> 😬</small></div>
    <div class="box green" data-step="3"><small style="font-size:28px;color:#1f2937"><code>* { box-sizing: border-box; }</code><br>→ exactly <b style="display:inline;font-size:30px">300px</b></small></div>
  </div>
</div>""",
 "steps": [
  "Now the second big idea: the box model. Every element is a rectangle with four layers. In the middle, the content. Around it, padding, the space inside, which shares the background. Then the border. And outside everything, the margin, transparent space that pushes other boxes away.",
  "So here's a card. Width three hundred pixels, sixteen pixels of padding, and a two pixel border. How wide is it?",
  "By default, width only measures the content. So the card is really three hundred, plus thirty-two of padding, plus four of border. Three hundred and thirty-six pixels. That surprises everyone.",
  "So almost every project starts with one line: box sizing, border box, on everything. Now width includes the padding and border, and the card is exactly three hundred pixels.",
 ]},

{"html": """
<h1>Box model <span class="u">details</span></h1>
<div class="fill" style="gap:30px">
  <div class="row" style="gap:30px" data-step="0">
    <pre class="code" style="font-size:34px">margin: <span class="n">10px 20px 30px 40px</span>;</pre>
    <div class="note">top → right → bottom → left (clockwise)</div>
  </div>
  <div class="row" style="gap:30px" data-step="1">
    <pre class="code" style="font-size:34px">margin: <span class="n">10px 20px</span>;</pre>
    <div class="note">top/bottom 10 · left/right 20</div>
  </div>
  <div class="box yellow" data-step="2"><b>Vertical margins collapse</b><small style="font-size:32px">a 20px bottom margin above a 30px top margin → a <u>30px</u> gap, not 50px (not inside flex or grid)</small></div>
</div>""",
 "steps": [
  "Two more details. Shorthand values go clockwise from the top. Top, right, bottom, left.",
  "With two values, the first is top and bottom, and the second is left and right.",
  "And vertical margins collapse. A twenty pixel bottom margin sitting above a thirty pixel top margin gives a gap of thirty, not fifty. The bigger one wins. This doesn't happen inside flex or grid layouts.",
 ]},

{"html": """
<h1>Units and <span class="u">colours</span></h1>
<table class="t" style="margin-top:10px;font-size:31px">
<tr><th>Unit</th><th>Relative to</th><th>Use it for</th></tr>
<tr data-step="0"><td><code>px</code></td><td>nothing, fixed</td><td>borders, small details</td></tr>
<tr data-step="0"><td><code>%</code></td><td>the parent's size</td><td>widths in a container</td></tr>
<tr data-step="1"><td><code>rem</code></td><td>the root font size (16px)</td><td><b>font sizes</b>, spacing</td></tr>
<tr data-step="1"><td><code>em</code></td><td>the element's own font size</td><td>padding that grows with text</td></tr>
<tr data-step="2"><td><code>vw</code> / <code>vh</code></td><td>1% of the screen width / height</td><td>full-screen sections</td></tr>
</table>
<div class="row" style="gap:16px;margin-top:26px;font-size:30px" data-step="3">
  <span class="pill" style="background:#1e90ff;color:#fff">#1e90ff</span>
  <span class="pill" style="background:rgb(30 144 255 / 50%)">rgb(30 144 255 / 50%)</span>
  <span class="pill" style="background:hsl(210 100% 70%)">hsl(210 100% 70%)</span>
</div>""",
 "steps": [
  "Next, units. Pixels are fixed. Use them for borders and small details. Percent is relative to the parent, handy for widths inside a container.",
  "Rem is relative to the root font size, usually sixteen pixels. Use rem for font sizes. If a user sets a bigger default font for readability, rem text grows with it, but pixel text ignores their choice. Em is relative to the element's own font size.",
  "And V W and V H are one percent of the screen's width and height. Great for full-screen sections.",
  "Colours can be written as a name, a hex code, R G B, with an optional transparency, or H S L, which makes lighter and darker shades really easy.",
 ]},

{"html": """
<h1><span class="u">display</span></h1>
<div class="row top" style="gap:24px;margin-top:14px;flex-wrap:wrap">
  <div class="box blue" style="width:530px" data-step="0"><b>block</b><small>new line, full width, width/height work</small></div>
  <div class="box orange" style="width:530px" data-step="0"><b>inline</b><small>flows in text, width/height ignored</small></div>
  <div class="box purple" style="width:530px" data-step="0"><b>inline-block</b><small>flows in text, but width/height work</small></div>
</div>
<div class="row" style="gap:30px;margin-top:40px">
  <div class="box red grow" data-step="1"><b>display: none</b><small style="font-size:32px">removed, <u>takes no space</u></small>
    <div style="margin-top:14px;display:flex;gap:10px"><span class="pill">A</span><span class="pill">C</span></div></div>
  <div class="box gray grow" data-step="1"><b>visibility: hidden</b><small style="font-size:32px">invisible, but <u>keeps its space</u></small>
    <div style="margin-top:14px;display:flex;gap:10px"><span class="pill">A</span><span class="pill" style="visibility:hidden">B</span><span class="pill">C</span></div></div>
</div>""",
 "steps": [
  "The display property decides how a box behaves. Block starts a new line, and takes the full width. Inline flows inside text, and ignores width and height. And inline block flows in text, but lets you set width and height. Flex and grid are coming in the next module.",
  "And a classic question: display none versus visibility hidden. Display none removes the element completely, so it takes no space. Visibility hidden makes it invisible, but its space is kept, leaving a gap.",
 ]},

{"html": """
<h1><span class="u">position</span></h1>
<table class="t" style="margin-top:6px;font-size:30px">
<tr><th>Value</th><th>Relative to</th><th>In the flow?</th></tr>
<tr data-step="0"><td><code>static</code></td><td>— default, top/left ignored</td><td>yes</td></tr>
<tr data-step="0"><td><code>relative</code></td><td>where it would normally be</td><td>yes</td></tr>
<tr data-step="1"><td><code>absolute</code></td><td>the nearest <b>positioned</b> ancestor</td><td>no</td></tr>
<tr data-step="2"><td><code>fixed</code></td><td>the screen: stays put when you scroll</td><td>no</td></tr>
<tr data-step="2"><td><code>sticky</code></td><td>normal, until you scroll past, then sticks</td><td>yes</td></tr>
</table>
<div class="row" style="gap:30px;margin-top:24px" data-step="3">
  <div style="position:relative;width:360px;height:170px;border:4px solid #374151;border-radius:18px;background:#fff;padding:20px;font-size:30px;flex-shrink:0">
    Card<span style="position:absolute;top:10px;right:10px;background:#ef4444;color:#fff;border-radius:999px;padding:4px 16px;font-size:24px">NEW</span></div>
  <pre class="code" style="font-size:26px;flex:1"><span class="t">.card</span> { position: relative; }   <span class="c">/* the anchor */</span>
<span class="t">.badge</span> { position: absolute; top: <span class="n">10px</span>; right: <span class="n">10px</span>; }</pre>
</div>""",
 "steps": [
  "Finally, position. Static is the default. Top and left do nothing. Relative nudges an element from where it would normally be, and keeps its space.",
  "Absolute takes the element out of the flow, and positions it relative to the nearest positioned ancestor. Remember that phrase. It's the cause of a classic bug.",
  "Fixed is relative to the screen, so it stays put when you scroll. And sticky scrolls normally, until it reaches a point, then sticks, like a header that stays at the top.",
  "Here's the classic pattern: a badge in the corner of a card. The card gets position relative, making it the anchor. The badge gets position absolute, top ten, right ten. And if you forget position relative on the card, the badge flies off to the corner of the whole page, because there's no positioned ancestor to anchor it.",
 ]},

{"html": """
<h1><span class="u">Recap</span></h1>
<ul class="pts" style="margin-top:14px;font-size:35px">
  <li data-step="0">Use external stylesheets, and classes for almost everything</li>
  <li data-step="0">Winner: !important → specificity (ids, classes, elements) → order</li>
  <li data-step="0">Box: content, padding, border, margin · use <code>border-box</code></li>
  <li data-step="0"><code>rem</code> for font sizes · <code>none</code> removes, <code>hidden</code> keeps space</li>
  <li data-step="0">absolute → the nearest <b>positioned</b> ancestor</li>
</ul>""",
 "steps": [
  ("Let's recap. Use external stylesheets, and classes for almost everything. When rules clash, important wins first, then specificity, counted as ids, classes and elements, and then order. Every box is content, padding, border and margin, and border box makes width behave. Use rem for font sizes. Display none removes an element, visibility hidden keeps its space. And absolute is positioned relative to the nearest positioned ancestor. Next time: layout with flexbox and grid. See you there!", 1.5),
 ]},
]
