TAG = "Frontend 2 · HTML Essentials"
FILE = "Frontend 2 HTML Essentials.mp4"

SLIDES = [
{"html": """
<div class="fill center">
  <div class="pill" style="align-self:center;margin-bottom:30px">FRONTEND · MODULE 2</div>
  <h1 style="font-size:124px"><span class="u">HTML Essentials</span></h1>
  <p class="sub" style="margin-top:26px;font-size:40px" data-step="1">About 30 tags · the skill is picking the right one</p>
</div>""",
 "steps": [
  "Welcome to module two: HTML essentials.",
  "Here's some good news. HTML is small. You'll use maybe thirty tags day to day, and React will write most of them for you later. What really matters is choosing the right tag, because that decides how search engines, screen readers, and the browser itself understand your page.",
 ]},

{"html": """
<h1>The page <span class="u">skeleton</span></h1>
<div class="row top" style="gap:30px;margin-top:6px">
<pre class="code grow" style="font-size:27px;line-height:1.45"><span data-hl="1">&lt;!<span class="a">DOCTYPE</span> html&gt;</span>
&lt;<span class="a">html</span> <span data-hl="1"><span class="t">lang</span>=<span class="s">"en"</span></span>&gt;
  <span data-hl="2">&lt;<span class="a">head</span>&gt;</span>
    <span data-hl="2">&lt;<span class="a">meta</span> <span class="t">charset</span>=<span class="s">"UTF-8"</span>&gt;</span>
    <span data-hl="3">&lt;<span class="a">meta</span> <span class="t">name</span>=<span class="s">"viewport"</span>
      <span class="t">content</span>=<span class="s">"width=device-width, initial-scale=1.0"</span>&gt;</span>
    <span data-hl="4">&lt;<span class="a">title</span>&gt;Java Fullstack Tracker&lt;/<span class="a">title</span>&gt;
    &lt;<span class="a">meta</span> <span class="t">name</span>=<span class="s">"description"</span> <span class="t">content</span>=<span class="s">"…"</span>&gt;</span>
    &lt;<span class="a">link</span> <span class="t">rel</span>=<span class="s">"stylesheet"</span> <span class="t">href</span>=<span class="s">"styles.css"</span>&gt;
  &lt;/<span class="a">head</span>&gt;
  <span data-hl="5">&lt;<span class="a">body</span>&gt;
    <span class="c">&lt;!-- everything the user sees --&gt;</span>
  &lt;/<span class="a">body</span>&gt;</span>
&lt;/<span class="a">html</span>&gt;</pre>
<div style="width:560px;display:flex;flex-direction:column;gap:16px">
  <div class="box gray" data-step="1"><small><b style="display:inline;font-size:28px">DOCTYPE + lang</b>: modern mode, right pronunciation</small></div>
  <div class="box gray" data-step="2"><small><b style="display:inline;font-size:28px">head</b>: info <u>about</u> the page, never drawn · UTF-8 for é ₹ 😀</small></div>
  <div class="box orange" data-step="3"><small><b style="display:inline;font-size:28px">viewport</b>: without it, phones fake a 980px screen</small></div>
  <div class="box gray" data-step="4"><small><b style="display:inline;font-size:28px">title + description</b>: the tab text and the search result</small></div>
  <div class="box green" data-step="5"><small><b style="display:inline;font-size:28px">body</b>: everything visible</small></div>
</div></div>""",
 "steps": [
  "Every HTML page has the same skeleton. Let's go through it piece by piece.",
  "The doctype tells the browser to use modern standards mode. And lang equals E N on the html tag helps screen readers pick the right pronunciation, and helps search engines and translators too.",
  "The head holds information about the page. Nothing in it is ever drawn. Charset U T F eight makes sure accented letters, currency symbols, and emoji all show correctly.",
  "Then the viewport meta tag. This one's important. Without it, phones pretend to be nine hundred and eighty pixels wide, and shrink your whole page down, so all the text is tiny. The viewport tag says: use the device's real width.",
  "The title is the text in the browser tab, and the headline in search results. And the description is the grey text under your link on Google.",
  "Finally, the body. Everything the user actually sees goes in here.",
 ]},

{"html": """
<h1>Text, links, images, <span class="u">lists</span></h1>
<div class="row top" style="gap:30px;margin-top:10px">
<pre class="code grow" style="font-size:28px;line-height:1.5"><span data-hl="0">&lt;<span class="a">h1</span>&gt;Learn Java Fullstack&lt;/<span class="a">h1</span>&gt;
&lt;<span class="a">h2</span>&gt;Phase 1: Basics&lt;/<span class="a">h2</span>&gt;</span>
&lt;<span class="a">p</span>&gt;Start with &lt;<span class="a">strong</span>&gt;variables&lt;/<span class="a">strong</span>&gt;.&lt;/<span class="a">p</span>&gt;

<span data-hl="1">&lt;<span class="a">a</span> <span class="t">href</span>=<span class="s">"/notes/day-02.html"</span>&gt;Day 2&lt;/<span class="a">a</span>&gt;
&lt;<span class="a">a</span> <span class="t">href</span>=<span class="s">"#recap"</span>&gt;Jump to recap&lt;/<span class="a">a</span>&gt;</span>

<span data-hl="2">&lt;<span class="a">img</span> <span class="t">src</span>=<span class="s">"duke.png"</span>
     <span class="t">alt</span>=<span class="s">"Duke, the Java mascot, waving"</span>
     <span class="t">width</span>=<span class="s">"120"</span> <span class="t">height</span>=<span class="s">"120"</span>&gt;</span>

<span data-hl="3">&lt;<span class="a">ul</span>&gt;&lt;<span class="a">li</span>&gt;HTML&lt;/<span class="a">li</span>&gt;&lt;<span class="a">li</span>&gt;CSS&lt;/<span class="a">li</span>&gt;&lt;/<span class="a">ul</span>&gt;</span></pre>
<div style="width:600px;display:flex;flex-direction:column;gap:16px">
  <div class="box orange" data-step="0"><small>Headings = <b style="display:inline;font-size:28px">structure</b>, not size. One h1, then h2 → h6 in order.</small></div>
  <div class="box blue" data-step="1"><small>Links: another site, a path on yours, or <code>#id</code> on the page</small></div>
  <div class="box green" data-step="2"><small><b style="display:inline;font-size:28px">alt</b> = the image's purpose · <code>alt=""</code> if decorative · width + height stop the page jumping</small></div>
  <div class="box gray" data-step="3"><small><code>ul</code> bullets · <code>ol</code> numbers</small></div>
</div></div>""",
 "steps": [
  "Now the everyday tags. Headings first. There's one h1 per page, the main title, and then h2 down to h6 for sub-sections, in order. And remember, headings are for structure, not for size. Don't pick h4 because it looks smaller. Style it with CSS instead. Screen reader users jump around a page by its headings.",
  "Links use the a tag with an href. It can point to another website, a path on your own site, or, with a hash, to an element on the same page.",
  "Images need alt text that describes the image's purpose. If it's purely decorative, use an empty alt, so screen readers skip it. And give images a width and a height. Then the browser reserves the space before the image loads, so the page doesn't jump around.",
  "And lists. U L gives you bullets, O L gives you numbers, and each item is an L I.",
 ]},

{"html": """
<h1>Semantic HTML vs <span class="u">div soup</span></h1>
<div class="row top" style="gap:50px;margin-top:20px">
  <div class="grow" data-step="0">
    <p class="center" style="font-size:32px;font-weight:700;color:#dc2626;margin-bottom:12px">❌ div soup</p>
    <div style="border:4px dashed #dc2626;border-radius:18px;padding:18px;display:grid;gap:12px;font-family:Consolas;font-size:28px">
      <div style="border:3px solid #94a3b8;padding:12px;border-radius:10px">div</div>
      <div style="display:grid;grid-template-columns:2fr 1fr;gap:12px"><div style="border:3px solid #94a3b8;padding:40px 12px;border-radius:10px">div</div><div style="border:3px solid #94a3b8;padding:40px 12px;border-radius:10px">div</div></div>
      <div style="border:3px solid #94a3b8;padding:12px;border-radius:10px">div</div>
    </div>
  </div>
  <div class="grow" data-step="1">
    <p class="center" style="font-size:32px;font-weight:700;color:#16a34a;margin-bottom:12px">✓ semantic</p>
    <div style="border:4px solid #16a34a;border-radius:18px;padding:18px;display:grid;gap:12px;font-family:Consolas;font-size:28px">
      <div style="border:3px solid #2563eb;background:#eff6ff;padding:12px;border-radius:10px">&lt;header&gt; + &lt;nav&gt;</div>
      <div style="display:grid;grid-template-columns:2fr 1fr;gap:12px"><div style="border:3px solid #16a34a;background:#f0fdf4;padding:40px 12px;border-radius:10px">&lt;main&gt; &lt;article&gt;</div><div style="border:3px solid #9333ea;background:#faf5ff;padding:40px 12px;border-radius:10px">&lt;aside&gt;</div></div>
      <div style="border:3px solid #64748b;background:#f8fafc;padding:12px;border-radius:10px">&lt;footer&gt;</div>
    </div>
  </div>
</div>
<p class="note center" style="margin-top:40px" data-step="2">Same look · but now screen readers, search engines and teammates know what each part is</p>""",
 "steps": [
  "You could build a whole page from divs. Div for the top, div for the content, div for the sidebar. This is called div soup. It can look perfectly fine, but nothing says what each part actually is.",
  "Semantic tags fix that. Header and nav for the top and the navigation. Main for the main content, with only one per page. Article for a self-contained piece, like a blog post or a product card. Aside for related side content. And footer at the bottom.",
  "It looks exactly the same. But now a screen reader can jump straight to the navigation or the main content, search engines understand the page better, and your teammates can read the code more easily.",
 ]},

{"html": """
<h1><span class="u">article</span> or section? 🤔</h1>
<div class="fill">
  <div class="box gray center" data-step="0" style="font-size:40px;padding:36px">A blog post, in a list of posts. Which tag?</div>
  <div class="row" style="gap:30px;margin-top:40px">
    <div class="box green grow" data-step="1"><b>&lt;article&gt; ✓</b><small style="font-size:32px">makes sense on its own · could be shared by itself</small></div>
    <div class="box blue grow" data-step="1"><b>&lt;section&gt;</b><small style="font-size:32px">a themed part <u>within</u> something, like "Comments"</small></div>
  </div>
</div>""",
 "steps": [
  ("Quick check. You have a list of blog posts. Should each post be an article, or a section? Pause and decide.", 1.5),
  "Article. Each post makes sense completely on its own, and could be shared by itself. A section is for a themed part within something bigger, like the comments, or a related posts block.",
 ]},

{"html": """
<h1><span class="u">Forms</span></h1>
<div class="row top" style="gap:30px;margin-top:6px">
<pre class="code grow" style="font-size:27px;line-height:1.5">&lt;<span class="a">form</span> <span class="t">action</span>=<span class="s">"/api/signup"</span> <span class="t">method</span>=<span class="s">"post"</span>&gt;
  <span data-hl="1">&lt;<span class="a">label</span> <span class="t">for</span>=<span class="s">"email"</span>&gt;Email&lt;/<span class="a">label</span>&gt;
  &lt;<span class="a">input</span> <span class="t">id</span>=<span class="s">"email"</span></span> <span data-hl="4"><span class="t">name</span>=<span class="s">"email"</span></span>
         <span data-hl="2"><span class="t">type</span>=<span class="s">"email"</span></span> <span data-hl="3"><span class="t">required</span></span>&gt;

  &lt;<span class="a">label</span> <span class="t">for</span>=<span class="s">"pw"</span>&gt;Password&lt;/<span class="a">label</span>&gt;
  &lt;<span class="a">input</span> <span class="t">id</span>=<span class="s">"pw"</span> <span class="t">type</span>=<span class="s">"password"</span>
         <span data-hl="3"><span class="t">minlength</span>=<span class="s">"8"</span> <span class="t">required</span></span>&gt;

  <span data-hl="5">&lt;<span class="a">button</span> <span class="t">type</span>=<span class="s">"submit"</span>&gt;Sign up&lt;/<span class="a">button</span>&gt;</span>
&lt;/<span class="a">form</span>&gt;</pre>
<div style="width:560px;display:flex;flex-direction:column;gap:16px">
  <div class="box blue" data-step="1"><small>Every input gets a <b style="display:inline;font-size:28px">label</b>: <code>for</code> = the input's <code>id</code></small></div>
  <div class="box gray" data-step="2"><small>Right <b style="display:inline;font-size:28px">type</b> → right phone keyboard + free checks</small></div>
  <div class="box yellow" data-step="3"><small><code>required</code>, <code>minlength</code>, <code>pattern</code>: browser blocks submit</small></div>
  <div class="box gray" data-step="4"><small><b style="display:inline;font-size:28px">name</b> = the key the server receives</small></div>
  <div class="box orange" data-step="5"><small>A button in a form <u>submits</u> by default · use <code>type="button"</code> if not</small></div>
</div></div>""",
 "steps": [
  "Forms are how users send you data. And even in React, you'll use these exact same elements. Here's a simple sign-up form.",
  "Rule one: every input needs a label. Connect them by setting the label's for attribute to the input's id. Then clicking the label focuses the input, and screen readers announce it properly.",
  "Pick the right type. Email, password, number, date. Phones then show the matching keyboard, and the browser checks the format for free.",
  "You also get built-in validation. Required, min length, max length, and pattern. The browser blocks the submit, and shows a message.",
  "The name attribute is the key the server receives, like email equals, whatever the user typed.",
  "And watch out: a button inside a form submits it by default. If a button shouldn't submit, give it type equals button.",
 ]},

{"html": """
<h1>Tables, and <span class="u">block vs inline</span></h1>
<div class="row top" style="gap:40px;margin-top:20px">
  <div class="box gray" style="width:640px" data-step="0"><b>Tables: only for data</b>
    <table class="t" style="font-size:28px;margin-top:14px"><tr><th>Topic</th><th>Solved</th></tr><tr><td>Arrays</td><td>12</td></tr><tr><td>Trees</td><td>7</td></tr></table>
    <small style="margin-top:12px">never for page layout</small></div>
  <div class="grow" style="display:flex;flex-direction:column;gap:22px">
    <div class="box blue" data-step="1"><b>Block</b><small>new line, full width · <code>div p h1 ul section form</code></small>
      <div style="margin-top:12px;background:#bfdbfe;border-radius:8px;padding:8px 14px;font-size:26px">div ─────────────────────────────</div></div>
    <div class="box orange" data-step="2"><b>Inline</b><small>sits in the text, only as wide as its content · <code>span a strong img</code></small>
      <div style="margin-top:12px;font-size:28px">Some text <span style="background:#fed7aa;border-radius:6px;padding:2px 8px">span</span> more text <span style="background:#fed7aa;border-radius:6px;padding:2px 8px">a</span> …</div></div>
  </div>
</div>""",
 "steps": [
  "Tables are for tabular data only. Rows and columns that belong together, like topics and how many problems you've solved. Never use a table to lay out a page. That's what CSS is for.",
  "And every element is one of two kinds by default. Block elements, like div, p, headings and lists, start on a new line and take the full width.",
  "Inline elements, like span, a, strong and img, sit inside a line of text, and are only as wide as their content. And with CSS, you can change this later, using the display property.",
 ]},

{"html": """
<h1>Accessibility <span class="u">basics</span></h1>
<ul class="pts" style="margin-top:14px;font-size:36px">
  <li class="ok" data-step="0">Use the right element: a <code>&lt;button&gt;</code>, not a clickable <code>&lt;div&gt;</code></li>
  <li class="ok" data-step="1">Images have <code>alt</code> · inputs have labels · headings in order</li>
  <li class="ok" data-step="2">Links say where they go: "Read the Day 12 notes", not "click here"</li>
  <li class="ok" data-step="3">Works with only a keyboard, and you can see the focus</li>
  <li class="ok" data-step="4">Enough contrast · colour is never the only signal</li>
</ul>
<div class="row" style="gap:30px;margin-top:20px" data-step="5">
  <div class="box teal grow"><small style="font-size:30px;color:#1f2937">🔗 link = <b style="display:inline;font-size:30px">goes somewhere</b> · 🔘 button = <b style="display:inline;font-size:30px">does something</b></small></div>
  <div class="term" style="font-size:28px">&lt;button aria-label="Close dialog"&gt;✕&lt;/button&gt;</div>
</div>""",
 "steps": [
  "About one in six people has a disability. And accessible pages work better for everyone. The basics cost almost nothing. First: use the right element. A real button can be reached with Tab, works with Enter and Space, and is announced as a button. A clickable div does none of that.",
  "Images get alt text, every input gets a label, and headings go in order, without skipping levels.",
  "Links should say where they go. Read the day twelve notes, not click here.",
  "Your page should work with only a keyboard. Tab moves through links, buttons and inputs, and you can always see which one has focus.",
  "Use enough colour contrast. And never use colour as the only signal. An error message should say error, not just turn red.",
  "Two last things. A link goes somewhere, a button does something. And ARIA attributes, like aria label, add meaning HTML can't express, such as naming an icon-only close button. But the first rule of ARIA is: if a real HTML element does the job, use that instead.",
 ]},

{"html": """
<h1><span class="u">Recap</span></h1>
<ul class="pts" style="margin-top:14px;font-size:35px">
  <li data-step="0">The viewport tag makes phones use their real width</li>
  <li data-step="0">One h1 · headings are structure, not size</li>
  <li data-step="0">alt describes the image's purpose · empty alt if decorative</li>
  <li data-step="0">header, nav, main, article, aside, footer instead of div soup</li>
  <li data-step="0">Every input has a label · HTML checks don't protect your API</li>
  <li data-step="0">Tables only for data · link goes, button does</li>
</ul>""",
 "steps": [
  ("Let's recap. The viewport tag makes phones use their real width. There's one h1 per page, and headings are about structure, not size. Alt text describes an image's purpose. Use semantic tags like header, nav, main and article, instead of div soup. Every input needs a label, and remember, the browser's validation doesn't protect your API. Spring Boot must check again. Tables are only for data. And a link goes somewhere, while a button does something. Next up: CSS. See you there!", 1.5),
 ]},
]
