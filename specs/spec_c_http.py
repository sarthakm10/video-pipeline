from conc import *

TAG = "Spring · HTTP and REST Basics"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring HTTP and REST Basics.mp4"

SLIDES = [
title_slide(0, "HTTP & REST Basics", "What actually travels between a browser and your Spring app",
  "Welcome to HTTP and REST basics.",
  "Before writing a single controller, it helps to know exactly what a request and a response look like on the wire. Everything Spring does, mapping URLs, reading JSON, setting status codes, is built on this. By the end you'll know URLs, the anatomy of requests and responses, HTTP methods and idempotency, status code families, the headers that matter, statelessness and tokens, REST design rules, and HTTPS.",
  pill="SPRING · CONCEPT"),

{"html": H("Clients, servers, ", "URLs") + code("""§0 https://api.example.com:443/api/tasks/7?include=comments#top
§1 └scheme┘└─── host ────┘port└── path ──┘└──── query ────┘frag""", 30) + row(
   box("blue", "client", "browser, mobile app, curl · <b style=\"display:inline\">starts</b> every exchange", 2, "flex:1"),
   box("green", "server", "your Spring app (in Tomcat) · <b style=\"display:inline\">answers</b>", 2, "flex:1"),
   box("orange", "the fragment", "<code>#top</code> never leaves the browser", 3, "flex:1"), style="margin-top:24px"),
 "steps": [
  "Every HTTP exchange starts from a URL. Here's one.",
  "It has parts. The scheme, https. The host, the server's name. The port, four four three by default for https. The path, which identifies the resource. And the query string, after the question mark, for options like filters.",
  "HTTP is a request response protocol. The client, a browser, a mobile app, or curl, always starts. The server, your Spring app running in Tomcat, only answers.",
  "One detail: the part after the hash, the fragment, is never sent to the server. It's only used by the browser.",
 ]},

{"html": H("A request and a ", "response") + row(
   code("""§0 POST /api/tasks HTTP/1.1
§0 Host: api.example.com
§0 Content-Type: application/json
§0 Authorization: Bearer eyJhbGci...
§0
§0 {"title": "Write notes"}""", 25, style="flex:1"),
   code("""§1 HTTP/1.1 201 Created
§1 Location: /api/tasks/42
§1 Content-Type: application/json
§1
§1 {"id": 42, "title": "Write notes",
§1  "done": false}""", 25, style="flex:1"), top=True) +
   note("Start line · headers · blank line · optional body: both directions", 2),
 "steps": [
  "A request is just text. A start line with the method, the path, and the version. Then headers, one per line: the host, what type the body is, and credentials. Then a blank line, and an optional body, here some JSON.",
  "The response has the same shape. A status line, two oh one created. Headers, like where the new resource lives. A blank line. And the body.",
  "So both directions are: a start line, headers, a blank line, and an optional body. Spring reads and writes these for you, but this is what your annotations map to.",
 ]},

{"html": H("Methods: safe and ", "idempotent") + table(["Method", "Purpose", "Safe", "Idempotent", "Body"], [
     (["<b>GET</b>", "read", "✅", "✅", "no"], 0),
     (["<b>POST</b>", "create · actions", "❌", "❌", "yes"], 1),
     (["<b>PUT</b>", "replace the whole resource", "❌", "✅", "yes"], 1),
     (["<b>PATCH</b>", "change some fields", "❌", "usually not", "yes"], 1),
     (["<b>DELETE</b>", "remove", "❌", "✅", "rarely"], 1)], size=30) + row(
   box("blue", "safe", "doesn't change anything on the server", 2, "flex:1"),
   box("green", "idempotent", "sending it twice = sending it once · safe to <b style=\"display:inline\">retry</b>", 2, "flex:1"), style="margin-top:22px"),
 "steps": [
  "GET reads. It's the only common method that should never change anything.",
  "POST creates or triggers actions. PUT replaces a whole resource, PATCH changes some fields, and DELETE removes.",
  "Two words matter in interviews. Safe means the request changes nothing: only GET, and HEAD and OPTIONS. Idempotent means repeating it has the same effect as doing it once. GET, PUT and DELETE are idempotent, POST isn't. That's why clients and proxies can safely retry a timed out PUT, but must be careful retrying a POST, which could create a duplicate.",
 ]},

{"html": H("Status code ", "families") + table(["Family", "Meaning", "Common ones"], [
     (["<b>2xx</b>", "success", "200 OK · 201 Created · 204 No Content"], 0),
     (["<b>3xx</b>", "go somewhere else", "301 Moved · 304 Not Modified"], 1),
     (["<b>4xx</b>", "<b>client</b> made a mistake", "400 · 401 · 403 · 404 · 409 · 429"], 2),
     (["<b>5xx</b>", "<b>server</b> failed", "500 · 502 · 503"], 3)], size=30) +
   note("401 = who are you? (not logged in) · 403 = I know you, but no", 4),
 "steps": [
  "Status codes come in families, and the first digit tells you a lot. Two hundreds mean success: OK, created, no content.",
  "Three hundreds mean go elsewhere. Moved permanently, or not modified, which lets the browser use its cached copy.",
  "Four hundreds mean the client made a mistake: bad input, not authenticated, not allowed, not found, conflict, or too many requests.",
  "Five hundreds mean the server failed, even though the request was fine. Monitoring alerts usually watch these.",
  "One pair is asked about constantly. Four oh one means the server doesn't know who you are. Four oh three means it knows exactly who you are, and the answer is still no.",
 ]},

{"html": H("Headers that ", "matter") + table(["Header", "Says"], [
     (["<code>Content-Type</code>", "the format of <b>this</b> body: <code>application/json</code>"], 0),
     (["<code>Accept</code>", "the format the client <b>wants back</b>"], 0),
     (["<code>Authorization</code>", "credentials: <code>Bearer &lt;token&gt;</code>"], 1),
     (["<code>Location</code>", "where the created resource lives"], 1),
     (["<code>Cache-Control</code> · <code>ETag</code>", "caching rules · a version tag for 304s"], 2),
     (["<code>Origin</code> + <code>Access-Control-Allow-Origin</code>", "CORS: may this website call this API?"], 3)], size=28),
 "steps": [
  "A handful of headers come up constantly. Content type says the format of the body being sent. Accept says what format the client wants back.",
  "Authorization carries credentials, usually a bearer token. Location, on a two oh one, points at the new resource.",
  "Cache control and E tag drive caching. With an E tag, the client can ask, has this changed? And the server can answer three oh four, not modified, with no body.",
  "And CORS. When a website on one origin calls an API on another, the browser sends the origin, and only lets the page read the response if the server explicitly allows that origin.",
 ]},

{"html": H("Stateless: sessions vs ", "tokens") + row(
   col(box("blue", "stateless", "each request carries everything needed · any server can answer", 0),
       box("orange", "session cookie", "server stores the session · browser sends <code>JSESSIONID</code> · needs shared state across servers", 1), gap=16, style="flex:1"),
   col(box("green", "token (JWT)", "signed, self-contained · sent in <code>Authorization</code> · the server just verifies the signature", 2),
       box("red", "trade-off", "tokens are hard to revoke early · keep them short-lived", 3), gap=16, style="flex:1"), top=True),
 "steps": [
  "HTTP is stateless. Each request must carry everything the server needs. That's what lets you run many copies of a server behind a load balancer: any of them can answer.",
  "But users log in. The classic approach is a session. The server remembers the user, and the browser sends a session cookie. With several servers, they must share the session store.",
  "The modern API approach is a token, often a JWT. It's signed by the server, holds the user's identity, and is sent with every request. The server only verifies the signature, with no lookup.",
  "The trade off: a token is valid until it expires, so revoking it early is hard. Keep tokens short lived, and refresh them.",
 ]},

{"html": H("Designing a REST ", "API") + table(["Do", "Not"], [
     (["<code>GET /api/tasks</code> · <code>POST /api/tasks</code>", "<code>/getTasks</code> · <code>/createTask</code>"], 0),
     (["plural nouns, nested for ownership: <code>/users/7/tasks</code>", "verbs in the path"], 0),
     (["filter, sort, page with the query: <code>?done=false&amp;sort=due&amp;page=0</code>", "a new endpoint per filter"], 1),
     (["version: <code>/api/v1/…</code> or a header", "breaking clients silently"], 2),
     (["one error shape: Problem Details", "a different error format per endpoint"], 3)], size=28),
 "steps": [
  "REST means resources are nouns in the URL, and the HTTP method is the verb. GET slash api slash tasks lists them, POST creates one. Not get tasks or create task in the path.",
  "Use plural nouns, and nest only for clear ownership, like a user's tasks. Filtering, sorting and paging belong in the query string, not in new endpoints.",
  "When you must change the API incompatibly, version it, in the path or with a header, so old clients keep working.",
  "And return errors in one consistent shape. Problem Details is the standard, covered in the validation video.",
 ]},

{"html": H("HTTPS and where Tomcat ", "fits") + row(
   box("green", "HTTPS = HTTP + TLS", "encrypted · the server proves its identity with a certificate", 0, "flex:1"),
   box("blue", "HTTP/2 · HTTP/3", "many requests over one connection · same methods and headers", 1, "flex:1"),
   box("purple", "Tomcat", "the embedded server: sockets, parsing HTTP, threads → hands requests to Spring", 2, "flex:1"), top=True) +
   note("Tools: <code>curl -i</code> · Postman · browser DevTools → Network tab", 3),
 "steps": [
  "HTTPS is HTTP inside a TLS connection. Everything is encrypted, and the server proves who it is with a certificate. In production, it's not optional.",
  "Newer versions, HTTP two and three, send many requests over one connection, more efficiently. But methods, status codes and headers are the same, so your code doesn't change.",
  "And where does Tomcat fit? It's the web server embedded in Spring Boot. It listens on the port, parses the raw HTTP, and hands each request, on a thread, to Spring's dispatcher servlet.",
  "To see all this for real, use curl with dash i to print headers, Postman, or the network tab in your browser's dev tools.",
 ]},

quiz([
  ("Which methods are idempotent?", "<b style=\"display:inline\">GET · PUT · DELETE</b> (not POST)", "blue",
   "Quiz time. Which common HTTP methods are idempotent?",
   "GET, PUT and DELETE. POST is not, because repeating it can create duplicates."),
  ("401 vs 403?", "401 = <b style=\"display:inline\">who are you?</b> · 403 = <b style=\"display:inline\">not allowed</b>", "red",
   "What's the difference between four oh one and four oh three?",
   "Four oh one means not authenticated. Four oh three means authenticated, but not allowed."),
  ("Content-Type vs Accept?", "what I'm <b style=\"display:inline\">sending</b> · what I <b style=\"display:inline\">want back</b>", "green",
   "What's the difference between the content type and accept headers?",
   "Content type describes the body being sent. Accept says which format the client wants in the response."),
]),

recap(["URL: scheme · host · port · path · query",
       "Message: start line · headers · blank line · body",
       "Safe = no change · idempotent = repeat-safe",
       "2xx ok · 4xx client error · 5xx server error",
       "Stateless: sessions vs short-lived tokens",
       "REST: nouns in paths, verbs as methods"],
  "Let's recap. A URL has a scheme, host, port, path and query. Requests and responses share one shape: a start line, headers, a blank line, and a body. Safe methods change nothing, and idempotent ones can be repeated safely. Two hundreds are success, four hundreds are the client's mistake, five hundreds the server's. HTTP is stateless, so logins use sessions or short lived tokens. And REST puts nouns in paths and uses methods as verbs. Now practise with the examples in your notes!"),
]
