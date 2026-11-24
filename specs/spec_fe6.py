from lib import *

TAG = "Frontend 6 · Functions, Scope and Closures"
FILE = "Frontend 6 Functions, Scope and Closures.mp4"

def scopes(step_inner=0):
    return f'''<div style="border:5px solid #64748b;border-radius:22px;padding:22px 26px;background:#f8fafc;font-size:30px">
  <b style="font-size:30px">🌍 global</b> &nbsp;<code>app = "Tracker"</code>
  <div style="border:5px solid #2563eb;border-radius:18px;padding:20px 24px;background:#eff6ff;margin-top:16px">
    <b style="font-size:30px">outer()</b> &nbsp;<code>user = "Asha"</code>
    <div style="border:5px solid #16a34a;border-radius:16px;padding:18px 22px;background:#f0fdf4;margin-top:14px">
      <b style="font-size:30px">inner()</b> &nbsp;<code>day = 5</code>
      <div style="margin-top:10px;font-size:28px">console.log(app, user, day) <span data-step="{step_inner}">← looks here, then outwards ↑↑</span></div>
    </div></div></div>'''

SLIDES = [
title_slide(6, "Functions, Scope & Closures", "Functions are values · they remember where they were born",
  "Welcome to module six: functions, scope, and closures.",
  "Functions are the heart of JavaScript. They're values you can store and pass around, they remember where they were created, and React components are just functions. And closures in particular come up in almost every frontend interview. So let's get them really clear."),

{"html": H("Three ways to write a ", "function") + code("""§1 function add(a, b) {           // 1 · declaration (hoisted)
§1   return a + b;
§1 }
§2 const multiply = function (a, b) { return a * b; };   // 2 · expression

§3 const square = (x) => x * x;             // 3 · arrow: returned automatically
§3 const greet = (name) => {                // a block body needs return
§3   return `Hi, ${name}`;
§3 };
§4 const makeUser = (name) => ({ name });  // object? wrap in ( )""", 31) + note("Arrows have no own <code>this</code>: great for callbacks, wrong for methods", 4),
 "steps": [
  "There are three ways to write a function in JavaScript.",
  "One: a function declaration. It's hoisted, which means you can call it even before the line where it's written.",
  "Two: a function expression. That's a function stored in a variable.",
  "Three: the arrow function. It's shorter, and it's the usual choice for callbacks. If the body is a single expression, its value is returned automatically. If you use curly braces, you need a return.",
  "One gotcha. To return an object from an arrow function, wrap it in parentheses, otherwise the braces look like a function body. And arrow functions don't have their own this. That makes them great for callbacks and React components, but wrong for object methods. More on that in module eight.",
 ]},

{"html": H("Parameters: defaults and ", "rest") + code("""§0 hello();                 // "Hello undefined": missing → undefined

§1 function paginate(items, page = 1, size = 10) { … }
§1 paginate(list, 3);       // page 3, size 10

§2 function sum(...nums) {  // rest: a real array
§2   return nums.reduce((total, n) => total + n, 0);
§2 }
§2 sum(1, 2, 3);            // 6

§3 createUser({ name: "Asha", role: "admin" });   // options object""", 31),
 "steps": [
  "JavaScript doesn't check how many arguments you pass. Missing ones are simply undefined, and extra ones are ignored.",
  "Default values fill in any missing arguments. So paginate with just a list uses page one, size ten.",
  "Rest parameters, with three dots, collect the remaining arguments into a real array. Like varargs in Java.",
  "And there's no method overloading. A second function with the same name just replaces the first. Instead, use defaults, rest parameters, or pass one options object. That gives you named arguments, in any order.",
 ]},

{"html": H("Scope and the ", "scope chain") + row(col(scopes(1), note("Lexical scope: decided by where code is <u>written</u>", 3, "margin-top:40px"), style="flex:1"), col(
   box("gray", "Global", "everything sees it", 0, "padding:14px 26px"), box("blue", "Function", "each function", 0, "padding:14px 26px"),
   box("green", "Block { }", "<code>let</code> / <code>const</code> only", 0, "padding:14px 26px"), box("red", "↓ not visible", "outer can't see <code>day</code>", 2, "padding:14px 26px"),
   style="width:440px;flex-shrink:0"), top=True),
 "steps": [
  "Scope decides where a variable can be seen. There's the global scope at the top level, a scope for every function, and a block scope for any curly braces, which only let and const respect.",
  "When code uses a variable, JavaScript looks in the current scope first, then the one around it, and so on outwards, until the global scope. That path is called the scope chain. So inner can see day, user, and app.",
  "But it only goes outwards, never inwards. The outer function can't see inner's day variable. That's a reference error.",
  "And scope is decided by where the code is written, not where it's called from. That's called lexical scope. And it's exactly what makes closures work.",
 ]},

{"html": H("Hoisting and the ", "TDZ") + table(["Declaration", "Before its line you get"], [
   (["<code>function f() {}</code>", "✓ a working function"], 0),
   (["<code>var x</code>", "<code>undefined</code> 😬"], 1),
   (["<code>let</code> / <code>const</code> / <code>class</code>", "✗ ReferenceError (temporal dead zone)"], 2)], size=34) +
   code("""§0 sayHi();                // works
§0 function sayHi() { … }
§1 console.log(a);         // undefined
§1 var a = 1;
§2 console.log(b);         // ReferenceError
§2 let b = 2;""", 30, style="margin-top:24px"),
 "steps": [
  "Before running code, JavaScript scans each scope and sets up its declarations. That's called hoisting. And it behaves differently for each kind. Function declarations are hoisted completely, body and all, so you can call them before their line.",
  "Var is hoisted too, but only the name. It's set to undefined. So reading it early silently gives you undefined. That's the kind of bug that makes var a bad idea.",
  "Let, const and class are hoisted, but not initialised. Between the start of the scope and their line, they're in the temporal dead zone. Touch them there, and you get a clear reference error. And that's a good thing. A mistake becomes a loud error, instead of a silent undefined.",
 ]},

{"html": H("", "Closures") + row(code("""function makeCounter() {
  let count = 0;
  return function () {
    count++;
    return count;
  };
}
§1 const next = makeCounter();
§1 next();   // 1
§1 next();   // 2
§2 const other = makeCounter();
§2 other();  // 1  ← its own count""", 32, style="flex:1"),
   col(box("purple", "🎒 a backpack", "the inner function carries <code>count</code> with it, even after <code>makeCounter</code> returned", 1),
       box("green", "fresh each call", "every <code>makeCounter()</code> makes a new <code>count</code>", 2),
       box("blue", "private", "nobody can touch <code>count</code> except <code>next</code>", 3), style="width:560px"), top=True),
 "steps": [
  "Now, closures. A closure is a function, together with the variables from the scope where it was created. Look at make counter. It creates a count variable, and returns an inner function that increases it.",
  "We call make counter, and store the result in next. Make counter has finished. Normally its count would be gone. But next still has access to it. Call next, one. Call it again, two. Think of it as a backpack. The inner function carries count along with it, wherever it goes.",
  "And every call to make counter makes a fresh count. So other starts again at one. Two separate backpacks.",
  "Notice too that count is completely private. Nothing outside can read or change it, except through next. Before classes had private fields, this was how JavaScript hid data.",
 ]},

{"html": H("Where you'll meet ", "closures") + pts([
   ("<b>Event handlers</b> that use variables around them: <code>() =&gt; alert(message)</code>", 0),
   ("<b>Function factories</b>: <code>const double = multiplier(2)</code>", 1),
   ("<b>React hooks</b>: each render's handlers close over that render's state", 2),
   ("<b>debounce, throttle, memoize</b> keep timers and caches in a closure", 2),
   ("⚠️ Closures keep variables alive → remove listeners and timers you don't need", 3, "x")], size=36),
 "steps": [
  "You'll meet closures everywhere. An event handler that uses a message variable from around it remembers that message, even when the click happens much later.",
  "Function factories. Multiplier two returns a function that remembers the factor two.",
  "In React, every render's event handlers close over that render's state. That explains the famous stale state bug you'll see in module seventeen. And debounce, throttle and memoize all keep their timers and caches in a closure.",
  "One warning. A closure keeps its variables alive in memory. So a listener that's never removed, or a cache that grows forever, can leak memory. The fix is to remove listeners and clear timers when you're done.",
 ]},

{"html": H("Higher-order functions and ", "callbacks") + code("""§0 function repeat(n, action) {            // takes a function
§0   for (let i = 0; i < n; i++) action(i);
§0 }
§1 const multiplier = (factor) => (x) => x * factor;   // returns one
§1 multiplier(2)(21);                       // 42

§2 [3, 1, 2].sort((a, b) => a - b);
§2 button.addEventListener("click", handleClick);   // pass, don't call!
§2 setTimeout(() => console.log("later"), 1000);""", 31) + note("Java's lambdas + Function / Predicate, but built in", 3),
 "steps": [
  "Because functions are values, you can pass them into other functions. A function that takes a function, like repeat here, is called a higher-order function.",
  "A function can also return a function. Multiplier takes a factor, and gives back a new function that multiplies by it.",
  "A function passed in to be called later is a callback. You use them constantly. A sort comparison, an event listener, a timer. And notice, handle click has no parentheses. You pass the function, you don't call it.",
  "If you know Java, this is what lambdas and functional interfaces give you. In JavaScript, it's simply built in.",
 ]},

quiz([
  ("<code>const f = () =&gt; { a: 1 };</code> &nbsp;what does <code>f()</code> return?", "<b style=\"display:inline;font-size:32px\">undefined</b> · the braces are a body · use <code>() =&gt; ({ a: 1 })</code>", "red",
   "Quiz time. This arrow function looks like it returns an object with a equals one. What does it actually return?",
   "Undefined! The curly braces are treated as a function body, not an object. Wrap the object in parentheses."),
  ("<code>console.log(x); var x = 5;</code> &nbsp;and with <code>let</code>?", "<b style=\"display:inline;font-size:32px\">undefined</b> · with let: ReferenceError (TDZ)", "yellow",
   "Next. Console log x, then var x equals five. What prints? And what if it was let?",
   "With var, undefined, because the name is hoisted but not the value. With let, a reference error, because of the temporal dead zone."),
  ("Two counters from <code>makeCounter()</code>: do they share <code>count</code>?", "<b style=\"display:inline;font-size:32px\">No</b> · each call creates a fresh closure", "green",
   "Last one. You call make counter twice. Do the two counters share the same count?",
   "No. Each call to make counter creates a brand new count, so each counter has its own closure."),
]),

recap(["Declaration (hoisted), expression, arrow (no own <code>this</code>)",
       "Defaults, rest <code>...args</code>, options objects · no overloading",
       "Scope chain looks outwards · lexical scope",
       "var → undefined early · let/const → TDZ error",
       "Closure = function + the variables where it was created",
       "Higher-order functions take or return functions"],
  "Let's recap. There are three ways to write a function, and arrows don't have their own this. Use defaults, rest parameters and options objects, since there's no overloading. The scope chain looks outwards, and scope is lexical. Var is undefined before its line, while let and const throw in the temporal dead zone. A closure is a function plus the variables where it was created. And higher-order functions take or return functions. Next time: arrays, objects, and modern syntax!"),
]
