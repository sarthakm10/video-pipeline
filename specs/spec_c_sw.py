from conc import *

TAG = "DSA · Sliding Window"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Sliding Window.mp4"
A = [2, 1, 5, 1, 3, 2]

SLIDES = [
title_slide(0, "Sliding Window", "Turn O(n·k) or O(n²) subarray work into one O(n) pass",
  "Welcome. Today's concept: the sliding window.",
  "It's one of the most common patterns for array and string questions. Instead of recomputing every subarray from scratch, you keep one window, and slide it. Add what enters on the right, remove what leaves on the left. By the end, you'll know what it is, why it's linear, when to use it, its three templates, and when it doesn't work.",
  pill="DSA · CONCEPT"),

{"html": H("The core ", "idea") + sub("Maximum sum of 3 consecutive elements") +
   col(cells(A, 0, 2, 0, "sum = 8"),
       cells(A, 1, 3, 1, "8 + 1 − 2 = 7"),
       cells(A, 2, 4, 2, "7 + 3 − 1 = <b>9</b>"),
       cells(A, 3, 5, 3, "9 + 2 − 5 = 6"), gap=18) +
   note("Each step: <u>+ the new element, − the old one</u> · O(1) per move", 4),
 "steps": [
  "Say you want the maximum sum of any three consecutive elements. Brute force adds up three numbers for every starting point. That's n times k work. Instead, start with the first window. Two, one, five. Sum eight.",
  "Now slide one step right. One enters, and two leaves. So the new sum is eight, plus one, minus two. Seven. We didn't re-add anything.",
  "Slide again. Three enters, one leaves. Nine. That's the best so far.",
  "And the last window. Two enters, five leaves. Six. So the answer is nine.",
  "That's the whole trick. Each move costs one addition, and one subtraction. Constant work per step, instead of re-summing the window.",
 ]},

{"html": H("Why it's always ", "O(n)") + row(
   col(box("blue", "two pointers", "<code>left</code> and <code>right</code> mark the window <code>[left, right]</code>", 0),
       box("green", "both only move forward", "never backwards", 1), gap=18, style="flex:1"),
   col(box("orange", "each element", "enters once · leaves at most once", 2),
       box("purple", "so the total work", "≤ 2n moves → <b style=\"display:inline\">O(n)</b>", 2), gap=18, style="flex:1"), top=True) +
   note("Even with a <code>while</code> inside the <code>for</code>, it's still linear", 3),
 "steps": [
  "A window is described by two indices. Left and right.",
  "And the key fact is, both only ever move forward. Right moves through the array once. Left follows behind it, and never goes back.",
  "So every element enters the window once, and leaves it at most once. That's at most two n pointer moves in total. Linear.",
  "This matters, because many window solutions have a while loop nested inside a for loop. It looks quadratic, but it isn't. The inner loop can only move left forward, and left can only travel n steps in the whole run.",
 ]},

{"html": H("When to ", "use it") + table(["Clue in the question", "Pattern"], [
     (["subarray / substring of <b>size k</b>", "fixed window"], 0),
     (["<b>longest</b> substring with at most / without …", "variable window, longest valid"], 1),
     (["<b>smallest</b> subarray with sum ≥ target", "variable window, shortest valid"], 1),
     (["contains all characters of … · anagram of …", "window + frequency counts"], 2),
     (["number of subarrays with <b>exactly</b> k …", "at most k, twice"], 2)], size=30) +
   note("First check: is it <u>contiguous</u>? Subsequences and subsets aren't windows", 3),
 "steps": [
  "How do you recognise a window problem? Listen for the clue words. A subarray or substring of size k means a fixed window.",
  "Longest substring with at most something, or without something, is a variable window looking for the longest valid one. Smallest subarray with a sum at least a target is a variable window looking for the shortest.",
  "Contains all characters, or anagram of, means a window plus a frequency count. And the number of subarrays with exactly k of something uses a trick we'll see in a minute.",
  "But the first question is always: does the problem want something contiguous? A window is a range of neighbours. If it says subsequence, or any subset, elements don't have to be next to each other. That's DP or backtracking, not a window.",
 ]},

{"html": H("The key property: ", "monotonicity") + row(
   box("green", "works ✅", "non-negative numbers, target sum ≥ 7<br>adding can only <b style=\"display:inline\">grow</b> the sum<br>→ if too big, shrinking is always right", 0, "flex:1"),
   box("red", "breaks ❌", "<code>[1, −1, 1]</code>, sum exactly 1<br>removing an element can <b style=\"display:inline\">increase</b> the sum<br>→ the window can't decide when to shrink", 1, "flex:1")) +
   note("Valid window → every smaller one valid too? Then you can slide greedily", 2),
 "steps": [
  "Variable windows rely on one property. Monotonicity. With non-negative numbers, adding an element can only increase the sum. So if the window's sum gets too big, shrinking from the left is always the right move. No choice to get wrong.",
  "Now take one, minus one, one, looking for subarrays that sum to exactly one. Removing the minus one makes the sum bigger. Removing a one makes it smaller. The window has no rule for when to shrink, so the greedy slide misses answers.",
  "So before using a variable window, ask: if a window is valid, is every smaller window valid too? Or if it's invalid, is every larger one invalid? If yes, slide away. If not, use prefix sums with a hash map instead.",
 ]},

{"html": H("Template 1: ", "fixed", " size") + code("""§0 for (int i = 0; i < n; i++) {
§0   add(a[i]);                          // enters on the right
§1   if (i >= k) remove(a[i - k]);       // leaves on the left
§2   if (i >= k - 1) record(answer);     // the window is full
§0 }""", 34) + cells(A, 3, 5, 1, "i = 5, k = 3 → leaves a[2]", style="margin-top:34px") +
   note("Start <code>best</code> at <u>Integer.MIN_VALUE</u>, not 0: all-negative input!", 3),
 "steps": [
  "Now the templates. First, the fixed size window. Loop with one index i. Every step, the element at i enters.",
  "Once i reaches k, the element k places behind leaves. For example at i equals five, with k three, a of two leaves, so the window is indexes three to five.",
  "And once i is at least k minus one, the window is full, so record the answer.",
  "One classic bug. If you start best at zero, and every number is negative, you return zero, which is wrong. Start at the smallest integer, or at the first full window's value.",
 ]},

{"html": H("Template 2: longest ", "valid") + code("""§0 int left = 0, best = 0;
§0 for (int right = 0; right < n; right++) {
§0   add(a[right]);                      // 1. always expand
§1   while (window is invalid) {         // 2. shrink until valid again
§1     remove(a[left]);
§1     left++;
§1   }
§2   best = Math.max(best, right - left + 1);   // 3. record AFTER the loop
§0 }""", 32) + note("Example: longest substring <u>without repeating characters</u>", 3),
 "steps": [
  "Template two finds the longest valid window. Right moves forward every iteration, and the new element always goes in. Expand first.",
  "If that made the window invalid, shrink from the left, removing elements, until it's valid again.",
  "Now the window is valid, so record its length. Right minus left, plus one. Notice the answer is recorded after the while loop, when the window is guaranteed valid.",
  "The classic example is the longest substring without repeating characters. Invalid means some character appears twice. Shrink until it doesn't.",
 ]},

{"html": H("Template 3: shortest ", "valid") + code("""§0 int left = 0, best = Integer.MAX_VALUE;
§0 for (int right = 0; right < n; right++) {
§0   add(a[right]);
§1   while (window is valid) {           // shrink WHILE it stays valid
§1     best = Math.min(best, right - left + 1);   // record INSIDE
§1     remove(a[left]);
§1     left++;
§1   }
§0 }""", 32) + table(["", "Longest valid", "Shortest valid"], [
     (["shrink while", "invalid", "valid"], 2),
     (["record", "after the loop", "inside the loop"], 2),
     (["start best at", "0", "MAX_VALUE"], 2)], size=28),
 "steps": [
  "Template three flips it, to find the shortest valid window. Like smallest subarray with a sum at least a target. Again, always expand.",
  "But now, shrink while the window is still valid, because each shrink might give a shorter answer. So record inside the loop, before removing.",
  "Here's the difference side by side. Longest shrinks while invalid, and records after the loop. Shortest shrinks while valid, and records inside the loop. And shortest starts at the largest integer. If it's still that at the end, there was no valid window at all.",
 ]},

{"html": H("Counting: the ", "at most K", " trick") + row(
   col(box("red", "exactly K", "not monotonic: growing can make it K+1, shrinking K−1", 0),
       box("green", "at most K", "monotonic ✅ · easy to slide", 1), gap=18, style="width:620px"),
   code("""§2 // for each right, after shrinking:
§2 count += right - left + 1;
§2 // = subarrays ending at right
§2 //   that start in [left, right]""", 28, style="flex:1"), top=True) +
   note("<span class=\"big\" style=\"font-size:54px;color:#16a34a\">exactly(K) = atMost(K) − atMost(K − 1)</span>", 3, "text-align:center;transform:none;margin-top:36px"),
 "steps": [
  "Some questions ask how many subarrays have exactly k distinct values. That's hard to slide. Grow the window, and you might reach k plus one. Shrink, and you might drop to k minus one. Not monotonic.",
  "But at most k is monotonic. A valid window stays valid when it shrinks. So that one slides easily.",
  "And counting is neat. For each right, once the window is valid, every subarray that ends at right, and starts anywhere from left to right, is valid too. That's right minus left plus one subarrays, added in one step.",
  "Then exactly k is just at most k, minus at most k minus one. Two easy windows, subtracted.",
 ]},

{"html": H("When it ", "fails") + row(
   box("red", "negative numbers + a sum target", "removing can raise the sum → use <b style=\"display:inline\">prefix sum + HashMap</b>", 0, "flex:1"),
   box("orange", "max / min of every window", "if the max leaves, which is next? → <b style=\"display:inline\">monotonic deque</b>", 1, "flex:1"),
   box("purple", "non-contiguous", "subsequence · any subset → <b style=\"display:inline\">DP / backtracking</b>", 2, "flex:1")) +
   pts([("Forgetting to delete zero-count keys from the map", 3), ("Window length is <code>right − left + 1</code>", 3),
        ("Use <code>long</code> when sums can overflow", 3)], size=32, style="margin-top:30px"),
 "steps": [
  "Knowing when not to use a window matters just as much. Negative numbers with a sum target break monotonicity, so use prefix sums and a hash map.",
  "The maximum of every window is another trap. A running sum is easy to update, but a maximum isn't. When the max leaves, which element is next? That needs a monotonic deque.",
  "And anything non-contiguous, like a subsequence, isn't a window at all. That's DP or backtracking.",
  "And three common bugs. When a count drops to zero, remove the key from the map, or its size is wrong. The window's length is right minus left plus one. And use long when sums can overflow.",
 ]},

quiz([
  ("Why is a window O(n) despite a nested <code>while</code>?", "each element enters once, <b style=\"display:inline\">leaves once</b>", "blue",
   "Quiz time. Why is a sliding window linear, even with a while loop inside the for loop?",
   "Because left and right only move forward, so each element enters once and leaves at most once."),
  ("Longest valid: where do you record?", "<b style=\"display:inline\">after</b> the shrink loop", "green",
   "In the longest valid template, where do you record the answer?",
   "After the shrink loop, when the window is valid again."),
  ("Subarrays summing to k, with negatives?", "<b style=\"display:inline\">prefix sum</b> + HashMap", "red",
   "Count subarrays that sum to k, when the array has negative numbers. Window or not?",
   "Not a window. Negatives break monotonicity, so use prefix sums with a hash map."),
]),

recap(["+ new element, − old element: O(1) per move",
       "Both pointers only move forward → O(n)",
       "Contiguous + monotonic → slide greedily",
       "Fixed · longest (record after) · shortest (record inside)",
       "exactly(K) = atMost(K) − atMost(K − 1)",
       "Negatives → prefix sums · window max → deque"],
  "Let's recap. A window adds the new element and removes the old one, so each move is constant work. Both pointers only move forward, so it's linear. Use it for contiguous problems where validity is monotonic. Three templates: fixed size, longest valid recording after the loop, and shortest valid recording inside it. Count exactly k as at most k minus at most k minus one. And when numbers are negative, use prefix sums, and for window maximums, a monotonic deque. Now practise the problems listed in your notes!"),
]
