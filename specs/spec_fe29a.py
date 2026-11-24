from lib import *

TAG = "Frontend 29A · Project: Task Manager UI, Part 1"
FILE = "Frontend 29A Project Build the Task Manager UI (Part 1).mp4"

SLIDES = [
title_slide("29A", "Project: Build the Task Manager UI", "Part 1 · steps 1 to 5: components, state, a fake API, hooks, routing",
  "Welcome to module twenty nine, part one: the project. Build the task manager UI.",
  "Ten steps, one per React day, from an empty folder to a deployed full-stack app. You'll build the React front end for the task manager API from the backend days. Projects, tasks, and JWT login. Each step uses what that day's module taught, and ends with a checkpoint. This part covers steps one to five. Type the code yourself, and commit after every checkpoint."),

{"html": H("The ", "plan") + fill(
   row(box("blue", "1 · components", "", 0, "flex:1"), box("blue", "2 · state", "", 0, "flex:1"), box("blue", "3 · fake API", "", 0, "flex:1"),
       box("blue", "4 · custom hooks", "", 0, "flex:1"), box("blue", "5 · routing", "", 0, "flex:1"), gap=14),
   row(box("green", "6 · TanStack Query", "", 1, "flex:1"), box("green", "7 · real API + login", "", 1, "flex:1"), box("green", "8 · forms + errors", "", 1, "flex:1"),
       box("green", "9 · polish", "", 1, "flex:1"), box("green", "10 · tests + deploy", "", 1, "flex:1"), gap=14),
   note("Steps 1–6 use a <u>fake API</u> in the browser · step 7 switches to your Spring Boot API", 2)),
 "steps": [
  "Here's the plan. Steps one to five build the app's core. Components, state, a fake API, custom hooks, and routing.",
  "Steps six to ten make it production ready. TanStack Query, the real API with login, forms and errors, polish, and finally tests and deployment.",
  "Steps one to six use a fake API in the browser, so you don't need the backend yet. Step seven switches to your real Spring Boot API.",
 ]},

{"html": H("Step 1: the task ", "list") + code("""§0 npm create vite@latest task-ui -- --template react-ts && npm install && npm run dev""", 25) + row(
   code("""§1 export type TaskStatus =
§1   "TODO" | "IN_PROGRESS" | "DONE";
§1 export type Task = {
§1   id: number; title: string;
§1   status: TaskStatus;
§1   priority: number;        // 1 to 5
§1   dueDate: string | null;  // ISO date
§1 };""", 25, style="flex:1"),
   code("""§2 function TaskList({ tasks }: Props) {
§2   if (tasks.length === 0)
§2     return <p>No tasks yet.</p>;
§2   return <ul>{tasks.map(task => (
§2     <li key={task.id}>
§2       <TaskCard task={task} />
§2     </li>))}</ul>;
§2 }""", 25, style="flex:1"), top=True, style="margin-top:18px") +
   note("✅ three cards · <code>[]</code> shows \"No tasks yet.\" · no key warnings · <code>npm run build</code> passes", 3),
 "steps": [
  "Step one. Create a Vite project with the React TypeScript template, and start the dev server.",
  "Describe the data. These types mirror your Spring task response record. I D, title, status, priority, and due date. So switching to the real API later needs no changes here. Spring sends a local date as an ISO string.",
  "Then two small components. A task card for one task, and a task list that maps them, with a key on each item, and an empty state. Start with three hard-coded sample tasks, and add a little CSS.",
  "Your checkpoint. The page shows three cards, and the done one is crossed out. An empty array shows no tasks yet. There are no key warnings. And npm run build passes, because it type-checks too. Commit.",
 ]},

{"html": H("Step 2: ", "state", " and events") + code("""§0 const [tasks, setTasks] = useState<Task[]>(sampleTasks);
§0 const [filter, setFilter] = useState<Filter>("ALL");
§1 const visible = filter === "ALL" ? tasks : tasks.filter(t => t.status === filter);   // derived
§1 const openCount = tasks.filter(t => t.status !== "DONE").length;
§2 function addTask(title: string, priority: number) {
§2   setTasks(ts => [...ts, { id: Date.now(), title, priority, status: "TODO", dueDate: null }]);
§2 }
§2 const changeStatus = (id: number, status: TaskStatus) =>
§2   setTasks(ts => ts.map(t => (t.id === id ? { ...t, status } : t)));
§2 const deleteTask = (id: number) => setTasks(ts => ts.filter(t => t.id !== id));
§3 <AddTaskForm onAdd={addTask} />
§3 <FilterTabs value={filter} onChange={setFilter} />
§3 <TaskList tasks={visible} onStatusChange={changeStatus} onDelete={deleteTask} />""", 24),
 "steps": [
  "Step two makes it interactive. State lives in App, the closest common parent of the form and the list. That's lifting state up.",
  "The visible list and the open count are derived during render, never stored. So they're always consistent with the tasks.",
  "Adding, changing status, and deleting all replace state, never mutate it. Spread to add, map to update, filter to remove.",
  "Then pass the callbacks down. A controlled add task form, with its button disabled while the title is empty. Filter tabs with aria pressed. And each task card gets a status select, and a labelled delete button. Checkpoint: everything works, and reloading loses your changes. That's expected. Step three fixes it.",
 ]},

{"html": H("Step 3: a fake ", "API") + row(code("""§0 const delay = (ms = 400) =>
§0   new Promise(r => setTimeout(r, ms));
§0 export async function getTasks(projectId: number) {
§0   await delay();
§0   if (Math.random() < 0.1)
§0     throw new Error("Server error (simulated)");
§0   return load().tasks.filter(…).map(strip);
§0 }""", 24, style="flex:1"),
   code("""§1 type Load =
§1   | { status: "loading" }
§1   | { status: "error"; message: string }
§1   | { status: "ready" };
§2 useEffect(() => {
§2   let ignore = false;
§2   api.getTasks(1)
§2     .then(d => { if (!ignore) { setTasks(d); … } })
§2     .catch(e => { if (!ignore) setLoad(…); });
§2   return () => { ignore = true; };
§2 }, [reloadKey]);""", 24, style="flex:1"), top=True) +
   note("✅ \"Loading…\" then the list · 1 in 10 shows the error + <u>Try again</u> · \"Adding…\" while saving", 3),
 "steps": [
  "Step three loads and saves tasks through an async API module, so the app already behaves like it talks to a server. The fake API stores data in local storage, adds a delay, and fails one time in ten, so you can test your error state. Its functions have the same shape as the real API in step seven.",
  "Model the request with a discriminated union. Loading, error with a message, or ready. Impossible combinations can't happen.",
  "Load in an effect, with an ignore flag in the cleanup, to drop late results. A reload key lets a try again button run it again. And focus the title input with a ref when the page loads.",
  "Checkpoint. You briefly see loading, then the list, and your changes survive a reload. Sometimes you see the error, and try again works. In development the effect runs twice, and nothing breaks. And the add button says adding while it saves.",
 ]},

{"html": H("Step 4: custom ", "hooks") + code("""§0 export function useTasks(projectId: number) {
§0   const [tasks, dispatch] = useReducer(tasksReducer, []);
§0   … load in an effect …
§0   const add = useCallback(async (title, priority) => {
§0     dispatch({ type: "added", task: await api.createTask(projectId, …) });
§0   }, [projectId]);
§0   return { tasks, status, error, add, setTaskStatus, remove, reload };
§0 }""", 25) + row(
   code("""§1 const q = useDebounce(query, 250);
§1 tasks.filter(t => t.title.toLowerCase()
§1   .includes(q.toLowerCase()))""", 24, style="flex:1"),
   code("""§2 <ThemeProvider><App /></ThemeProvider>
§2 root.dataset.theme = theme;""", 24, style="flex:1"), top=True, style="margin-top:18px") +
   note("App now reads like a summary: <code>const { tasks, add, remove } = useTasks(1);</code>", 3),
 "steps": [
  "Step four. App is getting crowded, so move all the task logic into a custom hook, use tasks. A reducer handles loaded, added, updated, and deleted. Components get data and actions, without knowing how loading works.",
  "Add a debounced search. Use debounce delays the query, and the list is filtered during render.",
  "And dark mode with context. A theme provider holds the theme, remembers it in local storage, and sets a data attribute on the root element, so CSS variables switch colours. Any component can toggle it with use theme.",
  "Now App reads like a summary. Checkpoint: everything still works, search filters a moment after you stop typing, and dark mode survives a reload. And the reducer is a pure function, testable without React.",
 ]},

{"html": H("Step 5: ", "routing") + table(["URL", "Page"], [
     (["<code>/</code>", "projects + a create form"], 0),
     (["<code>/projects/:projectId?status=TODO</code>", "one project's tasks"], 0),
     (["<code>/tasks/:taskId</code>", "one task: details, edit, delete"], 0),
     (["<code>*</code>", "page not found"], 0)], size=26) +
   code("""§1 const id = Number(useParams().projectId);          // a string from the URL
§1 const [params, setParams] = useSearchParams();
§1 const filter = params.get("status") ?? "ALL";
§1 <FilterTabs onChange={f => setParams(f === "ALL" ? {} : { status: f })} />""", 25, style="margin-top:20px") +
   note("✅ filter in the URL survives refresh · Back undoes it · no full page reloads", 2),
 "steps": [
  "Step five adds real URLs. The backend has projects, so the app becomes three pages. The projects list, one project's tasks, and one task's details. Plus a not found page. A layout route holds the top bar, and an outlet for the page.",
  "The project page reads its I D from the URL. Remember, it's a string. And the filter lives in the query string, so refresh, bookmarks, and the back button all work. Make each task title a link to its own page. And after deleting a task, navigate minus one goes back.",
  "Checkpoint. Choosing a filter changes the URL, refreshing keeps it, and back undoes it. A missing task shows not found. And navigating never reloads the page. Commit, and that's the first half of the project.",
 ]},

quiz([
  ("Why mirror the Spring DTOs in <code>types.ts</code>?", "the switch to the real API needs <b style=\"display:inline\">no changes</b>", "blue",
   "Quiz time. Why mirror the Spring D T Os in your types file?",
   "So switching to the real API in step seven needs no changes there."),
  ("Where does the filter live in step 5?", "in the <b style=\"display:inline\">URL</b> query string", "green",
   "Where does the filter live after step five?",
   "In the URL query string. So refresh, bookmarks, and back all work."),
  ("Why a discriminated union for loading?", "impossible states <b style=\"display:inline\">can't happen</b>", "purple",
   "And why model loading with a discriminated union?",
   "So impossible combinations, like loading and error at once, can't happen."),
]),

recap(["Step 1: types that mirror Spring · small components",
       "Step 2: state in App · derived values · never mutate",
       "Step 3: fake async API · loading, error, ready",
       "Step 4: useTasks + reducer · debounce · theme context",
       "Step 5: React Router · filter in the URL",
       "Commit after every checkpoint"],
  "Let's recap part one. Step one: types that mirror Spring, and small components. Step two: state in App, derived values, and never mutating. Step three: a fake async API, with loading, error, and ready states. Step four: a use tasks hook with a reducer, a debounced search, and a theme context. And step five: React Router, with the filter in the URL. Commit after every checkpoint. Next time: part two, steps six to ten!"),
]
