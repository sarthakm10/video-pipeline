from lib import *

TAG = "Frontend 25 · Web Security and Browser APIs"
FILE = "Frontend 25 Web Security and Browser APIs.mp4"

SLIDES = [
title_slide(25, "Web Security & Browser APIs", "XSS, CSRF, tokens, CORS, CSP, and the APIs behind modern apps",
  "Welcome to module twenty five: web security and browser APIs.",
  "The browser runs code from many places, so it has strict security rules. And attackers look for gaps in how your frontend and backend use them. This module covers the attacks that matter, XSS and CSRF, where to keep tokens, CORS and CSP in depth, and the browser storage and background APIs you'll meet."),

{"html": H("", "XSS", ": cross-site scripting") + table(["Kind", "The script comes from"], [
     (["Stored", "your database: a comment, a task title"], 0),
     (["Reflected", "the URL: <code>?q=&lt;script&gt;</code>"], 0),
     (["DOM-based", "frontend code inserting it unsafely"], 0)], size=29) +
   row(code("""§1 <div dangerouslySetInnerHTML={{ __html: c }} />  // ❌
§1 <a href={userWebsite}>  // ⚠️ javascript: URL
§1 el.innerHTML = value;   // ❌""", 27, style="flex:1"),
       box("green", "defences", "text by default · <b style=\"display:inline\">DOMPurify</b> · only http/https links · CSP · HttpOnly cookies", 2, "width:520px"), top=True, style="margin-top:24px"),
 "steps": [
  "XSS is an attacker getting their JavaScript to run in your page. Once it runs, it can do anything the user can. Read the page, read local storage, including tokens, and call your API as them. The script can be stored in your database, like a comment. Reflected from the URL. Or inserted by frontend code, unsafely.",
  "React escapes by default. Anything in curly braces is inserted as text. The dangerous exits are the ones React names loudly. Dangerously set inner HTML runs any HTML in it. A user's link can be a javascript colon URL. And plain inner HTML.",
  "So render user content as text. If you truly need user HTML, sanitise it with DOMPurify first. Allow only http and https links. And add a content security policy, and HttpOnly cookies, as a second line of defence.",
 ]},

{"html": H("", "CSRF", " and SameSite") + row(code("""§0 <!-- on evil.example -->
§0 <form action="https://bank.example/api/transfer"
§0       method="POST">
§0   <input type="hidden" name="to" value="attacker">
§0 </form>
§0 <script>document.forms[0].submit()</script>""", 26, style="flex:1"),
   col(box("blue", "SameSite=Lax / Strict", "no cookie on cross-site POSTs", 1),
       box("green", "CSRF tokens", "a random token other sites can't read", 1),
       box("purple", "Bearer header", "never sent automatically → no classic CSRF", 2), style="width:520px"), top=True),
 "steps": [
  "CSRF, cross-site request forgery, tricks a logged in user's browser into sending a request to your site, from another site. It works because browsers attach your site's cookies automatically. The attacker can't read the response, but the request happens, with the victim's cookie.",
  "The defences. Same site cookies. Lax, now the browser default, doesn't send the cookie on cross-site posts. Strict never sends it cross-site. And CSRF tokens, a random value every change must include, which another site can't read. And never change data on a GET.",
  "Here's the connection to tokens. A JWT sent in the authorization header isn't vulnerable to classic CSRF, because the browser never adds that header by itself. That's why stateless JWT APIs often disable Spring's CSRF protection. Move the token into a cookie, and CSRF is back.",
 ]},

{"html": H("Where to keep ", "tokens") + table(["", "localStorage + header", "HttpOnly cookie"], [
   (["Readable by JS", "<b>yes</b>: any XSS steals it", "no"], 0),
   (["Sent automatically", "no", "yes"], 0),
   (["CSRF risk", "none", "yes · SameSite + tokens"], 0),
   (["Simplicity", "simplest", "more setup"], 0)], size=28) +
   code("""§1 access token  → in memory, 5–15 min, Bearer header
§1 Set-Cookie: refresh_token=…; HttpOnly; Secure; SameSite=Strict; Path=/api/auth/refresh""", 25, style="margin-top:24px"),
 "steps": [
  "Local storage, with an authorization header, is the simplest. No CSRF risk. But any XSS can read and steal the token. An HttpOnly cookie can't be read by JavaScript at all. But it's sent automatically, so you need same site and CSRF tokens.",
  "The widely recommended setup for sensitive apps combines them. A short-lived access token, kept in memory, not local storage, and sent as a bearer header. And a long-lived refresh token, in an HttpOnly, secure, same site cookie, used only by the refresh endpoint. A stolen access token lasts minutes, and the refresh token can't be read at all. Many apps start with local storage for simplicity. Just know the trade-off, and how to explain it.",
 ]},

{"html": H("CORS in ", "depth") + row(
   col(box("gray", "simple request", "GET / POST with basic headers · sent directly", 0),
       box("orange", "preflight", "PUT, DELETE, JSON, <code>Authorization</code> → <code>OPTIONS</code> first", 1),
       box("red", "not API security", "protects users' browsers · curl ignores it", 3), style="width:520px"),
   col(code("""§1 OPTIONS /api/tasks
§1 Origin: https://app.com
§1 Access-Control-Request-Method: POST
§1 → 204 Access-Control-Allow-Origin: https://app.com""", 25),
       code("""§2 fetch(url, { credentials: "include" });
§2 Access-Control-Allow-Origin: https://app.com  // not *
§2 Access-Control-Allow-Credentials: true""", 25), style="flex:1"), top=True),
 "steps": [
  "The same origin policy stops a page from reading responses from another origin. Scheme, host, and port. CORS is how a server opts in. Simple requests, a GET or POST with basic headers, are sent directly, and the browser checks the response.",
  "Anything else, like a PUT, a JSON content type, or an authorization header, first triggers a preflight. An automatic options request asking permission. If the server allows the origin, method, and headers, the real request follows.",
  "Cookies across origins need both sides to agree. Fetch with credentials include, and the server must name the exact origin, never a star, and allow credentials.",
  "And remember, CORS is not a security feature for your API. It protects users' browsers. Anyone can still call your API from curl. Authentication is what protects the data.",
 ]},

{"html": H("CSP and ", "HTTPS") + row(code("""§0 Content-Security-Policy:
§0   default-src 'self';
§0   script-src 'self';
§0   img-src 'self' data: https:;
§0   connect-src 'self' https://api.mytasks.com;
§0   frame-ancestors 'none'""", 27, style="flex:1"),
   col(box("green", "no 'unsafe-inline'", "injected scripts won't run", 0),
       box("blue", "connect-src", "stolen data can't be sent away", 0),
       box("purple", "HTTPS + HSTS", "encrypted · never plain HTTP again", 1),
       box("gray", "also", "<code>nosniff</code> · Referrer-Policy · <code>npm audit</code>", 2), style="width:500px"), top=True),
 "steps": [
  "A content security policy tells the browser which sources of scripts, styles, images, and connections are allowed. Without unsafe inline, inline scripts are blocked, which kills most XSS. Connect source limits where fetch can send data. And frame ancestors none stops clickjacking. Roll it out with report only mode first.",
  "HTTPS encrypts traffic, so nobody on public wifi can read or change it, including tokens. And HSTS tells browsers never to connect over plain HTTP again.",
  "Also set headers like no sniff, and a referrer policy. Spring Security adds several by default. And keep dependencies updated with npm audit, or Dependabot.",
 ]},

{"html": H("Browser ", "storage") + table(["Storage", "Size", "API", "Use for"], [
   (["Cookies", "~4 KB", "sent with requests", "refresh tokens (HttpOnly)"], 0),
   (["localStorage", "~5 MB", "sync, strings", "theme, last tab"], 0),
   (["sessionStorage", "~5 MB", "sync, per tab", "per-tab drafts"], 0),
   (["<b>IndexedDB</b>", "large", "async, objects, files", "offline data, big caches"], 1),
   (["Cache Storage", "large", "request → response", "offline pages, assets"], 1)], size=29),
 "steps": [
  "Where should data live in the browser? Cookies are tiny, and sent with every request. Good for HttpOnly refresh tokens. Local storage holds about five megabytes of strings, synchronously, until cleared. Good for small preferences. And session storage is the same, but per tab.",
  "For anything bigger, IndexedDB stores objects and files, asynchronously. Good for offline data. The small i d b library wraps its awkward API in promises. And cache storage keeps request and response pairs, for offline copies, with a service worker.",
 ]},

{"html": H("Service workers and web ", "workers") + row(
   col(box("blue", "service worker", "between page and network · offline · caching strategies · push", 0),
       box("purple", "PWA", "service worker + manifest → installable · vite-plugin-pwa", 0),
       box("orange", "web worker", "a <b style=\"display:inline\">separate thread</b> · no DOM · messages only", 1), style="width:520px"),
   code("""§1 const worker = new Worker(
§1   new URL("./parse-worker.js", import.meta.url),
§1   { type: "module" });
§1 worker.postMessage(csvText);
§1 worker.onmessage = e => showRows(e.data);

§1 // parse-worker.js
§1 self.onmessage = e => {
§1   const rows = e.data.split("\\n").map(l => l.split(","));
§1   self.postMessage(rows);
§1 };""", 26, style="flex:1"), top=True) +
   note("Also: IntersectionObserver · ResizeObserver · BroadcastChannel · History API", 2),
 "steps": [
  "Service workers sit between your page and the network, and run in the background, even when the page is closed. They enable offline support, caching strategies like cache first or stale while revalidate, and push notifications. Add a manifest with a name and icons, and your site becomes an installable progressive web app.",
  "Web workers are different. They run JavaScript on a separate thread, so heavy work, like parsing a huge CSV, doesn't freeze the page. They can't touch the DOM. They only talk by messages.",
  "Other APIs worth knowing. Intersection observer detects when an element scrolls into view, for lazy loading and infinite scroll. Resize observer, broadcast channel for talking between tabs, and the history API that routers use.",
 ]},

quiz([
  ("When is React exposed to XSS?", "<code>dangerouslySetInnerHTML</code> · <code>javascript:</code> URLs · innerHTML", "red",
   "Quiz time. When is React exposed to XSS?",
   "Dangerously set inner HTML, javascript colon URLs, and direct inner HTML."),
  ("What triggers a preflight?", "PUT / DELETE · JSON · <code>Authorization</code>", "orange",
   "What triggers a CORS preflight?",
   "Non-simple requests. A PUT or DELETE, a JSON content type, or an authorization header."),
  ("Service worker vs web worker?", "network proxy · background thread", "blue",
   "And service worker versus web worker?",
   "A service worker is a network proxy, for offline and caching. A web worker is a background thread, for computation."),
]),

recap(["XSS: render as text · DOMPurify · CSP",
       "CSRF: SameSite cookies · CSRF tokens",
       "Access token in memory + HttpOnly refresh cookie",
       "Preflight for non-simple requests · CORS protects browsers",
       "CSP · HTTPS + HSTS · security headers",
       "IndexedDB · service workers · web workers"],
  "Let's recap. Prevent XSS by rendering user content as text, sanitising with DOMPurify, and adding a CSP. Prevent CSRF with same site cookies and CSRF tokens. A strong token setup keeps the access token in memory, and the refresh token in an HttpOnly cookie. Non-simple requests trigger a preflight, and CORS protects browsers, not your API. Use CSP, HTTPS with HSTS, and security headers. And know IndexedDB, service workers, and web workers. Next time: frontend system design!"),
]
