from lib import *

TAG = "Frontend 16 · State and Events"
FILE = "Frontend 16 State and Events.mp4"

SLIDES = [
title_slide(16, "State and Events", "Data that changes over time, changed the right way",
  "Welcome to module sixteen: state and events.",
  "State is what makes a component interactive. Data that changes over time, like a counter, a form's text, or a list of tasks. Change it the right way, and React re-renders for you. Most beginner React bugs come from changing it the wrong way. So this module is all about the right way."),

{"html": H("", "useState") + row(
   col(code("""§0 function Counter() {
§0   const [count, setCount] = useState(0);
§0   return (
§0     <button onClick={() => setCount(count + 1)}>
§0       Clicked {count} times
§0     </button>
§0   );
§0 }""", 29),
       code("""§1 let count = 0;                // reset every render
§1 onClick={() => { count++; }}    // no re-render → always 0""", 27), style="flex:1"),
   col(box("green", "useState", "keeps the value <u>between renders</u> · setter triggers a re-render", 1),
       box("blue", "each instance", "two &lt;Counter /&gt;s count separately", 2), style="width:480px"), top=True),
 "steps": [
  "Use state gives a component memory. It returns a pair. The current value, and a setter function. Zero is the starting value. Click the button, call set count, and React re-renders with the new count.",
  "Why not a normal variable? Two problems. Changing it doesn't tell React to re-render. And even if it did, let count equals zero would run again, and reset it. Use state fixes both. React stores the value between renders, and the setter triggers a re-render.",
  "And each component instance has its own state. Two counters count independently.",
 ]},

{"html": H("Props vs ", "state") + table(["", "Props", "State"], [
   (["Comes from", "the parent", "the component itself"], 0),
   (["Can it change it?", "no", "yes, with its setter"], 0),
   (["Changes when", "the parent re-renders", "you call <code>setX</code>"], 0)], size=34) +
   code("""§1 function handle() {
§1   setCount(count + 1);
§1   console.log(count);   // still the OLD value: this render's snapshot
§1 }""", 32, style="margin-top:30px"),
 "steps": [
  "So props versus state. Props come from the parent, and the component can't change them. State belongs to the component itself, and it changes when you call the setter.",
  "And state updates are not immediate. Calling set count schedules a re-render. Inside the current render, count keeps its old value. Think of each render as a snapshot.",
 ]},

{"html": H("Handling ", "events") + code("""function SearchBox() {
  const [query, setQuery] = useState("");
§1   function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
§1     e.preventDefault();
§1   }
  return (
    <form onSubmit={handleSubmit}>
§2       <input value={query} onChange={e => setQuery(e.target.value)} />
§0       <button type="button" onClick={() => setQuery("")}>Clear</button>
    </form>
  );
}""", 28) + note("Pass a function: <code>onClick={handle}</code> ✓ · <code>onClick={handle()}</code> ✗ runs during render", 3),
 "steps": [
  "Event props are camel case. On click, on change, on submit, on key down.",
  "Prevent default works just like in plain DOM code. It stops the form from reloading the page.",
  "And in React, on change on an input fires on every keystroke.",
  "The big rule. Pass a function, don't call it. On click equals handle click, or an arrow function. Never handle click with parentheses. That runs it during render. And name handlers handle something, and props that take handlers, on something. Like on delete, or on toggle.",
 ]},

{"html": H("Never ", "mutate") + code("""const [tasks, setTasks] = useState<Task[]>([]);

§0 tasks.push(newTask); setTasks(tasks);    // ❌ same array: React may skip it

§1 setTasks([...tasks, newTask]);                                           // add
§1 setTasks(tasks.filter(t => t.id !== id));                                // remove
§1 setTasks(tasks.map(t => (t.id === id ? { ...t, done: !t.done } : t)));  // update

§2 setForm({ ...form, title: "New title" });                  // one field
§2 setForm({ ...form, tags: [...form.tags, "urgent"] });      // copy every level""", 28),
 "steps": [
  "React decides whether to re-render by comparing the old and new reference. If you change an array in place, it's still the same reference, so React may skip the update, and your screen goes stale.",
  "So always replace, never mutate. Add with spread. Remove with filter. Update one item with map.",
  "Objects work the same way. Spread the object, and change one field. And for nested data, copy every level you change.",
 ]},

predict(("Functional ", "updates"), [
  ("setCount(count + 1);<br>setCount(count + 1);<br>setCount(count + 1);", "+1", "all three use the <u>same</u> old count",
   "Pause and predict. Count is zero. We call set count, count plus one, three times. What's count after the re-render?",
   "Just one! All three calls use the same old count, zero. So they all set it to one."),
  ("setCount(c =&gt; c + 1);<br>setCount(c =&gt; c + 1);<br>setCount(c =&gt; c + 1);", "+3", "each gets the previous result",
   "Now with a function instead.",
   "Three! Pass a function, and React gives it the latest value each time. Use the function form whenever the new state depends on the old, especially in timers and async code."),
], size=30),

{"html": H("Lifting ", "state up") + row(
   code("""function TaskPage() {
  const [tasks, setTasks] = useState(initial);
  const toggle = (id: number) =>
    setTasks(ts => ts.map(t =>
      t.id === id ? { ...t, done: !t.done } : t));
  return (
    <>
      <Header remaining={remaining} />
      <TaskList tasks={tasks} onToggle={toggle} />
    </>
  );
}""", 26, style="flex:1"),
   col(box("purple", "TaskPage", "owns <code>tasks</code>", 1, "text-align:center"),
       row(box("blue", "Header", "<code>remaining</code>", 1, "flex:1"), box("blue", "TaskList", "<code>tasks</code>, <code>onToggle</code>", 1, "flex:1"), gap=14),
       box("green", "↓ data down as props", "", 2), box("orange", "↑ changes up as callbacks", "<code>onToggle(id)</code>", 2), style="width:620px"), top=True),
 "steps": [
  "When two components need the same data, move the state to their closest common parent. Then pass it down as props, along with functions to change it.",
  "So task page owns the tasks. The header gets the remaining count. The task list gets the tasks, and an on toggle function.",
  "This is one-way data flow. Data flows down as props. Changes flow up as function calls. And only the owner updates the state. That makes bugs easy to trace. And when props have to pass through many layers that don't use them, called prop drilling, that's the cue for context, or a store.",
 ]},

{"html": H("Controlled vs ", "uncontrolled") + row(
   code("""§0 const [title, setTitle] = useState("");
§0 <input value={title}
§0   onChange={e => setTitle(e.target.value)} />
§0 <button disabled={!title.trim()}>Add</button>""", 27, style="flex:1"),
   code("""§1 const data = new FormData(e.currentTarget);
§1 onAdd(String(data.get("title")));
§1 <input name="title" defaultValue="" />""", 27, style="flex:1"), top=True) +
   table(["", "Controlled", "Uncontrolled"], [
     (["Value lives in", "React state", "the DOM"], 2),
     (["Live validation", "easy", "harder"], 2),
     (["Typical use", "most interactive forms", "simple forms, file inputs"], 2)], size=29),
 "steps": [
  "A controlled input's value comes from state, and every change goes through React. So you can validate as the user types, or disable the add button until there's a title. Clearing it is just setting state.",
  "An uncontrolled input keeps its own value in the DOM. You read it when you need it, for example with form data on submit.",
  "Controlled needs more code, but makes instant validation easy. Use it for most interactive forms. And always start with a defined value, like an empty string, or React warns about switching from uncontrolled to controlled.",
 ]},

{"html": H("Derived state: ", "compute it") + col(
   code("""§0 // ❌ duplicated state
§0 const [tasks, setTasks] = useState([]);
§0 const [doneCount, setDoneCount] = useState(0);""", 30),
   code("""§1 // ✓ computed during render
§1 const doneCount = tasks.filter(t => t.done).length;
§1 const visible = tasks.filter(t =>
§1   filter === "all" || (filter === "done") === t.done);""", 30)) +
   note("Could I compute this from something I already have? → don't store it · store <code>selectedId</code>, not a copy", 2),
 "steps": [
  "If a value can be calculated from props or existing state, don't put it in state. Here, done count is stored separately. It's easy to forget to update it, and then the two disagree.",
  "Instead, compute it during rendering. It's always correct. The same goes for filtered lists, sorted lists, totals, and whether a form is valid.",
  "So ask of every piece of state: could I compute this from something I already have? If yes, compute it. And keep state minimal. Store the selected I D, not a copy of the selected object, which goes stale.",
 ]},

quiz([
  ("Is a state update immediate?", "<b style=\"display:inline\">No</b> · it schedules a re-render", "red",
   "Quiz time. Is a state update immediate?",
   "No. It schedules a re-render. The current render keeps the old value."),
  ("Add an item to an array in state?", "<code>setItems([...items, item])</code> · never push", "green",
   "How do you add an item to an array in state?",
   "Set items, with a new array, spreading the old items, plus the new one. Never push."),
  ("What is lifting state up?", "move it to the closest <b style=\"display:inline\">common parent</b>", "purple",
   "And what's lifting state up?",
   "Moving shared state to the closest common parent, and passing it down."),
]),

recap(["<code>useState</code>: value + setter · keeps it between renders",
       "Updates aren't immediate · each render is a snapshot",
       "Pass functions to <code>onX</code> · don't call them",
       "Replace, never mutate · <code>setX(prev =&gt; …)</code>",
       "Lift state up · data down, changes up",
       "Controlled inputs · compute derived values"],
  "Let's recap. Use state gives you a value and a setter, and keeps the value between renders. Updates aren't immediate, and each render is a snapshot. Pass functions to event props, don't call them. Replace state, never mutate it, and use the function form when the new value depends on the old. Lift shared state up, so data flows down and changes flow up. And use controlled inputs, and compute derived values instead of storing them. Next time: effects and data fetching!"),
]
