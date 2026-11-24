from lib import *

TAG = "Frontend 14 · TypeScript Advanced"
FILE = "Frontend 14 TypeScript Advanced.mp4"

SLIDES = [
title_slide(14, "TypeScript Advanced", "Generics, derived types and unions the compiler checks for you",
  "Welcome to module fourteen: advanced TypeScript.",
  "This is the TypeScript that makes code reusable, and APIs safe. Generics, deriving types from other types, and unions the compiler checks exhaustively. You'll read these in every library's types. And the common ones, like partial, pick, omit and record, in everyday app code."),

{"html": H("", "Generics") + code("""§0 function first<T>(items: T[]): T | undefined { return items[0]; }
§0 const n = first([1, 2, 3]);       // T inferred: number

§1 interface ApiResponse<T> { data: T; status: number; error?: string }
§1 type TaskList = ApiResponse<Task[]>;

§2 function longest<T extends { length: number }>(a: T, b: T): T { … }
§2 longest("abc", "de");     // ✓
§2 longest(10, 20);          // ❌ number has no length

§3 async function getJson<T>(url: string): Promise<T> { … }
§3 const tasks = await getJson<Task[]>("/api/tasks");""", 29),
 "steps": [
  "Generics are type parameters, exactly like Java's list of T. First takes an array of T, and returns a T, or undefined. Call it with numbers, and T is inferred as number. The input and output types stay linked.",
  "Interfaces can be generic too. An API response of T, where data is T. Then a task list is an API response of task array.",
  "Constraints, with extends, say what a type parameter must have. Like bounded types in Java. Longest works with anything that has a length. Strings and arrays, yes. Numbers, no.",
  "And here's a typed fetch wrapper you'll actually use. Get JSON of T returns a promise of T. But remember, that's a promise to the compiler, not a runtime check.",
 ]},

{"html": H("keyof, typeof and ", "indexed access") + code("""type Task = { id: number; title: string; done: boolean };
§0 type TaskKey = keyof Task;           // "id" | "title" | "done"
§0 type TitleType = Task["title"];      // string

§1 const defaults = { theme: "dark", pageSize: 20 };
§1 type Settings = typeof defaults;     // { theme: string; pageSize: number }

§2 const ROLES = ["admin", "editor", "viewer"] as const;
§2 type Role = typeof ROLES[number];    // "admin" | "editor" | "viewer"

§3 function sortBy<T>(items: T[], key: keyof T): T[] { … }
§3 sortBy(tasks, "titel");              // ❌ not a keyof Task""", 29),
 "steps": [
  "These build types from other types, or values, so you write each shape only once. Key of task gives a union of its property names. And square brackets look up a property's type.",
  "Typeof on a value gives you its type. So you can derive a settings type straight from a defaults object.",
  "And here's a great trick. Mark an array as const, then typeof ROLES, index number, gives you a union of its values. One source of truth. The array exists at runtime, for a dropdown, and the type is derived from it.",
  "Put it together, and sort by only accepts real keys of task. A typo is caught at once.",
 ]},

{"html": H("Utility ", "types") + code("""interface Task { id: number; title: string; done: boolean; dueDate?: string }

§0 type TaskUpdate  = Partial<Task>;              // all optional → PATCH body
§1 type NewTask     = Omit<Task, "id">;           // all except id → POST body
§1 type TaskSummary = Pick<Task, "id" | "title">; // only these
§2 type FrozenTask  = Readonly<Task>;
§2 type Board       = Record<"todo" | "done", Task[]>;   // { todo: Task[]; done: Task[] }

§3 type LoadedUser = Awaited<ReturnType<typeof loadUser>>;
§3 type Open = Exclude<"todo" | "doing" | "done", "done">;   // "todo" | "doing" """, 28),
 "steps": [
  "Utility types are built-in generics that transform other types. Partial makes every property optional. Perfect for a patch request body.",
  "Omit gives you everything except some keys. A new task has everything except the I D, for a post body. Pick keeps only the keys you name.",
  "Readonly freezes every property. And record makes an object type, with these keys, and these values.",
  "A few more you'll see. Return type gets a function's return type, and awaited unwraps a promise. Exclude removes members from a union.",
 ]},

{"html": H("Discriminated ", "unions") + code("""§0 type RequestState<T> =
§0   | { status: "idle" }
§0   | { status: "loading" }
§0   | { status: "success"; data: T }
§0   | { status: "error"; error: string };

§1 switch (state.status) {
§1   case "loading": return "Loading…";
§1   case "success": return `${state.data.length} tasks`;   // data only here
§1   case "error":   return `Failed: ${state.error}`;       // error only here
§1 }""", 30) + note("Beats separate isLoading / data / error: no impossible combinations", 2),
 "steps": [
  "A discriminated union is a union of object types that share one literal field, the tag. Here, a request is idle, loading, a success with data, or an error with a message.",
  "Check the tag, and TypeScript narrows to that exact shape. Data only exists in the success case. Error only exists in the error case. Try to read data while loading, and it's a compile error.",
  "This beats separate is loading, data and error variables, where impossible combinations, like loading and error at once, can sneak in. You'll use exactly this shape for data fetching in React.",
 ]},

{"html": H("Exhaustive ", "checks") + code("""function assertNever(x: never): never {
  throw new Error(`Unhandled case: ${JSON.stringify(x)}`);
}
function icon(status: "todo" | "doing" | "done"): string {
  switch (status) {
    case "todo":  return "⬜";
    case "doing": return "🔄";
    case "done":  return "✅";
§1     default:      return assertNever(status);   // add "blocked" → build fails here
  }
}""", 30),
 "steps": [
  "Exhaustive checks make the compiler tell you when you forget a case. Assert never takes a parameter of type never, a value that can't exist.",
  "In the default branch, after every case is handled, status really is never, so this compiles. But if someone adds blocked to the union and forgets to handle it, status isn't never anymore. The build fails, pointing at every switch that needs updating.",
 ]},

{"html": H("Mapped and ", "conditional", " types") + code("""§0 type MyPartial<T>  = { [K in keyof T]?: T[K] };     // how Partial works
§0 type FormErrors<T> = { [K in keyof T]?: string };   // an error per field

§1 type IsString<T> = T extends string ? "yes" : "no";
§1 type A = IsString<"hi">;      // "yes"

§2 type ElementOf<T> = T extends (infer E)[] ? E : never;
§2 type X = ElementOf<string[]>;   // string

§3 type EventName = `on${Capitalize<"click" | "focus">}`;   // "onClick" | "onFocus" """, 29),
 "steps": [
  "This is how the utility types are built. You'll read these more than you write them. Mapped types loop over keys. For each K in key of T, make it optional. That's partial. Or map every field to a string, for form errors.",
  "Conditional types choose a type with a condition. If T extends string, yes, otherwise no. It's a ternary, for types.",
  "And infer pulls a type out of a pattern. If T is an array of something, infer that something. So element of string array is string.",
  "Template literal types even build string types. On, plus capitalised click or focus, gives on click, or on focus.",
 ]},

{"html": H("Enums, @types and ", "tsconfig") + row(
   col(code("""§0 enum Priority { Low, Medium, High }   // runtime object
§0 type PriorityU = "low" | "medium" | "high";   // ✓ preferred""", 30),
       code("""§1 npm install lodash
§1 npm install -D @types/lodash""", 30), style="flex:1"),
   code("""§2 {
§2   "compilerOptions": {
§2     "strict": true,
§2     "noUncheckedIndexedAccess": true,
§2     "jsx": "react-jsx",
§2     "paths": { "@/*": ["./src/*"] }
§2   }
§2 }""", 30, style="width:700px"), top=True),
 "steps": [
  "Enums exist in TypeScript, but most teams prefer literal unions. They're simpler, they match the strings your API sends, and they leave nothing behind in the bundle.",
  "Declaration files describe the types of JavaScript code. Most npm packages ship their own. For the rest, install the at types package from Definitely Typed.",
  "And in t s config, strict matters most. No unchecked indexed access makes array index lookups possibly undefined, which they are. And paths gives you clean imports like at slash components, instead of dot dot slash dot dot slash.",
 ]},

quiz([
  ("<code>Partial</code> vs <code>Omit</code> vs <code>Pick</code>?", "all optional · everything except · only these", "blue",
   "Quiz time. Partial versus omit versus pick?",
   "Partial makes everything optional. Omit keeps everything except some keys. Pick keeps only the keys you name."),
  ("A union from an array?", "<code>as const</code>, then <code>typeof ARR[number]</code>", "purple",
   "How do you derive a union type from an array?",
   "Mark it as const, then use typeof the array, indexed by number."),
  ("Force a switch to handle every case?", "<code>assertNever(x: never)</code> in <code>default</code>", "green",
   "And how do you force a switch to handle every case?",
   "Call assert never in the default branch."),
]),

recap(["Generics link input and output types · <code>extends</code> constrains",
       "keyof · typeof · <code>as const</code> + <code>[number]</code>",
       "Partial · Omit · Pick · Readonly · Record",
       "Discriminated unions: a tag field narrows the shape",
       "assertNever for exhaustive switches",
       "Prefer literal unions to enums · strict tsconfig"],
  "Let's recap. Generics link input and output types, and extends constrains them. Key of, typeof, and as const let you derive types instead of repeating them. Partial, omit, pick, readonly and record cover most everyday needs. Discriminated unions use a tag field to narrow the shape, and assert never makes switches exhaustive. And prefer literal unions to enums. Next time: React fundamentals!"),
]
