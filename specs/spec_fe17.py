from lib import *

TAG = "Frontend 17 · Effects and Data Fetching"
FILE = "Frontend 17 Effects and Data Fetching.mp4"

SLIDES = [
title_slide(17, "Effects and Data Fetching", "Syncing a component with the world outside React",
  "Welcome to module seventeen: effects and data fetching.",
  "Rendering must be pure. But apps need side effects. Loading data from your API, timers, subscriptions, talking to the DOM directly. Use effect is how a component syncs with the world outside React. It's powerful, and easy to misuse. So this module covers both the right uses, and the wrong ones."),

{"html": H("", "useEffect") + row(code("""function Clock() {
  const [now, setNow] = useState(new Date());
  useEffect(() => {
§0     const id = setInterval(() => setNow(new Date()), 1000);
§2     return () => clearInterval(id);        // cleanup
§1   }, []);                                  // dependencies
  return <p>{now.toLocaleTimeString()}</p>;
}""", 28, style="flex:1"),
   table(["Dependencies", "Runs"], [
     (["none", "after <b>every</b> render"], 1),
     (["<code>[]</code>", "once, after the first render"], 1),
     (["<code>[userId, page]</code>", "first render + when they change"], 1)], size=27), top=True) +
   note("Cleanup: clear timers · remove listeners · cancel requests · close connections", 2),
 "steps": [
  "An effect runs after React has updated the screen. Here, a clock starts an interval that updates the time every second.",
  "The dependency array decides when it runs. With no array, after every render, which is rarely what you want. An empty array means once, after the first render. And with values in it, after the first render, and again whenever one of them changes.",
  "The function you return is the cleanup. It runs before the effect runs again, and when the component is removed. Use it to undo whatever the effect set up. Clear timers, remove listeners, cancel requests. Forgetting it causes leaks.",
 ]},

{"html": H("The ", "dependency", " rule") + code("""useEffect(() => {
  function onKey(e: KeyboardEvent) { if (e.key === "Escape") onClose(); }
  window.addEventListener("keydown", onKey);
  return () => window.removeEventListener("keydown", onKey);
§0 }, [onClose]);       // every value from the component that the effect uses""", 29) +
   row(box("orange", "missing one?", "the effect uses <b style=\"display:inline\">stale</b> values from an old render", 1, "flex:1"),
       box("blue", "react-hooks/exhaustive-deps", "the ESLint rule lists them for you", 1, "flex:1"),
       box("green", "think", "\"keep X in sync with these values\", not \"run on mount\"", 2, "flex:1"), style="margin-top:28px"),
 "steps": [
  "Here's the rule. List every value from the component that the effect uses, in the dependency array. Props, state, and functions defined in the component. This effect uses on close, so on close goes in the array.",
  "Leave one out, and you get an effect that uses stale values from an old render. The exhaustive deps ESLint rule catches this for you.",
  "So think of an effect as keep X in sync with these values. Not as run this when the component mounts.",
 ]},

{"html": H("Fetching ", "data") + row(code("""useEffect(() => {
  async function load() {
    try {
      const res = await fetch("/api/tasks");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setTasks(await res.json());
    } catch (e) { setError(String(e)); }
    finally { setLoading(false); }
  }
§0   load();
}, []);
§1 if (loading) return <p>Loading tasks…</p>;
§1 if (error) return <p role="alert">{error}</p>;
§1 if (tasks.length === 0) return <p>No tasks yet.</p>;""", 26, style="flex:1"),
   col(box("purple", "effects can't be async", "define an async function inside, then call it", 0),
       box("green", "4 states", "loading · error · empty · data", 1),
       box("blue", "in real apps", "TanStack Query: caching, retries, refetching", 2), style="width:500px"), top=True),
 "steps": [
  "Here's the classic pattern for loading from your Spring Boot API. The effect function itself can't be async, because it must return nothing, or a cleanup. So define an async function inside, and call it. Check res dot ok, store the data, catch errors, and finally turn loading off.",
  "And always handle four states: loading, error, empty, and data. Users notice when one is missing.",
  "You should understand this pattern first. But in real apps, you'll usually let TanStack Query do it, with caching, retries and refetching, which we'll see in module nineteen.",
 ]},

{"html": H("Race ", "conditions") + row(
   col(box("gray", "type \"ja\"", "request A starts (slow)", 0), box("gray", "type \"java\"", "request B starts (fast)", 0),
       box("green", "B returns", "shows \"java\" results", 0), box("red", "A returns 😬", "overwrites with \"ja\" results", 0), gap=12, style="width:440px"),
   code("""§1 useEffect(() => {
§1   const controller = new AbortController();
§1   fetch(`/api/search?q=${query}`,
§1         { signal: controller.signal })
§1     .then(res => res.json())
§1     .then(setResults)
§1     .catch(err => {
§1       if (err.name !== "AbortError") throw err;
§1     });
§2   return () => controller.abort();
§1 }, [query]);""", 28, style="flex:1"), top=True),
 "steps": [
  "When an effect depends on a value that changes quickly, like a search box, responses can arrive out of order. Type j a, and a slow request starts. Type java, and a fast one starts. Java's results show up first. Then the old j a response arrives, and overwrites them. Wrong results!",
  "The fix goes in the cleanup. Create an abort controller, and pass its signal to fetch.",
  "Every time the query changes, React runs the previous effect's cleanup first, which aborts the old request. So only the latest response can ever set state. Combine it with debouncing, so you don't send a request on every keystroke.",
 ]},

{"html": H("Why effects run ", "twice") + fill(
   row(box("blue", "StrictMode · development only", "renders twice · runs effect → cleanup → effect again", 0, "flex:1"),
       box("green", "why", "simulates leaving and coming back · <b style=\"display:inline\">exposes missing cleanups</b>", 1, "flex:1")),
   row(box("red", "✗ don't", "remove StrictMode · add a didRun ref", 2, "flex:1"),
       box("green", "✓ do", "fix the cleanup · production runs effects once", 2, "flex:1"))),
 "steps": [
  "With strict mode on, which it is in Vite's template, React in development renders components twice. And it runs every effect, then its cleanup, then the effect again. So you'll see two requests in the network tab.",
  "That's deliberate. It simulates a component being removed and shown again, and it exposes missing cleanups. If your effect breaks when it runs twice, it would also break in production when users navigate back and forth.",
  "So don't fix it by removing strict mode, or adding a did run flag. Fix the cleanup. Production builds run effects once.",
 ]},

{"html": H("You might not need an ", "effect") + code("""§0 // ❌ extra state + effect + extra render
§0 useEffect(() => setVisible(tasks.filter(t => !t.done)), [tasks]);
§0 // ✓ compute during render
§0 const visible = tasks.filter(t => !t.done);

§1 // ❌ an effect watching a flag
§1 useEffect(() => { if (submitted) postOrder(order); }, [submitted]);
§1 // ✓ the handler knows what happened
§1 function handleSubmit() { postOrder(order); }

§2 <ProfileForm key={userId} userId={userId} />   // reset state with a key""", 28) +
   note("Caused by an <u>event</u> → handler · caused by being <u>on screen</u> → effect", 3),
 "steps": [
  "Effects are for syncing with external systems. Many effects in beginner code shouldn't exist at all. Transforming data for rendering? Just compute it during render.",
  "Reacting to a user action? Do it in the event handler. It knows exactly what happened.",
  "Resetting state when a prop changes? Give the component a key. A new user I D means a fresh component, with fresh state.",
  "Here's a quick test. If the code is caused by an event, it belongs in the handler. If it's caused by the component being on screen, it's an effect.",
 ]},

{"html": H("", "useRef") + row(
   col(code("""§0 const inputRef = useRef<HTMLInputElement>(null);
§0 useEffect(() => { inputRef.current?.focus(); }, []);
§0 <input ref={inputRef} />""", 27),
       code("""§1 const timer = useRef<number | null>(null);
§1 timer.current = window.setInterval(tick, 100);
§1 clearInterval(timer.current);""", 27), style="flex:1"),
   table(["", "useState", "useRef"], [
     (["Survives renders", "✓", "✓"], 2),
     (["Change re-renders", "✓", "<b>✗</b>"], 2),
     (["Use for", "what's on screen", "DOM, timer ids"], 2)], size=27), top=True),
 "steps": [
  "Use ref gives you a box, with a current property, that survives re-renders. Its first job is reaching a DOM element. Attach the ref to an input, and focus it when the form appears.",
  "Its second job is remembering a value without re-rendering. Like a timer I D, so you can stop it later.",
  "Both state and refs survive re-renders. But changing a ref does not cause a re-render. So use state for anything shown on screen, and refs for DOM nodes, timer I Ds, and values you don't show. And don't read or write a ref during rendering.",
 ]},

quiz([
  ("What does <code>[]</code> as dependencies mean?", "run <b style=\"display:inline\">once</b>, after the first render", "blue",
   "Quiz time. What does an empty dependency array mean?",
   "Run once, after the first render."),
  ("How do you prevent fetch race conditions?", "abort or ignore the old request in the <b style=\"display:inline\">cleanup</b>", "green",
   "How do you prevent race conditions when fetching?",
   "Abort, or ignore, the old request in the cleanup."),
  ("A POST after a button click: effect or handler?", "the event <b style=\"display:inline\">handler</b>", "orange",
   "And a POST request after a button click. Effect, or handler?",
   "The event handler."),
]),

recap(["Effects run after render · dependencies decide when",
       "List every value the effect uses",
       "Cleanup undoes timers, listeners, requests",
       "Handle loading, error, empty, data",
       "Abort stale requests · StrictMode runs effects twice in dev",
       "Events → handlers · <code>useRef</code> doesn't re-render"],
  "Let's recap. Effects run after render, and the dependency array decides when. List every value the effect uses. The cleanup undoes timers, listeners, and requests. When fetching, handle loading, error, empty, and data. Abort stale requests, and remember strict mode runs effects twice in development, to expose missing cleanups. Things caused by events belong in handlers. And use ref remembers values without re-rendering. Next time: hooks in depth!"),
]
