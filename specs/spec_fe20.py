from lib import *

TAG = "Frontend 20 · React with a Spring Boot API"
FILE = "Frontend 20 React with a Spring Boot API.mp4"

SLIDES = [
title_slide(20, "React with a Spring Boot API", "Connecting your frontend to the backend you already built",
  "Welcome to module twenty: React with a Spring Boot API.",
  "This is where the two halves meet. Your React app talks to the Spring Boot API from the backend days. We'll organise a real project, build one API client, fix CORS, log in with a JWT, validate forms, and deploy it all."),

{"html": H("Project ", "structure") + row(code("""src/
├─ main.tsx        providers
├─ App.tsx         routes
├─ api/
│  ├─ client.ts    one HTTP client
│  └─ types.ts     match Spring DTOs
├─ features/
│  ├─ auth/        login, AuthContext
│  └─ tasks/       pages, tasksApi
├─ components/     Button, Modal
└─ hooks/          useDebounce""", 28, style="flex-shrink:0"),
   col(box("blue", "by feature", "not by file type, once the app grows", 0),
       box("green", "API calls out of components", "<code>tasksApi.ts</code> · change an endpoint in one file", 1),
       code("""§2 export type Task = {
§2   id: number; title: string;
§2   done: boolean; dueDate: string | null;
§2 };""", 26), style="flex:1"), top=True),
 "steps": [
  "Once an app grows past a few screens, group code by feature, not by file type. Auth has its own folder, and so do tasks. Shared components and hooks get their own folders too.",
  "Keep API calls out of components. Tasks API exports get tasks and create task. Components call hooks that use them. So changing an endpoint touches one file.",
  "And mirror your Spring D T Os as TypeScript types, in one place. Then the compiler checks both sides agree. Tools like open API typescript can even generate them from Springdoc.",
 ]},

{"html": H("One API ", "client") + code("""§0 const BASE = import.meta.env.VITE_API_URL;
§0 async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
§1   const token = localStorage.getItem("token");
§0   const res = await fetch(`${BASE}${path}`, { ...options, headers: {
§0     "Content-Type": "application/json",
§1     ...(token ? { Authorization: `Bearer ${token}` } : {}),
§0   } });
§2   if (res.status === 204) return undefined as T;
§2   const body = await res.json().catch(() => null);
§2   if (!res.ok) throw new HttpError(res.status, body?.message, body);
§0   return body as T;
§0 }
§3 http.interceptors.request.use(config => { … });   // axios: runs on every request""", 26),
 "steps": [
  "A small client wraps the parts every request shares. The base URL comes from an environment variable, and every request sends JSON.",
  "If there's a token, it adds the authorization header, bearer and the token.",
  "And it handles responses in one place. A two oh four has no body. And if the response isn't OK, it throws an H T T P error with the status and the server's message. Fetch doesn't throw on a four hundred by itself.",
  "Axios is a popular alternative. It throws on errors, parses JSON, and has interceptors. Code that runs on every request or response. Either way, combine it with TanStack Query for caching and loading states.",
 ]},

{"html": H("", "CORS") + code("""§0 Access to fetch at 'http://localhost:8080/api/tasks' from origin
§0 'http://localhost:5173' has been blocked by CORS policy""", 25) + row(
   code("""§1 // vite.config.ts · development
§1 server: {
§1   proxy: { "/api": "http://localhost:8080" },
§1 }
§1 fetch("/api/tasks")   // same origin""", 26, style="flex:1"),
   code("""§2 config.setAllowedOrigins(List.of(frontendUrl));
§2 config.setAllowedMethods(List.of("GET", "POST", …));
§2 config.setAllowedHeaders(
§2   List.of("Authorization", "Content-Type"));
§3 http.cors(Customizer.withDefaults());""", 26, style="flex:1"), top=True, style="margin-top:22px"),
 "steps": [
  "Here's the error everyone meets. Vite runs on port fifty one seventy three, and Spring on eighty eighty. A different port is a different origin. So the browser blocks the response, unless the server allows it. CORS is enforced by the browser. Postman and curl don't care.",
  "Option one, for development: Vite's dev proxy. The browser only talks to Vite, which forwards slash A P I to Spring. Call fetch with a relative URL, and it's the same origin.",
  "Option two: allow the origin in Spring. You need this when the frontend and backend live on different domains in production. List the real frontend URL, never a star, plus the methods and headers.",
  "And with Spring Security, enable CORS in the security filter chain too. Otherwise the preflight options request is rejected before your config is reached.",
 ]},

{"html": H("Login with ", "JWT") + row(
   col(box("gray", "1 · POST /auth/login", "email + password", 0), box("green", "2 · { token }", "save it · set user in AuthContext", 0),
       box("blue", "3 · Bearer token", "on every request", 1), box("red", "4 · 401", "clear token → /login", 2), gap=10, style="width:440px"),
   code("""§0 async function login(email: string, password: string) {
§0   const { token } = await api.post<{ token: string }>(
§0     "/auth/login", { email, password });
§0   localStorage.setItem("token", token);
§0   setUser(userFromToken(token));
§0 }
§3 // payload = the middle part · readable by anyone
§3 const payload = JSON.parse(atob(token.split(".")[1]));""", 26, style="flex:1"), top=True),
 "steps": [
  "Here's the login flow with your Spring Security JWT setup. React posts the email and password. Spring returns a token. React saves it, and sets the user in an auth context.",
  "From then on, every request carries it in the authorization header.",
  "When the token expires, a request gets a four oh one. Handle that in one place. Clear the token, and send the user to the login page.",
  "And two interview points. A JWT is not encrypted. It's only signed. Anyone can read the payload, so never put secrets in it. And you can hide buttons by role, but the server must enforce it. Where to store the token, local storage or an H T T P only cookie, is a trade-off we'll see in module twenty five.",
 ]},

{"html": H("Forms: React Hook Form + ", "Zod") + code("""§0 const taskSchema = z.object({
§0   title: z.string().trim().min(3, "At least 3 characters").max(100),
§0   dueDate: z.string().optional(),
§0 });
§0 type TaskForm = z.infer<typeof taskSchema>;     // the type comes from the schema
§1 const { register, handleSubmit, setError, formState: { errors } } =
§1   useForm<TaskForm>({ resolver: zodResolver(taskSchema) });
§1 <input {...register("title")} aria-invalid={!!errors.title} />
§2 setError(field, { message });                 // map Spring's @Valid errors back""", 26) +
   row(box("green", "Zod", "instant feedback", 2, "flex:1"), box("blue", "@Valid in Spring", "the real gate", 2, "flex:1"),
       box("purple", "server errors → fields", "shown where they belong", 2, "flex:1"), style="margin-top:22px"),
 "steps": [
  "For forms with more than a couple of fields, React Hook Form handles the state, validation and submit, with few re-renders. And Zod describes the rules once, as a schema. Z dot infer turns that schema into the TypeScript type. One source for both.",
  "Use form takes a Zod resolver. Register connects each input, and errors holds the messages.",
  "And when Spring rejects the request with a four hundred, map its field errors back with set error. So the same rule lives in three places, on purpose. Zod for instant feedback, Spring's at valid as the real gate, and server errors shown next to the right field.",
 ]},

{"html": H("Build and ", "deploy") + col(table(["Part", "Where", "Config"], [
     (["React <code>dist/</code>", "Vercel, Netlify, S3", "<code>VITE_API_URL</code>, SPA rewrite"], 0),
     (["Spring Boot", "Render, Railway, AWS", "CORS origin, secrets as env vars"], 0)], size=30),
   row(code("""§1 { "rewrites": [{ "source": "/(.*)",
§1                 "destination": "/index.html" }] }""", 28, style="flex:1"),
   col(box("purple", "or one deployment", "<code>dist/</code> → <code>resources/static</code> · same origin, no CORS", 2),
       box("orange", "checklist", "no secrets in the frontend · HTTPS · refresh on <code>/tasks/42</code> works · test on Slow 4G", 3), style="width:620px"), top=True)),
 "steps": [
  "Npm run build type-checks and bundles everything into dist. The most common setup is two separate deployments. React goes to Vercel, Netlify, or S3, with the API URL set at build time. Spring Boot goes to Render, Railway, or AWS, with CORS allowing the real frontend, and secrets as environment variables.",
  "On a static host, add a rewrite, so every path serves index dot HTML. Otherwise refreshing a deep link gives a four oh four.",
  "Or deploy once. Copy dist into Spring Boot's static resources folder. The same origin serves the app and the API, so there's no CORS at all.",
  "Before going live, check. No secrets in the frontend. CORS allows only the real origin. H T T P S everywhere. Refreshing a deep link works. And loading and error states look right on a slow connection.",
 ]},

quiz([
  ("Who enforces CORS?", "the <b style=\"display:inline\">browser</b> · the server fixes it by allowing the origin", "blue",
   "Quiz time. Who enforces CORS?",
   "The browser. The server fixes it, by allowing the origin."),
  ("Is a JWT encrypted?", "<b style=\"display:inline\">No</b> · only signed", "red",
   "Is a JWT encrypted?",
   "No. It's only signed. Anyone can read the payload."),
  ("Refreshing <code>/tasks/42</code> gives 404?", "add a <b style=\"display:inline\">rewrite</b> to index.html", "green",
   "And refreshing slash tasks slash forty two gives a four oh four. Why?",
   "The static host needs a rewrite, so every path serves index dot HTML."),
]),

recap(["Organise by feature · API calls in their own modules",
       "Mirror Spring DTOs as TypeScript types",
       "One client: base URL, token, errors · axios interceptors",
       "CORS: Vite proxy in dev · allow the origin in Spring + the security chain",
       "JWT: signed, not encrypted · 401 → back to login",
       "Zod + React Hook Form · SPA rewrite on deploy"],
  "Let's recap. Organise by feature, and keep API calls in their own modules. Mirror your Spring D T Os as TypeScript types. Build one client for the base URL, the token, and errors. For CORS, use Vite's proxy in development, and allow the origin in Spring, including the security chain. A JWT is signed, not encrypted, and a four oh one sends the user back to login. Validate forms with Zod and React Hook Form. And add an SPA rewrite when you deploy. Next time: React performance!"),
]
