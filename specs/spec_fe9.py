from lib import *

TAG = "Frontend 9 · The DOM and Events"
FILE = "Frontend 9 The DOM and Events.mp4"

def chain(names, color, step, label):
    items = []
    for i, n in enumerate(names):
        items.append(f'<div class="pill" style="font-size:36px;padding:10px 26px;background:{color}">{n}</div>')
        if i < len(names) - 1:
            items.append('<span style="font-size:40px;color:#374151">→</span>')
    return (f'<div data-step="{step}" style="display:flex;align-items:center;gap:16px;margin-top:40px">'
            f'<b style="width:260px;font-size:36px">{label}</b>' + "".join(items) + "</div>")

SLIDES = [
title_slide(9, "The DOM and Events", "Where JavaScript meets the page",
  "Welcome to module nine: the DOM and events.",
  "This is where JavaScript meets the page. You'll find elements, change them, create new ones, and react to clicks and typing, with no framework at all. React does all of this for you later. And knowing what it does underneath makes React much easier to understand."),

{"html": H("Finding ", "elements") + row(
   code("""§0 document.getElementById("tasks");
§0 document.querySelector(".task");          // FIRST match
§0 document.querySelectorAll("#tasks > li"); // ALL: a NodeList

§1 const titles = [...document.querySelectorAll(".task")]
§1   .map(li => li.textContent);

§2 li.parentElement;      li.children;
§2 li.nextElementSibling;
§2 li.closest("ul");      // nearest matching ancestor""", 29, style="flex:1"),
   col(box("blue", "any CSS selector", "querySelector covers almost everything", 0),
       box("orange", "NodeList ≠ array", "spread it for map / filter", 1),
       box("red", "null?", "script ran before the HTML existed → <code>defer</code>", 3), style="width:500px"), top=True),
 "steps": [
  "The DOM is a tree of element objects, and document is its root. To find elements, get element by ID finds one by its ID. But query selector is the real workhorse. It takes any CSS selector and returns the first match. Query selector all returns every match.",
  "Query selector all gives you a node list. It's not a real array. It has for each and length, but for map or filter, spread it into an array first.",
  "From any element, you can walk the tree. Its parent, its children, its next sibling. And closest finds the nearest ancestor that matches a selector. That one's very handy.",
  "If nothing matches, query selector returns null, and calling a method on it throws the classic cannot read properties of null. A common cause is a script running before the HTML below it exists. Fix it with defer.",
 ]},

{"html": H("Changing the ", "page") + code("""const title = document.querySelector("h1");
§0 title.textContent = "My Tasks";           // plain text: safe ✓
§1 title.innerHTML = "My <em>Tasks</em>";    // parses HTML ⚠️
§2 title.classList.add("highlight");
§2 title.classList.toggle("dark");           // add if missing, remove if present
§2 title.dataset.day;                        // reads data-day="5"
§3 title.style.color = "teal";               // inline style: use sparingly
§3 input.value;                              // what the user typed""", 30) +
   row(box("red", "⚠️ innerHTML + user input = XSS", "use <code>textContent</code> for text", 1, "flex:1"),
       box("green", "toggle classes, not styles", "keep the looks in CSS", 2, "flex:1"), style="margin-top:24px"),
 "steps": [
  "Once you have an element, you can change it. Text content sets plain text. It's always safe.",
  "Inner HTML parses a string as HTML. That's dangerous with user input. If someone types an image tag with an on error script, that script runs in your page. That's called an XSS attack. So use text content for text, and inner HTML only with HTML you wrote yourself.",
  "Class list lets you add, remove and toggle classes. And dataset reads data attributes. Prefer toggling classes over setting styles. Keep the looks in CSS, and let JavaScript only say what state something is in.",
  "You can set inline styles, in camel case, but use them sparingly. And for inputs, value is what the user typed.",
 ]},

{"html": H("Creating and removing ", "elements") + code("""function addTask(title) {
  const li = document.createElement("li");
  li.className = "task";
  li.textContent = title;                        // safe even with HTML in it
§1   const del = document.createElement("button");
§1   del.textContent = "✕";
§1   del.addEventListener("click", () => li.remove());
§1   li.append(del);
  list.append(li);                               // prepend: at the start
}
§2 const fragment = document.createDocumentFragment();
§2 for (const t of tasks) fragment.append(makeLi(t));
§2 list.append(fragment);                         // ONE insertion""", 29),
 "steps": [
  "To add something to the page, create an element, set it up, and append it. Here's add task. Create an l i, give it a class, and set its text. Using text content keeps it safe, even if the title contains HTML.",
  "We can give it a delete button too. Create a button, and when it's clicked, remove the l i. Then append the button into the l i, and the l i into the list.",
  "A performance tip. Every change to the live DOM can make the browser redo the layout. So adding a thousand items one by one is slow. Build them in a document fragment first, and append once.",
 ]},

{"html": H("The problem React ", "solves") + fill(
   row(box("gray", "your data", "<code>tasks = [...]</code>", 0, "flex:1"), '<div class="arrow" data-step="0">keep in sync by hand 😩</div>',
       box("orange", "the real DOM", "every element to update, add, remove…", 0, "flex:1")),
   row(box("purple", "React", "describe the UI for the current data", 1, "flex:1"), '<div class="arrow" data-step="1">React works out the changes</div>',
       box("green", "the real DOM", "minimal updates, automatically", 1, "flex:1"))),
 "steps": [
  "Keeping the real DOM in sync with your data gets messy fast in a real app. Every time the data changes, you have to remember every element to update, add, or remove.",
  "That's exactly the problem React solves. You just describe what the UI should look like for the current data, and React works out the minimal DOM changes for you. We'll see how in module twenty two.",
 ]},

{"html": H("", "Events") + row(
   code("""function handleClick(event) {
  console.log(event.type);    // "click"
  console.log(event.target);  // what was clicked
}
§0 button.addEventListener("click", handleClick);
§0 button.removeEventListener("click", handleClick);
§2 form.addEventListener("submit", (e) => {
§2   e.preventDefault();       // don't reload the page
§2   addTask(form.elements.title.value.trim());
§2 });""", 28, style="flex:1"),
   table(["Event", "Fires when"], [
     (["<code>click</code>", "clicked (or Enter on a button)"], 1),
     (["<code>input</code>", "every keystroke"], 1),
     (["<code>change</code>", "value committed"], 1),
     (["<code>submit</code>", "form submitted"], 1),
     (["<code>keydown</code>", "<code>event.key</code> = \"Enter\"…"], 1),
     (["<code>scroll</code> / <code>resize</code>", "very often → debounce"], 1)], size=27), top=True),
 "steps": [
  "Events let you react to the user. Add event listener takes an event name and a function. The function gets an event object, with its type, and its target, the element that was actually clicked. To remove a listener, you need the very same function reference.",
  "These are the events you'll use most. Click. Input, which fires on every keystroke. Change, when a value is committed. Submit, on the form. Key down, where event dot key tells you which key. And scroll and resize, which fire so often you should debounce them.",
  "Prevent default stops the browser's built-in behaviour. On a form submit, it stops the page from reloading, so you can handle the data yourself. And avoid the old on click attribute in HTML. It mixes JavaScript into your markup.",
 ]},

{"html": H("Capturing and ", "bubbling") +
   chain(["window", "document", "body", "ul", "li", "button"], "#dbeafe", 0, "1 · capture ↓") +
   chain(["button"], "#fde68a", 1, "2 · target") +
   chain(["button", "li", "ul", "body", "document", "window"], "#dcfce7", 2, "3 · bubble ↑") +
   code("""§3 event.target          // where it started: the button
§3 event.currentTarget   // whose listener is running now
§3 event.stopPropagation();   // stop bubbling (use sparingly)""", 30, style="margin-top:34px"),
 "steps": [
  "When you click a button inside a list, the event travels in three phases. First, capturing. It travels down from the window, to the target.",
  "Then the target phase, at the clicked element itself.",
  "Then bubbling. It travels back up, to the window. Listeners run in the bubbling phase by default. So a click on the button also triggers click listeners on the l i, the u l, and the body.",
  "Event target is where the event started. Current target is the element whose listener is running right now. And stop propagation stops it bubbling further, but use that sparingly.",
 ]},

{"html": H("Event ", "delegation") + code("""document.querySelector("#tasks").addEventListener("click", (e) => {
  const button = e.target.closest("button.delete");
  if (!button) return;           // not a delete button
  button.closest("li").remove();
});""", 31) + row(box("green", "one listener", "instead of hundreds: less memory", 1, "flex:1"),
                  box("green", "works for new items", "no need to attach to every new li", 1, "flex:1"),
                  box("purple", "React does this", "one listener per event type at the root", 2, "flex:1"), style="margin-top:28px"),
 "steps": [
  "Event delegation uses bubbling. Instead of one listener per delete button, put one listener on the parent list. When a click bubbles up, closest checks if it came from a delete button. If not, return. If so, remove its l i.",
  "Why is that better? One listener instead of hundreds, so less memory. And it works for items added later, without attaching anything new.",
  "React itself uses delegation. It attaches one listener per event type at the root, and dispatches to your components.",
 ]},

{"html": H("Forms and ", "localStorage") + code("""§0 const data = Object.fromEntries(new FormData(form));   // { title, priority }
§0 if (!form.checkValidity()) return form.reportValidity();

§1 localStorage.setItem("tasks", JSON.stringify(tasks));   // strings only
§1 const saved = JSON.parse(localStorage.getItem("tasks") ?? "[]");""", 29) +
   table(["", "localStorage", "sessionStorage"], [
     (["Lasts", "until cleared", "until the tab closes"], 1),
     (["Shared", "all tabs of the site", "one tab"], 1),
     (["⚠️", "any script can read it", "→ never store passwords"], 2)], size=29),
 "steps": [
  "To read a whole form at once, pass it to form data, and turn that into a plain object. Check validity runs the browser's built-in validation.",
  "Web storage keeps small amounts of data in the browser, as strings. So stringify objects to save them, and parse them to read them back. Local storage lasts until it's cleared, and it's shared across tabs. Session storage lasts until the tab closes. This very tracker stores your progress in local storage.",
  "But remember, any script on the page can read it. So never store passwords there.",
 ]},

quiz([
  ("<code>textContent</code> vs <code>innerHTML</code>?", "textContent: plain text, <b style=\"display:inline\">safe</b> · innerHTML: parses HTML, XSS risk", "red",
   "Quiz time. Text content versus inner HTML?",
   "Text content sets plain text, and it's safe. Inner HTML parses HTML, which is an XSS risk with user input."),
  ("<code>event.target</code> vs <code>currentTarget</code>?", "where it started · whose listener is running", "blue",
   "Event target versus current target?",
   "Target is where the event started. Current target is the element whose listener is running."),
  ("What is event delegation?", "One listener on a parent, catching children's events by <b style=\"display:inline\">bubbling</b>", "green",
   "And what is event delegation?",
   "One listener on a parent, handling events from its children, thanks to bubbling."),
]),

recap(["<code>querySelector</code> takes any CSS selector · NodeList isn't an array",
       "textContent is safe · innerHTML + user input = XSS",
       "Toggle classes, keep styles in CSS",
       "Build many elements in a fragment, append once",
       "<code>preventDefault()</code> · events bubble up by default",
       "Delegation: one listener on the parent"],
  "Let's recap. Query selector takes any CSS selector, and a node list isn't a real array. Text content is safe, while inner HTML with user input is an XSS risk. Toggle classes and keep styles in CSS. Build many elements in a fragment, and append once. Prevent default stops the browser's behaviour, and events bubble up by default. And delegation means one listener on the parent. Next time: asynchronous JavaScript!"),
]
