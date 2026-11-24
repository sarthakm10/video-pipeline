from lib import *

TAG = "Frontend 28 · Frontend Interview Questions"
FILE = "Frontend 28 Frontend Interview Questions.mp4"


def rapid(t1, t2, cards):
    d = quiz(cards)
    d["html"] = d["html"].replace(H("Quick ", "quiz"), H(t1, t2), 1)
    return d


B = lambda s: f'<b style="display:inline">{s}</b>'

SLIDES = [
title_slide(28, "Frontend Interview Questions", "Rapid-fire answers from the whole course, plus your project story",
  "Welcome to module twenty eight: frontend interview questions.",
  "The final module. Rapid-fire questions from every part of the course, with short answers you can actually say in an interview. For each one, pause and answer it yourself before I do. Then we'll prepare your project story, and a final checklist."),

rapid("HTML and CSS ", "rapid-fire", [
  ("Semantic HTML: why?", "elements for their " + B("meaning") + " · screen readers, SEO, readability", "blue",
   "First, HTML and CSS. What is semantic HTML, and why does it matter?",
   "Using elements for their meaning, like header, nav, main, and button, instead of generic divs. It helps screen readers, search engines, and other developers."),
  ("<code>box-sizing: border-box</code>?", "width " + B("includes") + " padding and border", "green",
   "What does box sizing border box change?",
   "The width and height include padding and border. So a three hundred pixel box stays three hundred pixels wide."),
  ("Flexbox vs Grid?", "one dimension, from content · rows " + B("and") + " columns", "purple",
   "Flexbox versus grid?",
   "Flexbox lays out one dimension, sized from the content. Navbars and toolbars. Grid lays out rows and columns together, from the container. Page layouts and card grids."),
  ("<code>em</code> vs <code>rem</code>?", "own font size, compounds · " + B("root") + ", predictable", "orange",
   "And em versus rem?",
   "Em is relative to the element's own font size, so it compounds. Rem is relative to the root, so it's predictable, and respects the user's browser setting."),
]),

rapid("JavaScript ", "rapid-fire", [
  ("<code>let</code>, <code>const</code>, <code>var</code>?", "block-scoped · " + B("function") + "-scoped, hoisted as undefined", "blue",
   "JavaScript now. Let, const, and var?",
   "Let and const are block scoped, and in the temporal dead zone before their line. Const can't be reassigned. Var is function scoped, and hoisted as undefined. Use const by default."),
  ("What is a closure?", "a function that " + B("remembers") + " its creation scope", "green",
   "What is a closure?",
   "A function that remembers the variables from the scope where it was created, even after that scope finished. It powers private state, debounce, and React hooks."),
  ("How is <code>this</code> set?", "by " + B("how it's called") + " · arrows use the outer one", "purple",
   "How is this determined?",
   "By how a regular function is called. With new, it's the new object. Object dot method, it's the object. A plain call, undefined in strict mode. Arrow functions use the surrounding this."),
  ("The event loop?", "stack empty → " + B("all microtasks") + " → render → one task", "orange",
   "Explain the event loop.",
   "One thread runs the call stack. When it's empty, all queued microtasks run, like promise callbacks. Then the browser may render. Then one task, like a timer, runs. That's why a resolved promise beats a zero millisecond timeout."),
]),

rapid("More ", "JavaScript", [
  ("<code>Promise.all</code> vs <code>allSettled</code>?", "fails fast · waits for " + B("every") + " result", "blue",
   "Promise dot all versus all settled?",
   "All resolves with every value, or rejects as soon as one fails. All settled waits for all of them, and reports each one's status."),
  ("Debounce vs throttle?", "after calls " + B("stop") + " · at most once per interval", "green",
   "Debounce versus throttle?",
   "Debounce runs once, after the calls stop, like a search box. Throttle runs at most once per interval, during continuous calls, like scrolling."),
  ("Event delegation?", "one listener on the " + B("parent") + " · <code>event.target</code>", "purple",
   "What is event delegation?",
   "One listener on a parent handles events from its children, through bubbling. Fewer listeners, and it works for elements added later."),
  ("Shallow vs deep copy?", "top level only · " + B("<code>structuredClone</code>"), "orange",
   "And shallow versus deep copy?",
   "A shallow copy, like spread, copies top level properties and shares nested objects. A deep copy, like structured clone, copies every level."),
]),

rapid("TypeScript ", "rapid-fire", [
  ("<code>any</code> vs <code>unknown</code> vs <code>never</code>?", "no checks · " + B("narrow first") + " · can't exist", "blue",
   "TypeScript. Any versus unknown versus never?",
   "Any switches type checking off. Unknown accepts anything, but must be narrowed before use. And never is a value that can't exist."),
  ("Generics?", "reusable code that " + B("keeps types linked"), "green",
   "What are generics for?",
   "Reusable code that keeps types linked. First of T returns the same type it received, instead of losing it to any."),
  ("Discriminated union?", "a shared " + B("literal tag") + " narrows the shape", "purple",
   "What is a discriminated union?",
   "A union of object types sharing a literal tag, like status. Checking the tag narrows to one shape. Ideal for request states and reducer actions."),
  ("Types at runtime?", B("No") + " · validate API data with Zod", "red",
   "And do TypeScript types exist at runtime?",
   "No. They're erased when compiling. So validate untrusted API responses at runtime, for example with Zod."),
]),

rapid("React ", "rapid-fire", [
  ("Why not the index as a key?", "reorder → state on the " + B("wrong items"), "blue",
   "React. Why do list items need keys, and why not the index?",
   "Keys let React match items between renders, and keep their state. The index changes when the list reorders, so state ends up on the wrong items."),
  ("Why update state immutably?", "React compares " + B("references"), "green",
   "Why must state be updated immutably?",
   "React compares references to detect changes. Mutating keeps the same reference, so the component may not re-render."),
  ("Rules of hooks: why?", "React tracks hooks by " + B("call order"), "purple",
   "What are the rules of hooks, and why?",
   "Only call hooks at the top level, and only from components or custom hooks. Because React identifies each hook by its call order."),
  ("useMemo · useCallback · memo?", "a value · a function · " + B("skip a render"), "orange",
   "Use memo, use callback, and React dot memo?",
   "Use memo caches a value. Use callback caches a function. And React dot memo skips re-rendering a component whose props are shallowly equal. Use them where profiling shows a need."),
]),

rapid("More ", "React", [
  ("What causes a re-render?", "own state · " + B("parent") + " · context", "blue",
   "What causes a component to re-render?",
   "Its state changing, its parent re-rendering, or a context it uses changing."),
  ("Effect cleanup: when?", "before the " + B("next run") + " and on unmount", "green",
   "When does an effect's cleanup run?",
   "Before the effect runs again, and when the component unmounts. To clear timers, listeners, and requests."),
  ("Context vs Zustand?", "every consumer re-renders · " + B("selectors"), "purple",
   "Context versus a store like Zustand?",
   "Context re-renders every consumer on change. A store with selectors re-renders only what changed. And server data belongs in TanStack Query."),
  ("CSR vs SSR?", "built in the browser · " + B("ready HTML") + " + hydration", "orange",
   "And CSR versus SSR?",
   "CSR builds the page in the browser with JavaScript. SSR sends ready HTML from the server for each request, then hydrates it. Faster first paint, and better SEO."),
]),

rapid("Browser and ", "security", [
  ("Typing a URL and pressing Enter?", "DNS · TCP + TLS · HTTP · " + B("DOM + CSSOM → paint"), "blue",
   "Browser, performance and security. What happens when you type a URL and press enter?",
   "A DNS lookup, TCP and TLS handshakes, and the HTTP request. Then the browser parses HTML into the DOM and CSS into the CSSOM, builds the render tree, does layout and paint, and runs JavaScript."),
  ("Why aren't Bearer APIs hit by CSRF?", "the browser " + B("never adds") + " the header", "green",
   "Why are bearer token APIs not affected by CSRF?",
   "Because your code adds the bearer token. The browser never adds it automatically, so forged requests don't carry it."),
  ("What's a preflight?", "an " + B("OPTIONS") + " check before non-simple requests", "purple",
   "What's a CORS preflight?",
   "The options request the browser sends first, for non-simple requests. JSON, PUT or DELETE, or an authorization header."),
  ("An accessible custom dropdown?", "prefer " + B("native select") + " · else button + listbox + keys", "orange",
   "And how do you make a custom dropdown accessible?",
   "Prefer a native select. Otherwise, a button with aria expanded, a listbox of options, arrow keys, enter and escape, and focus returning to the button. Or use Radix or React Aria."),
]),

{"html": H("Your project ", "story") + fill(
   row(box("blue", "1 · what it is", "a task manager with login · Spring Boot + PostgreSQL · React + TypeScript", 0, "flex:1"),
       box("green", "2 · architecture", "REST + JWT · React Router · TanStack Query · RHF + Zod · Vercel", 0, "flex:1")),
   row(box("orange", "3 · a hard problem", "out-of-order search results → AbortController + debounce", 1, "flex:1"),
       box("purple", "4 · a trade-off", "token in localStorage, XSS risk known → next: HttpOnly refresh cookie", 1, "flex:1")),
   box("gray", "5 · results and next", "Vitest + RTL + one Playwright flow · Lighthouse scores · what you'd build next", 2)),
 "steps": [
  "Interviewers will ask, tell me about a project. Have the fullstack task manager ready, as a two minute story. First, what it is. A task manager with login, built with Spring Boot and PostgreSQL, and React with TypeScript. Then your architecture. A REST API with JWT auth, React Router, TanStack Query, React Hook Form with Zod, and deployed on Vercel.",
  "Then one hard problem you solved. For example, search results arrived out of order, and you fixed the race condition with an abort controller and debouncing. And a trade-off you made consciously. You kept the token in local storage for simplicity, you know the XSS risk, and the next step is an HttpOnly refresh cookie.",
  "And finish with results and what's next. Your tests, your Lighthouse scores, and what you'd build next. Interviewers remember a clear technical story more than a list of tools.",
 ]},

{"html": H("Final ", "checklist") + row(
   col(box("blue", "portfolio", "live links + README · every UX state · works on a phone · Lighthouse a11y 90+ · tests in CI · no secrets", 0), style="flex:1"),
   col(pts([("Explain the event loop, closures, <code>this</code>, promises", 1),
            ("Write debounce, throttle, <code>Promise.all</code>, deep clone", 1),
            ("Explain re-renders, keys, effects, hook rules", 1),
            ("Build a todo app + debounced search in an hour", 1),
            ("Walk through RADIO · explain CORS, JWT, XSS, CSRF", 1),
            ("Your project story, timed at two minutes", 1)], size=29), style="flex:1.4"), top=True),
 "steps": [
  "Your portfolio checklist. Live links for the frontend and the API, and a GitHub repo with a clear README. Loading, empty, and error states everywhere, and it works on a phone. Ninety plus for accessibility in Lighthouse. A few meaningful tests, running in CI. And no secrets in the repo.",
  "And your final interview checklist. Explain the event loop, closures, this, and promises out loud. Write debounce, throttle, promise dot all, and a deep clone from memory. Explain re-renders, keys, effects, and the rules of hooks. Build a todo app and a debounced search in under an hour. Walk through a system design with RADIO, and explain CORS, JWT storage, XSS, and CSRF. And time your project story at two minutes.",
 ]},

recap(["Rapid-fire answers: short, then an example",
       "Go-to project: the fullstack Task Manager",
       "Story: what, architecture, hard problem, trade-off, results",
       "Explain: event loop, closures, this, promises",
       "Write: debounce, throttle, Promise.all, deep clone",
       "Design with RADIO · explain CORS, JWT, XSS, CSRF"],
  "Let's recap. Give short answers, then an example. Your go-to project is the fullstack task manager, told as a story: what it is, the architecture, a hard problem, a trade-off, and results. Be ready to explain the event loop, closures, this, and promises. Write debounce, throttle, promise dot all, and a deep clone from memory. And design with RADIO, and explain CORS, JWT, XSS, and CSRF. You've gone from your first HTML page to designing frontend systems. Together with Java and Spring, that's genuinely fullstack. Next up: the project, building the task manager UI!"),
]
