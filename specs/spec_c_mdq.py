from conc import *

TAG = "DSA · Monotonic Deque"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Monotonic Deque.mp4"

SLIDES = [
title_slide(0, "Monotonic Deque", "A queue kept in sorted order: the best of the window is always at the front",
  "Welcome. Today's concept: the monotonic deque.",
  "A monotonic stack answers questions about the next greater element. But some problems need the best value inside a window that keeps sliding. Old values must leave from one end, and new values arrive at the other. That needs a deque. By the end you'll know why a deque, sliding window maximum, tracking the max and the min together, shortest subarray with negatives, and how a deque speeds up dynamic programming.",
  pill="DSA · CONCEPT"),

{"html": H("Why a ", "deque") + row(
   col(box("blue", "a window slides", "new values enter on the <b style=\"display:inline\">right</b> · old values expire on the <b style=\"display:inline\">left</b>", 0),
       box("orange", "a stack can't do it", "it only touches one end · expired values would be stuck at the bottom", 1),
       box("green", "a deque can", "<code>pollLast</code> drops useless values · <code>pollFirst</code> drops expired ones", 2), gap=16, style="flex:1"),
   col(cells([4, 2, 3, 1, 5], 1, 3, 0, "window", size=40),
       cells([3, 1], None, None, 2, "deque", size=40), gap=22, style="width:760px"), top=True) +
   note("Keep it monotonic: values decreasing from front to back → front = window max", 3),
 "steps": [
  "Picture a window sliding over an array. Each step, one value enters on the right, and one value leaves on the left.",
  "A monotonic stack can't handle this. It only works at one end, so a value that falls out of the window would be stuck at the bottom.",
  "A deque works at both ends. From the back, we drop values that can never matter again. From the front, we drop values that have left the window.",
  "Keep the deque decreasing from front to back, and its front is always the maximum of the window.",
 ]},

{"html": H("Sliding window ", "maximum") + row(
   code("""§0 Deque<Integer> dq = new ArrayDeque<>();   // indices
§0 for (int i = 0; i < n; i++) {
§1   while (!dq.isEmpty() && nums[dq.peekLast()] <= nums[i])
§1     dq.pollLast();                        // can never be the max
§0   dq.offerLast(i);
§2   if (dq.peekFirst() <= i - k) dq.pollFirst();   // expired
§3   if (i >= k - 1) ans[i - k + 1] = nums[dq.peekFirst()];
§0 }""", 25, style="flex:1"),
   table(["i", "deque (values)", "max"], [
     (["0", "4", "—"], 0), (["1", "4, 2", "—"], 1), (["2", "4, 3", "4"], 1),
     (["3", "3, 1", "3"], 2), (["4", "5", "5"], 3)], size=27), top=True) +
   note("Every index enters once and leaves once → <b style=\"display:inline\">O(n)</b>, not O(n·k)", 4),
 "steps": [
  "Here's the core loop, for windows of size k, on four, two, three, one, five, with k equal to three. The deque stores indices, not values, so we can tell when one has expired.",
  "Before adding a new value, pop smaller values off the back. A smaller, older value can never be the maximum again, because the new one is bigger and stays longer. So when three arrives, two is dropped.",
  "Then check the front. If its index has left the window, poll it. At index three, the four expires.",
  "Once the first full window is reached, the front is the answer. So the maxima are four, three and five.",
  "Each index is pushed once and popped at most once, so the whole thing is linear, no matter how big k is.",
 ]},

{"html": H("Max and min ", "together") + sub("Longest subarray where max − min ≤ limit") + row(
   col(box("blue", "two deques", "<code>maxDq</code> decreasing · <code>minDq</code> increasing", 0),
       box("orange", "grow right", "add <code>nums[r]</code> to both", 0),
       box("red", "shrink left", "while <code>max − min &gt; limit</code>: move <code>l</code>, drop expired fronts", 1),
       box("green", "answer", "<code>r − l + 1</code> after every step", 2), gap=14, style="width:640px"),
   code("""§0 for (int r = 0; r < n; r++) {
§0   while (!maxDq.isEmpty() && maxDq.peekLast() < nums[r]) maxDq.pollLast();
§0   while (!minDq.isEmpty() && minDq.peekLast() > nums[r]) minDq.pollLast();
§0   maxDq.offerLast(nums[r]); minDq.offerLast(nums[r]);
§1   while (maxDq.peekFirst() - minDq.peekFirst() > limit) {
§1     if (maxDq.peekFirst() == nums[l]) maxDq.pollFirst();
§1     if (minDq.peekFirst() == nums[l]) minDq.pollFirst();
§1     l++;
§1   }
§2   best = Math.max(best, r - l + 1);
§0 }""", 21, style="flex:1"), top=True),
 "steps": [
  "Some windows need both the maximum and the minimum. Keep two deques: one decreasing for the max, one increasing for the min. Every new value goes into both.",
  "This window has no fixed size. When the max minus the min is too big, shrink from the left. If the value leaving is at the front of either deque, drop it there too. Here the deques store values, so equal values are kept with the strict comparison, and each copy leaves once.",
  "After each step the window is valid, so its length is a candidate answer. Still linear time.",
 ]},

{"html": H("Shortest subarray with sum ≥ K, with ", "negatives") + (
   col(box("red", "sliding window fails", "a negative number means growing the window can <b style=\"display:inline\">shrink</b> the sum", 0),
       box("blue", "use prefix sums", "sum(i..j) = <code>P[j+1] − P[i]</code> · want it ≥ K, with <code>j</code> close to <code>i</code>", 1),
       box("green", "front: use it", "while <code>P[j] − P[front] ≥ K</code>: record, poll front (it can't do better)", 2),
       box("purple", "back: drop it", "while <code>P[back] ≥ P[j]</code>: poll back (a later, smaller start is better)", 3), gap=14, style="flex:1")
   ) + note("Increasing deque of prefix-sum indices · O(n)", 4),
 "steps": [
  "Shortest subarray with a sum of at least K looks like a sliding window problem. But with negative numbers, the usual window breaks: adding an element can make the sum smaller, so you can't know when to shrink.",
  "Switch to prefix sums. The sum of a subarray is the difference of two prefix sums. We want a difference of at least K, with the two indices as close as possible.",
  "Keep a deque of prefix indices. When the current prefix minus the front's prefix reaches K, that's a candidate. Record it and poll the front, because any later end would only be longer.",
  "From the back, drop any prefix that's greater than or equal to the current one. The current index is a later start with a smaller prefix, so it's always at least as good.",
  "So the deque holds increasing prefix sums, and the whole thing is linear.",
 ]},

{"html": H("Deque-optimised ", "DP") + sub("dp[i] = nums[i] + max(dp[i−k] … dp[i−1])") + row(
   col(box("red", "naive", "look back over k values for every i → <b style=\"display:inline\">O(n·k)</b>", 0),
       box("green", "the max of a sliding window", "of <code>dp</code> values → the deque from before → <b style=\"display:inline\">O(n)</b>", 1),
       box("blue", "the recipe", "a DP that takes the best of the last k states", 2), gap=16, style="width:680px"),
   code("""§1 dp[0] = nums[0]; dq.offerLast(0);
§1 for (int i = 1; i < n; i++) {
§1   if (dq.peekFirst() < i - k) dq.pollFirst();
§1   dp[i] = nums[i] + dp[dq.peekFirst()];
§1   while (!dq.isEmpty() && dp[dq.peekLast()] <= dp[i]) dq.pollLast();
§1   dq.offerLast(i);
§1 }""", 24, style="flex:1"), top=True) +
   note("Jump Game VI · Constrained Subsequence Sum", 3),
 "steps": [
  "The deque also speeds up dynamic programming. Suppose each state is its own value plus the best of the previous k states. Looking back over k states every time costs n times k.",
  "But the best of the previous k states is just the maximum of a sliding window over the dp array. So keep the same deque, over dp values instead of input values. Each state is now constant time on average.",
  "Look for that shape: a recurrence that takes the max or min of the last k states.",
  "That's jump game six and constrained subsequence sum.",
 ]},

{"html": H("Stack or deque? And the ", "traps") + table(["Question", "Tool"], [
     (["next greater / smaller element, spans", "<b>monotonic stack</b>"], 0),
     (["max / min of a <b>sliding</b> window", "<b>monotonic deque</b>"], 0),
     (["best of the last k DP states", "<b>monotonic deque</b>"], 0)], size=29) + pts([
     ("store <b style=\"display:inline\">indices</b> when you need to know what expired", 1),
     ("<code>&lt;</code> vs <code>&lt;=</code> when popping: decide how duplicates behave", 1),
     ("use <code>ArrayDeque</code>: <code>offerLast</code>, <code>pollFirst</code>, <code>peekFirst</code> · not <code>Stack</code>", 2)], size=31),
 "steps": [
  "When to choose which? Next greater or smaller element problems use a monotonic stack. Anything about the best value in a sliding window, including DP over the last k states, uses a monotonic deque.",
  "Two common bugs. Store indices, or you can't tell when a value has left the window. And decide carefully between strict and non strict comparison when popping, because that controls what happens with equal values.",
  "In Java, use array deque, with offer last, poll first and peek first. Avoid the old stack class and linked list.",
 ]},

quiz([
  ("Sliding window max: what's at the front?", "the index of the window <b style=\"display:inline\">maximum</b>", "blue",
   "Quiz time. In sliding window maximum, what's at the front of the deque?",
   "The index of the current window's maximum."),
  ("Why pop smaller values off the back?", "they can <b style=\"display:inline\">never</b> be the max again", "green",
   "Why do we pop smaller values off the back before adding a new one?",
   "Because the new value is bigger and stays longer, so they can never be the maximum again."),
  ("Total cost for n elements?", "<b style=\"display:inline\">O(n)</b>: each in once, out once", "purple",
   "What's the total cost for n elements?",
   "Linear. Every index enters once and leaves at most once."),
]),

recap(["Deque: drop useless from the back, expired from the front",
       "Decreasing deque → front = window max",
       "Store indices to detect expiry",
       "Max and min together: two deques",
       "Negatives: deque over prefix sums",
       "DP over the last k states → deque → O(n)"],
  "Let's recap. A monotonic deque drops useless values from the back and expired values from the front. Kept decreasing, its front is the window maximum. Store indices so you know when one expires. For max and min together, use two deques. With negative numbers, run the deque over prefix sums. And a DP that takes the best of the last k states becomes linear with a deque. Now practise the problems listed in your notes!"),
]
