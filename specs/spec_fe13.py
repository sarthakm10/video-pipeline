from lib import *

TAG = "Frontend 13 · TypeScript Basics"
FILE = "Frontend 13 TypeScript Basics.mp4"

SLIDES = [
title_slide(13, "TypeScript Basics", "JavaScript with types: mistakes caught before the code runs",
  "Welcome to module thirteen: TypeScript basics.",
  "TypeScript is JavaScript with types. After Java, it'll feel familiar. The compiler tells you about mistakes before the code runs. Most React jobs today use TypeScript, and adding types to everything you've learned so far takes surprisingly little."),

{"html": H("Why ", "TypeScript", "?") + row(
   col(code("""§0 // JavaScript
§0 total([{ name: "Book", prise: 12 }]);
§0 // NaN: a typo nobody noticed""", 29),
       code("""§1 type Item = { name: string; price: number };
§1 function total(items: Item[]): number { … }
§1 total([{ name: "Book", prise: 12 }]);
§1 // ❌ 'prise' does not exist in type 'Item'""", 29), style="flex:1"),
   col(box("green", "errors before running", "typos · wrong arguments · maybe-undefined", 2),
       box("blue", "autocomplete", "your editor knows every property", 2),
       box("purple", "safe refactoring", "rename a field → every break listed", 2), style="width:500px"), top=True) +
   note("<code>tsc</code> checks, then <u>strips</u> the types · nothing exists at runtime", 3),
 "steps": [
  "JavaScript only finds type mistakes when the code runs, often in front of a user. Here, price is misspelled as prise, and the total silently becomes NaN.",
  "TypeScript checks it while you type. Describe an item, with a name and a price. Now the typo is a red underline, straight away.",
  "So you get errors before running, autocomplete everywhere, and safe refactoring. Rename a field, and the compiler lists every place that breaks. And types become documentation.",
  "Here's how it works. You write dot t s, or dot t s x files for React. The compiler checks them, then strips the types, producing plain JavaScript. Types never exist at runtime. So there's no speed cost. But also no runtime checking.",
 ]},

{"html": H("Basic types and ", "inference") + row(code("""§0 let title: string = "Learn TS";
§0 let day: number = 47;
§0 let tags: string[] = ["ts", "types"];
§0 let point: [number, number] = [3, 4];   // tuple

§1 let count = 0;          // inferred: number
§1 count = "zero";         // ❌ not assignable
§1 const doubled = [1, 2].map(n => n * 2);  // number[]

§2 const lang = "ts";      // type "ts" (literal)""", 30, style="flex:1"),
   col(box("green", "annotate", "function parameters · the shapes of your data", 1),
       box("gray", "let it infer", "local variables", 1), style="width:460px"), top=True),
 "steps": [
  "The basic types are what you'd expect. String, number for every kind of number, boolean, and arrays like string square brackets. A tuple is a fixed length array, with a type for each position.",
  "But most of the time, you don't write types at all. TypeScript infers them. Count starts as zero, so it's a number, and assigning a string is an error. So here's a good habit. Annotate function parameters and the shapes of your data. Let inference handle local variables.",
  "And const gives an even narrower type. A const set to the string t s has the type t s, exactly. That's a literal type, which we'll use in a moment.",
 ]},

{"html": H("Typing ", "functions") + code("""§0 function add(a: number, b: number): number { return a + b; }
§0 add(1, "2");   // ❌ string is not assignable to number

§1 function log(message: string, level?: "info" | "warn"): void { … }
§1 function sum(...nums: number[]): number { … }

§2 type Comparator = (a: number, b: number) => number;
§2 const ascending: Comparator = (a, b) => a - b;   // a, b inferred

§3 async function getTask(id: number): Promise<Task> { … }""", 30),
 "steps": [
  "Function parameters get types, and the return type goes after the parentheses. Pass the wrong type, or the wrong number of arguments, and it's an error.",
  "A question mark makes a parameter optional. Void means the function returns nothing useful. And rest parameters are typed as arrays.",
  "You can describe a function type itself, for callbacks. Comparator takes two numbers and returns a number. Then a and b are inferred, no annotations needed.",
  "And an async function returns a promise of something. Promise of task.",
 ]},

{"html": H("Object types: interface vs ", "type") + row(code("""§0 interface Task {
§0   readonly id: number;
§0   title: string;
§0   done: boolean;
§0   dueDate?: string;    // optional
§0 }
§0 type User = { id: number; name: string };

§1 interface Admin extends User { permissions: string[] }
§1 type Manager = User & { teamSize: number };""", 29, style="flex:1"),
   table(["", "interface", "type"], [
     (["Object shapes", "✓", "✓"], 2),
     (["Extending", "extends", "&amp;"], 2),
     (["Unions, tuples", "✗", "✓"], 2)], size=28), top=True) +
   note("Use <code>type</code> by default · be consistent · TypeScript is <u>structural</u>: shape matters, not the name", 3),
 "steps": [
  "Describe the shape of an object with an interface, or a type alias. Read only means it can't be reassigned, and a question mark makes a field optional.",
  "Interfaces extend with extends. Types combine with an ampersand, called an intersection.",
  "Both describe objects. But only type can express unions and tuples. So a good rule is to use type by default, or interface if your team prefers. Just be consistent.",
  "And unlike Java, TypeScript is structural. Any object with the right shape fits. A class doesn't need to say implements task for its objects to be accepted as a task.",
 ]},

{"html": H("Unions, literals and ", "narrowing") + code("""§0 type Status = "todo" | "in-progress" | "done";
§0 let s: Status = "finished";   // ❌ not assignable

§1 function formatId(id: number | string): string {
§1   if (typeof id === "number") return id.toFixed(0);   // id: number
§1   return id.toUpperCase();                            // id: string
§1 }
§2 if ("meow" in pet) pet.meow();             // in narrows
§2 if (value instanceof Date) value.toISOString();""", 30),
 "steps": [
  "A union means one of these types. And a literal type is one exact value. So status can only be todo, in progress, or done. Anything else is an error. Literal unions replace many Java enums, and your editor autocompletes them.",
  "To use a union safely, you narrow it. Check which member you have, and TypeScript follows your logic. After typeof id equals number, id is a number. After that, it must be a string.",
  "The in operator narrows too, and so does instance of.",
 ]},

{"html": H("Strict null ", "checks") + code("""const el = document.querySelector("#title");   // Element | null
§1 el.textContent = "Hi";          // ❌ 'el' is possibly 'null'
§2 el?.classList.add("big");       // ✓
§2 if (el) el.textContent = "Hi";  // ✓ narrowed""", 34) +
   note("No more \"Cannot read properties of undefined\"", 3),
 "steps": [
  "Strict null checks are the biggest win of all. Query selector might not find anything, so its type is element, or null.",
  "Use it directly, and TypeScript says: el is possibly null.",
  "You have to handle it first. With optional chaining, or by checking it in an if.",
  "And that removes the whole cannot read properties of undefined class of crashes.",
 ]},

{"html": H("any, unknown, ", "never") + table(["Type", "Meaning", "Use it"], [
   (["<code>any</code>", "turns checking off", "almost never: it spreads"], 0),
   (["<code>unknown</code>", "anything · check before using", "JSON, <code>catch</code> errors"], 1),
   (["<code>never</code>", "can't exist", "always throws · exhaustive checks"], 2)], size=31) +
   code("""§0 let a: any = JSON.parse(text);  a.foo.bar();   // compiles, crashes 😬
§1 let u: unknown = JSON.parse(text);  u.foo;     // ❌ check it first
§3 const input = document.querySelector("#email") as HTMLInputElement;  // trust me""", 28, style="margin-top:24px") +
   note('Turn on <code>"strict": true</code> in tsconfig.json', 3),
 "steps": [
  "Any turns type checking off for that value. Everything compiles, and then crashes at runtime. Use it almost never.",
  "Unknown means it could be anything, so check before you use it. Perfect for untrusted input, like parsed JSON, or caught errors.",
  "Never is a value that can't exist. For a function that always throws, or exhaustive checks, which we'll see next module.",
  "Turn on strict true in your t s config. Vite's templates already do. And when you know more than the compiler, a type assertion, with as, tells it so. But if you're wrong, that's on you.",
 ]},

quiz([
  ("Do types exist at runtime?", "<b style=\"display:inline\">No</b> · they're erased · validate untrusted data separately", "red",
   "Quiz time. Do TypeScript types exist at runtime?",
   "No. They're erased when compiling. So you still need to validate untrusted data."),
  ("<code>interface</code> vs <code>type</code>?", "both describe objects · only type does unions and tuples", "blue",
   "Interface versus type?",
   "Both describe objects. Only type can do unions and tuples."),
  ("<code>any</code> vs <code>unknown</code>?", "any disables checking · unknown forces you to check", "green",
   "Any versus unknown?",
   "Any disables checking. Unknown forces you to check first."),
]),

recap(["TypeScript = JavaScript + types, erased at runtime",
       "Annotate parameters and data shapes · infer the rest",
       "<code>name?: type</code> optional · <code>void</code> returns nothing",
       "type by default · structural, not nominal",
       "Literal unions · narrow with typeof, in, instanceof",
       "strict mode · unknown over any"],
  "Let's recap. TypeScript is JavaScript plus types, and the types are erased at runtime. Annotate parameters and data shapes, and let inference do the rest. A question mark makes things optional, and void means nothing useful is returned. Use type by default, and remember TypeScript is structural. Literal unions replace enums, and you narrow them with typeof, in, and instance of. And turn on strict mode, and prefer unknown over any. Next time: advanced TypeScript!"),
]
