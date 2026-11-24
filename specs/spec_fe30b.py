from lib import *

TAG = "Frontend 30B · Portals, Class Components and Next.js"
FILE = "Frontend 30B React Patterns, TypeScript and Next.js (Part 2).mp4"

SLIDES = [
title_slide("30B", "Portals, Classes & Next.js", "Part 2 · portals and refs, class components, and the Next.js App Router",
  "Welcome to module thirty, part two.",
  "In this final part: portals, and passing refs to your own components. Class components and their lifecycle methods, and how they map to hooks. And the basics of Next.js: the App Router, layouts, server and client components, and server actions."),

{"html": H("", "Portals") + code("""§0 import { createPortal } from "react-dom";
§0 function Modal({ open, onClose, children }: ModalProps) {
§0   if (!open) return null;
§0   return createPortal(
§0     <div className="backdrop" onClick={onClose}>
§0       <div className="modal" role="dialog" aria-modal="true"
§0            onClick={e => e.stopPropagation()}>
§0         {children}
§0       </div>
§0     </div>,
§0     document.body
§0   );
§0 }""", 26) +
   note("Events bubble through the <u>React</u> tree · still add focus, Tab trap, Escape, restore focus", 2),
 "steps": [
  "A portal renders a component's output into a different DOM node, usually document dot body, while it stays in the same place in the React tree.",
  "Why? A modal or tooltip rendered deep inside a card can be clipped by the card's overflow hidden, or trapped under other content by a parent's z index or transform. Rendering it at the end of body escapes all of that.",
  "Two things to know. Events bubble through the React tree, not the DOM tree. So a click inside the portal still reaches its React parents. And a portal adds no accessibility for free. Focus the dialog, trap tab inside, close on escape, and restore focus afterwards. Or use the native dialog element.",
 ]},

{"html": H("Passing ", "refs") + code("""§0 function TextField({ label, ref, ...rest }: React.ComponentProps<"input"> & { label: string }) {
§0   return <label>{label} <input ref={ref} {...rest} /></label>;
§0 }
§0 const emailRef = useRef<HTMLInputElement>(null);
§0 <TextField label="Email" ref={emailRef} />     // later: emailRef.current?.focus()

§1 // before React 19
§1 const TextField = forwardRef<HTMLInputElement, Props>(function TextField({ label, ...rest }, ref) {
§1   return <label>{label} <input ref={ref} {...rest} /></label>;
§1 });""", 24) +
   note("<code>useImperativeHandle</code> exposes just <code>open()</code> / <code>close()</code> · use refs sparingly", 2),
 "steps": [
  "Sometimes a parent needs the DOM node inside a child, say to focus the input inside your text field. In React nineteen, ref is simply a prop of function components. Pass it on to the real input.",
  "Before React nineteen, you had to wrap the component in forward ref. You'll see that in most existing code.",
  "To expose specific methods instead of the whole node, like open and close on a custom dialog, use imperative handle lets the child decide what the ref gives. But use refs sparingly. Props and state should drive most behaviour.",
 ]},

{"html": H("Class ", "components") + code("""§0 class UserProfile extends React.Component<Props, State> {
§0   state: State = { user: null, error: null };
§1   componentDidMount() { this.load(); }                 // like useEffect(…, [])
§1   componentDidUpdate(prevProps: Props) {               // compare to react to changes
§1     if (prevProps.userId !== this.props.userId) this.load();
§1   }
§1   componentWillUnmount() { this.controller?.abort(); } // cleanup
§2   handleRefresh = () => this.load();                   // arrow field: this stays bound
§2   render() {
§2     const { user, error } = this.state;
§2     if (error) return <p>{error}</p>;
§2     if (!user) return <p>Loading…</p>;
§2     return <div><h2>{user.name}</h2><button onClick={this.handleRefresh}>Refresh</button></div>;
§2   }
§2 }""", 24),
 "steps": [
  "Before hooks arrived in twenty nineteen, components with state were classes. Plenty of production code still uses them, and interviews ask how they map to hooks. A class extends React dot component, typed with props and state.",
  "Lifecycle methods run at set moments. Component did mount, after the first render. Component did update, after every update, where you compare the previous props. And component will unmount, before removal, for cleanup.",
  "Handlers are arrow class fields, so this stays bound. And render returns the JSX, reading this dot state and this dot props.",
 ]},

{"html": H("Classes vs ", "hooks") + table(["Class component", "Hooks equivalent"], [
     (["<code>this.state</code> / <code>this.setState</code>", "<code>useState</code> / <code>useReducer</code>"], 0),
     (["<code>componentDidMount</code>", "<code>useEffect(fn, [])</code>"], 0),
     (["<code>componentDidUpdate</code>", "<code>useEffect(fn, [dep])</code>"], 0),
     (["<code>componentWillUnmount</code>", "the cleanup returned from <code>useEffect</code>"], 0),
     (["<code>PureComponent</code>", "<code>React.memo</code>"], 1),
     (["instance fields (<code>this.timer</code>)", "<code>useRef</code>"], 1),
     (["<code>componentDidCatch</code>", "<b>no hook</b>: error boundaries stay classes"], 2)], size=28) +
   note("<code>setState</code> <u>merges</u> · logic split across methods · <code>UNSAFE_</code> methods are legacy", 3),
 "steps": [
  "Here's the mapping. State and set state become use state, or use reducer. Did mount is an effect with an empty dependency array. Did update is an effect with dependencies. And will unmount is the cleanup function the effect returns.",
  "Pure component becomes React dot memo. And instance fields, like a timer, become refs.",
  "But one thing has no hook equivalent. Error boundaries, with get derived state from error and component did catch, must still be classes. Most apps use the small react error boundary library, which is a class under the hood.",
  "Other differences. This dot set state merges the object into state, while use state replaces it. And related logic is split across several lifecycle methods, while one effect with a cleanup keeps it together. That's the main reason hooks won. Methods prefixed UNSAFE are legacy, and candidates for refactoring.",
 ]},

{"html": H("Next.js: the App ", "Router") + code("""§0 npx create-next-app@latest tasks-next      # accept the defaults
§0 cd tasks-next && npm run dev               # http://localhost:3000""", 25) + code("""§1 app/
§1 ├─ layout.tsx          wraps every page, stays mounted
§1 ├─ page.tsx            "/"
§1 ├─ loading.tsx         Suspense fallback while a page loads
§1 ├─ error.tsx           error boundary ("use client")
§1 ├─ not-found.tsx       the 404 page
§1 └─ projects/
§1    ├─ page.tsx         "/projects"
§1    └─ [projectId]/
§1       └─ page.tsx      "/projects/42"  (a dynamic segment)""", 25, style="margin-top:18px"),
 "steps": [
  "Next dot j s is a React framework. Routing from folders, server rendering, data loading on the server, and production defaults. Create a project, accept the defaults, and start the dev server.",
  "Routing is the app folder. Each folder is a URL segment, and special file names have special jobs. Layout wraps every page and stays mounted. Page is the route itself. Loading is shown while a page loads, and error catches errors. And a folder in square brackets, like project I D, is a dynamic segment.",
 ]},

{"html": H("Server ", "Components") + code("""§0 export default async function ProjectPage({ params }: { params: Promise<{ projectId: string }> }) {
§0   const { projectId } = await params;                // a promise in Next.js 15
§0   const res = await fetch(`${process.env.API_URL}/projects/${projectId}/tasks`,
§0                           { cache: "no-store" });
§0   if (res.status === 404) notFound();
§0   const page: { content: Task[] } = await res.json();
§0   return (
§0     <main>
§0       <AddTaskForm projectId={Number(projectId)} />
§0       <ul>{page.content.map(t => <li key={t.id}>{t.title}</li>)}</ul>
§0     </main>
§0   );
§0 }""", 24) +
   note("<code>API_URL</code> stays on the server · <code>NEXT_PUBLIC_</code> = exposed to the browser", 1),
 "steps": [
  "Pages are server components by default. They can be async, and fetch data directly. And their code never ships to the browser. In Next fifteen, params is a promise, so await it. If the API says four oh four, call not found.",
  "Process dot env dot API URL is read on the server, so it can point at your Spring API and stay out of the browser. Variables prefixed NEXT PUBLIC are the ones exposed to the browser, like Vite's VITE prefix.",
 ]},

{"html": H("Client components and server ", "actions") + row(code("""§0 "use client";
§0 export function AddTaskForm({ projectId }) {
§0   const [error, formAction, pending] =
§0     useActionState(addTask, null);
§0   return (
§0     <form action={formAction}>
§0       <input type="hidden" name="projectId"
§0              value={projectId} />
§0       <input name="title" required />
§0       <button disabled={pending}>Add</button>
§0       {error && <p role="alert">{error}</p>}
§0     </form>);
§0 }""", 23, style="flex:1"),
   code("""§1 "use server";
§1 export async function addTask(_prev, formData: FormData) {
§1   const title = String(formData.get("title") ?? "").trim();
§1   if (!title) return "Title is required";
§1   const res = await fetch(`${API}/projects/${id}/tasks`, {
§1     method: "POST",
§1     body: JSON.stringify({ title, priority: 3 }) });
§1   if (!res.ok) return "Couldn't add the task";
§1   revalidatePath(`/projects/${id}`);
§1   return null;
§1 }""", 23, style="flex:1"), top=True) +
   note("Also: <code>next/link</code> · <code>next/image</code> · <code>metadata</code> · <code>route.ts</code> · <code>middleware.ts</code>", 2),
 "steps": [
  "Client components, marked use client at the top, are needed for state, effects, event handlers, and browser APIs. Keep them small, at the leaves. This form uses use action state, which gives you the action's result, and a pending flag.",
  "A server action, marked use server, is a function that runs on the server, but can be called straight from a form. No API route to write. It validates, posts to your Spring API, and then revalidate path re-renders the page with fresh data.",
  "Other building blocks. Next link for navigation, next image for optimised images, a metadata export for the page title, route files for API endpoints, and middleware for things like redirecting logged out users.",
 ]},

{"html": H("Next.js or a Vite ", "SPA", "?") + row(
   box("blue", "Next.js", "public pages · SEO · fast first load · server-side data · marketing, shops, blogs · deploy on Vercel", 0, "flex:1"),
   box("green", "Vite SPA", "everything behind a login · talks to a Spring API · simpler · like the Module 29 project", 1, "flex:1")) +
   note("Server by default · <code>\"use client\"</code> only for state, effects, handlers, browser APIs", 2),
 "steps": [
  "When should you choose Next dot j s? For public pages that need SEO and a fast first load, like marketing sites, e-commerce, and blogs. Or when you want data loaded on the server. It deploys most easily on Vercel, though it runs anywhere Node runs.",
  "For an app that's entirely behind a login, and talks to a Spring API, like the project in module twenty nine, a Vite SPA is simpler and just as good.",
  "And inside Next, the rule is simple. Server components by default. Switch to a client component only when you need state, effects, event handlers, or browser APIs, and keep those small, so most of the page ships no JavaScript.",
 ]},

quiz([
  ("Why render a modal in a portal?", "escape <b style=\"display:inline\">overflow</b> and stacking contexts", "blue",
   "Quiz time. Why render a modal in a portal?",
   "So an ancestor's overflow or stacking context can't clip it or hide it. It still keeps its place in the React tree, so context and events still work."),
  ("What still needs a class?", "<b style=\"display:inline\">error boundaries</b>", "red",
   "Which feature still requires a class component?",
   "Error boundaries. Catching render errors has no hook equivalent."),
  ("File for <code>/projects/42</code>?", "<code>app/projects/[projectId]/page.tsx</code>", "green",
   "In the App Router, which file serves slash projects slash forty two?",
   "App, projects, project I D in square brackets, page dot t s x."),
  ("What does <code>\"use server\"</code> mark?", "a <b style=\"display:inline\">Server Action</b>", "purple",
   "And what does use server mark?",
   "A server action. A function that runs on the server, and can be called from a form."),
]),

recap(["createPortal: another DOM node, same React tree",
       "React 19: ref is a prop · forwardRef before",
       "Lifecycle methods → useEffect + cleanup",
       "Error boundaries are still classes",
       "App Router: folders are routes · Server Components by default",
       "\"use client\" at the leaves · Server Actions for forms"],
  "Let's recap part two. Create portal renders into another DOM node, while keeping its place in the React tree. In React nineteen, ref is just a prop, and forward ref came before. Lifecycle methods map to use effect and its cleanup, and error boundaries are still classes. In Next dot j s, folders are routes, and pages are server components by default. Use client components at the leaves, and server actions for forms. And that's the end of the frontend course. From your first HTML page to React, TypeScript, and Next dot j s. Together with Java and Spring, you're now a fullstack developer. Well done!"),
]
