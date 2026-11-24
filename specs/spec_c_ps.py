from conc import *

TAG = "DSA · Prefix Sum and Difference Array"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Prefix Sum and Difference Array.mp4"
A = [3, 1, 4, 1, 5, 9]
P = [0, 3, 4, 8, 9, 14, 23]

SLIDES = [
title_slide(0, "Prefix Sums", "Pay O(n) once, then answer every range sum in O(1)",
  "Welcome. Today's concept: prefix sums, and their mirror image, difference arrays.",
  "Whenever a question keeps asking for the sum of a range, adding it up each time costs linear time per question. A prefix sum array stores running totals once, and then any range sum is a single subtraction. By the end you'll know how to build one, the off by one trick, the prefix sum plus hash map pattern for counting subarrays, two dimensional prefix sums, and difference arrays for range updates.",
  pill="DSA · CONCEPT"),

{"html": H("Running ", "totals") +
   col(cells(A, None, None, 0, "a", size=44),
       cells(P, None, None, 1, "prefix p", size=44, mark={0: "#e5e7eb"}), gap=22) +
   code("""§1 int[] p = new int[n + 1];             // p[0] = 0
§1 for (int i = 0; i < n; i++) p[i + 1] = p[i] + a[i];""", 30, style="margin-top:24px") +
   note("One extra slot, <code>p[0] = 0</code>, removes every edge case", 2),
 "steps": [
  "Here's an array: three, one, four, one, five, nine.",
  "The prefix array stores running totals. p of i is the sum of the first i elements. So p of zero is zero, p of one is three, p of two is four, then eight, nine, fourteen, twenty three. Building it is one pass: each total is the previous total plus the next element.",
  "Notice the prefix array is one longer than the input, with a zero at the front. That extra slot means a range starting at index zero needs no special case. You'll see why in a second.",
 ]},

{"html": H("Any range sum in ", "O(1)") +
   col(cells(A, 2, 4, 0, "a[2..4] = 4 + 1 + 5 = 10", size=44),
       cells(P, None, None, 1, "p[5] − p[2] = <b>10</b>", size=44, mark={5: "#bbf7d0", 2: "#fecaca"}), gap=22) +
   box("blue", "the formula", "<code>sum(l..r) = p[r + 1] − p[l]</code> · everything up to r, minus everything before l", 2, "margin-top:26px") +
   note("Many queries on a fixed array → prefix sum", 3),
 "steps": [
  "Say we want the sum from index two to index four: four plus one plus five, which is ten.",
  "With the prefix array, take the total up to index four, that's p of five, fourteen. Subtract the total before index two, p of two, which is four. Fourteen minus four is ten. One subtraction, no loop.",
  "In general, the sum from l to r is p of r plus one, minus p of l. Everything up to r, minus everything before l. And for l equals zero, p of zero is zero, so the formula still works. That's the extra slot paying off.",
  "So whenever an array doesn't change and you're asked many range sums, build the prefix array once. Linear setup, then constant time per query.",
 ]},

{"html": H("Prefix sum + ", "HashMap") + sub("Count subarrays that sum to k") + row(
   col(box("purple", "the key idea", "a subarray ending here sums to k ⇔ an earlier prefix equals <code>sum − k</code>", 0),
       box("green", "so keep a map", "prefix value → how many times seen · start with <code>{0: 1}</code>", 1), gap=18, style="flex:1"),
   code("""§1 Map<Integer,Integer> seen = new HashMap<>();
§1 seen.put(0, 1);
§2 int sum = 0, count = 0;
§2 for (int x : a) {
§2   sum += x;
§2   count += seen.getOrDefault(sum - k, 0);
§2   seen.merge(sum, 1, Integer::sum);
§2 }""", 25, style="width:720px"), top=True) +
   note("Works with <u>negative numbers</u>, where a sliding window fails", 3),
 "steps": [
  "Now the most important pattern. Count the subarrays that add up to k. A subarray from i to j has sum p of j minus p of i. We want that to equal k. Rearranged: we want an earlier prefix equal to the current sum minus k.",
  "So walk once, keeping a running sum, and a hash map counting how often each prefix value has appeared. Start it with zero seen once, which stands for the empty prefix, so subarrays starting at index zero are counted.",
  "At each element, add how many times sum minus k has been seen, then record the current sum. That's linear time.",
  "And unlike a sliding window, this works with negative numbers. A window assumes that growing it only increases the sum. Prefix sums make no such assumption.",
 ]},

{"html": H("The same trick, other ", "keys") + table(["Question", "Store in the map"], [
     (["subarray sum = k", "prefix sum → count"], 0),
     (["sum divisible by k", "<code>((sum % k) + k) % k</code> → count"], 1),
     (["equal 0s and 1s (longest)", "treat 0 as −1 · prefix → <b>first index</b>"], 2),
     (["XOR of a range", "<code>px[r+1] ^ px[l]</code> · XOR undoes itself"], 3)], size=30) +
   note("Count → store counts · longest → store the first index you saw it", 2),
 "steps": [
  "The prefix plus map idea adapts to many questions by changing what you store. For a sum equal to k, store prefix sums and their counts.",
  "For sums divisible by k, two prefixes with the same remainder bracket a divisible subarray. So store remainders. In Java, fix negative remainders by adding k and taking the remainder again.",
  "For the longest subarray with equal zeros and ones, turn every zero into minus one. Now you want the longest subarray summing to zero. Since you want the longest, store the first index each prefix appeared, not a count.",
  "And prefix sums aren't only for addition. Prefix XOR works the same way, because XOR undoes itself. The XOR of a range is two prefix values XORed together.",
 ]},

{"html": H("Prefix and suffix ", "products") + sub("Product of everything except self, without division") +
   col(cells([1, 2, 3, 4], None, None, 0, "a", size=42),
       cells([1, 1, 2, 6], None, None, 1, "left: before i", size=42),
       cells([24, 12, 4, 1], None, None, 2, "right: after i", size=42),
       cells([24, 12, 8, 6], None, None, 3, "left × right", size=42, mark={0: "#bbf7d0", 1: "#bbf7d0", 2: "#bbf7d0", 3: "#bbf7d0"}), gap=14),
 "steps": [
  "Prefixes don't have to be sums. Here's a classic: for each position, the product of every other element, without using division.",
  "A left to right pass builds the product of everything before each position. One, one, two, six.",
  "A right to left pass builds the product of everything after it. Twenty four, twelve, four, one. That's a suffix product.",
  "Multiply them position by position, and you have the answer. Twenty four, twelve, eight, six. Two linear passes, and you can even reuse the output array to keep extra space constant.",
 ]},

{"html": H("2D prefix ", "sums") + row(
   col(box("blue", "build", "<code>P[i+1][j+1] = a[i][j] + P[i][j+1] + P[i+1][j] − P[i][j]</code>", 0),
       box("green", "query a rectangle", "big − top strip − left strip + the corner counted twice", 1),
       box("orange", "inclusion–exclusion", "subtract two overlapping regions → add their overlap back", 2), gap=18, style="flex:1"),
   code("""§1 sum = P[r2+1][c2+1]
§1     - P[r1][c2+1]
§1     - P[r2+1][c1]
§1     + P[r1][c1];""", 30, style="width:520px"), top=True),
 "steps": [
  "The same idea works on a grid. P of i, j holds the sum of the whole rectangle from the top left corner down to that cell. To build it, add the cell, the total above, and the total to the left. But the region above and to the left was added twice, so subtract it once.",
  "To get any rectangle's sum, take the big rectangle down to its bottom right corner. Subtract the strip above it and the strip to its left. The top left corner was subtracted twice, so add it back.",
  "That's inclusion exclusion. Whenever you subtract two overlapping regions, add their overlap back. After one pass to build, every rectangle query is four lookups.",
 ]},

{"html": H("Difference arrays: range ", "updates") + sub("Add 5 to a[1..3] and 2 to a[2..4], then read the array") +
   col(cells([0, 5, 0, 0, -5, 0], None, None, 0, "+5 on 1..3", size=42, mark={1: "#bbf7d0", 4: "#fecaca"}),
       cells([0, 5, 2, 0, -5, -2], None, None, 1, "+2 on 2..4", size=42, mark={2: "#bbf7d0", 5: "#fecaca"}),
       cells([0, 5, 7, 7, 2, 0], None, None, 2, "prefix sum of d", size=42), gap=16) +
   note("Each update O(1) · one prefix pass at the end", 3),
 "steps": [
  "Now the mirror image. Instead of many range queries, you have many range updates. Add five to positions one to three. Updating every cell costs linear time per update. A difference array marks only the edges: plus five where the range starts, and minus five just after it ends.",
  "Then add two to positions two to four. Plus two at index two, minus two at index five.",
  "When all updates are done, take one prefix sum of the difference array. The plus and minus marks spread out into exactly the right values: zero, five, seven, seven, two, zero.",
  "Each update is two writes, and one pass at the end rebuilds the array. That's how flight bookings, car pooling, and many scheduling questions are solved.",
 ]},

{"html": H("Which tool ", "when") + table(["Situation", "Tool"], [
     (["fixed array · many range sums", "prefix sum"], 0),
     (["count / longest subarray with a sum property", "prefix sum + HashMap"], 0),
     (["many range updates, read at the end", "difference array"], 1),
     (["updates <b>and</b> queries mixed together", "Fenwick tree / segment tree"], 2)], size=31) +
   pts([("Use <code>long</code> when sums can overflow <code>int</code>", 3), ("Index shift: <code>p</code> is one longer than <code>a</code>", 3),
        ("Seed the map with <code>{0: 1}</code> or <code>{0: -1}</code>", 3)], size=31, style="margin-top:22px"),
 "steps": [
  "To choose: a fixed array with many range sums, use a prefix sum. Counting or finding the longest subarray with some sum property, prefix sum plus a hash map.",
  "Many range updates that you only read at the end: a difference array.",
  "But if updates and queries are mixed together, both of these break, because one update would force a rebuild. That's when you need a Fenwick tree or a segment tree, which we cover in range queries.",
  "And three common bugs. Sums can overflow an int, so use long. Remember the prefix array is one longer, so the indices shift by one. And seed the map: zero with count one for counting, or zero at index minus one for longest length.",
 ]},

quiz([
  ("sum(l..r) using p?", "<code>p[r + 1] − p[l]</code>", "blue",
   "Quiz time. With a prefix array p, what's the sum from l to r?",
   "p of r plus one, minus p of l."),
  ("Subarray sum = k with negatives. Window or prefix?", "<b style=\"display:inline\">prefix sum + HashMap</b>", "purple",
   "Count subarrays that sum to k, and the array has negative numbers. Sliding window, or prefix sums?",
   "Prefix sums with a hash map. Negative numbers break the sliding window."),
  ("10,000 range additions, then print the array?", "<b style=\"display:inline\">difference array</b>", "green",
   "You get ten thousand range additions, and only then print the array. Which tool?",
   "A difference array. Each update is two writes, and one prefix pass at the end."),
]),

recap(["Prefix array: n + 1 slots, p[0] = 0",
       "Range sum = p[r + 1] − p[l], O(1)",
       "Prefix + HashMap counts subarrays, handles negatives",
       "Change the key: remainder, first index, XOR",
       "2D: inclusion–exclusion, four lookups",
       "Difference array: O(1) range update, one pass to read"],
  "Let's recap. A prefix array has one extra slot holding zero. Any range sum is then one subtraction. Prefix sums with a hash map count subarrays with a given sum, even with negative numbers, and changing the key handles remainders, longest lengths, and XOR. In two dimensions, inclusion exclusion gives any rectangle in four lookups. And a difference array turns each range update into two writes. Now practise the problems listed in your notes!"),
]
