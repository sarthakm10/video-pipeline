from lib import *

TAG = "Frontend 27 · Machine Coding Round"
FILE = "Frontend 27 Machine Coding Round.mp4"

SLIDES = [
title_slide(27, "Machine Coding Round", "Build a small, working, accessible UI in 60–90 minutes",
  "Welcome to module twenty seven: the machine coding round.",
  "In a machine coding round, you build a small working UI in sixty to ninety minutes, usually in React, while someone watches. It tests whether you can turn requirements into clean, working, accessible code under time pressure. This module is a game plan, plus the problems that come up most."),

{"html": H("The game ", "plan") + row(
   col(table(["Minutes", "Do"], [
     (["0–8", "read twice · <b>ask</b> · checklist + out of scope"], 1),
     (["8–15", "component tree + <b>state shape</b>"], 1),
     (["15–55", "core flow <b>end to end</b>, unstyled"], 1),
     (["55–65", "edge cases, keyboard, labels, states"], 1),
     (["65–75", "light styling · what you'd improve"], 1)], size=27), style="flex:1"),
   col(box("green", "they judge", "works · code quality · edge cases · UX + a11y · communication", 0),
       box("orange", "working beats pretty", "a basic version early, then improve", 2), style="width:500px"), top=True),
 "steps": [
  "You get a prompt, like build a todo app with filters, and a blank project. They judge five things. Does it work, completely? Code quality: small components, clear names, sensible state. Edge cases: empty input, double clicks, errors. UX and accessibility. And communication. Explain decisions as you go.",
  "Here's a time plan for seventy five minutes. Read the prompt twice, ask questions, and write a checklist. Sketch the component tree and the state shape. Build the core flow end to end, unstyled. Then edge cases, keyboard, and labels. And finish with light styling, and what you'd improve with more time.",
  "And remember, working beats pretty. Get a basic version working early. An unfinished, beautifully styled app scores worse. Practise your Vite setup, so you don't fight tooling in the interview.",
 ]},

{"html": H("Build: a ", "todo app") + code("""§0 const [todos, setTodos] = useState<Todo[]>(load);       // lazy: reads storage once
§0 useEffect(() => { localStorage.setItem("todos", JSON.stringify(todos)); }, [todos]);
§1 const visible = todos.filter(t =>
§1   filter === "all" ? true : filter === "done" ? t.done : !t.done);   // derived
§1 const left = todos.filter(t => !t.done).length;
§2 function add(e: React.FormEvent) {
§2   e.preventDefault();
§2   const value = text.trim();
§2   if (!value) return;
§2   setTodos(ts => [...ts, { id: crypto.randomUUID(), text: value, done: false }]);
§2   setText("");
§2 }
§3 <button aria-label={`Delete "${todo.text}"`}>✕</button>
§3 onKeyDown={e => { if (e.key === "Enter") save(); if (e.key === "Escape") cancel(); }}""", 25),
 "steps": [
  "The most common prompt. Add, toggle, delete, edit, filter, count items left, and persist across reloads. Pass load to use state, without calling it. That's a lazy initialiser, so local storage is read only on the first render. And an effect saves whenever the todos change.",
  "Store only the filter value. The visible list, and the count of items left, are derived during render. Interviewers notice duplicated state.",
  "When adding, trim the text, ignore empty input, and give each todo a stable I D, with crypto random UUID. And use functional updates.",
  "And the details that score points. Label icon buttons, like delete, with aria label. And keyboard editing: enter saves, escape cancels. Extensions they might ask for: drag to reorder, due dates, or syncing with an API.",
 ]},

{"html": H("Build: a search ", "box") + code("""§0 const debounced = useDebounce(query.trim(), 300);
§0 useEffect(() => {
§0   if (debounced.length < 2) { setResults([]); setStatus("idle"); return; }
§0   const controller = new AbortController();
§0   setStatus("loading");
§0   fetch(`/api/items?q=${encodeURIComponent(debounced)}`, { signal: controller.signal })
§0     .then(r => r.json()).then(data => { setResults(data); setStatus("done"); })
§0     .catch(err => { if (err.name !== "AbortError") setStatus("error"); });
§0   return () => controller.abort();          // stale requests never land
§0 }, [debounced]);
§1 if (e.key === "ArrowDown") setActive(i => Math.min(i + 1, results.length - 1));
§1 <li role="option" aria-selected={i === active} onMouseDown={e => e.preventDefault()}>
§2 <>{text.slice(0, i)}<mark>{text.slice(i, i + q.length)}</mark>{text.slice(i + q.length)}</>""", 24),
 "steps": [
  "Search an API as you type. Debounce the query, require a minimum length, and abort the previous request in the cleanup, so stale results never land. And track every state: idle, loading, done, and error.",
  "Arrow keys move the active option, enter picks, and escape closes. Use the combobox ARIA pattern, with aria active descendant. And on mouse down, prevent default, so clicking an option doesn't blur the input first.",
  "Highlight the match by slicing the string, and wrapping the match in a mark element. Never inner HTML. An extension: cache results per query in a map.",
 ]},

{"html": H("Build: small ", "components") + row(
   col(box("blue", "tabs", "<code>role=\"tablist\"</code> · arrow keys move · <code>tabIndex</code> 0 on the active tab only", 0),
       box("green", "accordion", "buttons with <code>aria-expanded</code> · one open or many? · <code>details</code>/<code>summary</code>", 0),
       box("purple", "modal", "native <code>&lt;dialog&gt;</code> + <code>showModal()</code>: focus trap, Escape, backdrop", 1), style="width:600px"),
   code("""§2 function StarRating({ value, onChange, max = 5 }) {
§2   const [hover, setHover] = useState(0);
§2   const shown = hover || value;
§2   return (
§2     <div role="radiogroup" aria-label="Rating"
§2          onMouseLeave={() => setHover(0)}>
§2       {stars.map(n => (
§2         <button role="radio" aria-checked={value === n}
§2           onMouseEnter={() => setHover(n)}
§2           onClick={() => onChange(n)}>
§2           {n <= shown ? "★" : "☆"}
§2         </button>))}
§2     </div>);
§2 }""", 24, style="flex:1"), top=True) +
   note("Reusable = <u>controlled</u>: <code>value</code> + <code>onChange</code> · the parent owns the state", 3),
 "steps": [
  "Small components test API design, state, and accessibility. Tabs use a tab list, with arrow keys moving between tabs, and only the active tab in the tab order. An accordion uses buttons with aria expanded. Ask whether one or many panels may be open. And details and summary give one with no JavaScript at all.",
  "For a modal, use the native dialog element, with show modal. It handles the focus trap, escape, and the backdrop for you.",
  "A star rating. Hover previews, click sets, and it's a radio group for screen readers. The shown value is the hover value, or the real value.",
  "And make it controlled. Value and on change come from the parent, which owns the state. That's what makes a component reusable.",
 ]},

{"html": H("Build: pagination and infinite ", "scroll") + code("""§0 const [params, setParams] = useSearchParams();
§0 const page = Number(params.get("page") ?? 1);              // in the URL
§0 const { data, isPlaceholderData } = useQuery({
§0   queryKey: ["users", page],
§0   queryFn: () => api.get(`/users?page=${page}`),
§0   placeholderData: keepPreviousData,                     // old page stays visible
§0 });
§1 const loadMore = useCallback(async () => {
§1   if (loading.current || !hasMore) return;               // a ref guard
§1   loading.current = true;
§1   const page = await api.get(`/posts?cursor=${cursor ?? ""}`);
§1   setItems(prev => [...prev, ...page.items]);
§1   setHasMore(page.nextCursor !== null);
§1   loading.current = false;
§1 }, [cursor, hasMore]);""", 25),
 "steps": [
  "Numbered pagination keeps the page in the URL, so refresh, sharing, and the back button all work. Keep previous data shows the old page while the next one loads. And for Spring Data's page responses, remember the page number is zero based.",
  "Infinite scroll, without a library. An intersection observer calls load more. A ref guards against loading twice at once, and has more marks the end of the list. Also handle errors with a retry button, and add a load more button as the accessible fallback.",
 ]},

{"html": H("Build: a form and a ", "timer") + row(code("""§0 const rules = {
§0   email: v => /^\\S+@\\S+\\.\\S+$/.test(v) ? "" : "Enter a valid email",
§0   password: v => v.length >= 8 ? "" : "At least 8 characters",
§0   confirm: (v, all) => v === all.password ? "" : "Passwords don't match",
§0 };
§0 // errors are derived · shown after blur (touched) · all on submit""", 28, style="flex:1")) +
   code("""§1 const ticking = running && left > 0;            // derived: stops at zero
§1 useEffect(() => {
§1   if (!ticking) return;
§1   const id = setInterval(() => setLeft(l => Math.max(l - 1, 0)), 1000);
§1   return () => clearInterval(id);               // pause, reset, unmount
§1 }, [ticking]);""", 28, style="margin-top:22px") +
   note("<code>setLeft(left - 1)</code> = stale closure · for precision, store the <u>end time</u>", 2),
 "steps": [
  "A sign up form without libraries. They often want to see you do it by hand. One rule per field, returning an error message or an empty string. Errors are derived, never stored. Show a field's error after it's touched, not while typing the first character. And show all of them on submit.",
  "A countdown timer tests timers and cleanup. Ticking is derived, so it stops by itself at zero. The effect starts an interval, and its cleanup clears it, on pause, reset, and unmount.",
  "Call out the functional update. Set left, left minus one, would read a stale value inside the interval's closure. And set interval drifts, so for precision, store the end time, and compute what's left on each tick.",
 ]},

quiz([
  ("How do you store a todo filter?", "only the <b style=\"display:inline\">filter value</b> · the list is derived", "blue",
   "Quiz time. How should a todo filter be stored?",
   "Only the filter value. The visible list is derived."),
  ("Easiest accessible modal?", "native <code>&lt;dialog&gt;</code> + <code>showModal()</code>", "purple",
   "What's the easiest accessible modal?",
   "The native dialog element, with show modal."),
  ("Bug with <code>setLeft(left - 1)</code>?", "<b style=\"display:inline\">stale closure</b> · use <code>l =&gt; l - 1</code>", "red",
   "And what's the bug with set left, left minus one, in a countdown?",
   "A stale closure. Use the functional update instead."),
]),

recap(["Clarify · plan state · core flow first · then polish",
       "Working beats pretty",
       "Todo: lazy init, derived filter, stable ids",
       "Search: debounce, abort, every state, combobox",
       "Controlled components · native dialog",
       "Page in the URL · ref guard · functional updates"],
  "Let's recap. Clarify the requirements, plan the state, build the core flow first, then polish. Working beats pretty. A todo app uses lazy initial state, a derived filter, and stable I Ds. A search box needs debouncing, aborting, every state, and the combobox pattern. Make components controlled, and use the native dialog. Keep the page in the URL, guard infinite scroll with a ref, and use functional updates in timers. Next time: frontend interview questions!"),
]
