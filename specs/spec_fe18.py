from lib import *

TAG = "Frontend 18 · Hooks in Depth"
FILE = "Frontend 18 Hooks in Depth.mp4"

SLIDES = [
title_slide(18, "Hooks in Depth", "useReducer, context, memoisation and your own custom hooks",
  "Welcome to module eighteen: hooks in depth.",
  "Hooks are how function components get React features. State, effects, context, and memoisation. Beyond use state and use effect, a handful more cover almost every app. And your own custom hooks let you reuse logic as easily as you reuse components."),

{"html": H("The rules of ", "hooks") + row(
   col(box("green", "1 · top level only", "never in conditions, loops, nested functions, or after an early return", 0),
       box("blue", "2 · React functions only", "components and custom <code>useX</code> hooks", 0), style="width:560px"),
   code("""§1 if (!userId) return <p>Pick a user</p>;
§1 const [tab, setTab] = useState("posts");  // ❌

§2 // Render 1: useState → slot 1 · useEffect → slot 2
§2 // Render 2: (skipped!)  useEffect → reads slot 1 😬""", 27, style="flex:1"), top=True),
 "steps": [
  "Hooks have two rules, enforced by a linter. One: only call hooks at the top level. Never inside conditions, loops, or after an early return. Two: only call them from components, or custom hooks.",
  "Here, use state comes after an early return. So on some renders it's called, and on others it's not.",
  "Why does that matter? React doesn't know hooks by name. It stores each component's hook data in a list, and matches calls by order. The first hook gets slot one, the second gets slot two. If a condition skips a hook, every later hook reads the wrong slot.",
 ]},

{"html": H("", "useReducer") + code("""§0 type Action =
§0   | { type: "added"; title: string }
§0   | { type: "toggled"; id: number }
§0   | { type: "deleted"; id: number };

§1 function tasksReducer(tasks: Task[], action: Action): Task[] {
§1   switch (action.type) {
§1     case "added":   return [...tasks, { id: Date.now(), title: action.title, done: false }];
§1     case "toggled": return tasks.map(t => (t.id === action.id ? { ...t, done: !t.done } : t));
§1     case "deleted": return tasks.filter(t => t.id !== action.id);
§1   }
§1 }
§2 const [tasks, dispatch] = useReducer(tasksReducer, []);
§2 dispatch({ type: "toggled", id: 3 });""", 27),
 "steps": [
  "When state has several related values, and many ways to change them, gather the logic in a reducer. First, describe the actions. What can happen? Added, toggled, deleted.",
  "The reducer is a pure function. It takes the current state and an action, and returns the new state. Every change lives in one place, named by what happened.",
  "Use reducer gives you the state, and a dispatch function. Dispatch an action, and React runs the reducer. It's easy to unit test without React. And this is the same pattern Redux is built on.",
 ]},

{"html": H("useContext: no more ", "prop drilling") + code("""§0 const ThemeContext = createContext<ThemeCtx | null>(null);

§1 export function ThemeProvider({ children }: { children: React.ReactNode }) {
§1   const [theme, setTheme] = useState<Theme>("dark");
§1   const toggle = () => setTheme(t => (t === "dark" ? "light" : "dark"));
§1   return <ThemeContext.Provider value={{ theme, toggle }}>{children}</ThemeContext.Provider>;
§1 }
§2 function ThemeButton() {              // any depth, no props
§2   const { theme, toggle } = useContext(ThemeContext)!;
§2   return <button onClick={toggle}>Switch from {theme}</button>;
§2 }""", 27) + note("Every reader re-renders when the value changes → split contexts · not a full state manager", 3),
 "steps": [
  "Some data is needed by many components at different depths. The logged in user, the theme, the language. Passing it through every layer is prop drilling. Context lets any descendant read it directly. First, create a context.",
  "Then a provider component holds the state, and makes it available to everything inside it.",
  "And any component, at any depth, reads it with use context. No props needed.",
  "One thing to know. Every component that reads a context re-renders when its value changes. So don't put fast-changing data in one big context. Split them. And context is for passing data down. It's not a full state manager.",
 ]},

{"html": H("useMemo and ", "useCallback") + code("""§0 const visible = useMemo(                        // caches a VALUE
§0   () => tasks.filter(t => t.title.includes(query)),
§0   [tasks, query]
§0 );
§1 const handleToggle = useCallback(                // caches a FUNCTION
§1   (id: number) => setTasks(ts => ts.map(…)),
§1   []
§1 );""", 30) + row(box("green", "helps", "expensive calculations · stable props for <code>React.memo</code> children · effect dependencies", 2, "flex:1"),
                    box("red", "doesn't", "wrapping every small calculation and handler", 2, "flex:1"), style="margin-top:24px"),
 "steps": [
  "On every render, everything in the component runs again. Usually that's fine. These two hooks cache a result between renders, while their dependencies stay the same. Use memo caches a value.",
  "Use callback caches a function.",
  "When do they actually help? For an expensive calculation, like filtering thousands of items. To keep a reference stable for a child wrapped in React dot memo. Or for a value used as an effect dependency. But don't wrap every small calculation. Each one costs memory and adds noise. And the React compiler can now add this automatically.",
 ]},

{"html": H("Custom ", "hooks") + row(code("""function useDebounce<T>(value: T, delay = 300): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(id);
  }, [value, delay]);
  return debounced;
}""", 27, style="flex:1"),
   col(box("purple", "use + other hooks", "a function starting with <code>use</code>", 0),
       box("orange", "shares logic, not state", "each caller gets its own copy", 1), style="width:440px"), top=True) +
   code("""§2 const [query, setQuery] = useLocalStorage("last-search", "");
§2 const debounced = useDebounce(query, 300);
§2 const { data, loading, error } = useFetch<Task[]>(`/api/tasks?q=${debounced}`);""", 27, style="margin-top:24px"),
 "steps": [
  "A custom hook is a function starting with use, that calls other hooks. Use debounce gives you a value that only updates after it stops changing. It's just state, plus an effect with a timer and a cleanup.",
  "Custom hooks share logic, not state. Each component that calls one gets its own copy.",
  "And using them reads like plain English. A query saved in local storage, debounced, then fetched. Extract a custom hook when the same stateful logic appears in two components.",
 ]},

{"html": H("More ", "hooks") + table(["Hook", "What it does"], [
   (["<code>useLayoutEffect</code>", "runs <b>before paint</b>: measure the DOM without flicker (rarely)"], 0),
   (["<code>useId</code>", "a stable unique id to link labels and inputs"], 1),
   (["<code>useTransition</code>", "mark an update <b>non-urgent</b>: the UI stays responsive"], 2),
   (["<code>useDeferredValue</code>", "let a slow part lag behind a fast input"], 3)], size=31) +
   code("""§2 const [isPending, startTransition] = useTransition();
§2 startTransition(() => setTab(next));   // a heavy tab won't freeze the buttons""", 29, style="margin-top:24px"),
 "steps": [
  "A few more. Use layout effect is like use effect, but runs before the browser paints. Use it only to measure the DOM and adjust, without a flicker.",
  "Use I D gives a stable, unique I D, for linking labels and inputs.",
  "Use transition marks a state update as non-urgent. Switching to a heavy tab won't freeze the buttons, and is pending lets you show a spinner.",
  "And use deferred value lets a slow part of the screen lag behind a fast input. Neither makes work faster. They let React do the urgent updates first.",
 ]},

quiz([
  ("Why the top-level rule?", "React matches hooks to stored state by <b style=\"display:inline\">order</b>", "blue",
   "Quiz time. Why must hooks be called at the top level?",
   "Because React matches hook calls to stored state by their order."),
  ("<code>useMemo</code> vs <code>useCallback</code>?", "cache a value · cache a function", "green",
   "Use memo versus use callback?",
   "Use memo caches a value. Use callback caches a function."),
  ("Two components using one custom hook: shared state?", "<b style=\"display:inline\">No</b> · only the logic", "orange",
   "And do two components using the same custom hook share state?",
   "No. They share only the logic. Each gets its own state."),
]),

recap(["Hooks: top level only, React functions only",
       "useReducer: (state, action) → new state",
       "Context ends prop drilling · readers re-render",
       "useMemo (value) · useCallback (function) · only when it helps",
       "Custom hooks share logic, not state",
       "useTransition / useDeferredValue keep the UI responsive"],
  "Let's recap. Call hooks only at the top level, and only from React functions. A reducer is a pure function from state and action to new state. Context ends prop drilling, but every reader re-renders when it changes. Use memo caches a value, use callback caches a function, and use them only when they help. Custom hooks share logic, not state. And use transition and use deferred value keep the UI responsive. Next time: routing and state management!"),
]
