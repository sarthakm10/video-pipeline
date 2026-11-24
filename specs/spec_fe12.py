from lib import *

TAG = "Frontend 12 · JavaScript Interview Deep Dive"
FILE = "Frontend 12 JavaScript Interview Deep Dive.mp4"

SLIDES = [
title_slide(12, "JavaScript Interview Deep Dive", "Output puzzles and write-it-from-scratch classics",
  "Welcome to module twelve: the JavaScript interview deep dive.",
  "Frontend interviews test JavaScript itself, and they test it hard. Expect what does this print puzzles, and write it from scratch tasks, like debounce, throttle, deep clone, and polyfills. This module collects the classics, each with a clean answer you can write on a whiteboard."),

{"html": H("Coercion: the ", "rules") + row(
   col(box("orange", "+ with a string", "joins: the other side becomes a string", 0),
       box("blue", "- * / %", "convert both sides to numbers", 0),
       box("purple", "==", "null == undefined only · booleans → numbers · objects → primitives", 0), style="width:560px"),
   code("""§1 1 + "2"        // "12"
§1 "3" - 1        // 2
§1 true + 1       // 2
§2 [] + []        // ""
§2 [] + {}        // "[object Object]"
§3 null == 0      // false
§3 [1] == 1       // true
§3 [] == ![]      // true 🤯""", 32, style="flex:1"), top=True) +
   note("In the interview: explain the rule, then say you'd use === and explicit <code>Number(x)</code>", 4),
 "steps": [
  "When an operator gets the wrong types, JavaScript converts them. Three rules explain most puzzles. Plus with a string joins text. The other maths operators convert both sides to numbers. And double equals has its own conversion rules.",
  "So one plus the string two is the string twelve. The string three minus one is two. True plus one is two, because true becomes one.",
  "Arrays become strings. An empty array becomes an empty string, so empty plus empty is empty. And an object becomes the string object Object.",
  "Null only loosely equals undefined, so null double equals zero is false. And the famous one. Empty array equals not empty array is true! Not empty array is false, which is zero. And the empty array becomes an empty string, which is also zero.",
  "In the interview, explain the rule. Then say that in real code, you'd use triple equals and explicit conversions.",
 ]},

predict(("The famous ", "loop"), [
  ("for (var i = 0; i &lt; 3; i++)<br>&nbsp;&nbsp;setTimeout(() =&gt; log(i), 0);", "3, 3, 3", "<code>var</code> → ONE <code>i</code> · timers run after the loop ends",
   "The most famous output question. A for loop with var, scheduling three timeouts that log i. What prints?",
   "Three, three, three! Var makes one i for the whole function. The timers run after the loop has finished, when i is three, and all three callbacks share that same variable."),
  ("for (let i = 0; i &lt; 3; i++)<br>&nbsp;&nbsp;setTimeout(() =&gt; log(i), 0);", "0, 1, 2", "<code>let</code> → a new binding per iteration",
   "Now the same loop, with let.",
   "Zero, one, two. Let creates a new binding for each iteration. So each callback closes over its own i."),
], size=30),

predict(("More ", "output", " classics"), [
  ("let a = { n: 1 };<br>let b = a;<br>a = { n: 2 };<br>log(b.n);", "1", "a was re-pointed, not changed",
   "Pause and predict. A is an object with n one. B equals a. Then a is pointed at a new object. What's b dot n?",
   "One. B still points to the first object. A was re-pointed to a new object. The first one wasn't changed."),
  ("function f() { return<br>&nbsp;&nbsp;{ ok: true };<br>}<br>log(f());", "undefined", "a line break after <code>return</code> inserts a semicolon",
   "And this function returns an object, on the line after return. What does f return?",
   "Undefined! A line break right after return automatically inserts a semicolon. So it returns nothing."),
], size=30),

predict(("Event loop ", "order"), [
  ('log("1");<br>setTimeout(() =&gt; log("2"));<br>Promise.resolve().then(() =&gt; log("3"));<br>queueMicrotask(() =&gt; log("4"));<br>log("5");',
   "1, 5, 3, 4, 2", "sync → all microtasks → one task",
   "Event loop time. Log one. A timeout logging two. A promise then logging three. A microtask logging four. And log five.",
   "One, five, three, four, two. Synchronous code first. Then all the microtasks, in order. Then the timer task."),
  ('async function run() {<br>&nbsp;&nbsp;log("A"); await null; log("B");<br>}<br>log("start"); run(); log("end");',
   "start, A, end, B", "before the first <code>await</code> runs synchronously",
   "And with async. Run logs A, awaits, then logs B. We log start, call run, and log end.",
   "Start, A, end, B. Everything before the first await runs synchronously. The rest becomes a microtask."),
], size=27),

{"html": H("", "Debounce") + row(code("""function debounce(fn, wait) {
  let timer;
  return function (...args) {
§1     clearTimeout(timer);           // cancel the pending call
§1     timer = setTimeout(() => fn.apply(this, args), wait);
  };
}
§2 const search = debounce(q => fetchResults(q), 300);
§2 search("j"); search("ja"); search("jav"); search("java");
§2 // after 300 ms of quiet → one call: "java" """, 29, style="flex:1"),
   col(box("green", "runs once", "after the calls <b style=\"display:inline\">stop</b> for <code>wait</code> ms", 0),
       box("blue", "use for", "search-as-you-type · auto-save · resize end", 2), style="width:460px"), top=True),
 "steps": [
  "Debounce and throttle both limit how often a function runs, when an event fires rapidly. Debounce runs the function only after the calls stop, for a given wait.",
  "Here's how it works. It returns a new function. Every call clears the previous timer, and starts a new one. So only the last call survives. And fn dot apply keeps the caller's this, and its arguments.",
  "So for a search box, the user types j, j a, j a v, java. And only once they pause for three hundred milliseconds do we search, once, for java. Notice timer lives on between calls. That's a closure.",
 ]},

{"html": H("", "Throttle") + row(code("""function throttle(fn, wait) {
  let last = 0;
  return function (...args) {
    const now = Date.now();
§1     if (now - last >= wait) {
§1       last = now;
§1       fn.apply(this, args);
§1     }
  };
}
§2 window.addEventListener("scroll", throttle(onScroll, 200));""", 29, style="flex:1"),
   table(["", "Debounce", "Throttle"], [
     (["Runs", "once, after the burst", "regularly during it"], 3),
     (["Use", "search box", "scroll, rate-limit clicks"], 3)], size=27), top=True),
 "steps": [
  "Throttle runs the function at most once every wait milliseconds, however often it's called.",
  "It remembers when it last ran. If enough time has passed, it runs, and updates last. Otherwise, the call is simply ignored.",
  "Use it for scroll or resize handlers, or a save button that mustn't fire ten times.",
  "So the difference: debounce runs once, after the burst ends. Throttle runs regularly, during the burst. A common follow-up is adding a cancel method.",
 ]},

{"html": H("Deep clone and ", "flatten") + code("""function deepClone(value, seen = new WeakMap()) {
§0   if (value === null || typeof value !== "object") return value;
§1   if (seen.has(value)) return seen.get(value);    // circular references
  const copy = Array.isArray(value) ? [] : {};
  seen.set(value, copy);
§0   for (const key of Object.keys(value)) copy[key] = deepClone(value[key], seen);
  return copy;
}
§2 const flatten = (arr) => arr.reduce((out, item) =>
§2   Array.isArray(item) ? out.concat(flatten(item)) : out.concat([item]), []);
§2 flatten([1, [2, [3, [4]]]]);    // [1, 2, 3, 4]""", 28),
 "steps": [
  "Deep clone, without structured clone. If the value is a primitive, return it as it is. Otherwise, make an empty array or object, and recursively clone every key into it.",
  "The detail that impresses interviewers is circular references. An object that points to itself would recurse forever. So keep a weak map of objects you've already copied, and reuse the copy.",
  "Flatten a nested array. Reduce over it. If an item is an array, flatten it recursively and concat. Otherwise, just add the item.",
 ]},

{"html": H("Curry and ", "memoize") + row(code("""§0 function curry(fn) {
§0   return function curried(...args) {
§0     if (args.length >= fn.length)
§0       return fn.apply(this, args);
§0     return (...more) =>
§0       curried.apply(this, [...args, ...more]);
§0   };
§0 }
§0 add3(1)(2)(3);   // 6
§0 add3(1, 2)(3);   // 6""", 28, style="flex:1"),
   code("""§1 function memoize(fn) {
§1   const cache = new Map();
§1   return function (...args) {
§1     const key = JSON.stringify(args);
§1     if (!cache.has(key))
§1       cache.set(key, fn.apply(this, args));
§1     return cache.get(key);
§1   };
§1 }""", 28, style="flex:1"), top=True) + note("Same idea as React's <code>useMemo</code> and dynamic programming", 2),
 "steps": [
  "Curry turns a function of three arguments into one you can call one at a time. If we have enough arguments, fn dot length tells us how many, we call the function. Otherwise, return a function that collects more.",
  "Memoize caches results. Turn the arguments into a key. If we haven't seen it, call the function and store the result. Either way, return from the cache. The second call is instant.",
  "That's the same idea as React's use memo, and dynamic programming.",
 ]},

{"html": H("Polyfills: ", "map", " and bind") + row(code("""Array.prototype.myMap = function (cb, thisArg) {
  const result = [];
  for (let i = 0; i < this.length; i++) {
§1     if (i in this)                     // skip holes
      result[i] = cb.call(thisArg, this[i], i, this);
  }
  return result;
};""", 28, style="flex:1"),
   code("""§2 Function.prototype.myBind =
§2   function (thisArg, ...preset) {
§2     const fn = this;
§2     return function (...later) {
§2       return fn.apply(thisArg,
§2         [...preset, ...later]);
§2     };
§2   };""", 28, style="width:600px"), top=True),
 "steps": [
  "A polyfill adds a missing built-in feature, for old environments. Interviewers use them to check you really understand a feature. Call them my map and so on, so you don't overwrite the real ones. Inside, this is the array. Loop over it, call the callback with the item, the index, and the array, and collect the results.",
  "A nice detail: skip holes in sparse arrays, with i in this.",
  "And my bind. Save the function. Return a new function that, when called, applies the original with the fixed this, and the preset arguments, followed by any later ones.",
 ]},

{"html": H("Write ", "Promise.all") + code("""function promiseAll(items) {
  return new Promise((resolve, reject) => {
    const results = [];
    let done = 0;
§3     if (items.length === 0) return resolve(results);
    items.forEach((item, i) => {
§2       Promise.resolve(item).then(value => {   // plain values count
§1         results[i] = value;                    // keep input order
§1         if (++done === items.length) resolve(results);
§3       }, reject);                               // first failure rejects
    });
  });
}""", 29),
 "steps": [
  "Writing promise dot all is a top interview question. Return a new promise. Keep a results array, and a count of how many have finished.",
  "When each one resolves, store its value at its own index, not with push. That keeps the input order, not the finish order. And when the count reaches the total, resolve with all the results.",
  "Wrap each item in promise dot resolve, so plain values work too.",
  "And the edge cases they look for. An empty array resolves straight away. And the first failure rejects everything.",
 ]},

{"html": H("Generators and ", "garbage collection") + row(code("""§0 function* idGenerator() {
§0   let id = 1;
§0   while (true) yield id++;   // lazy, infinite
§0 }
§0 const ids = idGenerator();
§0 ids.next().value;   // 1
§0 ids.next().value;   // 2""", 29, style="flex:1"),
   col(box("purple", "WeakMap / WeakSet", "don't keep keys alive · attach data to DOM nodes safely", 1),
       box("gray", "mark-and-sweep", "keep everything reachable from the roots, free the rest", 2),
       box("red", "leaks", "listeners & timers never removed · growing caches · detached DOM nodes", 3), style="width:600px"), top=True),
 "steps": [
  "A generator function, with a star, returns an iterator. Yield pauses the function between values. So you can even have an infinite sequence, computed lazily, one value at a time.",
  "A weak map holds its keys weakly. An entry doesn't stop its key from being garbage collected. So it's perfect for attaching data to objects you don't own, like DOM nodes, without leaking memory.",
  "JavaScript frees memory automatically, with mark and sweep. Starting from the roots, everything reachable is kept, and the rest is freed.",
  "So leaks happen when something stays reachable by accident. Listeners and timers never removed, caches that keep growing, and references to removed DOM nodes. In React, effect cleanups exist largely for this.",
 ]},

quiz([
  ("Is the Promise executor synchronous?", "<b style=\"display:inline\">Yes</b> · only then/catch callbacks are deferred", "blue",
   "Quiz time. Does the function you pass to new Promise run synchronously?",
   "Yes! Only the then and catch callbacks are deferred."),
  ("Debounce vs throttle?", "debounce: once after calls stop · throttle: at most once per interval", "green",
   "Debounce versus throttle?",
   "Debounce runs once, after the calls stop. Throttle runs at most once per interval."),
  ("What must <code>promiseAll</code> preserve?", "<b style=\"display:inline\">input order</b> · reject on the first failure", "purple",
   "And what must your promise all preserve?",
   "The input order. And it must reject on the first failure."),
]),

recap(["+ with a string joins · other maths converts to numbers",
       "var loop → 3, 3, 3 · let loop → 0, 1, 2",
       "sync → all microtasks → one task",
       "Debounce & throttle rely on closures",
       "deepClone handles cycles · promiseAll keeps order",
       "WeakMap doesn't leak · remove listeners and timers"],
  "Let's recap. Plus with a string joins text, and other maths converts to numbers. A var loop prints three, three, three, and a let loop prints zero, one, two. Synchronous code runs first, then all microtasks, then one task. Debounce and throttle both rely on closures. Deep clone must handle cycles, and promise all must keep the input order. And weak maps don't leak, but forgotten listeners and timers do. Next time: TypeScript!"),
]
