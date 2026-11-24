TAG = "Frontend 1 · How the Web Works"
FILE = "Frontend 1 How the Web Works for Frontend.mp4"

SLIDES = [
{"html": """
<div class="fill center">
  <div class="pill" style="align-self:center;margin-bottom:30px">FRONTEND · MODULE 1</div>
  <h1 style="font-size:118px"><span class="u">How the Web Works</span></h1>
  <p class="sub" style="margin-top:26px;font-size:40px" data-step="1">What the browser does with your files · and the tools you'll use every day</p>
</div>""",
 "steps": [
  "Welcome to the frontend side of fullstack!",
  "Your Java code runs on a server. But everything a user actually sees, the buttons, the forms, the pages, runs in their browser. That's the frontend. This first module is the map: what the browser does with your files, and the tools you'll use every single day.",
 ]},

{"html": """
<h1>Frontend vs <span class="u">backend</span></h1>
<div class="fill">
<div class="row" style="justify-content:center;gap:16px">
  <div class="box gray center" style="width:250px" data-step="0"><b>👤 User</b><small>clicks "My tasks"</small></div>
  <div class="arrow" data-step="0">click</div>
  <div class="box blue center" style="width:380px" data-step="0"><b>Browser</b><small>frontend<br>HTML · CSS · JS · React</small></div>
  <div class="arrow" data-step="1"><code>GET /api/tasks</code></div>
  <div class="box green center" style="width:380px" data-step="1"><b>Spring Boot</b><small>backend<br>Java · Spring · SQL</small></div>
  <div class="arrow" data-step="1">SQL</div>
  <div class="box purple center" style="width:230px" data-step="1"><b>🗄️ DB</b></div>
</div>
<div class="row" style="justify-content:center;margin-top:44px;gap:30px" data-step="2">
  <div class="term" style="font-size:32px">← JSON <span style="color:#fbbf24">[{"id":1,"title":"Learn CSS"}]</span></div>
  <div class="note">the backend never draws anything!</div>
</div>
</div>""",
 "steps": [
  "A fullstack app has two halves that talk over HTTP. On one side, the user and their browser. That's the frontend, written in HTML, CSS, JavaScript, and later React.",
  "On the other side, your Spring Boot server, the backend. When the user clicks My tasks, the browser sends a request, GET slash API slash tasks. Spring Boot asks the database, and gets the rows back.",
  "And here's the key idea. The backend never draws anything. It just sends data, usually JSON. The frontend turns that data into what the user sees. That's why one Spring Boot API can serve a website, a phone app, and another service, all at the same time.",
 ]},

{"html": """
<h1>Validation: <span class="u">where does it run?</span></h1>
<div class="fill">
<div class="row" style="gap:40px">
  <div class="box blue grow" data-step="0"><b>Frontend check ⚡</b><small style="font-size:34px">instant feedback for the user<br>→ a <u>nice experience</u></small></div>
  <div class="box green grow" data-step="1"><b>Backend check 🔒</b><small style="font-size:34px">anyone can skip the browser with curl or Postman<br>→ the <u>real safety</u></small></div>
</div>
<p class="note center" style="margin-top:50px" data-step="2">Answer: both. Never trust the frontend alone.</p>
</div>""",
 "steps": [
  ("Quick question. When a user fills in a form, where should the validation run? Frontend, or backend? Pause and think.", 1.5),
  "The frontend checks early, so the user gets instant feedback. But that's only for a nice experience. Anyone can skip your page entirely, and send a request straight to the API with curl or Postman.",
  "So the answer is both. The backend must always check again. Frontend validation is for comfort, backend validation is for safety.",
 ]},

{"html": """
<h1>Three languages, <span class="u">three jobs</span></h1>
<div class="row top" style="gap:26px;margin-top:20px">
  <div class="box orange grow" data-step="0"><b>HTML 🦴</b><small>structure &amp; content<br>the <u>skeleton</u></small>
    <pre class="code" style="font-size:24px;margin-top:16px;padding:16px 20px">&lt;<span class="a">button</span> <span class="t">class</span>=<span class="s">"buy"</span>&gt;
  Buy now
&lt;/<span class="a">button</span>&gt;</pre></div>
  <div class="box blue grow" data-step="1"><b>CSS 👕</b><small>colours, spacing, layout<br>the <u>clothes</u></small>
    <pre class="code" style="font-size:24px;margin-top:16px;padding:16px 20px"><span class="t">.buy</span> {
  background: royalblue;
  color: white;
}</pre></div>
  <div class="box yellow grow" data-step="2"><b>JavaScript 💪</b><small>behaviour<br>the <u>muscles</u></small>
    <pre class="code" style="font-size:24px;margin-top:16px;padding:16px 20px">button.<span class="k">addEventListener</span>(
  <span class="s">"click"</span>,
  () =&gt; alert(<span class="s">"Added!"</span>));</pre></div>
</div>
<p class="note center" style="margin-top:40px" data-step="3">React doesn't replace them. It writes the HTML for you from data.</p>""",
 "steps": [
  "Every web page is made of three languages, and each has one job. HTML is the structure and content: headings, text, images, buttons. Think of it as the skeleton. Here's a button.",
  "CSS is the looks: colours, fonts, spacing, layout. It's the clothes. Now our button is blue with white text.",
  "And JavaScript is behaviour. Reacting to clicks, fetching data, changing the page. The muscles. Now, clicking the button actually does something.",
  "And where does React fit in? React doesn't replace these three. It's a JavaScript library that writes the HTML for you, from your data. You describe what the page should look like, and React keeps it up to date.",
 ]},

{"html": """
<h1>What happens when you <span class="u">open a page</span></h1>
<div class="row" style="gap:12px;margin-top:20px;flex-wrap:wrap">
  <div class="box gray center" style="width:290px" data-step="0"><b>1 · DNS</b><small>domain → IP address</small></div>
  <div class="arrow" data-step="1" style="min-width:60px"></div>
  <div class="box gray center" style="width:330px" data-step="1"><b>2 · Request</b><small>TCP + TLS, then <code>GET /</code></small></div>
  <div class="arrow" data-step="2" style="min-width:60px"></div>
  <div class="box orange center" style="width:330px" data-step="2"><b>3 · HTML</b><small>the server answers</small></div>
</div>
<div class="row" style="gap:12px;margin-top:34px">
  <div class="box orange center" style="width:250px" data-step="3"><b>DOM</b><small>tree from HTML</small></div>
  <div class="box blue center" style="width:250px" data-step="4"><b>CSSOM</b><small>rules from CSS</small></div>
  <div class="arrow" data-step="5" style="min-width:60px"></div>
  <div class="box purple center" style="width:280px" data-step="5"><b>Render tree</b><small>only what's visible</small></div>
  <div class="arrow" data-step="6" style="min-width:60px"></div>
  <div class="box green center" style="width:220px" data-step="6"><b>Layout</b><small>where &amp; how big</small></div>
  <div class="box green center" style="width:200px" data-step="6"><b>Paint</b><small>pixels</small></div>
</div>
<div class="box yellow" style="margin-top:34px" data-step="7"><small style="font-size:32px;color:#1f2937">⚡ JavaScript changes the <b style="display:inline;font-size:32px">DOM</b>, and the browser redoes render tree → layout → paint</small></div>""",
 "steps": [
  "Now, what actually happens when you type a URL and press enter? Step one is DNS. It turns the domain name into an IP address, like looking up a phone number.",
  "Step two: the browser opens a connection, with TLS if it's https, and sends a request. GET slash.",
  "Step three: the server answers with an HTML file.",
  "The browser reads that HTML from top to bottom, and builds the DOM, the Document Object Model. It's a tree of objects, one for every element on the page. Along the way, it finds links to CSS, images and scripts, and requests those too.",
  "The CSS gets parsed into the CSSOM, all the styling rules.",
  "Then the DOM and the CSSOM combine into the render tree. That's only the things that are actually visible.",
  "Next comes layout, working out where every box goes and how big it is. And then paint, filling in the actual pixels.",
  "And after that, JavaScript can change the DOM. When it does, the browser re-runs parts of these last steps. That's how pages update without reloading.",
 ]},

{"html": """
<h1>Why this matters <span class="u">to you</span></h1>
<ul class="pts" style="margin-top:24px">
  <li data-step="0">JavaScript edits the <b>DOM</b>, not the HTML file on the server</li>
  <li data-step="1">A <code>&lt;script&gt;</code> in the head <b>blocks the page</b>, so use <code>defer</code> or put it at the end of the body</li>
  <li data-step="2"><b>Layout is expensive</b>: changing size or position costs more than changing colour or opacity</li>
</ul>
<div class="box teal" style="margin-top:30px" data-step="3"><b>🚀 Interview tip</b><small style="font-size:32px">"What happens when you type a URL?" Walk every layer: DNS, TCP, TLS, HTTP, DOM, CSSOM, layout, paint, then JavaScript. Mention one optimisation per stage.</small></div>""",
 "steps": [
  "So why should you care about all this? Three reasons. First, JavaScript works on the DOM, not on the HTML file. When you change the DOM, the page changes instantly, but the file on the server stays exactly the same.",
  "Second, a script tag in the head blocks the whole page, until it downloads and runs. That's why scripts go at the end of the body, or get the defer attribute.",
  "And third, layout is expensive. Changing an element's size or position makes the browser redo layout. Changing only its colour or opacity is much cheaper.",
  "And a tip for interviews. What happens when you type a URL is a classic question. A strong answer walks through every layer we just saw, and mentions one way to speed up each stage. That really stands out.",
 ]},

{"html": """
<h1>Browser <span class="u">DevTools</span></h1>
<p class="sub">F12 · or right-click anything → Inspect</p>
<table class="t">
<tr><th>Tab</th><th>What you do there</th></tr>
<tr data-step="0"><td><b>Elements</b></td><td>see the live DOM, edit HTML and CSS, see which CSS rule won</td></tr>
<tr data-step="1"><td><b>Console</b></td><td>read errors and <code>console.log</code> output, run JavaScript</td></tr>
<tr data-step="2"><td><b>Network</b></td><td>every request: URL, status, timing, the JSON that came back</td></tr>
<tr data-step="3"><td><b>Sources</b></td><td>read the code, set breakpoints, step through it like IntelliJ</td></tr>
</table>""",
 "steps": [
  "Every browser comes with developer tools. Press F12, or right-click anything and choose Inspect. Four tabs cover most of your day. Elements shows the live DOM. You can edit HTML and CSS right there, and see exactly which CSS rule won.",
  "Console is where errors show up, along with anything you print with console dot log. You can also type JavaScript straight into it.",
  "Network lists every request the page makes. The URL, the status code, how long it took, and the JSON the server sent back.",
  "And Sources lets you read the page's JavaScript, set breakpoints, and step through it line by line, just like debugging in IntelliJ.",
 ]},

{"html": """
<h1>Which tab <span class="u">first?</span> 🤔</h1>
<div class="fill">
  <div class="box gray center" data-step="0" style="font-size:44px;padding:40px">Your page shows <b style="display:inline;font-size:44px">"Loading…"</b> forever.</div>
  <div class="row" style="gap:30px;margin-top:40px">
    <div class="box blue grow" data-step="1"><b>1 · Network</b><small style="font-size:32px">Find the API call. Red, 404, 500 or CORS? → the request or the server is the problem.</small></div>
    <div class="box yellow grow" data-step="2"><b>2 · Console</b><small style="font-size:32px">Call succeeded? → look for a JavaScript error in the code that handles the response.</small></div>
  </div>
</div>""",
 "steps": [
  ("Let's test that. Your page shows Loading, forever. Which DevTools tab do you open first? Pause and think.", 1.5),
  "Network. Find the API request and look at its status. If it failed, a 404, a 500, or a CORS error, then the problem is the request, or the server.",
  "But if the request succeeded, switch to the Console. There's probably a JavaScript error in the code that handles the response.",
 ]},

{"html": """
<h1>Your <span class="u">first page</span></h1>
<div class="row top" style="gap:30px;margin-top:10px">
<pre class="code grow" style="font-size:27px;line-height:1.45"><span data-hl="1">&lt;!<span class="a">DOCTYPE</span> html&gt;
&lt;<span class="a">html</span> <span class="t">lang</span>=<span class="s">"en"</span>&gt;</span>
  &lt;<span class="a">head</span>&gt;
    &lt;<span class="a">title</span>&gt;Hello web&lt;/<span class="a">title</span>&gt;
    <span data-hl="2">&lt;<span class="a">link</span> <span class="t">rel</span>=<span class="s">"stylesheet"</span> <span class="t">href</span>=<span class="s">"style.css"</span>&gt;</span>
  &lt;/<span class="a">head</span>&gt;
  &lt;<span class="a">body</span>&gt;
    &lt;<span class="a">h1</span>&gt;Hello, web!&lt;/<span class="a">h1</span>&gt;
    &lt;<span class="a">button</span> <span class="t">id</span>=<span class="s">"hi"</span>&gt;Say hi&lt;/<span class="a">button</span>&gt;
    <span data-hl="3">&lt;<span class="a">script</span> <span class="t">src</span>=<span class="s">"app.js"</span>&gt;&lt;/<span class="a">script</span>&gt;</span>
  &lt;/<span class="a">body</span>&gt;
&lt;/<span class="a">html</span>&gt;</pre>
<div style="width:620px;display:flex;flex-direction:column;gap:18px">
  <div class="box gray" data-step="0"><small>📁 <b style="display:inline;font-size:28px">hello-web/</b><br>index.html · style.css · app.js</small></div>
  <div class="box blue" data-step="2"><small><b style="display:inline;font-size:28px">style.css</b><br><code>h1 { color: teal; }</code></small></div>
  <div class="box yellow" data-step="3"><small><b style="display:inline;font-size:28px">app.js</b><br>on click → change the text</small></div>
  <div class="box green" data-step="4"><small>VS Code + <b style="display:inline;font-size:28px">Live Server</b><br>→ <code>http://localhost</code>, reloads on save</small></div>
</div></div>""",
 "steps": [
  "Time to build your first page. You don't need to install anything new. A browser and VS Code are enough. Make a folder called hello web, with three files: index dot html, style dot css, and app dot js.",
  "The HTML starts with the doctype, and the html tag with lang equals E N. Tip: in VS Code, type an exclamation mark and press Tab, and it writes this whole skeleton for you.",
  "In the head, a link tag pulls in the stylesheet. And in style dot css, we make the heading teal.",
  "At the very end of the body, a script tag loads app dot js. That's the script that makes the button change the text when you click it.",
  "Finally, add the Live Server extension in VS Code, right-click index dot html, and choose Open with Live Server. It gives you a real localhost address, and reloads the page every time you save.",
 ]},

{"html": """
<h1>Why not just <span class="u">double-click</span> it?</h1>
<div class="fill">
<div class="row" style="gap:40px">
  <div class="box red grow" data-step="0"><b><code>file:///C:/hello-web/index.html</code></b><small style="font-size:32px">fetch, ES modules and some APIs are <u>blocked</u> for security</small></div>
  <div class="box green grow" data-step="1"><b><code>http://localhost:5500</code></b><small style="font-size:32px">a real address, behaves like a website ✓</small></div>
</div>
</div>""",
 "steps": [
  "You might wonder, why not just double-click the HTML file? For a simple page, that works. But the browser opens it as a file colon slash slash address, and many features, like fetch and JavaScript modules, are blocked there for security.",
  "A local server like Live Server gives you a real http localhost address. It behaves just like a real website, so everything works.",
 ]},

{"html": """
<h1><span class="u">Recap</span></h1>
<ul class="pts" style="margin-top:16px;font-size:36px">
  <li data-step="0">Frontend shows data and takes input · backend stores data and applies rules</li>
  <li data-step="0">The API sends <b>JSON</b>, not pages</li>
  <li data-step="0">HTML = structure · CSS = looks · JavaScript = behaviour</li>
  <li data-step="0">HTML → DOM, CSS → CSSOM → render tree → layout → paint</li>
  <li data-step="0">Scripts block the page unless you use <code>defer</code></li>
  <li data-step="0">Data missing? Open <b>Network</b> first</li>
</ul>""",
 "steps": [
  ("Let's recap. The frontend shows data and takes input, while the backend stores data and applies the rules. The API sends JSON, not pages. HTML is the structure, CSS the looks, and JavaScript the behaviour. The browser turns HTML into the DOM, and CSS into the CSSOM, then builds the render tree, lays it out, and paints it. Scripts block the page unless you use defer. And when your data doesn't show up, open the Network tab first. Next time, we dive into HTML itself. See you there!", 1.5),
 ]},
]
