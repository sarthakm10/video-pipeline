from lib import *

TAG = "Frontend 15 · React Fundamentals"
FILE = "Frontend 15 React Fundamentals.mp4"

SLIDES = [
title_slide(15, "React Fundamentals", "Components: functions that take data and return what the screen should show",
  "Welcome to module fifteen: React fundamentals.",
  "React builds user interfaces from components. Functions that take data, and return what the screen should show. You stop writing find this element and change it code, and describe the UI for the current data instead. React works out the DOM changes. This module and the next seven take you from your first component to how React works inside."),

{"html": H("UI = f(", "state", ")") + fill(
   '<div class="big center" data-step="0" style="font-size:110px">UI = f(state)</div>',
   code("""§1 function Greeting() {
§1   const name = "Asha";
§1   return <h1>Hello, {name}!</h1>;
§1 }""", 36),
   row(box("blue", "components", "reusable pieces, each a function", 2, "flex:1"), box("green", "declarative", "say <u>what</u> to show, not how", 2, "flex:1"),
       box("purple", "one-way data", "parents → children", 2, "flex:1"), box("gray", "a library", "for the view only", 2, "flex:1"))),
 "steps": [
  "With plain DOM code, every change means remembering which elements to update. As an app grows, the screen and the data drift apart. React flips it around. You write a function from state, your data, to UI. When the state changes, React calls your function again, and updates only the parts of the DOM that changed.",
  "Here's a component. A function that returns what looks like HTML, with the name inserted in curly braces.",
  "The key ideas. Components are reusable pieces, each one a function. React is declarative. You say what to show, not how to change the DOM. Data flows one way, from parents down to children. And React is a library for the view, not a full framework. Routing and data fetching come from other libraries.",
 ]},

{"html": H("Your first ", "project") + row(
   col(code("""npm create vite@latest task-ui -- --template react-ts
npm install && npm run dev""", 27),
       code("""§2 // main.tsx
§2 createRoot(document.getElementById("root")!)
§2   .render(<StrictMode><App /></StrictMode>);""", 27), style="flex:1"),
   code("""§1 task-ui/
§1 ├─ index.html   <div id="root">
§1 ├─ src/
§1 │  ├─ main.tsx  mounts <App />
§1 │  └─ App.tsx   top component
§1 └─ package.json""", 27, style="width:600px"), top=True) +
   note("One HTML page that swaps content without reloading: a <u>single-page application</u>", 3),
 "steps": [
  "Create a project with Vite, using the React TypeScript template.",
  "Here's what you get. Index dot HTML, with one empty div, with the ID root. And in source, main dot t s x, and App dot t s x, your top component.",
  "Main dot t s x finds the root div, and renders your App component into it, wrapped in strict mode, which helps find bugs during development.",
  "So the whole app lives in one HTML page, and swaps content without reloading. That's called a single page application.",
 ]},

{"html": H("", "JSX") + row(code("""function TaskHeader() {
  const count = 3;
  return (
    <header className="task-header">
§1       <h1>{user.name}'s tasks</h1>
§1       <p>{count} task{count === 1 ? "" : "s"} left</p>
§2       <img src={user.avatar} alt="" />
    </header>
  );
}""", 27, style="flex:1"),
   col(table(["Rule", "Example"], [
     (["<code>{ }</code> = any expression", "<code>{count * 2}</code>"], 1),
     (["<code>class</code> → <code>className</code>", "<code>htmlFor</code> too"], 2),
     (["camelCase attributes", "<code>onClick</code>"], 2),
     (["style is an object", "<code>style={{ color: \"teal\" }}</code>"], 2),
     (["every tag closes", "<code>&lt;img /&gt;</code>"], 2),
     (["one root element", "<code>&lt;&gt;…&lt;/&gt;</code>"], 3)], size=27), style="width:640px;flex-shrink:0"), top=True),
 "steps": [
  "JSX is HTML-like syntax inside JavaScript. The build turns it into ordinary function calls, so it's just JavaScript underneath.",
  "Curly braces hold any JavaScript expression. A variable, a calculation, or a ternary. But not statements like if or for.",
  "A few rules differ from HTML. Class becomes class name, and for becomes html for. Attributes are camel case, like on click. Style takes an object. And every tag must close, even img.",
  "A component returns one root element. To return siblings, wrap them in a fragment, an empty tag. And JSX escapes values automatically, so user input shows as text, never HTML. That protects you from XSS.",
 ]},

{"html": H("Components and ", "props") + code("""§0 type TaskCardProps = { title: string; done: boolean; minutes?: number };

§0 function TaskCard({ title, done, minutes = 30 }: TaskCardProps) {
§0   return (
§0     <article className={done ? "card done" : "card"}>
§0       <h3>{title}</h3> <span>{minutes} min</span>
§0     </article>
§0   );
§0 }
§1 <TaskCard title="Learn JSX" done={true} />
§1 <TaskCard title="Learn props" done={false} minutes={45} />""", 28) +
   note("Props are <u>read-only</u> · Capitalised = your component · lowercase = HTML", 2),
 "steps": [
  "A component is a function whose name starts with a capital letter, and returns JSX. Props are its inputs. Type them, and destructure them in the parameter list, with defaults if you like.",
  "Then pass props like attributes. Strings in quotes, everything else in curly braces.",
  "Two rules. Props are read-only. A component must never change its own props. And capitalised tags are your components, while lowercase tags are HTML elements.",
 ]},

{"html": H("", "children", " and pure components") + row(code("""function Card({ title, children }:
  { title: string; children: React.ReactNode }) {
  return (
    <section className="card">
      <h2>{title}</h2>
      {children}
    </section>
  );
}
§0 <Card title="Today">
§0   <p>Two tasks left.</p>
§0 </Card>""", 28, style="flex:1"),
   col(box("purple", "children", "whatever goes between the tags", 0),
       box("green", "keep components pure", "same props in → same JSX out", 1),
       box("red", "no side effects while rendering", "no fetching, no changing outside variables", 1), style="width:520px"), top=True),
 "steps": [
  "Children is whatever you put between a component's tags. That makes wrapper components easy. Card shows a title, and then whatever's inside it.",
  "And keep components pure. Same props in, same JSX out. No side effects during rendering. No fetching, and no changing outside variables. React may render a component more than once, and purity keeps that safe. Side effects belong in event handlers and effects.",
 ]},

{"html": H("Lists and ", "keys") + code("""<ul>
  {tasks.map(task => (
§0     <li key={task.id}>{task.title}</li>
  ))}
</ul>""", 32) + row(box("green", "✓ a database id", "unique among siblings, stable across renders", 1, "flex:1"),
                     box("red", "✗ Math.random()", "a new key every render: rebuilds everything, loses state", 2, "flex:1"),
                     box("orange", "⚠️ the index", "only if the list never reorders, filters or inserts", 2, "flex:1"), style="margin-top:28px"),
 "steps": [
  "To render a list, map the array to elements. And every item needs a key.",
  "React uses keys to match items between renders. Which were added, removed, or moved. A good key is unique among its siblings, and stable across renders. A database I D is perfect.",
  "Math dot random gives a new key every render, so React rebuilds every item, and loses its state. And the array index only works if the list never reorders, filters, or gets items inserted. Otherwise, state ends up attached to the wrong items.",
 ]},

{"html": H("Conditional ", "rendering") + code("""§0 if (loading) return <p>Loading…</p>;          // early return
§0 if (error) return <p className="error">{error}</p>;

§1 {tasks.length === 0 ? <p>No tasks yet!</p> : <TaskList tasks={tasks} />}
§2 {hasPending && <span className="badge">Pending</span>}

§3 {tasks.length && <TaskList tasks={tasks} />}       // shows "0" 😬
§3 {tasks.length > 0 && <TaskList tasks={tasks} />}   // ✓""", 29),
 "steps": [
  "Three ways to render conditionally. For whole component states, like loading or error, return early.",
  "For one of two things, use a ternary.",
  "And for something or nothing, use double ampersand. You can also return null to render nothing at all.",
  "But watch out for the double ampersand trap. If the left side is the number zero, React renders a zero on the screen! So compare properly. Length greater than zero gives a real boolean.",
 ]},

{"html": H("Styling ", "components") + code("""§0 import "./TaskCard.css";                     // 1 · plain CSS (global)
§1 import styles from "./TaskCard.module.css";   // 2 · CSS Modules (local)
§1 <article className={styles.card}>
§2 <article className="p-4 rounded-xl border">  // 3 · Tailwind
§3 <div style={{ width: `${percent}%` }}>      // 4 · inline, dynamic only
§3 className={clsx("card", done && "done")}    // joining classes""", 29) +
   note("Pick one main approach · Tailwind and CSS Modules are the most common", 3),
 "steps": [
  "The CSS you already know still does the work. The question is how you attach it. One: a plain CSS file, imported by a component. Its class names are global.",
  "Two: CSS modules. Name the file dot module dot css, and its class names become local to the component. No clashes.",
  "Three: Tailwind. Utility classes, right in the JSX.",
  "Four: inline styles, but only for dynamic values, like a progress bar's width. And the tiny c l s x helper joins classes conditionally. Pick one main approach per project. Tailwind and CSS modules are the most common in React jobs today.",
 ]},

quiz([
  ("<code>class</code> in JSX?", "<code>className</code> · and <code>for</code> → <code>htmlFor</code>", "blue",
   "Quiz time. How do you write class in JSX?",
   "Class name. And for becomes html for."),
  ("What makes a good key?", "a <b style=\"display:inline\">stable, unique id</b> from the data", "green",
   "What makes a good key?",
   "A stable, unique I D from the data. Not math dot random, and usually not the index."),
  ("Why can <code>&amp;&amp;</code> render a 0?", "React renders numbers · <code>0 &amp;&amp; x</code> is 0", "red",
   "And why can double ampersand render a zero?",
   "Because React renders numbers, and zero and anything evaluates to zero."),
]),

recap(["UI = f(state) · components are capitalised functions",
       "JSX: <code>{ }</code> expressions · className · one root",
       "Props are read-only · <code>children</code> for wrappers",
       "Keep components pure",
       "Keys: stable, unique ids",
       "Early return · ternary · <code>&amp;&amp;</code> (beware 0)"],
  "Let's recap. UI is a function of state, and components are capitalised functions. In JSX, curly braces hold expressions, class becomes class name, and you return one root. Props are read-only, and children makes wrappers easy. Keep components pure. Use stable, unique I Ds for keys. And render conditionally with early returns, ternaries, and double ampersand, but beware the zero. Next time: state and events!"),
]
