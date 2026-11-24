from conc import *

TAG = "DSA · Monotonic Stack"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Monotonic Stack.mp4"
T = [73, 74, 75, 71, 69, 72, 76]


def stack(vals, step, label):
    return cells(vals or ["·"], None, None, step, label, size=36)


SLIDES = [
title_slide(0, "Monotonic Stack", "Keep the stack sorted; every pop answers a question",
  "Welcome. Today's concept: the monotonic stack.",
  "Questions like: for each day, how long until a warmer day? For each bar, how far can it stretch? Checking every pair is quadratic. A monotonic stack answers all of them in one pass, because every element is pushed once and popped once. By the end you'll know the idea, the four variants, why it's linear, and the famous applications: next greater element, daily temperatures, the largest rectangle in a histogram, and removing digits greedily.",
  pill="DSA · CONCEPT"),

{"html": H("The ", "idea") + row(
   col(box("blue", "the question", "for each element: the <b style=\"display:inline\">next greater</b> element to its right", 0),
       box("purple", "the stack", "holds elements still <b style=\"display:inline\">waiting</b> for their answer · kept decreasing", 1),
       box("green", "the pop", "a bigger element arrives → everyone smaller on top just found their answer", 2), gap=18, style="width:620px"),
   code("""§1 Deque<Integer> st = new ArrayDeque<>();
§1 for (int i = 0; i < n; i++) {
§2   while (!st.isEmpty() && a[st.peek()] < a[i])
§2     ans[st.pop()] = a[i];          // answered!
§1   st.push(i);
§1 }
§3 // left in the stack → no greater element (-1)""", 25, style="flex:1"), top=True),
 "steps": [
  "Here's the classic question. For each element, find the next greater element to its right.",
  "Walk left to right, and keep a stack of elements that are still waiting for their answer. Store indices, so you can write answers and measure distances.",
  "When a new element arrives, look at the top of the stack. If the top is smaller, the new element is the first greater thing to its right. That's its answer. Pop it, and keep popping while the top is smaller. Then push the new element, which now waits too.",
  "Because we pop everything smaller before pushing, the stack is always decreasing from bottom to top. That's why it's called monotonic. Anything left at the end never found a greater element.",
 ]},

{"html": H("Daily ", "temperatures") + sub("How many days until a warmer day?") +
   col(cells(T, None, None, 0, "temps", size=36),
       stack([75, 71, 69], 1, "stack after 69"),
       stack([75, 72], 2, "72: pops 69, 71"),
       stack([76], 3, "76: pops 72, 75"),
       cells([1, 1, 4, 2, 1, 1, 0], None, None, 4, "answer", size=36, mark={2: "#bbf7d0", 3: "#bbf7d0"}), gap=12),
 "steps": [
  "Let's watch it on daily temperatures. For each day, how many days until a warmer one?",
  "Seventy three is beaten by seventy four, which is beaten by seventy five. Then seventy one and sixty nine are both colder, so they stay on the stack. Seventy five, seventy one, sixty nine: decreasing.",
  "Seventy two arrives. It's warmer than sixty nine, which waited one day, and warmer than seventy one, which waited two days. Both pop. Seventy five is warmer, so it stays.",
  "Seventy six pops seventy two, after one day, and seventy five, after four days. The answer is the difference between the two indices.",
  "So every day gets its answer at the moment it's popped. Seventy six is never popped, so it gets zero.",
 ]},

{"html": H("Why it's ", "O(n)") + row(
   col(box("orange", "a while loop inside a for loop…", "looks like O(n²)", 0),
       box("green", "…but count pushes and pops", "each index is pushed <b style=\"display:inline\">once</b> and popped at most <b style=\"display:inline\">once</b>", 1),
       box("blue", "total", "≤ 2n stack operations → O(n) · amortised", 2), gap=18, style="flex:1"),
   box("purple", "what the pops prove", "a popped element can never be anyone's answer again: something bigger and closer now sits in front of it", 3, "width:600px"), top=True),
 "steps": [
  "A while loop inside a for loop looks quadratic. But don't count loop iterations, count what happens to each element.",
  "Each index is pushed exactly once, and it can be popped at most once. Once it's gone, it's gone.",
  "So across the whole run there are at most two n stack operations. That's linear, amortised over all the elements.",
  "And why is popping safe? Once a bigger element arrives, it's both closer and bigger than the popped one. For anything further right, the new element blocks the old one, so the old one can never be the answer again.",
 ]},

{"html": H("The four ", "variants") + table(["You want the…", "Stack order", "Pop when the top is…"], [
     (["next <b>greater</b>", "decreasing", "&lt; current"], 0),
     (["next <b>smaller</b>", "increasing", "&gt; current"], 1),
     (["previous greater / smaller", "same stacks", "answer = the top <b>after</b> popping"], 2),
     (["circular array", "loop <code>2n</code> times", "use <code>i % n</code>"], 3)], size=30) +
   note("Equal values? Decide <code>&lt;</code> vs <code>&lt;=</code>: it matters for duplicates", 3),
 "steps": [
  "There are four variants, and they're all the same loop. For next greater, keep the stack decreasing, and pop while the top is smaller.",
  "For next smaller, flip it: keep it increasing, and pop while the top is bigger.",
  "For previous greater or smaller, use the same stacks, but read the answer differently. After popping, whatever remains on top is the nearest element to the left that survived. That's the previous one.",
  "For a circular array, loop twice around, using i mod n, so elements near the end can find answers near the start. And with duplicates, decide whether equal values pop or not. Less than versus less or equal changes the answer.",
 ]},

{"html": H("Largest rectangle in a ", "histogram") + row(
   col(box("blue", "for each bar", "how far can a rectangle of <b style=\"display:inline\">its</b> height stretch?", 0),
       box("purple", "left and right limits", "the previous smaller bar · the next smaller bar", 1),
       box("green", "one increasing stack", "when a bar is popped, the current bar is its right limit, the new top its left limit", 2), gap=18, style="flex:1"),
   code("""§2 for (int i = 0; i <= n; i++) {
§2   int h = (i == n) ? 0 : heights[i];
§2   while (!st.isEmpty() && heights[st.peek()] > h) {
§2     int height = heights[st.pop()];
§2     int left = st.isEmpty() ? -1 : st.peek();
§2     best = Math.max(best, height * (i - left - 1));
§2   }
§2   st.push(i);
§2 }""", 24, style="width:800px"), top=True) +
   note("Maximal rectangle in a 0/1 matrix: run this on every row's heights", 3),
 "steps": [
  "The most famous application. In a histogram, find the largest rectangle. For each bar, imagine a rectangle exactly as tall as that bar. How wide can it get?",
  "It stretches left until a shorter bar blocks it, and right until a shorter bar blocks it. So we need the previous smaller and the next smaller bar for every position.",
  "One increasing stack gives both at once. When a bar is popped, the bar that popped it is its right limit, and the new top of the stack is its left limit. The width is the distance between them. A height zero sentinel at the end flushes out every remaining bar.",
  "And the maximal rectangle of ones in a matrix is this same algorithm, run once per row, where each column's height counts the ones stacked above it.",
 ]},

{"html": H("Greedy stacks: remove k ", "digits") + sub("Make 1432219 as small as possible by removing 3 digits") +
   col(cells([1, 4, 3, 2, 2, 1, 9], None, None, 0, "digits", size=36),
       stack([1, 3], 1, "3: pop 4 (k = 2)"),
       stack([1, 2], 2, "2: pop 3 (k = 1)"),
       stack([1, 2, 1, 9], 3, "1: pop 2 (k = 0)"), gap=14) +
   note("Result <b>1219</b>: a smaller digit early beats anything after it", 4),
 "steps": [
  "Monotonic stacks also power greedy problems. Remove three digits from one four three two two one nine, to make the smallest number.",
  "Keep an increasing stack of digits. One goes in, then four. Three arrives, and it's smaller than four. Replacing four with three makes the number smaller, so pop four. That uses one removal.",
  "Two arrives, smaller than three. Pop three. One removal left.",
  "Two is pushed. Then one is smaller than that two, so pop it, and the removals are used up. Everything else is kept.",
  "The result is one two one nine. The greedy reason: a smaller digit in an earlier position beats anything that comes after it. Remove duplicate letters uses the same stack, with an extra check that a letter appears again later.",
 ]},

{"html": H("Recognise the ", "pattern") + pts([
     ("“next / previous greater or smaller” → monotonic stack", 0),
     ("“how far can this element reach / stretch” → find both limits", 1),
     ("“sum of min/max over all subarrays” → each element's contribution = left × right reach", 2),
     ("sliding window maximum → the <b>deque</b> version", 3),
     ("store <b>indices</b>, not values: distances and answers need them", 3)], size=33),
 "steps": [
  "When should you think of it? The words next or previous, together with greater or smaller, are the clearest signal.",
  "Also any question about how far an element can reach before something blocks it, like the histogram.",
  "A clever one: the sum of the minimums of all subarrays. Instead of checking every subarray, ask for each element in how many subarrays it's the minimum. That's how far it reaches left, times how far it reaches right. Both come from monotonic stacks.",
  "If the window has a fixed size and slides, like the sliding window maximum, you need the deque version, covered in its own video. And always store indices on the stack, not values.",
 ]},

quiz([
  ("Next greater element: stack order?", "<b style=\"display:inline\">decreasing</b> (bottom → top)", "blue",
   "Quiz time. For the next greater element, is the stack increasing or decreasing?",
   "Decreasing. Anything smaller than the new element gets popped, and that new element is its answer."),
  ("Why is it O(n) with a nested while?", "each index pushed once, popped <b style=\"display:inline\">once</b>", "green",
   "There's a while loop inside a for loop. Why is it still linear?",
   "Each index is pushed once and popped at most once, so there are at most two n operations."),
  ("Histogram: a bar is popped. Its left limit?", "the new <b style=\"display:inline\">top</b> of the stack", "purple",
   "In the histogram algorithm, a bar is popped. Where is its left limit?",
   "The new top of the stack, which is the previous smaller bar."),
]),

recap(["Stack = elements still waiting for an answer",
       "Pop = that element just got its answer",
       "Pushed once, popped once → O(n)",
       "Greater → decreasing stack · smaller → increasing",
       "Histogram: popped bar's limits = current and new top",
       "Greedy digits: smaller digit earlier wins"],
  "Let's recap. A monotonic stack holds the elements still waiting for an answer. When one is popped, it just got its answer. Every element is pushed once and popped once, so it's linear. For next greater, keep the stack decreasing. For next smaller, increasing. In the histogram, a popped bar is limited by the current bar and the new top. And in greedy digit problems, a smaller digit earlier always wins. Now practise the problems listed in your notes!"),
]
