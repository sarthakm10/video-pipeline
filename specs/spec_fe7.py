from lib import *

TAG = "Frontend 7 · Arrays, Objects and Modern Syntax"
FILE = "Frontend 7 Arrays, Objects and Modern Syntax.mp4"

SLIDES = [
title_slide(7, "Arrays, Objects & Modern Syntax", "Most frontend code is reshaping data",
  "Welcome to module seven: arrays, objects, and modern syntax.",
  "Most frontend code is reshaping data. You take the JSON from your API, filter it, sort it, pick a few fields, and show it. This module is the toolkit for that. Plus the modern syntax, like destructuring, spread, and the question mark operators, that fills every React file."),

{"html": H("Arrays: mutate or ", "copy", "?") + row(
   code("""const tasks = ["plan", "code"];
tasks.push("test");      // add at the end
tasks.pop();             // remove from the end
tasks.at(-1)             // "code": counts from the end
tasks.includes("plan")   // true

§1 const nums = [10, 20, 30, 40];
§1 nums.slice(1, 3);   // [20, 30] · nums unchanged
§1 nums.splice(1, 2);  // removes 2 → nums is [10, 40]""", 30, style="flex:1"),
   col(box("red", "mutate ✎", "push · pop · shift · unshift · splice · sort · reverse", 1),
       box("green", "return new ✓", "slice · concat · map · filter · toSorted · [...arr]", 1),
       style="width:560px"), top=True) + note("React state must be replaced, not mutated → use the green column", 2),
 "steps": [
  "Arrays in JavaScript are dynamic, like Java's array list. Push adds to the end, pop removes from the end. At minus one gives you the last item, and includes checks if something's there.",
  "The important split is this. Some methods change the array in place. Push, pop, splice, sort and reverse. Others return a brand new array, and leave the original alone. Slice, concat, map and filter. Look: slice copies part of nums, but splice actually removes items from it.",
  "Why does this matter? Because in React, state must be replaced, not mutated. So in React code, you'll mostly use the green column.",
 ]},

{"html": H("map, filter, ", "reduce") + code("""const tasks = [
  { id: 1, title: "Learn CSS", done: true,  minutes: 60 },
  { id: 2, title: "Learn JS",  done: false, minutes: 120 },
  { id: 3, title: "Build app", done: false, minutes: 90 },
];
§1 tasks.map(t => t.title);           // ["Learn CSS", "Learn JS", "Build app"]
§2 tasks.filter(t => !t.done);        // the two unfinished tasks
§3 tasks.find(t => t.id === 2);       // first match, or undefined
§3 tasks.some(t => t.done);           // true: at least one
§3 tasks.every(t => t.minutes > 30);  // true: all of them
§4 tasks.reduce((sum, t) => sum + t.minutes, 0);   // 270""", 30),
 "steps": [
  "These array methods replace most loops. Each one takes a callback. Here's a list of tasks, just like the JSON your API would send.",
  "Map transforms every item. Map each task to its title, and you get an array of titles.",
  "Filter keeps the items that pass a test. Here, the tasks that aren't done.",
  "Find returns the first match, or undefined. Some asks: does at least one pass? Every asks: do all of them pass?",
  "And reduce turns an array into a single value. Start the sum at zero, add each task's minutes, and you get two hundred and seventy.",
 ]},

{"html": H("Chaining and the ", "sort", " gotcha") + code("""§0 const pendingTitles = tasks
§0   .filter(t => !t.done)
§0   .map(t => t.title.toUpperCase());   // ["LEARN JS", "BUILD APP"]

§1 [10, 9, 1, 100].sort();                 // [1, 10, 100, 9] 😬 compared as strings
§2 [10, 9, 1, 100].sort((a, b) => a - b);  // [1, 9, 10, 100] ✓
§2 tasks.sort((a, b) => a.title.localeCompare(b.title));

§3 const sorted = tasks.toSorted((a, b) => a.minutes - b.minutes);  // original kept""", 30),
 "steps": [
  "These methods chain nicely, just like Java streams. Filter the unfinished tasks, then map them to upper case titles.",
  "Now a classic gotcha. Sort with no compare function sorts items as strings. So one hundred comes before nine, because the character one comes before nine.",
  "Always pass a compare function. A minus b sorts numbers ascending. For text, use locale compare.",
  "And remember, sort mutates the array. If you need the original, use to sorted, or sort a copy.",
 ]},

{"html": H("", "Objects") + row(
   code("""const user = {
  name: "Asha",
  "favourite-lang": "Java",
  greet() { return `Hi, I'm ${this.name}`; },
};
user.name                // dot notation
user["favourite-lang"]   // bracket notation
user.city = "Pune";      // add
§1 const name = "Ben", role = "admin";
§1 const u = { name, role };         // shorthand
§1 const form = { [field]: "x" };    // computed key""", 29, style="flex:1"),
   code("""§2 Object.keys(scores)
§2 // ["asha", "ben"]
§2 Object.values(scores)
§2 // [90, 75]
§2 Object.entries(scores)
§2 // [["asha", 90], ["ben", 75]]""", 29, style="width:560px"), top=True),
 "steps": [
  "An object is a collection of keys and values, created directly with curly braces. No class needed. Read properties with a dot, or with square brackets, which take any string, or a variable. And you can add properties whenever you like.",
  "Two shorthands you'll see everywhere. If a variable has the same name as the key, just write it once. And square brackets inside an object literal give you a computed key.",
  "To loop over an object, use object dot keys, values, or entries. Entries gives you key value pairs, which you can loop over with for of. And the JSON from your Spring Boot API arrives as exactly these plain objects and arrays.",
 ]},

{"html": H("", "Destructuring") + code("""const user = { name: "Asha", role: "admin", address: { city: "Pune" } };

§0 const { name, role } = user;           // "Asha", "admin"
§1 const { name: userName } = user;       // rename
§1 const { active = true } = user;        // default when missing
§1 const { address: { city } } = user;    // nested → "Pune"

§2 const [first, second] = ["a", "b", "c"];
§2 [x, y] = [y, x];                       // swap

§3 function TaskCard({ title, done = false }) { … }   // React props!""", 31),
 "steps": [
  "Destructuring pulls values out of objects and arrays, straight into variables. Const, curly braces, name and role, equals user. That's two variables in one line.",
  "You can rename while you destructure, give a default if the value's missing, and even reach into nested objects.",
  "Arrays destructure by position. First and second. And there's a neat trick for swapping two variables, without a temporary.",
  "Destructuring also works in function parameters. And that's exactly how every React component reads its props. You'll write this a thousand times.",
 ]},

{"html": H("Spread and ", "rest", ": same three dots") + row(
   col(box("green", "spread · expands", "", 0),
       code("""const all = [...a, ...b, 5];
const copy = [...a];
const settings = { ...base, size: "lg" };
Math.max(...[3, 9, 2]);   // 9""", 29, step=0), style="flex:1"),
   col(box("blue", "rest · collects", "", 1),
       code("""const { password, ...safeUser }
  = userFromDb;
const [head, ...tail] = [1, 2, 3];
// head = 1, tail = [2, 3]""", 29, step=1), style="flex:1"), top=True) +
   note("Spread: right of <code>=</code> or in a call · Rest: left of <code>=</code> or in parameters", 2),
 "steps": [
  "Three dots does two different jobs. Spread expands an array or object into another one. Join two arrays, make a copy, or build a settings object from a base, overriding size. Later keys win.",
  "Rest is the opposite. It collects whatever's left. Pull out the password, and put everything else in safe user. Or split an array into its head and the tail.",
  "So how do you tell them apart? Spread is on the right of the equals sign, or in a function call. Rest is on the left, or in a parameter list.",
 ]},

{"html": H("<code style=\"font-size:inherit\">?.</code> and ", "<code style=\"font-size:inherit\">??</code>") + row(
   code("""§0 user.address.city;      // 💥 TypeError
§0 user.address?.city;     // undefined, no crash
§0 user.getAvatar?.();     // calls only if it exists

§1 const count = 0;
§1 count || 10   // 10 😬 0 is falsy
§1 count ?? 10   // 0 ✓  only null/undefined
§2 const city = user.address?.city ?? "Unknown";""", 31, style="flex:1"),
   col(box("purple", "?. optional chaining", "stops at null or undefined", 0),
       box("green", "?? nullish coalescing", "fallback only for null / undefined", 1),
       box("gray", "|| ", "fallback for any falsy value", 1), style="width:520px"), top=True),
 "steps": [
  "API data is often incomplete. If address is missing, reading address dot city crashes with a type error. Optional chaining, question mark dot, stops and returns undefined instead. It works for method calls and array access too.",
  "Nullish coalescing, two question marks, gives a fallback, but only for null and undefined. Compare it with the older or operator, which falls back on any falsy value. So if count is zero, or gives you ten. Oops. But question mark question mark keeps the zero.",
  "And they combine beautifully. Address, question mark, city, otherwise, unknown. Safe, and with a sensible default.",
 ]},

{"html": H("Map, Set and ", "JSON") + row(
   code("""§0 const visits = new Map();
§0 visits.set("home", 3);
§0 visits.get("home");     // 3
§0 visits.size;            // 1

§1 const tags = new Set(["java", "react", "java"]);
§1 tags.size;              // 2
§1 [...new Set([1, 2, 2, 3])]   // [1, 2, 3] dedupe""", 29, style="flex:1"),
   code("""§2 const text = JSON.stringify(task);
§2 // '{"id":1,"title":"Learn JS"}'
§2 const back = JSON.parse(text);

§3 // ✗ functions, undefined,
§3 //   Map, Set, Date
§3 // parse throws → try/catch""", 27, style="width:640px"), top=True),
 "steps": [
  "Map and Set work like Java's hash map and hash set. A Map takes any type of key, keeps insertion order, and has a size property. Use it for frequent adds and removes. A plain object is simpler for fixed records.",
  "A Set drops duplicates. And spreading a new Set into an array is the classic one line way to remove duplicates.",
  "JSON is just text. JSON dot stringify turns an object into text, and JSON dot parse turns it back.",
  "But JSON can't hold functions, undefined, maps, sets, or dates. Dates become strings. And parse throws on invalid text, so wrap untrusted input in a try catch.",
 ]},

{"html": H("References and ", "copies") + code("""§0 const a = { name: "Asha", skills: ["java"] };
§0 const b = a;            // same object!
§0 b.name = "Ben";         // a.name is "Ben" too 😬

§1 const c = { ...a };     // shallow copy
§1 c.name = "Chen";        // a unaffected ✓
§1 c.skills.push("react"); // a.skills changed 😬 shared inner array

§2 const d = structuredClone(a);   // deep copy: every level ✓

§3 { x: 1 } === { x: 1 }   // false: compares references""", 31),
 "steps": [
  "Objects and arrays are shared by reference, just like in Java. Assigning a to b doesn't copy anything. It's the same object. Change b's name, and a's name changes too.",
  "Spreading makes a shallow copy. A new outer object, so changing c's name is fine. But nested objects are still shared. Push to c's skills, and a's skills change too.",
  "For a deep copy that copies every level, use structured clone. It's built in.",
  "And triple equals compares references, not contents. Two objects that look identical are still not equal.",
 ]},

{"html": H("", "Immutable", " updates") + code("""const done    = { ...task, done: true };                     // update a field
const added   = [...tasks, newTask];                         // add
const removed = tasks.filter(t => t.id !== id);              // remove
const edited  = tasks.map(t => (t.id === id ? { ...t, title } : t));   // replace one""", 29) +
   note("React compares references: mutate in place → same reference → screen doesn't update", 1),
 "steps": [
  "Immutability means never changing data in place. Instead, you create updated copies. Here are the four patterns you'll use constantly. Update a field with object spread. Add with array spread. Remove with filter. And replace one item with map.",
  "Why bother? Because React compares references to see what changed. If you mutate an array in place, it's still the same reference, so React thinks nothing changed, and the screen doesn't update. Copy, don't mutate.",
 ]},

predict(("Predict the ", "output"), [
  ("[10, 9, 1].sort()", "[1, 10, 9]", "compared as strings · pass <code>(a, b) =&gt; a - b</code>",
   "Pause and predict. What does sorting ten, nine, one give you?",
   "One, ten, nine! Without a compare function, they're compared as strings."),
  ("0 ?? 5  vs  0 || 5", "0 · 5", "?? only replaces null and undefined",
   "And zero, question mark question mark five, versus zero or five?",
   "Zero, and five. Question mark question mark keeps the zero. Or replaces any falsy value."),
]),

quiz([
  ("<code>map</code> vs <code>forEach</code>?", "map returns a <b style=\"display:inline\">new array</b> · forEach returns undefined", "green",
   "Quiz time. What's the difference between map and for each?",
   "Map returns a new array. For each just loops, and returns undefined."),
  ("<code>find</code> vs <code>filter</code>?", "find → first match or undefined · filter → all matches, as an array", "blue",
   "Find versus filter?",
   "Find returns the first match, or undefined. Filter returns every match, as an array."),
  ("Copy an object with one field changed?", "<code>{ ...obj, field: value }</code>", "purple",
   "And how do you copy an object with one field changed?",
   "Spread the object, then set the field. Later keys win."),
]),

recap(["Know which methods mutate · prefer the ones that copy",
       "map, filter, find, some, every, reduce replace loops",
       "<code>sort()</code> compares strings · pass <code>(a, b) =&gt; a - b</code>",
       "Destructuring, spread (expand) and rest (collect)",
       "<code>?.</code> stops at null · <code>??</code> keeps 0 and \"\"",
       "Shallow vs deep copy · update with copies, never mutate"],
  "Let's recap. Know which array methods mutate, and prefer the ones that return a copy. Map, filter, find, some, every and reduce replace most loops. Sort compares strings, so pass a compare function. Destructuring pulls values out, spread expands, and rest collects. Optional chaining stops at null, and nullish coalescing keeps zero and empty strings. And update data with copies, never by mutating. Next time: the DOM and events!"),
]
