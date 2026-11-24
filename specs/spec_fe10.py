from lib import *

TAG = "Frontend 10 · Asynchronous JavaScript"
FILE = "Frontend 10 Asynchronous JavaScript.mp4"

def arrow(label, step):
    return f'<div class="arrow" data-step="{step}">{label}</div>'

SLIDES = [
title_slide(10, "Asynchronous JavaScript", "One thread, never blocking: the event loop, promises and async/await",
  "Welcome to module ten: asynchronous JavaScript.",
  "JavaScript runs on one thread. Yet a page can fetch data, run timers, and respond to clicks, all at once. The event loop is how. Then promises and async await let you write wait for the server code that reads top to bottom. This is the most important module for calling your Spring Boot API."),

{"html": H("Why ", "async", "?") + code("""console.log("1. ask the server");
fetch("/api/tasks").then(() => console.log("3. data arrived"));
console.log("2. carry on immediately");
§1 // prints 1, 2, 3""", 34) + row(
   box("red", "one main thread", "runs your JS, handles clicks, repaints the page · block it → page freezes", 0, "flex:1"),
   box("blue", "Java / Spring", "blocks a thread per request · many threads", 2, "flex:1"),
   box("green", "browser", "only one thread · never block · start work, get called back", 2, "flex:1"), style="margin-top:30px"),
 "steps": [
  "The browser runs your JavaScript, handles clicks, and repaints the page, all on one main thread. If your code takes three seconds, the page freezes for three seconds. No scrolling, no clicks, nothing. So slow things like network requests and timers don't block. You start them, and give a function to run when they finish.",
  "So this prints one, two, then three. The fetch starts, the code carries on immediately, and the callback runs later, when the data arrives. The browser does the waiting itself, outside your JavaScript.",
  "Compare that with Spring. There, you'd usually block a thread while waiting for the database, and the server has many threads. In the browser there's only one, so blocking is never an option. Java's completable future is the closest cousin of a JavaScript promise.",
 ]},

{"html": H("The event ", "loop") + row(
   box("blue", "call stack", "what's running now", 0, "width:300px"), arrow("empty?", 1),
   box("purple", "ALL microtasks", "<code>.then</code>, code after <code>await</code>", 1, "width:340px"), arrow("", 2),
   box("gray", "maybe render", "repaint the page", 2, "width:280px"), arrow("", 3),
   box("orange", "ONE task", "<code>setTimeout</code>, click, network", 3, "width:320px"), gap=10, style="align-items:center;margin-top:40px") +
   note("↺ then all microtasks again · <u>microtasks always run before the next task</u>", 4, "margin-top:60px;font-size:40px"),
 "steps": [
  "Here's how the event loop works. The call stack holds the functions running right now, one at a time. Meanwhile, the browser's web APIs handle timers, network requests and events in the background.",
  "When the call stack is empty, the loop runs all the microtasks. Those are promise callbacks: dot then, and the code after an await.",
  "Then the browser may repaint the page.",
  "Then it takes one task from the task queue. That's a set timeout callback, a click handler, or network I/O.",
  "And then it's back to all the microtasks again. So the key rule is this. Microtasks always run before the next task. That rule is behind every what's the output question.",
 ]},

predict(("What's the ", "output", "?"), [
  ('console.log("A");<br>setTimeout(() =&gt; log("B"), 0);<br>Promise.resolve().then(() =&gt; log("C"));<br>console.log("D");',
   "A, D, C, B", "sync first · then microtask C · then task B, even with delay 0",
   "Pause and predict. Log A. Set timeout B, with zero delay. A promise then C. And log D. What order?",
   "A, D, C, B. A and D are synchronous, so they run first. Then the microtask C. Then the task B, even though its delay was zero. Set timeout zero means as soon as possible after the current work, and all the microtasks. Not now."),
], size=30),

{"html": H("Callback ", "hell") + code("""getUser(id, (err, user) => {
  if (err) return showError(err);
  getTasks(user.id, (err, tasks) => {
    if (err) return showError(err);
    getComments(tasks[0].id, (err, comments) => {
      if (err) return showError(err);
      render(user, tasks, comments);    // three levels deep
    });
  });
});""", 31) + note("Hard to read · errors handled at every level · hard to run in parallel or cancel", 1),
 "steps": [
  "The original async style passes a function to call when the work is done. But when each step depends on the previous one, callbacks nest deeper and deeper. This is the pyramid of doom.",
  "It's hard to read, you handle errors at every level, and it's hard to run steps in parallel, or cancel them. Promises fix all of this.",
 ]},

{"html": H("", "Promises") + row(
   col(box("yellow", "pending", "waiting…", 0),
       row(box("green", "fulfilled", "<code>resolve(value)</code>", 0, "flex:1"), box("red", "rejected", "<code>reject(error)</code>", 0, "flex:1"), gap=16),
       note("settled = never changes again", 0, "margin-top:6px;font-size:32px"), style="width:620px"),
   code("""§1 fetch("/api/tasks")
§1   .then(res => res.json())
§1   .then(tasks => render(tasks))
§2   .catch(err => showError(err))
§2   .finally(() => hideSpinner());

§3 const wait = (ms) =>
§3   new Promise(resolve =>
§3     setTimeout(resolve, ms));""", 30, style="flex:1"), top=True),
 "steps": [
  "A promise is an object for a value that will arrive later. It starts pending. Then it's either fulfilled, with a value, or rejected, with an error. Once it's settled, it never changes again.",
  "Fetch returns a promise. Each dot then returns a new promise, so they chain flat, instead of nesting. If a then callback returns a promise, the chain waits for it.",
  "One catch at the end handles a failure anywhere above it. And finally runs either way. Perfect for hiding a loading spinner.",
  "You can make your own promise too, mostly to wrap older callback APIs. Wait returns a promise that resolves after some milliseconds. And a rejection that's never caught shows uncaught in promise in the console.",
 ]},

{"html": H("async and ", "await") + code("""async function loadDashboard(userId) {
  try {
§1     const user = await getUser(userId);    // pauses this function, not the page
§1     const tasks = await getTasks(user.id);
§1     return { user, tasks };                 // always returns a promise
  } catch (error) {
§2     console.error("Couldn't load", error);
§2     throw error;
  } finally {
    hideSpinner();
  }
}""", 31),
 "steps": [
  "Async await is syntax over promises that reads like normal, top to bottom code. Put async before a function, and it always returns a promise.",
  "Await pauses that function until the promise settles, then gives you its value. Only this function pauses. The page, and all your other code, keeps running.",
  "And errors are caught with an ordinary try catch. No dot catch needed.",
 ]},

{"html": H("Don't await one ", "by one") + code("""§0 // Slow: ~2 s
§0 const user = await getUser(id);
§0 const settings = await getSettings(id);

§1 // Fast: ~1 s, both at the same time
§1 const [user, settings] = await Promise.all([getUser(id), getSettings(id)]);

§2 tasks.forEach(async t => await save(t));   // ✗ doesn't wait
§2 for (const t of tasks) await save(t);       // ✓ one by one
§2 await Promise.all(tasks.map(save));         // ✓ in parallel""", 31),
 "steps": [
  "A very common mistake. If two requests don't depend on each other, don't await them one by one. If each takes a second, this takes two seconds.",
  "Start both at once with promise dot all, and it takes one second. Both requests run at the same time.",
  "And watch out for await inside for each. For each ignores the promises, so it doesn't wait at all. Use for of to go one by one, or promise dot all with map, to go in parallel.",
 ]},

{"html": H("", "fetch", ": calling your API") + code("""async function createTask(title) {
  const res = await fetch(`${API}/tasks`, {
§0     method: "POST",
§0     headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
§0     body: JSON.stringify({ title }),
  });
§1   if (!res.ok) throw new Error(`HTTP ${res.status}`);   // 404 / 500 don't throw!
  return res.json();                                     // 201 Created
}""", 29) + note("<code>fetch</code> only rejects on <u>network</u> failure · always check <code>res.ok</code>", 1),
 "steps": [
  "Fetch is the browser's built-in HTTP client. To call a Spring Boot endpoint with a POST, pass the method, the headers, with the content type and your token, and the body, as a JSON string.",
  "And here's the big gotcha. Fetch only rejects on a network failure, like the server being down, or CORS blocking it. A four oh four, or a five hundred, is a successful fetch! The response just has ok set to false. So always check res dot ok. Many teams use axios instead, which throws on errors automatically.",
 ]},

{"html": H("Cancelling with ", "AbortController") + code("""const controller = new AbortController();
fetch(`${API}/search?q=java`, { signal: controller.signal })
  .catch(err => { if (err.name !== "AbortError") throw err; });

§1 controller.abort();      // the fetch rejects with an AbortError""", 32) +
   note("The user typed again, or left the page → cancel the old request (React effect cleanups, module 17)", 2),
 "steps": [
  "Sometimes you need to cancel a request. Create an abort controller, and pass its signal to fetch.",
  "Call abort, and the fetch rejects with an abort error, which you can safely ignore.",
  "You'll use this when the user types again before a search finishes, or leaves the page. React apps do this in effect cleanups, in module seventeen.",
 ]},

{"html": H("Waiting for ", "several") + table(["Method", "Resolves", "Rejects", "Use it for"], [
   (["<code>Promise.all</code>", "all succeed", "any fails (fast)", "everything the page needs"], 0),
   (["<code>allSettled</code>", "all finish", "never", "widgets that fail alone"], 1),
   (["<code>race</code>", "first to settle", "first settles with a failure", "a timeout"], 2),
   (["<code>any</code>", "first success", "all fail", "fastest mirror"], 3)], size=31),
 "steps": [
  "There are four ways to wait for several promises. Promise dot all resolves when all of them succeed, with an array of values in order. But if any one fails, it fails fast.",
  "All settled waits for every result, success or not, and never rejects. Great for a dashboard where each widget can fail on its own.",
  "Race settles with whichever finishes first. Race a fetch against a five second timer, and you've got a timeout.",
  "And any resolves with the first success, and only fails if they all fail. Writing promise dot all yourself is a common interview question, in module twelve.",
 ]},

quiz([
  ("Does <code>fetch</code> reject on a 404?", "<b style=\"display:inline\">No</b> · check <code>res.ok</code>", "red",
   "Quiz time. Does fetch reject on a four oh four?",
   "No! It only rejects on network failures. Check res dot ok."),
  ("What does an <code>async</code> function return?", "Always a <b style=\"display:inline\">promise</b>", "blue",
   "What does an async function return?",
   "Always a promise."),
  ("<code>all</code> vs <code>allSettled</code>?", "all fails fast · allSettled waits for every result", "green",
   "Promise all versus all settled?",
   "All fails fast on any rejection. All settled waits for every result."),
]),

recap(["One thread: start slow work, get called back",
       "Microtasks (promises) run before the next task",
       "A, D, C, B · <code>setTimeout(fn, 0)</code> isn't \"now\"",
       "Promises chain flat · one <code>.catch</code>",
       "async/await + try/catch · <code>Promise.all</code> for parallel",
       "fetch: check <code>res.ok</code> · cancel with AbortController"],
  "Let's recap. JavaScript has one thread, so you start slow work and get called back. Promise callbacks are microtasks, and they run before the next task. So the answer is A, D, C, B, and set timeout zero isn't now. Promises chain flat, with one catch. Async await reads top to bottom, with try catch, and promise dot all runs things in parallel. And with fetch, always check res dot ok, and cancel with an abort controller. Next time: modules, npm, and tooling!"),
]
