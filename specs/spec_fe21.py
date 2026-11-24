from lib import *

TAG = "Frontend 21 · React Performance"
FILE = "Frontend 21 React Performance.mp4"

SLIDES = [
title_slide(21, "React Performance", "Find the slow part, then apply the matching fix",
  "Welcome to module twenty one: React performance.",
  "React is fast by default, and most apps never need tuning. When one does, it's almost always the same few causes. Components re-rendering for no reason, huge lists, or too much JavaScript loaded up front. This module shows how rendering works, how to find the slow part, and the fix for each cause."),

{"html": H("Render, then ", "commit") + fill(
   row(box("gray", "trigger", "a state change", 0, "flex:1"), '<div class="arrow" data-step="0" style="min-width:60px"></div>',
       box("blue", "render phase", "call components · diff the trees", 0, "flex:1"), '<div class="arrow" data-step="0" style="min-width:60px"></div>',
       box("green", "commit phase", "minimal DOM changes", 0, "flex:1"), '<div class="arrow" data-step="0" style="min-width:60px"></div>',
       box("purple", "paint → effects", "then useEffect runs", 0, "flex:1"), gap=16),
   row(box("orange", "re-renders when", "its own state changes · its <b style=\"display:inline\">parent</b> re-renders · a context it reads changes", 1, "flex:1"),
       box("red", "not on the list", "\"its props changed\"", 1, "flex:1")),
   note("Re-render ≠ slow · it's a problem only when <u>expensive</u> or <u>very frequent</u>", 2)),
 "steps": [
  "An update has two phases. In the render phase, React calls your components to get the new JSX, and compares it with the previous one. Nothing on screen changes yet. In the commit phase, React applies the minimal set of DOM changes. Then the browser paints, and effects run.",
  "A component re-renders when its own state changes, when its parent re-renders, or when a context it reads changes. Notice what's not on the list: its props changed. Children re-render because their parent did, even with identical props.",
  "And that's usually fine. A re-render is just calling a function. If the JSX is the same, React touches no DOM at all. It's only a problem when a component is expensive, or renders very often, like on every keystroke.",
 ]},

{"html": H("", "React.memo") + code("""§0 const TaskRow = memo(function TaskRow({ task, onToggle }: Props) {
§0   return <li onClick={() => onToggle(task.id)}>{task.title}</li>;
§0 });

§1 const toggle = (id: number) => { … };       // ❌ new function every render

§2 const toggle = useCallback((id: number) => {
§2   setTasks(ts => ts.map(t => (t.id === id ? { ...t, done: !t.done } : t)));
§2 }, []);                                      // ✓ same function every render""", 28),
 "steps": [
  "React dot memo wraps a component, so it skips re-rendering when its props are shallowly equal. Every prop the same as last time.",
  "The catch. A parent creates new objects and functions on every render. So they're never the same, and memo is useless. Every row re-renders anyway.",
  "Stabilise those props. Use callback for functions, and use memo for objects and computed values. This toggle uses a functional update, so it needs no dependencies. Now typing in a filter re-renders the list, but each memoised row is skipped.",
 ]},

{"html": H("Simpler than ", "memo") + row(
   col(box("green", "1 · move state down", "only the search box uses <code>filter</code>? keep the state in the search box", 0),
       code("""§0 function SearchBox() {
§0   const [filter, setFilter] = useState("");
§0   …
§0 }""", 27), style="flex:1"),
   col(box("blue", "2 · pass children", "the same element when <code>Layout</code>'s state changes", 1),
       code("""§1 <Layout>
§1   <ExpensiveTree />
§1 </Layout>""", 27), style="flex:1"), top=True) +
   note("The React Compiler (Module 22) automates much of this", 2),
 "steps": [
  "Often a simpler fix beats memoisation. One: move state down. If only the search box uses the filter, put that state in the search box. Then typing re-renders only it, not the whole page.",
  "Two: pass expensive parts as children. When layout's own state changes, children is the same element as before, so the expensive tree isn't re-rendered.",
  "And the React compiler, which we'll see next module, now adds much of this memoisation automatically.",
 ]},

{"html": H("Keys and component ", "identity") + code("""§0 {isEditing ? <input defaultValue={title} /> : <span>{title}</span>}   // type changes → reset

§1 <EditProfile key={userId} userId={userId} />   // new userId → fresh state

§2 function Parent() {
§2   function Child() { return <input />; }   // ❌ a NEW type every render
§2   return <Child />;                          // remounts: loses focus and text
§2 }""", 28) + note("Same <u>type</u> + same <u>position</u> + same <u>key</u> = state kept", 0),
 "steps": [
  "React keeps a component's state as long as the same component type stays in the same position, with the same key. Change any of those, and the old component is destroyed, with its state. Switching from an input to a span resets it.",
  "So a key can reset a component on purpose. A new user I D means a brand new profile editor, with fresh state. That's cleaner than an effect that resets every field.",
  "And a common bug. Defining a component inside another component. Every render creates a new component type, so the child is unmounted and remounted. The input loses its focus and its text. Always define components at the top level of a module.",
 ]},

{"html": H("Code ", "splitting") + code("""§0 const Dashboard = lazy(() => import("./features/dashboard/Dashboard"));
§0 const Settings = lazy(() => import("./features/settings/Settings"));

§1 <Suspense fallback={<Spinner />}>          {/* while a chunk downloads */}
§1   <Routes>
§1     <Route path="/" element={<Dashboard />} />
§1     <Route path="/settings" element={<Settings />} />
§1   </Routes>
§1 </Suspense>

§2 const { jsPDF } = await import("jspdf");    // a big library, inside the click handler""", 28),
 "steps": [
  "By default, the whole app is one JavaScript bundle, downloaded before anything shows. Code splitting loads parts only when they're needed. Lazy takes a dynamic import, and Vite turns each one into a separate file. The component needs a default export.",
  "Suspense shows a fallback, like a spinner, while a chunk downloads. Splitting by route is the biggest, easiest win.",
  "Also split heavy, rarely used parts. A chart library, a rich text editor, or an admin panel. Or import a big library inside the click handler that needs it. And you can preload a chunk when the user hovers over its link, so the spinner rarely appears.",
 ]},

{"html": H("", "Virtualization") + row(
   col(box("gray", "rows 0–37", "empty spacer", 0), box("green", "rows 38–60", "the only rows in the DOM", 0, "padding:40px 26px"),
       box("gray", "rows 61–9,999", "empty spacer", 0), gap=12, style="width:420px"),
   code("""§1 const virtualizer = useVirtualizer({
§1   count: items.length,
§1   getScrollElement: () => parentRef.current,
§1   estimateSize: () => 40,        // row height
§1   overscan: 8,
§1 });
§1 virtualizer.getVirtualItems().map(row => (
§1   <div key={row.key} style={{
§1     transform: `translateY(${row.start}px)` }}>
§1     {items[row.index].title}
§1   </div>
§1 ))""", 27, style="flex:1"), top=True) +
   note("Or <u>pagination</u> / infinite scroll, which also saves server work", 2),
 "steps": [
  "Rendering ten thousand rows means ten thousand DOM nodes. Slow to render, slow to scroll, and heavy on memory. Virtualization renders only the rows in view, plus a few extra, and swaps them as you scroll. The rest is just empty space.",
  "TanStack Virtual does the maths. Give it the count, the scroll container, and an estimated row height. Then render only the virtual items, each moved into place. React window and react virtuoso work too.",
  "The alternative is pagination, or infinite scroll, which also saves server work. Virtualize when users genuinely need to scroll through thousands of items that are already loaded.",
 ]},

{"html": H("Measure ", "first") + row(
   col(box("blue", "React DevTools → Profiler", "record · do the slow thing · stop · the flame graph shows <b style=\"display:inline\">why</b> each rendered", 0),
       box("orange", "production build", "<code>npm run build &amp;&amp; npm run preview</code> · dev mode is slower", 0), style="width:460px"),
   col(table(["Problem", "Fix"], [
     (["state too high", "move it down · pass children"], 1),
     (["memo child re-renders", "useCallback / useMemo"], 1),
     (["thousands of rows", "virtualize or paginate"], 1),
     (["slow first load", "code splitting"], 1),
     (["laggy typing", "useDeferredValue"], 1),
     (["context re-renders all", "split it · store + selectors"], 1)], size=30), style="flex:1"), top=True),
 "steps": [
  "Measure before optimising. Guessing usually optimises the wrong thing. Install the React developer tools. In the profiler tab, record, do the slow interaction, and stop. The flame graph shows every component that rendered, how long it took, and why. And always test with a production build. Development mode is much slower, and renders twice.",
  "Then apply the matching fix. State too high? Move it down, or pass children. A memoised child re-renders anyway? Stabilise its props. Thousands of rows? Virtualize or paginate. A slow first load? Code splitting. Laggy typing? Use deferred value. And a context that re-renders everything? Split it, or use a store with selectors.",
 ]},

quiz([
  ("Three causes of a re-render?", "own state · <b style=\"display:inline\">parent</b> re-render · context", "blue",
   "Quiz time. What are the three causes of a re-render?",
   "Its own state changes, its parent re-renders, or a context it reads changes."),
  ("Why might <code>memo</code> not help?", "new object or function props every render", "orange",
   "Why might React dot memo not help?",
   "Because the parent passes new objects or functions every render."),
  ("How do you reset a component's state?", "change its <b style=\"display:inline\">key</b>", "green",
   "And how do you reset a component's state on purpose?",
   "Change its key."),
]),

recap(["Render (call + diff) → commit (DOM)",
       "Re-render ≠ slow · parent renders re-render children",
       "memo needs stable props · or move state down, pass children",
       "Same type + position + key keeps state",
       "lazy + Suspense · virtualize long lists",
       "Measure with the Profiler, on a production build"],
  "Let's recap. An update renders, by calling components and diffing, then commits the DOM changes. A re-render isn't slow by itself, and children re-render when their parent does. Memo needs stable props, but moving state down or passing children is often simpler. The same type, position, and key keeps a component's state. Lazy and suspense split your code, and virtualization handles long lists. And always measure with the profiler, on a production build. Next time: React internals and modern React!"),
]
