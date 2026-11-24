from lib import *

TAG = "Frontend 22 · React Internals and Modern React"
FILE = "Frontend 22 React Internals and Modern React.mp4"

SLIDES = [
title_slide(22, "React Internals & Modern React", "How React works under the hood, and what's new",
  "Welcome to module twenty two: React internals and modern React.",
  "Senior frontend interviews ask how React works, not just how to use it. This module covers the virtual DOM and reconciliation, Fiber and concurrent rendering, suspense and error boundaries, the rendering strategies, Next.js and server components, and what React nineteen adds."),

{"html": H("Virtual DOM and ", "reconciliation") + code("""§0 { type: "li", props: { className: "task", children: "Learn React" } }""", 28) +
   row(box("blue", "heuristic 1 · different type", "<code>div</code> → <code>section</code>: destroy the old subtree and its state", 1, "flex:1"),
       box("green", "heuristic 2 · keys", "match children across renders: move, insert, delete", 1, "flex:1"), style="margin:22px 0") +
   code("""§2 Before: <li key="a">A</li> <li key="b">B</li>
§2 After:  <li key="c">C</li> <li key="a">A</li> <li key="b">B</li>
§2 keys:    insert "c" · reuse a and b            → 1 DOM insertion
§2 indexes: "A"→"C", "B"→"A", add "B"             → 2 changes + 1 insertion""", 26) +
   note("Not \"faster than the DOM\" · declarative code that's <u>fast enough</u>, automatically", 3),
 "steps": [
  "JSX produces React elements. Lightweight JavaScript objects describing what should be on screen. The tree of them is often called the virtual DOM. On each update, React builds a new tree and compares it with the old one. That diff is called reconciliation.",
  "A perfect tree diff is far too slow, so React uses two heuristics, which make it linear. One: different element types produce different trees. If a div becomes a section, React destroys the old subtree, with its state. Two: keys identify children across renders.",
  "Here's why keys matter. Insert C at the start. With keys, React inserts one node, and reuses A and B. With indexes, it rewrites two items and adds a third.",
  "And a common misconception. The virtual DOM isn't faster than the DOM. Hand-written updates can be faster. Its value is that you write simple declarative code, and get updates that are fast enough, automatically.",
 ]},

{"html": H("Fiber and ", "concurrent", " rendering") + row(
   col(box("purple", "Fiber", "one node per component: type, props, state, hooks, links to parent, child, sibling", 0),
       box("blue", "interruptible", "render in small units · pause, resume, prioritise, abandon", 0),
       box("orange", "commit is atomic", "never a half-updated screen · so renders must be <b style=\"display:inline\">pure</b>", 1), style="width:600px"),
   code("""§2 async function save() {
§2   const task = await createTask(form);
§2   setTasks(ts => [...ts, task]);
§2   setForm(empty);
§2   setSaving(false);
§2 }   // three updates → one re-render
§3 flushSync(() => setTasks(...));  // rare: update now""", 27, style="flex:1"), top=True),
 "steps": [
  "Fiber is React's internal engine. Each component instance has a fiber, a node holding its type, props, state, hooks, and links to its parent, child, and sibling. Because rendering walks this structure in small units, React can pause, resume, prioritise, or abandon work. That's concurrent rendering. Typing can interrupt filtering a big list. You opt in with use transition and use deferred value.",
  "The render phase can be interrupted, but the commit is always done in one go, so users never see a half-updated screen. That's why components must be pure. A render may run, be thrown away, and run again.",
  "And automatic batching. Several state updates in the same event, timeout, or promise callback produce just one re-render.",
  "In the rare case you need the DOM updated right away, like scrolling to a just-added item, flush sync forces it.",
 ]},

{"html": H("Suspense and error ", "boundaries") + row(
   col(code("""§0 <Suspense fallback={<TaskListSkeleton />}>
§0   <TaskList />     {/* suspends until ready */}
§0 </Suspense>""", 27),
       code("""§1 <ErrorBoundary fallback={<p>Something went wrong.</p>}>
§1   <TaskList />
§1 </ErrorBoundary>""", 27), style="flex:1"),
   col(box("blue", "Suspense", "loading states by <b style=\"display:inline\">where</b> you put boundaries", 0),
       box("green", "error boundary", "a render error shows a fallback, not a blank page", 1),
       box("red", "doesn't catch", "event handlers · async code · itself → try/catch", 2), style="width:520px"), top=True),
 "steps": [
  "Suspense shows a fallback while something inside isn't ready. Lazy code, or data from libraries that support it. You declare loading states by where you put the boundaries, instead of if loading in every component. Nested boundaries let the page appear piece by piece.",
  "Error boundaries catch errors thrown while rendering a subtree, and show a fallback. Without one, an uncaught render error unmounts the whole app, and you get a blank white page. They're still class components underneath, so most people use the react error boundary library.",
  "But they don't catch errors in event handlers, in async code, or in the boundary itself. Use try catch for those. And put boundaries around independent sections, so one failure doesn't take down the page.",
 ]},

{"html": H("CSR, SSR, SSG and ", "hydration") + table(["", "HTML built", "First paint", "Good for"], [
   (["<b>CSR</b>", "in the browser", "after JS runs", "apps behind a login (Vite)"], 0),
   (["<b>SSR</b>", "on the server, per request", "fast, real content", "personalised public pages"], 0),
   (["<b>SSG</b>", "at build time", "fastest, from a CDN", "blogs, docs, marketing"], 0),
   (["<b>ISR</b>", "build time + rebuilt every N s", "fast", "catalogues, news"], 0)], size=28) +
   row(box("green", "hydration", "attach handlers to server HTML", 1, "flex:1"),
       box("red", "mismatch", "<code>Date.now()</code>, <code>Math.random()</code>, <code>window</code> in render → move to useEffect", 2, "flex:1"),
       box("blue", "streaming SSR", "HTML in chunks as Suspense resolves", 3, "flex:1"), style="margin-top:24px"),
 "steps": [
  "Where and when is the HTML produced? Client side rendering builds it in the browser, so the first paint waits for JavaScript. Great for apps behind a login. Server side rendering builds it on the server for each request. Static generation builds it once, at build time. And incremental static regeneration rebuilds static pages in the background.",
  "With SSR and SSG, the browser gets ready-made HTML first. Then React hydrates it. It attaches event handlers and state to the existing HTML, instead of rebuilding it.",
  "A hydration mismatch happens when the server's HTML differs from the client's first render. Typical causes: the current time, random values, or reading window during render. Move browser-only logic into an effect.",
  "And streaming SSR sends HTML in chunks, as suspense boundaries resolve. So slow data doesn't hold up the whole page.",
 ]},

{"html": H("Next.js and Server ", "Components") + row(code("""§0 // app/tasks/page.tsx · a Server Component
§0 export default async function TasksPage() {
§0   const tasks = await fetch(API + "/tasks").then(r => r.json());
§0   return <main><TaskFilter /><ul>{…}</ul></main>;
§0 }
§1 // app/tasks/TaskFilter.tsx
§1 "use client";
§1 export function TaskFilter() {
§1   const [q, setQ] = useState("");
§1   return <input value={q} onChange={…} />;
§1 }""", 26, style="flex:1"),
   col(table(["Server", "Client"], [
     (["async, data, secrets", "state, effects, events"], 2),
     (["zero JS shipped", "code ships to browser"], 2)], size=26), style="width:560px;flex-shrink:0"), top=True) +
   note("Login-only app + Spring Boot → a Vite SPA is simpler · Next.js for SEO and fast public pages", 3),
 "steps": [
  "Next.js is the most popular React framework. Routing by folders, server rendering, static generation, and production defaults. Its app router is built on React server components. They run only on the server. They can be async, fetch data directly, and use secrets. And their code is never sent to the browser.",
  "Add use client at the top of a file, and it's a client component. It can use state, effects, and event handlers.",
  "So keep most of the tree on the server, and only the interactive leaves on the client. Smaller bundles and faster loads.",
  "With a Spring Boot backend and an app behind a login, like the task manager, a Vite single page app is simpler, and very common. Choose Next.js when you need SEO, or fast first loads for public pages.",
 ]},

{"html": H("What's new in React ", "19") + code("""§0 const [error, submitAction, isPending] = useActionState(
§0   async (_prev, formData: FormData) => { await createTask(…); return null; }, null);
§0 <form action={submitAction}> … <button disabled={isPending}>Add</button></form>

§1 const [optimisticTasks, addOptimistic] = useOptimistic(tasks,
§1   (current, title: string) => [...current, { id: -1, title, done: false }]);

§2 const theme = use(ThemeContext);     // can be called inside conditions""", 26) +
   row(box("gray", "smaller", "<code>ref</code> is a prop · <code>&lt;Context&gt;</code> as provider · <code>&lt;title&gt;</code> hoisted", 3, "flex:1"),
       box("purple", "React Compiler", "adds memoisation at build time", 3, "flex:1"), style="margin-top:22px"),
 "steps": [
  "React nineteen adds actions. Pass an async function to a form's action. With use action state, React handles the pending state, errors, and resetting the form.",
  "Use optimistic shows the expected result immediately, while the request runs, and rolls back automatically if it fails.",
  "Use reads a promise, with suspense, or a context. And unlike other hooks, it can be called inside conditions.",
  "Smaller changes. Ref is now a normal prop, so no more forward ref. And the React compiler analyses your components at build time, and adds memoisation automatically. It relies on components following the rules, one more reason to follow them.",
 ]},

quiz([
  ("Is the virtual DOM faster than the DOM?", "<b style=\"display:inline\">Not inherently</b> · fast enough, declaratively", "orange",
   "Quiz time. Is the virtual DOM faster than direct DOM updates?",
   "Not inherently. It makes declarative updates fast enough."),
  ("What does an error boundary miss?", "event handlers · async code", "red",
   "What does an error boundary not catch?",
   "Errors in event handlers, and in async code."),
  ("Server vs Client Component?", "data, no JS shipped · state, effects, events", "blue",
   "And server component versus client component?",
   "Server components fetch data and ship no JavaScript. Client components have state, effects, and events."),
]),

recap(["Reconciliation: diff element trees · type + key heuristics",
       "Fiber: interruptible rendering · commit is atomic",
       "Automatic batching · one re-render",
       "Suspense for loading · error boundaries for render errors",
       "CSR · SSR · SSG · ISR · hydration",
       "Server Components · React 19 actions · the Compiler"],
  "Let's recap. Reconciliation diffs element trees, using types and keys. Fiber makes rendering interruptible, while the commit is atomic. Automatic batching turns several updates into one re-render. Suspense handles loading, and error boundaries catch render errors. You know CSR, SSR, SSG, ISR, and hydration. And server components, React nineteen actions, and the compiler are modern React. Next time: testing frontend code!"),
]
