from lib import *

TAG = "Frontend 19 · Routing and State Management"
FILE = "Frontend 19 Routing and State Management.mp4"

SLIDES = [
title_slide(19, "Routing & State Management", "Real URLs for your SPA, and a home for every kind of state",
  "Welcome to module nineteen: routing and state management.",
  "Real apps have many pages, and data that many components share. React Router gives your single page app real URLs. State management tools decide where shared data lives. And the most useful idea here: most global state is actually server data. And a tool like TanStack Query handles it better than any store."),

{"html": H("React ", "Router") + code("""<BrowserRouter>
  <Routes>
§0     <Route element={<Layout />}>
§0       <Route index element={<Home />} />                   {/* "/" */}
§0       <Route path="tasks" element={<TaskList />} />        {/* "/tasks" */}
§1       <Route path="tasks/:id" element={<TaskDetail />} />  {/* "/tasks/42" */}
§0       <Route path="*" element={<NotFound />} />
§0     </Route>
  </Routes>
</BrowserRouter>
§2 function Layout() {
§2   return <><nav><NavLink to="/tasks">Tasks</NavLink></nav><main><Outlet /></main></>;
§2 }
§1 const { id } = useParams();     // "42": always a string""", 27),
 "steps": [
  "React Router maps URLs to components, without reloading the page. Each route has a path and an element. Index is the home page, and a star catches anything else.",
  "A colon in a path is a URL parameter. Read it with use params. And it's always a string.",
  "Nested routes share a layout, like a navbar. The matched child page renders where you put the outlet. And use link, or nav link, instead of an a tag. They change the URL without a full page reload. Nav link even adds an active class for you.",
 ]},

{"html": H("Navigating and ", "protecting") + code("""§0 const navigate = useNavigate();
§0 const saved = await createTask(task);
§0 navigate(`/tasks/${saved.id}`);          // navigate(-1) goes back

§1 function RequireAuth() {
§1   const { user } = useAuth();
§1   if (!user) return <Navigate to="/login" replace />;
§1   return <Outlet />;
§1 }
§1 <Route element={<RequireAuth />}> … </Route>""", 29) +
   note("Hiding a page is <u>convenience, not security</u> · Spring Security protects every endpoint", 2),
 "steps": [
  "To navigate after an action, like saving, use navigate. Go to the new task's page. Navigate minus one goes back.",
  "Protected routes send logged out users to the login page. Require auth checks for a user. If there isn't one, it redirects. Otherwise, it renders the child routes.",
  "But remember, hiding a page in the frontend is convenience, not security. Anyone can call your API directly. Spring Security must protect every endpoint. And for deployment, the server must return index dot HTML for every path, so refreshing slash tasks slash forty two doesn't give a four oh four.",
 ]},

{"html": H("Where should state ", "live", "?") + table(["Kind", "Example", "Home"], [
   (["Local UI", "dropdown open, input text", "<code>useState</code>"], 0),
   (["Shared UI", "selected task in two panels", "lift to common parent"], 0),
   (["App-wide, rare changes", "user, theme, language", "context"], 1),
   (["URL", "page, filters, search, tab", "<code>useSearchParams</code>"], 2),
   (["Server data", "tasks, users from your API", "<b>TanStack Query</b>"], 3),
   (["Complex client global", "cart, multi-step editor", "Zustand / Redux Toolkit"], 4)], size=29),
 "steps": [
  "Before reaching for a library, sort your state into kinds. Each one has a natural home. Local UI state, like whether a dropdown is open, lives in use state. Shared UI state is lifted to the common parent.",
  "App-wide data that rarely changes, like the user or the theme, goes in context.",
  "Filters, tabs and pagination belong in the URL. Then users can bookmark, share and refresh, and the back button works.",
  "Server data isn't really your state. It's a cache of what's on the server, with loading, errors, staleness and refetching. TanStack Query solves all of that for you.",
  "And only complex, client-only global state, like a shopping cart, needs a store. Many apps that once needed Redux now need only TanStack Query, plus a little context.",
 ]},

{"html": H("Redux ", "Toolkit") + code("""§0 const cartSlice = createSlice({
§0   name: "cart",
§0   initialState: [] as CartItem[],
§0   reducers: {
§0     added(state, action: PayloadAction<{ id: number; name: string }>) {
§1       const item = state.find(i => i.id === action.payload.id);
§1       if (item) item.qty++;              // Immer makes this a safe copy
§1       else state.push({ ...action.payload, qty: 1 });
§0     },
§0   },
§0 });
§2 const store = configureStore({ reducer: { cart: cartSlice.reducer } });
§2 const count = useSelector((s: RootState) => s.cart.length);""", 27),
 "steps": [
  "Redux keeps app state in one store. Components dispatch actions, reducers compute the new state, and components select what they need. Redux Toolkit is the official, modern way to write it. A slice has a name, an initial state, and reducers.",
  "And look, this reducer seems to mutate the state. That's fine here, because a library called Immer turns those changes into a safe, immutable copy.",
  "Configure store creates the store, and use selector reads just what a component needs. It re-renders only when that value changes. Teams pick Redux for predictable updates, great dev tools with time travel, and a standard structure for large teams.",
 ]},

{"html": H("", "Zustand") + row(code("""§0 export const useCart = create<CartState>()(set => ({
§0   items: [],
§0   add: item => set(state => ({
§0     items: [...state.items, { ...item, qty: 1 }],
§0   })),
§0   remove: id => set(state => ({
§0     items: state.items.filter(i => i.id !== id),
§0   })),
§0 }));
§1 const count = useCart(s => s.items.length);
§1 const add = useCart(s => s.add);""", 27, style="flex:1"),
   table(["", "Context", "Zustand", "RTK"], [
     (["Setup", "built in", "tiny", "more"], 2),
     (["Re-renders", "every reader", "selected slice", "selected slice"], 2),
     (["Best for", "theme, user", "most global state", "large teams"], 2)], size=25), top=True),
 "steps": [
  "Zustand is a much smaller global store. It's just a hook you create. No providers, no actions, no slices. The state and the functions that change it live together.",
  "Any component selects a slice, and re-renders only when that slice changes.",
  "So compare them. Context is built in, but every reader re-renders. Zustand is tiny, and only re-renders what changed. Great for most client side global state. And Redux Toolkit has more structure, for large apps and teams.",
 ]},

{"html": H("TanStack ", "Query") + code("""§0 const { data: tasks, isPending, error } = useQuery({
§0   queryKey: ["tasks"],                          // the cache key
§0   queryFn: () => api.get<Task[]>("/tasks"),
§0 });

§1 const mutation = useMutation({
§1   mutationFn: (title: string) => api.post<Task>("/tasks", { title }),
§1   onSuccess: () => queryClient.invalidateQueries({ queryKey: ["tasks"] }),
§1 });
§1 mutation.mutate("New task");""", 28) +
   row(box("green", "caching + dedupe", "two components, one request", 2, "flex:1"),
       box("blue", "stale-while-revalidate", "cached data now, fresh in the background", 2, "flex:1"),
       box("purple", "no race conditions", "results keyed by <code>queryKey</code>", 2, "flex:1"), style="margin-top:22px"),
 "steps": [
  "TanStack Query fetches, caches, deduplicates, retries, and refreshes server data. It replaces most hand written use effect fetching. Use query takes a query key, which is the cache key, and a function that returns a promise. You get the data, a pending flag, and any error.",
  "To change data, use mutation. When it succeeds, invalidate the tasks query, and the list refetches automatically.",
  "And you get a lot for free. Two components asking for tasks share one request. Cached data shows instantly, while fresh data loads in the background. And no race conditions, because results are keyed by the query key. Put everything the data depends on in the key, like the status and page.",
 ]},

quiz([
  ("Where should filters and pagination live?", "in the <b style=\"display:inline\">URL</b>", "blue",
   "Quiz time. Where should filters and pagination live?",
   "In the URL. Then bookmarks, sharing and the back button all work."),
  ("Does a protected route secure your data?", "<b style=\"display:inline\">No</b> · the backend must check every request", "red",
   "Does a protected route secure your data?",
   "No. The backend must check every request."),
  ("Best home for server data?", "a server-state cache: <b style=\"display:inline\">TanStack Query</b>", "green",
   "And what's the best home for server data?",
   "A server state cache, like TanStack Query."),
]),

recap(["Routes, <code>:params</code>, nested layouts with <code>&lt;Outlet /&gt;</code>",
       "Link, not a href · <code>useNavigate</code> after actions",
       "Protected routes are convenience · secure the API",
       "Filters, tabs, pages → the URL",
       "Server data → TanStack Query",
       "Client global state → Zustand or Redux Toolkit"],
  "Let's recap. React Router gives you routes, URL parameters, and nested layouts with an outlet. Use link instead of a tags, and use navigate after actions. Protected routes are a convenience, so always secure the API. Put filters, tabs and pages in the URL. Server data belongs in TanStack Query. And only complex client state needs Zustand or Redux Toolkit. Next time: React with a Spring Boot API!"),
]
