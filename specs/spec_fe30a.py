from lib import *

TAG = "Frontend 30A · React with TypeScript and Patterns"
FILE = "Frontend 30A React Patterns, TypeScript and Next.js (Part 1).mp4"

SLIDES = [
title_slide("30A", "React Patterns & TypeScript", "Part 1 · typing components properly, and the patterns libraries are built from",
  "Welcome to module thirty, part one: React with TypeScript, and component patterns.",
  "These are the topics that fill the gap between I can build an app, and I can work on any React codebase. In this part: typing components properly, and the patterns reusable libraries are built from. Part two covers portals, class components, and Next.js."),

{"html": H("Typing props and ", "children") + code("""§0 type TaskCardProps = {
§0   title: string;
§0   priority?: number;                       // optional
§0   status: "TODO" | "IN_PROGRESS" | "DONE";  // a literal union
§0   onSelect: (id: number) => void;          // a callback prop
§0 };
§0 function TaskCard({ title, priority = 3, status, onSelect }: TaskCardProps) { … }

§1 type CardProps = { title: string; children: React.ReactNode };
§1 // or: React.PropsWithChildren<{ title: string }>""", 26) +
   note("Plain functions with typed props · <code>React.FC</code> in older code adds nothing today", 2),
 "steps": [
  "Props are just an object type. Name it after the component, plus props. Mark optional props with a question mark, use literal unions to allow only certain values, and type callback props as functions.",
  "Children are typed as React node, which covers everything React can render. Elements, strings, numbers, arrays, and null. Or use props with children.",
  "Write components as plain functions with typed props. You'll see React dot F C in older code. It's fine, but it adds nothing today.",
 ]},

{"html": H("Events and ", "state") + row(
   col(table(["Handler", "Event type"], [
     (["<code>onChange</code> on input", "<code>ChangeEvent&lt;HTMLInputElement&gt;</code>"], 0),
     (["<code>onSubmit</code> on form", "<code>FormEvent&lt;HTMLFormElement&gt;</code>"], 0),
     (["<code>onClick</code> on button", "<code>MouseEvent&lt;HTMLButtonElement&gt;</code>"], 0),
     (["<code>onKeyDown</code>", "<code>KeyboardEvent&lt;HTMLInputElement&gt;</code>"], 0)], size=30), style="flex:1")) +
   code("""§1 const [count, setCount] = useState(0);                   // number, inferred
§1 const [user, setUser] = useState<User | null>(null);      // null now, a User later
§1 const [tasks, setTasks] = useState<Task[]>([]);           // [] alone → never[]
§1 const [status, setStatus] = useState<"idle" | "loading" | "error">("idle");""", 25, style="margin-top:22px"),
 "steps": [
  "Events have their own types, parameterised by the element. Change event for inputs, form event for submit, mouse event for clicks, and keyboard event for keys. A shortcut: write the handler inline once, hover the event in your editor, and copy the type it shows.",
  "State is inferred from the initial value. Annotate it when the initial value doesn't tell the whole story. Null now, but a user later. And an empty array, which TypeScript would infer as never array, so pushing anything later would be an error.",
 ]},

{"html": H("Refs and HTML ", "props") + code("""§0 const inputRef = useRef<HTMLInputElement>(null);
§0 useEffect(() => { inputRef.current?.focus(); }, []);   // ?. : it can be null
§0 const timerRef = useRef<number | null>(null);           // a mutable value

§1 type ButtonProps = React.ComponentProps<"button"> & { variant?: "primary" | "ghost" };
§1 function Button({ variant = "primary", className = "", ...rest }: ButtonProps) {
§1   return <button className={`btn btn-${variant} ${className}`} {...rest} />;
§1 }
§1 <Button type="submit" disabled={saving} onClick={save}>Save</Button>   // all typed""", 26),
 "steps": [
  "Refs to DOM elements start as null, until React attaches them. So type the element, and use optional chaining. A ref can also hold a mutable value, like a timer I D.",
  "To build a button that accepts everything a real button does, type its props as component props of button, plus your own. Then spread the rest onto the real button. Type, disabled, on click, all fully typed.",
 ]},

{"html": H("Generics, context and ", "reducers") + code("""§0 function List<T>({ items, getKey, renderItem }: ListProps<T>) {
§0   return <ul>{items.map(item => <li key={getKey(item)}>{renderItem(item)}</li>)}</ul>;
§0 }
§0 <List items={tasks} getKey={t => t.id} renderItem={t => t.title} />   // t: Task

§1 const AuthContext = createContext<AuthContextValue | null>(null);
§1 export function useAuth() {
§1   const ctx = useContext(AuthContext);
§1   if (!ctx) throw new Error("useAuth must be used inside <AuthProvider>");
§1   return ctx;                               // no null checks in components
§1 }
§2 type Action = { type: "added"; task: Task } | { type: "deleted"; id: number };
§2 dispatch({ type: "deleted" });              // ❌ Property 'id' is missing""", 25),
 "steps": [
  "Generic components keep the types of the data you pass in. This list works for any item type. Pass tasks, and t is inferred as a task. In a t s x file, a generic arrow function needs a comma after T, so it isn't read as JSX.",
  "For context, include null in its type, and write a hook that throws if there's no provider. Then components never need null checks.",
  "And for reducers, a discriminated union of actions makes every dispatch checked. Forget the I D, and it's a compile error.",
 ]},

{"html": H("Composition and ", "slots") + code("""§0 function Dialog({ title, footer, children }: DialogProps) {
§0   return (
§0     <div className="dialog">
§0       <header>{title}</header>
§0       <div className="body">{children}</div>
§0       {footer && <footer>{footer}</footer>}
§0     </div>
§0   );
§0 }
§1 <Dialog title="Delete task?"
§1   footer={<><Button variant="ghost">Cancel</Button><Button>Delete</Button></>}>
§1   This can't be undone.
§1 </Dialog>""", 26),
 "steps": [
  "Now the patterns. First, composition. Before adding a prop for every variation, let the parent pass the content in. Children, plus named slots like title and footer.",
  "So the caller decides what goes in each slot. And composition helps performance too. Children created by the parent don't re-render when the wrapper's own state changes.",
 ]},

{"html": H("Compound ", "components") + row(code("""§0 function Tab({ id, children }: TabProps) {
§0   const { active, setActive } = useTabs();   // context
§0   return <button role="tab"
§0     aria-selected={active === id}
§0     onClick={() => setActive(id)}>{children}</button>;
§0 }
§0 Tabs.List = TabList;
§0 Tabs.Tab = Tab;
§0 Tabs.Panel = TabPanel;""", 25, style="flex:1"),
   code("""§1 <Tabs defaultTab="open">
§1   <Tabs.List>
§1     <Tabs.Tab id="open">Open</Tabs.Tab>
§1     <Tabs.Tab id="done">Done</Tabs.Tab>
§1   </Tabs.List>
§1   <Tabs.Panel id="open">
§1     <TaskList status="TODO" />
§1   </Tabs.Panel>
§1 </Tabs>""", 25, style="flex:1"), top=True) +
   note("The caller decides layout and order · Tabs handles the state · how <u>Radix</u> and Headless UI work", 2),
 "steps": [
  "Compound components are several components that work together, and share state through context. Tabs holds the active tab in a provider. Each tab reads it with a hook, and attaches as a property, like tabs dot tab.",
  "Using it reads like HTML. A tab list with tabs, and a panel for each.",
  "The user of tabs decides the layout and order, and tabs handles the state. That's how libraries like Radix and Headless UI are built.",
 ]},

{"html": H("Render props, HOCs, and ", "hooks") + row(
   col(code("""§0 <MousePosition>
§0   {({ x, y }) => <p>{x}, {y}</p>}
§0 </MousePosition>""", 25),
       code("""§1 function withAuth<P extends object>(
§1     Component: React.ComponentType<P>) {
§1   return function Protected(props: P) {
§1     if (!useAuth().user) return <Navigate to="/login" />;
§1     return <Component {...props} />;
§1   };
§1 }""", 25), style="flex:1"),
   col(table(["Pattern", "Today"], [
     (["composition", "everywhere"], 2),
     (["compound", "UI libraries"], 2),
     (["render props", "→ hooks"], 2),
     (["HOCs", "→ hooks"], 2),
     (["<b>custom hooks</b>", "the default"], 2)], size=26), style="width:440px;flex-shrink:0"), top=True),
 "steps": [
  "Render props. A component takes a function as its child, and calls it with its data. Here, mouse position gives you x and y, and you decide what to render.",
  "A higher order component is a function that takes a component, and returns a new one with extra behaviour. With auth redirects logged out users to the login page.",
  "Render props and HOCs were the main ways to share logic before hooks. Today a custom hook usually does it more simply, with no extra components, and no wrapper hell in dev tools. You'll still meet them in older code, like Redux's connect. So know how to compare them.",
 ]},

quiz([
  ("Why does <code>useState([])</code> need a type?", "an empty array infers <code>never[]</code>", "blue",
   "Quiz time. Why does use state with an empty array need a type annotation?",
   "Because an empty array is inferred as never array, so adding items later is a type error."),
  ("Accept every attribute of a button?", "<code>React.ComponentProps&lt;\"button\"&gt;</code> + spread", "green",
   "How do you make a component accept every attribute a normal button accepts?",
   "Type its props as component props of button, and spread the rest onto the real button."),
  ("Why did hooks replace HOCs?", "logic with <b style=\"display:inline\">no wrapper</b> components", "purple",
   "And why did custom hooks mostly replace HOCs and render props?",
   "Hooks share logic without adding components to the tree. No wrapper nesting, no prop name collisions, and the data flow is visible where you call them."),
]),

recap(["Props: an object type · children: React.ReactNode",
       "Events: ChangeEvent, FormEvent, MouseEvent",
       "Annotate state when the initial value isn't enough",
       "ComponentProps&lt;\"button\"&gt; · generic components",
       "Composition · compound components",
       "Render props + HOCs → custom hooks"],
  "Let's recap part one. Props are an object type, and children are a React node. Events have their own types, like change event and form event. Annotate state when the initial value isn't enough. Extend HTML props with component props, and write generic components. Compose with children and slots, and build compound components with context. And render props and HOCs have mostly given way to custom hooks. Next time: part two, portals, class components, and Next.js!"),
]
