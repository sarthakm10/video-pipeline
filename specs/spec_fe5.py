from lib import *

TAG = "Frontend 5 · JavaScript Basics"
FILE = "Frontend 5 JavaScript Basics.mp4"

SLIDES = [
title_slide(5, "JavaScript Basics", "What's different from Java: types, equality, truthy values and a few surprises",
  "Welcome to module five. It's time for JavaScript!",
  "And here's the good part. You already know how to program. Variables, conditions, loops and functions all carry over from Java. So this module focuses on what's different: dynamic types, two kinds of equality, truthy values, and a few famous surprises."),

{"html": H("Java vs ", "JavaScript") + table(["", "Java", "JavaScript"], [
   (["Types", "static: <code>int x</code>", "dynamic: <code>let x</code> holds anything"], 0),
   (["Runs on", "the JVM", "the browser's engine (V8), or Node.js"], 1),
   (["Structure", "everything in classes", "functions and objects are enough"], 2),
   (["Functions", "methods in classes", "values: store, pass, return them"], 2),
   (["Threads", "many", "one main thread + an event loop"], 3)], size=32),
 "steps": [
  "Despite the name, JavaScript has almost nothing to do with Java. The biggest difference is types. In Java, types are static and checked when you compile. In JavaScript, they're dynamic. A variable can hold anything.",
  "Java runs on the JVM. JavaScript is the only language browsers run natively, and since Node.js, it also runs on servers and in build tools. That's why all the frontend tooling is JavaScript too.",
  "In Java, everything lives inside classes. In JavaScript, plain functions and objects are enough, and classes are optional. And functions are values. You can store them in variables, pass them around, and return them.",
  "And JavaScript has one main thread, with an event loop. We'll see why that matters in module ten.",
 ]},

{"html": H("Variables: ", "const", ", let, var") + row(
   code("""const name = "Asha";   // can't be reassigned
let score = 0;          // can change
score = score + 10;

§1 const user = { name: "Asha" };
§1 user.name = "Ben";   // fine: the object changed
§1 user = {};           // TypeError""", 32, style="flex:1"),
   col(box("green", "const", "by default", 0), box("blue", "let", "when the value must change", 0),
       box("red", "var ✗", "never: ignores blocks, gets hoisted", 2), style="width:520px"), top=True) +
   note("const = Java's final: the variable is fixed, not the object", 1),
 "steps": [
  "JavaScript has three ways to declare a variable. Use const by default. A const can't be reassigned. Use let when the value really needs to change.",
  "But careful. Const stops you reassigning the variable, not changing the object it points to. Just like final in Java. So changing user dot name is fine. Pointing user at a new object is an error.",
  "And var? Never use it. It ignores block scope and gets hoisted, which causes bugs. We'll see exactly why in the next module.",
 ]},

{"html": H("Template ", "literals") + fill(
   code("""const day = 5;
console.log(`Day ${day} of 100: ${day * 2}% done`);
// Day 5 of 100: 10% done""", 40),
   row(box("gray", "backticks", "<code>`…`</code> not quotes", 1), box("gray", "${ }", "any expression inside", 1),
       box("gray", "multi-line", "can span lines", 1))),
 "steps": [
  "Building strings is much nicer than in Java. Use backticks instead of quotes, and put any expression inside dollar, curly braces.",
  "So you get backticks, expressions inside, and they can even span several lines. You'll use these all the time.",
 ]},

{"html": H("The ", "types") + table(["Type", "Examples", "Note"], [
   (["<code>number</code>", "42, 3.14, NaN, Infinity", "one type for integers and decimals"], 0),
   (["<code>string</code> / <code>boolean</code>", "\"hi\", true", "strings are immutable"], 0),
   (["<code>undefined</code>", "undefined", "declared, nothing assigned yet"], 1),
   (["<code>null</code>", "null", "empty on purpose"], 1),
   (["<code>bigint</code> / <code>symbol</code>", "10n, Symbol(\"id\")", "rarer"], 1),
   (["<code>object</code>", "{}, [], functions, dates", "everything else"], 2)], size=31),
 "steps": [
  "JavaScript has seven primitive types, plus objects. Number is one type for both whole numbers and decimals. Then string and boolean, as you'd expect.",
  "Undefined means a variable was declared, but nothing's been assigned yet. Null means empty on purpose. You set it yourself. Bigint and symbol are less common.",
  "And everything that isn't a primitive is an object. Plain objects, arrays, functions, dates. All objects.",
 ]},

predict(("typeof ", "surprises"), [
  ("typeof []", '"object"', "arrays are objects · check with <code>Array.isArray([])</code>",
   "Let's test the typeof operator, which tells you a value's type at runtime. What's typeof an empty array?",
   "Object! Arrays are objects in JavaScript. To check for an array, use Array dot is array."),
  ("typeof null", '"object"', "a bug from 1995, kept so old sites don't break",
   "And typeof null?",
   "Also object. That's actually a bug from nineteen ninety five, and it was never fixed, so old websites wouldn't break."),
]),

{"html": H("== vs ", "===") + row(
   col(box("red", "== loose ✗", "converts types first", 0),
       code("""0 == ""            // true 😬
"1" == 1           // true
null == undefined  // true""", 32, step=0), style="flex:1"),
   col(box("green", "=== strict ✓", "same type and same value", 1),
       code("""0 === ""           // false
"1" === 1          // false""", 32, step=1), style="flex:1"), top=True) +
   note("Always use === and !== · the one exception: <code>x == null</code>", 2),
 "steps": [
  "Now the most famous JavaScript trap: two kinds of equality. Double equals is loose. It converts types before comparing, with confusing rules. So zero equals an empty string. The string one equals the number one. True!",
  "Triple equals is strict. Same type, and same value. No conversions, no surprises.",
  "So always use triple equals. The one accepted exception is x double equals null, which checks for both null and undefined at once.",
 ]},

{"html": H("Truthy and ", "falsy") + fill(
   box("red", "Exactly these are falsy", '<span style="font-family:Consolas;font-size:38px;color:#1f2937">false · 0 · -0 · 0n · "" · null · undefined · NaN</span>', 0),
   box("green", "Everything else is truthy", '<span style="font-family:Consolas;font-size:38px;color:#1f2937">"0" · "false" · [] · {}</span>', 1),
   code("""const title = userTitle || "Untitled";   // fallback""", 34, step=2)),
 "steps": [
  "In an if statement, any value gets turned into a boolean. Exactly eight values are falsy: false, zero, minus zero, big int zero, the empty string, null, undefined, and NaN.",
  "Everything else is truthy. Even the string zero, the string false, an empty array, and an empty object. Yes, an empty array is truthy.",
  "This powers a common pattern. Title equals user title, or, untitled. Or returns the first truthy value, so it's a quick fallback. But careful: it also replaces zero and empty strings. In module seven, you'll meet a safer operator for that.",
 ]},

predict(("Predict the ", "output"), [
  ('"5" + 1', '"51"', "+ with a string joins text",
   "Pause and predict. What's the string five, plus one?", "The string fifty one. When plus meets a string, it joins text."),
  ('"5" - 1', "4", "- only does maths, so it converts the string",
   "And the string five, minus one?", "Four! Minus only does maths, so it converts the string into a number."),
  ("7 / 2", "3.5", "no integer division · <code>Math.floor(7 / 2)</code> → 3",
   "Seven divided by two?", "Three point five. There's no integer division in JavaScript. Use math dot floor if you want three."),
  ("0.1 + 0.2 === 0.3", "false", "0.30000000000000004 · same in Java's double · use cents for money",
   "And the classic. Is point one plus point two, equal to point three?",
   "False! You get point three, followed by lots of zeros and a four. It's not a JavaScript bug. Java's double does the same, because point one can't be stored exactly in binary. For money, work in whole cents."),
]),

{"html": H("Loops: ", "of", " vs in") + row(
   code("""const days = ["Mon", "Tue", "Wed"];

§0 for (const day of days) console.log(day);
§0 // Mon, Tue, Wed  ← values

§1 const scores = { asha: 90, ben: 75 };
§1 for (const name in scores)
§1   console.log(name, scores[name]);  // keys""", 32, style="flex:1"),
   col(box("green", "for…of", "values · use for arrays", 0), box("blue", "for…in", "keys · use for objects", 1),
       box("red", "✗ for…in on arrays", "string indexes \"0\", \"1\"…", 2), style="width:520px"), top=True),
 "steps": [
  "If, else, switch, while and the classic for loop all look exactly like Java. But there are two new loops. For of gives you the values. Use it for arrays.",
  "For in gives you the keys. Use it for objects. An easy way to remember: of, for values, in, for keys.",
  "And don't use for in on arrays. It gives you the indexes as strings, and can even pick up inherited properties.",
 ]},

{"html": H("Strings and ", "numbers") + row(
   code("""s.trim()               // remove spaces
s.includes("React")    // true
"a,b,c".split(",")     // ["a","b","c"]
"hello".slice(1, 3)    // "el"
"x".padStart(3, "0")   // "00x"
""", 30, step=0, style="flex:1"),
   code("""Number("42px")         // NaN
parseInt("42px", 10)   // 42
(3.14159).toFixed(2)   // "3.14"
NaN === NaN            // false!
Number.isNaN(x)        // ✓ check""", 30, step=1, style="flex:1"), top=True),
 "steps": [
  "Strings have all the methods you'd expect. Trim, includes, split, slice, pad start. And like Java, they never change the original string. They return a new one.",
  "For numbers, Number converts a string, but gives NaN, not a number, if there's anything extra. Parse int reads digits until it can't. And NaN has a strange property. It's not equal to anything, not even itself. So to check for it, use Number dot is NaN.",
 ]},

recap(["const by default, let to reassign, never var",
       "Variables don't have types, values do",
       "Always <code>===</code> · <code>typeof null</code> is \"object\"",
       "Falsy: false, 0, \"\", null, undefined, NaN · <code>[]</code> is truthy",
       "<code>\"5\" + 1</code> is \"51\" · <code>0.1 + 0.2</code> isn't 0.3",
       "for…of for values, for…in for keys"],
  "Let's recap. Use const by default, let when you reassign, and never var. Variables don't have types, values do. Always use triple equals. Remember the eight falsy values, and that an empty array is truthy. Plus with a string joins text, and point one plus point two isn't exactly point three. And use for of for values, for in for keys. Next time: functions, scope, and closures. See you there!"),
]
