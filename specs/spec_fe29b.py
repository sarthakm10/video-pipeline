from lib import *

TAG = "Frontend 29B · Project: Task Manager UI, Part 2"
FILE = "Frontend 29B Project Build the Task Manager UI (Part 2).mp4"

SLIDES = [
title_slide("29B", "Project: Build the Task Manager UI", "Part 2 · steps 6 to 10: TanStack Query, the real API, forms, polish, deploy",
  "Welcome to module twenty nine, part two.",
  "In part one, you built the app's core on a fake API. Now you make it real. TanStack Query, your Spring Boot API with JWT login, proper forms, polish, and finally tests and deployment. By step ten, you have a portfolio project you can demo and explain in an interview."),

{"html": H("Step 6: TanStack ", "Query") + code("""§0 export function useTasks(projectId: number) {           // same return shape
§0   const key = ["projects", projectId, "tasks"];
§0   const query = useQuery({ queryKey: key, queryFn: () => api.getTasks(projectId) });
§1   const statusMutation = useMutation({
§1     mutationFn: ({ id, status }) => api.updateTask(id, { status }),
§1     onMutate: async ({ id, status }) => {                    // optimistic
§1       const previous = queryClient.getQueryData<Task[]>(key);
§1       queryClient.setQueryData<Task[]>(key, old => old?.map(t => t.id === id ? { ...t, status } : t));
§1       return { previous };
§1     },
§1     onError: (_e, _v, ctx) => queryClient.setQueryData(key, ctx?.previous),   // roll back
§1     onSettled: invalidate,
§1   });""", 24) + note("✅ page components <u>didn't change</u> · cached projects show instantly · Devtools show the queries", 2),
 "steps": [
  "Step six swaps use tasks' internals for TanStack Query. Caching, refetching, and no race conditions, for free. Wrap the app in a query client provider. Then use query loads the tasks, keyed by the project.",
  "Mutations change data, and invalidate the query afterwards. And status changes are optimistic. On mutate updates the cache first, and keeps the previous value. If the request fails, on error rolls it back.",
  "And here's the payoff of step four. The hook returns the same shape as before, so no page component needs to change. Going back to a project shows its tasks instantly, from the cache. Checkpoint: the devtools show your queries, and the reducer and hand-written effect are gone.",
 ]},

{"html": H("Step 7: the real ", "API") + row(code("""§0 // vite.config.ts
§0 server: { proxy: { "/api": "http://localhost:8080" } }

§1 export async function request<T>(path, options = {}) {
§1   const res = await fetch(`${BASE}${path}`, { ...options,
§1     headers: { "Content-Type": "application/json",
§1       ...(token ? { Authorization: `Bearer ${token}` } : {}) } });
§1   if (res.status === 401 && token) onUnauthorized();
§1   if (res.status === 204) return undefined as T;
§1   const body = await res.json().catch(() => null);
§1   if (!res.ok) throw new ApiError(res.status, body?.detail);
§1   return body as T;
§1 }
§2 export const getTask = (id: number) => request<Task>(`/tasks/${id}`);""", 24, style="flex:1")),
 "steps": [
  "Step seven replaces the fake API with your real Spring Boot task manager API. Start Spring on port eighty eighty. Then proxy slash A P I to it in Vite's config, so there's no CORS to fight yet.",
  "Write one HTTP client. It adds the bearer token, turns Spring's problem detail errors into JavaScript errors, and calls a logout handler on any four oh one.",
  "Then a tasks API module, with the same function names as the fake one. Spring returns tasks as a page, so read its content. Now each hook changes just one import line.",
 ]},

{"html": H("Step 7: JWT ", "login") + row(code("""§0 async function login(email: string, password: string) {
§0   const { token } = await request<{ token: string }>(
§0     "/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
§0   setToken(token);
§0   setUser(userFromToken(token));        // display only; the server verifies
§0 }
§0 const logout = () => { setToken(null); setUser(null); queryClient.clear(); };
§1 export function RequireAuth() {
§1   const { user } = useAuth();
§1   const location = useLocation();
§1   return user ? <Outlet />
§1     : <Navigate to="/login" replace state={{ from: location }} />;
§1 }""", 24, style="flex:1")) +
   note("401 everywhere → header missing · 404 from Vite → restart for the proxy · 403 on POST → disable CSRF", 2),
 "steps": [
  "An auth context holds the user, plus login, sign up, and logout. Login posts the credentials, stores the token, and reads the user from its payload. That's for display only. The server verifies the signature. Logout clears the token and the query cache, so no other user's data lingers.",
  "Require auth wraps the app's routes. A logged out user goes to the login page, which remembers where they were going, and sends them back after logging in. Checkpoint: data now comes from PostgreSQL, and two users never see each other's projects.",
  "If it doesn't work: a four oh one on everything means the authorization header is missing. A four oh four from Vite means restart it for the proxy. And a four oh three on POST may be Spring's CSRF protection, which a stateless JWT API should disable.",
 ]},

{"html": H("Step 8: forms and ", "errors") + code("""§0 export const taskSchema = z.object({
§0   title: z.string().trim().min(1, "Title is required").max(200),
§0   priority: z.coerce.number().int().min(1).max(5),
§0   dueDate: z.string()
§0     .refine(v => v === "" || v >= today(), "The due date can't be in the past")
§0     .transform(v => (v === "" ? null : v)),
§0 });
§1 } catch (e) {                     // Spring's 400: "title: must not be blank"
§1   if (e instanceof ApiError && e.status === 400) setError(field, { message });
§1   else setError("root", { message });
§1 }""", 25) + note("Token expired → any 401 logs out → login page says <u>\"Your session expired\"</u>", 2),
 "steps": [
  "Step eight builds a proper task form, for both create and edit. One Zod schema matches the backend's rules. Title required, at most two hundred characters. Priority one to five, coerced from the select's string. And no due date in the past. An empty date becomes null.",
  "When Spring rejects the request with a four hundred, its message names the field. So set the error under that field. Anything else shows above the button. Reuse the same form for editing, with default values from the task, saved with a PATCH.",
  "And token expiry. The token lasts fifteen minutes. Any four oh one already logs the user out, and require auth remembers where they were. So just tell them why: your session expired, please log in again. Real apps add refresh tokens, a great stretch goal.",
 ]},

{"html": H("Step 9: ", "polish") + row(
   code("""§0 const query = useInfiniteQuery({
§0   queryKey: ["projects", projectId, "tasks", status],
§0   queryFn: ({ pageParam }) => request<Page<Task>>(
§0     `/projects/${projectId}/tasks?page=${pageParam}&size=20`),
§0   initialPageParam: 0,
§0   getNextPageParam: (last, _all, lastParam) =>
§0     lastParam + 1 < last.totalPages ? lastParam + 1 : undefined,
§0 });""", 23, style="flex:1"),
   col(box("gray", "skeletons", "same size as cards → no CLS", 1),
       box("red", "error boundary", "around the routes", 1),
       box("purple", "lazy pages", "a chunk each · Suspense", 1),
       box("green", "a11y + Profiler", "labels · keyboard · announce · focus h1 · Lighthouse 90+", 2), gap=12, style="width:440px"), top=True),
 "steps": [
  "Step nine is the difference between it works and it's good. Real pagination. Your API pages results, so use infinite query with a load more button. And pass the status filter to the server, because the browser no longer has every task.",
  "Show skeletons the same size as real cards, so nothing jumps. Wrap the routes in an error boundary, so a bug shows a message, not a blank page. And lazy load the pages, so each becomes its own chunk.",
  "Then an accessibility pass. Labels on every input, everything works by keyboard, announce task added in a live region, and move focus to the heading after a route change. Run Lighthouse on a production build and aim for ninety plus. And profile once, to check typing re-renders only the list.",
 ]},

{"html": H("Step 10: tests and ", "deploy") + row(code("""§0 it("rejects a blank title and a past date", () => {
§0   const r = taskSchema.safeParse({ title: " ", priority: 3,
§0                                    dueDate: "2000-01-01" });
§0   expect(r.error?.issues.map(i => i.path[0]))
§0     .toEqual(["title", "dueDate"]);
§0 });
§1 await user.click(screen.getByRole("button", { name: "Add task" }));
§1 expect(await screen.findByText("Title is required")).toBeInTheDocument();
§1 expect(onSubmit).not.toHaveBeenCalled();""", 23, style="flex:1")) +
   row(box("blue", "backend", "Render / Railway / AWS · DB · JWT secret · CORS origin", 2, "flex:1"),
       box("green", "frontend", "Vercel / Netlify · <code>VITE_API_URL</code> · SPA rewrite", 2, "flex:1"),
       box("orange", "README", "screenshot · live link · stack · how to run", 3, "flex:1"), style="margin-top:22px"),
 "steps": [
  "Step ten. Prove it works. Set up Vitest, Testing Library, and MSW as a fake Spring API. Then three kinds of tests. A pure test of the schema, with no React needed.",
  "A behaviour test of the form, the way a user sees it. Click add with no title, see the error, and check nothing was submitted. And one integration test, rendering the project page inside its providers, with tasks coming from MSW.",
  "Then deploy. The backend on Render, Railway, or AWS, with its database, JWT secret, and your frontend's URL as the allowed CORS origin. The frontend on Vercel or Netlify, with the API URL variable, and the SPA rewrite so deep links work.",
  "And write the README. It's what recruiters read first. A screenshot, the live link, the features and tech stack, how to run it, and what you'd do next.",
 ]},

quiz([
  ("Why did no page change in step 6?", "components only use the <b style=\"display:inline\">hook</b>", "blue",
   "Quiz time. Why didn't any page component change in step six?",
   "Because components only use the use tasks hook. Its return shape stayed the same."),
  ("Why filter on the server in step 9?", "with pages, the browser <b style=\"display:inline\">lacks</b> every task", "green",
   "Why must the status filter move to the server in step nine?",
   "Because with pagination, the browser no longer has every task."),
  ("Why clear the query cache on logout?", "no other user's data <b style=\"display:inline\">lingers</b>", "purple",
   "And why clear the query cache on logout?",
   "So no previous user's data lingers in the cache."),
]),

recap(["Step 6: TanStack Query behind the same hook · optimistic updates",
       "Step 7: proxy · one client · JWT login · RequireAuth",
       "Step 8: one Zod schema · server errors under fields · expiry",
       "Step 9: pagination · skeletons · error boundary · lazy · a11y",
       "Step 10: Vitest + RTL + MSW · deploy both · README",
       "A portfolio project you can explain"],
  "Let's recap part two. Step six put TanStack Query behind the same hook, with optimistic updates. Step seven connected the real API, with a proxy, one client, JWT login, and protected routes. Step eight added one Zod schema, server errors under the right fields, and smooth token expiry. Step nine polished it with pagination, skeletons, an error boundary, lazy pages, and accessibility. And step ten added tests, deployed both halves, and wrote the README. Now you have a portfolio project you can explain. Next time: React patterns, TypeScript, and Next.js!"),
]
