from lib import *

TAG = "Frontend 8 · this, Prototypes and Classes"
FILE = "Frontend 8 this, Prototypes and Classes.mp4"

def arrow(label, step):
    return f'<div class="arrow" data-step="{step}">{label}</div>'

SLIDES = [
title_slide(8, "this, Prototypes & Classes", "JavaScript objects work differently from Java's under the hood",
  "Welcome to module eight: this, prototypes, and classes.",
  "JavaScript's objects work differently from Java's under the hood. The value of this depends on how a function is called, and inheritance uses prototypes, with class as friendlier syntax on top. Modern React uses little of this directly. But interviewers love it, and it explains a lot of confusing bugs."),

{"html": H("How ", "this", " is decided") + table(["How it's called", "this is", "Example"], [
   (["with <code>new</code>", "the brand-new object", "<code>new User(\"Asha\")</code>"], 0),
   (["<code>call</code> / <code>apply</code> / <code>bind</code>", "whatever you pass", "<code>greet.call(user)</code>"], 1),
   (["as a method", "the object before the dot", "<code>user.greet()</code>"], 2),
   (["plain call", "<code>undefined</code> (strict mode)", "<code>const g = user.greet; g()</code>"], 3),
   (["arrow function", "the <code>this</code> around it", "<code>() =&gt; this.name</code>"], 4)], size=31) +
   note("Java: <code>this</code> is always the current object · JS: decided at <u>call time</u>", 0),
 "steps": [
  "In Java, this is always the current object. In JavaScript, a regular function's this is decided at the moment it's called, by how it's called. Check these rules in order. Called with new? Then this is the brand new object.",
  "Called with call, apply or bind? Then this is whatever you pass in.",
  "Called as a method, object dot function? Then this is the object before the dot.",
  "Called as a plain function, with nothing before it? Then this is undefined, in strict mode and in modules.",
  "And arrow functions are the exception. They don't have their own this at all. They use the this of the code around them.",
 ]},

{"html": H("The lost ", "this") + code("""const user = {
  name: "Asha",
  greet() { return `Hi, ${this.name}`; },
};
§0 user.greet();       // "Hi, Asha": called as a method
§1 const g = user.greet;
§1 g();                // 💥 TypeError: this is undefined

§2 setTimeout(user.greet, 100);                 // ✗ lost again
§3 setTimeout(() => user.greet(), 100);         // ✓ called as a method
§3 setTimeout(user.greet.bind(user), 100);      // ✓ this fixed with bind""", 31),
 "steps": [
  "Let's see the rules in action. User dot greet. It's called as a method, so this is user, and we get hi, Asha.",
  "Now copy the method into a variable g, and call g on its own. It's a plain call now. There's nothing before the dot, so this is undefined, and it crashes. The method lost its object.",
  "This happens every time you pass a method as a callback. Set timeout calls greet later, as a plain function. Lost again.",
  "Two fixes. Wrap it in an arrow function, so it's called as a method. Or use bind, to fix this permanently.",
 ]},

{"html": H("Arrows inside ", "methods") + code("""const timer = {
  seconds: 0,
  start() {
§0     setInterval(() => { this.seconds++; }, 1000);          // ✓ this is timer
§1     // setInterval(function () { this.seconds++; }, 1000);  // ✗ this is lost
  },
§2   // stop: () => this.seconds   ✗ arrow AS a method: this is outside
};""", 31) + note("Arrow functions inside methods ✓ · arrow functions as methods ✗", 2),
 "steps": [
  "Arrow functions take this from where they're written. And that's exactly what you want inside a method. The arrow function passed to set interval uses start's this, which is the timer. So seconds goes up.",
  "With a regular function, set interval calls it as a plain function, so this is lost.",
  "But don't use an arrow function as the method itself. Then it takes this from outside the object, which isn't the object at all. So: arrows inside methods, yes. Arrows as methods, no.",
 ]},

{"html": H("call, apply and ", "bind") + code("""function introduce(greeting, punctuation) {
  return `${greeting}, I'm ${this.name}${punctuation}`;
}
const asha = { name: "Asha" };
§0 introduce.call(asha, "Hello", "!");      // "Hello, I'm Asha!"
§1 introduce.apply(asha, ["Hey", "."]);     // "Hey, I'm Asha."
§2 const bound = introduce.bind(asha, "Hi");
§2 bound("?");                              // "Hi, I'm Asha?" """, 30) +
   row(box("blue", "call", "runs now · args listed", 0), box("purple", "apply", "runs now · args as an <b style=\"display:inline\">A</b>rray", 1),
       box("green", "bind", "returns a new function", 2), style="margin-top:24px"),
 "steps": [
  "Call, apply and bind all set this explicitly. Call runs the function right now, with this set to asha, and the arguments listed one by one.",
  "Apply also runs it now, but takes the arguments as an array. A memory trick: apply takes an array. Both start with A.",
  "Bind doesn't run anything. It returns a brand new function, with this fixed forever. And it can pre-fill arguments too, like hi here. That's called partial application. Writing your own bind is a classic interview task, which we'll do in module twelve.",
 ]},

{"html": H("The prototype ", "chain") + code("""const animal = { eats: true, describe() { return `${this.name} eats`; } };
const dog = Object.create(animal);   // dog's prototype is animal
dog.name = "Rex";""", 30) +
   row(box("orange", "dog", "<code>name: \"Rex\"</code>", 0, "width:300px"), arrow("prototype", 1),
       box("blue", "animal", "<code>eats</code>, <code>describe()</code>", 1, "width:330px"), arrow("prototype", 2),
       box("gray", "Object.prototype", "<code>toString()</code>", 2, "width:390px"), arrow("", 2),
       box("red", "null", "", 2, "width:120px"), gap=10, style="margin-top:34px;align-items:center") +
   code("""§1 dog.eats          // true: found on the prototype
§1 dog.describe()    // "Rex eats": this = dog
§3 [1, 2].map        // from Array.prototype""", 30, style="margin-top:30px"),
 "steps": [
  "Every JavaScript object has a hidden link to another object, called its prototype. Here, object dot create makes dog, with animal as its prototype. Dog only has its own name.",
  "So what happens when you read dog dot eats? Dog doesn't have it. So JavaScript looks in the prototype, animal, and finds it. Methods work the same way, and this is still dog.",
  "And animal has its own prototype, object dot prototype, where to string lives. Then null, the end of the chain. That chain is how JavaScript does inheritance.",
  "Built-ins work the same way. Map comes from array dot prototype. That's why you shouldn't change built-in prototypes in your app code.",
 ]},

{"html": H("", "Classes") + row(code("""class Account {
  static bankName = "JS Bank";
  balance = 0;                    // field
  constructor(owner) { this.owner = owner; }
  deposit(amount) {               // on the prototype
    this.balance += amount;
    return this;                  // chaining
  }
}
§1 class SavingsAccount extends Account {
§1   constructor(owner, rate) {
§1     super(owner);              // before using this!
§1     this.rate = rate;
§1   }
§1 }""", 28, style="flex:1"),
   col(box("gray", "syntax over prototypes", "methods live once on <code>Account.prototype</code>", 0),
       box("red", "one constructor", "no overloading · use defaults", 2),
       box("red", "no interfaces", "duck-typed (TypeScript adds them)", 2),
       box("orange", "methods aren't bound", "<code>const d = s.deposit</code> loses <code>this</code>", 2), style="width:560px"), top=True),
 "steps": [
  "Class gives JavaScript the syntax you know from Java. Static fields, instance fields, a constructor, and methods. But underneath, it's prototypes. Methods live once on account dot prototype, and every instance links to it.",
  "Extends works as you'd expect. One rule: in a subclass constructor, call super before using this.",
  "Some differences from Java. There's only one constructor, no overloading, so use default parameters. There are no interfaces, because JavaScript is duck typed. TypeScript adds them. And methods aren't bound, so copying a method out loses this. In modern React you'll rarely write classes, because components are functions. But they're handy for services and data models.",
 ]},

{"html": H("Getters, setters and ", "#private") + row(code("""class Temperature {
§0   #celsius = 0;                  // truly private
§1   get fahrenheit() {
§1     return this.#celsius * 9 / 5 + 32;
§1   }
§1   set celsius(value) {
§1     if (value < -273.15) throw new RangeError("Too cold");
§1     this.#celsius = value;
§1   }
}
§2 t.celsius = 25;   // setter
§2 t.fahrenheit;     // 77, getter
§3 t.#celsius;       // SyntaxError""", 27, style="flex:1"),
   col(table(["Java", "JavaScript"], [
     (["<code>private</code>", "<code>#field</code>"], 0),
     (["<code>getX()</code> / <code>setX()</code>", "<code>get x()</code> / <code>set x(v)</code>"], 1),
     (["<code>protected</code>", "✗ (<code>_name</code> convention)"], 3)], size=28), style="width:600px;flex-shrink:0"), top=True),
 "steps": [
  "A field starting with a hash is private. Only code inside the class can see it, and the language enforces that.",
  "Getters and setters are written with get and set. But you use them like normal properties, not method calls. And a setter is a good place for validation.",
  "So you assign t dot celsius, and read t dot fahrenheit. Seventy seven.",
  "And reading the private field from outside is a syntax error. There's no protected in JavaScript. An underscore at the start of a name is just a convention that means please don't touch.",
 ]},

predict(("Predict the ", "output"), [
  ("const g = user.greet; g()", "TypeError", "plain call → <code>this</code> is undefined",
   "Pause and predict. User dot greet returns hi, this dot name. We copy it to g and call g. What happens?",
   "A type error. It's a plain call, so this is undefined, and reading name from undefined crashes."),
  ("dog.hasOwnProperty(\"eats\")", "false", "<code>eats</code> lives on the prototype, not on <code>dog</code>",
   "And does dog have its own eats property?",
   "False. Dog can read eats, but it lives on the prototype, animal. Has own property only checks the object itself."),
]),

quiz([
  ("<code>this</code> inside an arrow function?", "The <code>this</code> of the surrounding code · arrows have none", "green",
   "Quiz time. What's this inside an arrow function?",
   "The this of the surrounding code. Arrow functions don't have their own."),
  ("<code>call</code> vs <code>apply</code> vs <code>bind</code>?", "call: args listed · apply: an array · bind: a new function", "blue",
   "Call versus apply versus bind?",
   "Call and apply both run now. Call takes the arguments listed, apply takes an array. Bind returns a new function."),
  ("What are JS classes built on?", "<b style=\"display:inline\">Prototypes</b> · class is syntax on top", "purple",
   "And what are JavaScript classes built on?",
   "Prototypes. Class is just nicer syntax on top."),
]),

recap(["<code>this</code> depends on how a function is called",
       "Plain call → undefined · passing a method loses <code>this</code>",
       "Arrows use the surrounding <code>this</code>",
       "call (listed) · apply (array) · bind (new function)",
       "Missing property? Look up the prototype chain",
       "class = prototypes + nicer syntax · <code>#private</code> fields"],
  "Let's recap. This depends on how a function is called. A plain call gives undefined, so passing a method as a callback loses this. Arrow functions use the this around them. Call takes arguments listed, apply takes an array, and bind returns a new function. A missing property is looked up along the prototype chain. And classes are prototypes with nicer syntax, with hash for private fields. Next time: working with the DOM!"),
]
