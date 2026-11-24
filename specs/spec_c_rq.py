from conc import *

TAG = "DSA · Range Query Structures"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Range Query Structures.mp4"

SLIDES = [
title_slide(0, "Range Queries", "Fenwick trees, lazy segment trees and sparse tables: sums and minimums over any range, fast",
  "Welcome. Today's concept: range query structures.",
  "Prefix sums answer range sums in constant time, but only while the array never changes. Once values update, or whole ranges change at once, you need something smarter. By the end you'll know how to choose a structure, the Fenwick tree and its one magic expression, its variants, segment trees with lazy propagation for range updates, and the sparse table for constant time minimums.",
  pill="DSA · CONCEPT"),

{"html": H("Choosing a ", "structure") + table(["Situation", "Use", "Query", "Update"], [
     (["array never changes · sums", "<b>prefix sums</b>", "O(1)", "rebuild O(n)"], 0),
     (["point updates · sums", "<b>Fenwick tree</b>", "O(log n)", "O(log n)"], 1),
     (["range updates · range queries", "<b>segment tree + lazy</b>", "O(log n)", "O(log n)"], 2),
     (["never changes · min / max", "<b>sparse table</b>", "<b>O(1)</b>", "—"], 3)], size=29) +
   note("Ask two questions: does it change? and is the operation sum, or min/max?", 4),
 "steps": [
  "Start by asking what you need. If the array never changes, prefix sums answer any range sum in constant time.",
  "If single values change between queries, a Fenwick tree does both in log n, with very little code.",
  "If whole ranges change at once, like add five to everything from index three to nine, use a segment tree with lazy propagation.",
  "And if the array never changes but you need range minimums or maximums, a sparse table answers in constant time.",
  "So two questions decide it: does the data change, and what operation are you combining?",
 ]},

{"html": H("Fenwick tree: the ", "idea") + row(
   table(["i", "binary", "i & −i", "tree[i] covers"], [
     (["1", "0001", "1", "[1, 1]"], 0), (["2", "0010", "2", "[1, 2]"], 0),
     (["3", "0011", "1", "[3, 3]"], 0), (["4", "0100", "4", "[1, 4]"], 0),
     (["6", "0110", "2", "[5, 6]"], 1), (["8", "1000", "8", "[1, 8]"], 1)], size=27),
   col(box("blue", "lowest set bit", "<code>i & -i</code> · how far back <code>tree[i]</code> reaches", 0),
       box("green", "query(7)", "<code>tree[7] + tree[6] + tree[4]</code> · strip the low bit each time", 2),
       box("orange", "1-indexed", "index 0 has no low bit · shift everything by one", 3), gap=16, style="width:640px"), top=True),
 "steps": [
  "A Fenwick tree, or binary indexed tree, is just an array. Each slot stores the sum of a block that ends at that index. The block's length is the lowest set bit of the index, written i and minus i.",
  "So slot six, binary one one zero, covers two values: five and six. Slot eight covers all eight.",
  "To get the prefix sum up to seven, add slot seven, then strip its lowest bit to reach six, then strip again to reach four. Three slots, and you have one to seven. That's log n steps.",
  "It must be one indexed, because zero has no lowest set bit, and the loop would never move.",
 ]},

{"html": H("Fenwick in ", "code") + code("""§0 void update(int i, int delta) {          // a[i] += delta
§0   for (; i <= n; i += i & -i) tree[i] += delta;
§0 }
§1 int query(int i) {                        // sum of a[1..i]
§1   int s = 0;
§1   for (; i > 0; i -= i & -i) s += tree[i];
§1   return s;
§1 }
§2 int rangeSum(int l, int r) { return query(r) - query(l - 1); }""", 28) +
   row(box("purple", "set a value", "update with <code>new − old</code>", 3, "flex:1"),
       box("green", "build", "n updates: O(n log n)", 3, "flex:1"), style="margin-top:20px"),
 "steps": [
  "Update adds a change to every slot whose block contains i. Adding the lowest set bit jumps to the next such slot.",
  "Query is the mirror image: subtract the lowest set bit to walk down through the blocks that make up the prefix.",
  "A range sum is two prefix queries subtracted.",
  "To set a value instead of adding to it, update with the difference between the new and old values. And build by updating once per element.",
 ]},

{"html": H("Fenwick ", "variants") + row(
   box("blue", "range update, point query", "Fenwick over a <b style=\"display:inline\">difference array</b> · add to l, subtract after r · value = prefix sum", 0, "flex:1"),
   box("purple", "range update, range sum", "two Fenwick trees · a known formula combines them", 1, "flex:1"),
   box("green", "count smaller after self", "compress values to ranks · scan right to left · <code>query(rank − 1)</code>, then <code>update(rank, 1)</code>", 2, "flex:1"), top=True) +
   note("A Fenwick tree over <b style=\"display:inline\">value ranks</b> counts \"how many seen so far are smaller\"", 3),
 "steps": [
  "Fenwick trees bend to other jobs. To add a value to a whole range and read single points, store a difference array in the tree. Add at the left end, subtract just after the right end, and a point's value is the prefix sum.",
  "Range updates with range sums need two trees combined by a formula. It's in your notes, and rarely needed in interviews.",
  "The most famous trick: count smaller numbers after each element. Replace values by their rank in sorted order. Scan from the right. For each value, ask how many smaller ranks are already in the tree, then add this one.",
  "So a Fenwick tree indexed by value, rather than position, counts how many smaller elements you've seen. Inversion counting works the same way.",
 ]},

{"html": H("Segment trees and lazy ", "propagation") + row(
   graph({"[0,7]": (330, 60), "[0,3]": (170, 180), "[4,7]": (490, 180), "[0,1]": (90, 300), "[2,3]": (250, 300), "[4,5]": (410, 300), "[6,7]": (570, 300)},
         [("[0,7]", "[0,3]"), ("[0,7]", "[4,7]"), ("[0,3]", "[0,1]"), ("[0,3]", "[2,3]"), ("[4,7]", "[4,5]"), ("[4,7]", "[6,7]")],
         w=660, h=360, r=46, step=0, colors={"[4,7]": ("#fde68a", "#d97706")}),
   col(box("blue", "each node = one range", "children split it in half · array of size <code>4n</code> · sum, min, max, gcd", 0),
       box("orange", "range update without lazy", "touches every leaf in the range → O(n)", 1),
       box("green", "lazy", "fully covered node: update it, store a <b style=\"display:inline\">pending tag</b>, stop · push the tag down only when you visit its children", 2), gap=16, style="flex:1"), top=True),
 "steps": [
  "A segment tree stores a value for every range in a halving tree. The root covers everything, and each child covers half of its parent. Stored in an array of size four n, it answers queries and point updates in log n, for sums, minimums, maximums, or anything that combines.",
  "But adding to a whole range would touch every leaf in it, which is linear.",
  "Lazy propagation fixes that. When a node's range is fully inside the update, update the node's own value, leave a pending tag saying add five to my children, and stop. The tag is pushed down only when a later operation needs to go below that node. Range updates are now log n too.",
 ]},

{"html": H("Sparse table: O(1) range ", "minimum") + row(
   col(box("blue", "precompute", "<code>st[k][i]</code> = min of the 2<sup>k</sup> values starting at <code>i</code> · O(n log n)", 0),
       box("green", "query [l, r]", "pick the largest <code>2<sup>k</sup> ≤ length</code> · min of two blocks that <b style=\"display:inline\">overlap</b>", 1),
       box("red", "limits", "no updates · overlap is fine for min, max, gcd, <b style=\"display:inline\">not</b> sum", 2), gap=16, style="flex:1"),
   col(cells([5, 2, 7, 3, 6, 1, 4], 0, 3, 1, "block 1", size=34),
       cells([5, 2, 7, 3, 6, 1, 4], 2, 5, 1, "block 2", size=34),
       note("min[0..5] = min(2, 1) = 1", 1, "margin-top:6px"), gap=12, style="width:780px"), top=True),
 "steps": [
  "A sparse table precomputes the minimum of every block whose length is a power of two, starting at every index. Each level is built from two halves of the level below.",
  "To answer a range, take the largest power of two that fits, and combine two blocks: one starting at the left end, one ending at the right end. They may overlap, and that's fine, because counting a value twice doesn't change a minimum. Constant time.",
  "That's also its limit. It can't handle updates, and the overlap trick only works for operations like min, max and gcd, not for sums.",
 ]},

quiz([
  ("What does <code>i & -i</code> give?", "the <b style=\"display:inline\">lowest set bit</b> of i", "blue",
   "Quiz time. In a Fenwick tree, what does i and minus i give you?",
   "The lowest set bit of i, which is the length of the block that slot covers."),
  ("Add 5 to a[3..9], then query sums?", "segment tree with <b style=\"display:inline\">lazy</b> propagation", "orange",
   "You need to add five to a whole range, then query sums. Which structure?",
   "A segment tree with lazy propagation."),
  ("Why can't a sparse table do sums in O(1)?", "the two blocks <b style=\"display:inline\">overlap</b>: sums would double-count", "red",
   "Why can't a sparse table answer range sums in constant time?",
   "Because its two blocks overlap, and a sum would count the middle twice."),
]),

recap(["Static sums → prefix sums",
       "Point update + sum → Fenwick (i & -i, 1-indexed)",
       "Fenwick over ranks → count smaller elements",
       "Range update → segment tree + lazy tags",
       "Static min/max → sparse table, O(1)",
       "Watch: 1-indexing · long overflow · size 4n"],
  "Let's recap. For static sums, prefix sums are enough. Point updates with range sums call for a Fenwick tree, built on the lowest set bit and indexed from one. A Fenwick tree over value ranks counts smaller elements. Range updates need a segment tree with lazy tags. And static range minimums come from a sparse table in constant time. Watch for one indexing, overflow, and the four n size. Now practise the problems listed in your notes!"),
]
