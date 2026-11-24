from conc import *

TAG = "DSA · Kadane's Algorithm"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Kadanes Algorithm.mp4"
A = [-2, 1, -3, 4, -1, 2, 1, -5, 4]

SLIDES = [
title_slide(0, "Kadane's Algorithm", "The best subarray ending here: extend it, or start fresh",
  "Welcome. Today's concept: Kadane's algorithm.",
  "Find the contiguous subarray with the largest sum. Trying every subarray is quadratic or worse. Kadane's algorithm does it in one pass, with one decision per element. By the end you'll know that decision, why it's really dynamic programming, and how it stretches to circular arrays, products, and stock prices.",
  pill="DSA · CONCEPT"),

{"html": H("The maximum ", "subarray") +
   col(cells(A, None, None, 0, "the array", size=40),
       cells(A, 3, 6, 1, "4 − 1 + 2 + 1 = <b>6</b>", size=40), gap=20) +
   row(box("red", "brute force", "every start × every end → O(n²)", 2, "flex:1"),
       box("green", "Kadane", "one pass, O(n) time, O(1) space", 2, "flex:1"), style="margin-top:26px"),
 "steps": [
  "Here's the problem. An array with positive and negative numbers. Find the contiguous run with the largest sum.",
  "For this array, it's four, minus one, two, one. Total six. Notice it includes a negative number, because the elements on both sides more than make up for it.",
  "Brute force tries every start and every end, which is quadratic. Kadane does it in a single pass, with constant extra space.",
 ]},

{"html": H("One decision per ", "element") + row(
   col(box("purple", "cur", "best sum of a subarray that <b style=\"display:inline\">ends right here</b>", 0),
       box("blue", "the choice", "extend the previous run, or start fresh at <code>x</code>", 1),
       box("green", "best", "the largest <code>cur</code> seen anywhere", 2), gap=18, style="flex:1"),
   code("""§1 int cur = a[0], best = a[0];
§1 for (int i = 1; i < n; i++) {
§1   cur = Math.max(a[i], cur + a[i]);
§2   best = Math.max(best, cur);
§1 }""", 30, style="width:720px"), top=True) +
   note("A negative running sum only drags the future down → drop it", 3),
 "steps": [
  "Kadane keeps one number, cur: the best sum of a subarray that ends exactly at the current position.",
  "At each element there are only two options. Extend the best run that ended one step earlier, by adding this element. Or start a brand new run, containing just this element. Take whichever is bigger.",
  "Separately, best remembers the largest cur seen anywhere, because the answer can end at any position.",
  "The intuition: if the run so far has a negative sum, carrying it forward can only make every future sum smaller. So throw it away and start fresh.",
 ]},

{"html": H("Watch it ", "run") + table(["x", "−2", "1", "−3", "4", "−1", "2", "1", "−5", "4"], [
     (["<b>cur</b>", "−2", "1", "−2", "4", "3", "5", "6", "1", "5"], 0),
     (["<b>best</b>", "−2", "1", "1", "4", "4", "5", "<b>6</b>", "6", "6"], 1)], size=30) +
   row(box("orange", "at 1", "−2 + 1 = −1 &lt; 1 → <b style=\"display:inline\">start fresh</b>", 2, "flex:1"),
       box("orange", "at 4", "−2 + 4 = 2 &lt; 4 → <b style=\"display:inline\">start fresh</b>", 2, "flex:1"),
       box("blue", "at −1", "4 − 1 = 3 &gt; −1 → <b style=\"display:inline\">extend</b>", 2, "flex:1"), style="margin-top:26px"),
 "steps": [
  "Let's run it. cur starts at minus two. At one, extending gives minus one, but starting fresh gives one. So start fresh. At minus three, extending gives minus two, which beats minus three. At four, extending gives two, starting fresh gives four. Fresh again. Then minus one, two and one each extend: three, five, six.",
  "best follows the largest cur. It reaches six at the element one, and nothing later beats it.",
  "So the restarts happen exactly where the running sum went negative. And a negative element in the middle, like minus one, is kept, because the run before it is still worth carrying.",
 ]},

{"html": H("Why it works: it's ", "DP") + row(
   col(box("blue", "state", "<code>dp[i]</code> = best sum of a subarray ending at i", 0),
       box("green", "transition", "<code>dp[i] = max(a[i], dp[i−1] + a[i])</code>", 1),
       box("purple", "answer", "<code>max over all dp[i]</code>", 1),
       box("gray", "space", "only <code>dp[i−1]</code> is used → one variable", 2), gap=16, style="flex:1"),
   box("orange", "the 'reset to 0' version", "<code>cur = max(0, cur + x)</code> returns <b style=\"display:inline\">0</b> for an all-negative array · start from <code>a[0]</code> instead", 3, "width:560px"), top=True),
 "steps": [
  "Kadane is really dynamic programming. The state: dp of i is the best sum of a subarray that ends at i.",
  "Any subarray ending at i either is just a of i, or extends a subarray ending at i minus one. The best of those is dp of i minus one. That gives the transition. The answer is the largest dp value.",
  "Each step only looks one back, so the whole table collapses into a single variable. That's the same space trick as in every one dimensional DP.",
  "One trap. A popular version resets cur to zero whenever it goes negative. For an array of only negative numbers, that returns zero, which is wrong. The answer is the largest single element. Starting from a of zero avoids that.",
 ]},

{"html": H("Variations of the same ", "idea") + table(["Problem", "Twist"], [
     (["return the subarray itself", "remember where the current run <b>started</b>"], 0),
     (["circular array", "max(normal Kadane, total − <b>min</b> subarray)"], 1),
     (["maximum <b>product</b>", "track max <b>and</b> min: a negative flips them"], 2),
     (["buy and sell stock once", "Kadane on daily price <b>differences</b>"], 3)], size=31),
 "steps": [
  "Kadane has many cousins. To return the subarray, not just its sum, remember the index where the current run started. When best improves, save that start and the current end.",
  "In a circular array, the best run may wrap around the end. A wrapping run is the total minus the part it skips in the middle, so subtract the minimum subarray from the total. Take the better of that and normal Kadane. If every number is negative, use normal Kadane only.",
  "For the maximum product, a negative number turns the smallest product into the largest. So track both the current maximum and the current minimum, and swap their roles on a negative.",
  "And buy and sell a stock once is Kadane in disguise. The profit between two days is the sum of the daily changes in between. So run Kadane on the differences, or equivalently, track the cheapest price so far.",
 ]},

{"html": H("Circular: the ", "wrap-around") +
   col(cells([5, -3, 5], None, None, 0, "normal Kadane: 7", size=44),
       cells([5, -3, 5], None, None, 1, "7 − (−3) = <b>10</b>", size=44, mark={0: "#bbf7d0", 2: "#bbf7d0", 1: "#fecaca"}), gap=20) +
   note("The wrap-around run = everything except the worst middle part", 2),
 "steps": [
  "Here's the circular case. Five, minus three, five. Normal Kadane takes all three, sum seven.",
  "But in a circle, the last five is next to the first five. Skip the minus three, and you get ten. The total is seven, the minimum subarray is minus three, and seven minus minus three is ten.",
  "So the wrap around run is just everything except the worst stretch in the middle. That's one extra Kadane pass, looking for the minimum instead of the maximum.",
 ]},

{"html": H("Recognise it, avoid the ", "traps") + pts([
     ("“largest / smallest sum of a <b>contiguous</b> subarray” → Kadane", 0),
     ("subsequence, not contiguous? → just add all positives", 1),
     ("all negative → answer is the largest element, not 0", 2),
     ("product → keep max <b>and</b> min", 2),
     ("2D max rectangle → fix two rows, Kadane on column sums: O(rows² · cols)", 3)], size=34),
 "steps": [
  "When do you reach for it? Any question about the largest or smallest sum of a contiguous subarray.",
  "If the elements don't need to be contiguous, it's a subsequence, and the answer is just the sum of all positive numbers. No algorithm needed.",
  "Watch the all negative case, and remember products need both a maximum and a minimum.",
  "And it extends to two dimensions. For the largest sum rectangle in a matrix, fix a top row and a bottom row, add up each column between them, and run Kadane on those column sums.",
 ]},

quiz([
  ("What does cur mean?", "best sum of a run <b style=\"display:inline\">ending here</b>", "purple",
   "Quiz time. In Kadane's algorithm, what exactly does cur hold?",
   "The best sum of a subarray that ends at the current position."),
  ("All negative: [−3, −1, −2]?", "<b style=\"display:inline\">−1</b>, not 0", "red",
   "The array is minus three, minus one, minus two. What's the maximum subarray sum?",
   "Minus one. The subarray must be non-empty, so the answer is the largest element."),
  ("Max product subarray: what extra do you track?", "the running <b style=\"display:inline\">minimum</b>", "green",
   "For the maximum product subarray, what do you track besides the running maximum?",
   "The running minimum, because multiplying by a negative turns it into the maximum."),
]),

recap(["cur = best sum ending here · best = best anywhere",
       "cur = max(x, cur + x): extend or start fresh",
       "It's DP with one variable of state",
       "Start from a[0], not 0, for all-negative arrays",
       "Circular: max(Kadane, total − min subarray)",
       "Product: track max and min"],
  "Let's recap. Kadane keeps the best sum ending at the current position, and the best seen anywhere. At each element, extend the run or start fresh. It's dynamic programming with a single variable. Start from the first element so all-negative arrays work. For circular arrays, compare normal Kadane with the total minus the minimum subarray. And for products, track both the maximum and the minimum. Now practise the problems listed in your notes!"),
]
