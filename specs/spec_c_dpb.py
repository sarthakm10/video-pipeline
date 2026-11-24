from conc import *

TAG = "DSA · Dynamic Programming, Part 2"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Dynamic Programming (Part 2).mp4"
LIS = [10, 9, 2, 5, 3, 7, 101, 18]

SLIDES = [
title_slide(0, "Dynamic Programming", "Part 2: grids, subsequences, strings, intervals, trees and states",
  "Welcome to part two of dynamic programming.",
  "In part one we built the method: find the state, write the transition, set the base cases, choose the order. Then we used it on take or skip, and knapsack. Today we apply the same method to the other big families: grids, increasing subsequences, two strings, intervals, trees, bitmasks, and state machines. Each family has a recognisable state. Once you can spot it, the code almost writes itself.",
  pill="DSA · CONCEPT · PART 2"),

{"html": H("Family 3: ", "grids") + sub("How many paths from the top-left to the bottom-right, moving only right or down?") + row(
   col(cells([1, 1, 1], None, None, 0, "row 0", size=44),
       cells([1, 2, 3], None, None, 1, "row 1", size=44, mark={1: "#fde68a", 2: "#fde68a"}),
       cells([1, 3, 6], None, None, 2, "row 2", size=44, mark={2: "#bbf7d0"}), gap=14),
   code("""§0 dp[0][*] = dp[*][0] = 1;   // one way along an edge
§1 dp[r][c] = dp[r-1][c]       // from above
§1          + dp[r][c-1];      // from the left""", 30, style="flex:1"), top=True) +
   note("State = a cell · transition = the cells you can <u>arrive from</u>", 3),
 "steps": [
  "Family three: grids. How many paths go from the top-left corner to the bottom-right, if you can only move right or down? The first row and the first column have exactly one path each. You can only walk straight along the edge.",
  "Every other cell can only be reached from the cell above, or the cell to its left. So its count is the sum of those two. One plus one is two. Two plus one is three.",
  "Fill row by row, and the corner holds six. Six paths in a three by three grid.",
  "That's the shape of all grid DP. The state is a cell. The transition looks at the cells you could have arrived from. Add obstacles, and a blocked cell is just zero. Ask for the cheapest path, and the plus becomes a min. Same table, different combine.",
 ]},

{"html": H("Family 4: increasing ", "subsequences") + sub("Longest strictly increasing subsequence (not necessarily contiguous)") +
   col(cells(LIS, None, None, 0, "a", size=38),
       cells([1, 1, 1, 2, 2, 3, 4, 4], None, None, 1, "dp[i]", size=38, mark={6: "#bbf7d0", 7: "#bbf7d0"}), gap=14) +
   code("""§1 dp[i] = 1 + max(dp[j])  for every j < i with a[j] < a[i]
§2 answer = max over all dp[i]          // not dp[n-1]!""", 30, style="margin-top:26px"),
 "steps": [
  "Family four: subsequences. Find the longest strictly increasing subsequence. The elements don't have to be next to each other, so this isn't a sliding window.",
  "The state: dp of i is the length of the longest increasing subsequence that ends exactly at i. To compute it, look at every earlier element that's smaller, and extend the best of them by one. Seven can extend two, five, which has length two, so seven gets three. One hundred and one extends that to four.",
  "One trap: the answer is the maximum over all positions, not the last cell, because the best subsequence can end anywhere. This version is n squared.",
 ]},

{"html": H("LIS in ", "O(n log n)") + sub("Keep tails[k] = the smallest possible tail of an increasing run of length k+1") +
   col(cells([2, 5], None, None, 0, "after 2, 5", size=38),
       cells([2, 3], None, None, 1, "3 replaces 5", size=38, mark={1: "#fde68a"}),
       cells([2, 3, 7, 101], None, None, 2, "7, 101 extend", size=38),
       cells([2, 3, 7, 18], None, None, 3, "18 replaces 101", size=38, mark={3: "#fde68a"}), gap=14) +
   note("Binary search the first tail ≥ x · <u>length</u> is right, the contents aren't an actual LIS", 4),
 "steps": [
  "There's a faster version, worth knowing for interviews. Keep an array called tails. tails of k is the smallest number that can end an increasing run of length k plus one. After two and five, tails is two, five.",
  "Then three arrives. It can't extend five, but it can replace it. A run of length two ending in three is better than one ending in five, because more numbers can follow it.",
  "Seven extends the array, and so does a hundred and one.",
  "Then eighteen replaces a hundred and one, for the same reason.",
  "For each number, binary search the first tail that's greater or equal, and replace it, or append if there's none. That's n log n. One warning: the length of tails is the answer, but its contents are not necessarily a real subsequence.",
 ]},

{"html": H("Family 5: two ", "strings") + row(
   col(box("blue", "state", "<code>dp[i][j]</code> = answer for the first <b style=\"display:inline\">i</b> chars of s and the first <b style=\"display:inline\">j</b> chars of t", 0),
       box("gray", "base", "an empty string: row 0 and column 0", 0), gap=18, style="width:620px"),
   col(code("""§1 // longest common subsequence
§1 if (s[i-1] == t[j-1]) dp[i][j] = dp[i-1][j-1] + 1;
§1 else dp[i][j] = max(dp[i-1][j], dp[i][j-1]);""", 26),
       code("""§2 // edit distance
§2 if (s[i-1] == t[j-1]) dp[i][j] = dp[i-1][j-1];
§2 else dp[i][j] = 1 + min(dp[i-1][j],     // delete
§2                         dp[i][j-1],     // insert
§2                         dp[i-1][j-1]);  // replace""", 26), gap=18, style="flex:1"), top=True) +
   note("Match → <u>diagonal</u> · no match → choose among the neighbours", 3),
 "steps": [
  "Family five: two strings. The state is almost always the same. dp of i, j is the answer for the first i characters of one string, and the first j of the other. Row zero and column zero mean an empty string, and those are the base cases.",
  "Longest common subsequence. If the last characters match, they extend the answer for both strings without them. That's the diagonal, plus one. If they don't match, drop one character from either string, and take the better result.",
  "Edit distance asks for the fewest inserts, deletes and replacements to turn one string into the other. If the characters match, it's free: take the diagonal. Otherwise pay one, plus the best of delete, insert, or replace. Each neighbour in the table is one of those operations.",
  "So the pattern is: on a match, go diagonal. On a mismatch, choose among the neighbours. Palindrome problems are the same idea, with a string compared against its own reverse, or a range i to j.",
 ]},

{"html": H("Family 6: ", "intervals") + row(
   col(box("blue", "state", "<code>dp[i][j]</code> = best answer for the range <code>i..j</code>", 0),
       box("orange", "order", "by <b style=\"display:inline\">length</b>: short ranges before the long ones that need them", 1),
       box("purple", "transition", "try every split point <code>k</code> inside the range", 1), gap=18, style="width:640px"),
   code("""§1 for (int len = 2; len <= n; len++)
§1   for (int i = 0; i + len - 1 < n; i++) {
§1     int j = i + len - 1;
§1     for (int k = i; k < j; k++)
§1       dp[i][j] = best(dp[i][j],
§1                   dp[i][k] + dp[k+1][j] + cost(i, k, j));
§1   }""", 26, style="flex:1"), top=True) +
   note("Burst balloons: think about which one bursts <u>last</u>, not first", 2),
 "steps": [
  "Family six: intervals. When the answer for a range depends on how you split it, the state is a range, i to j.",
  "Fill by length, shortest first, because a long range is built from shorter ones. For each range, try every split point k, and combine the two sides plus the cost of joining them. That's three nested loops, so cubic time. Matrix chain multiplication is the classic example.",
  "The famous trick is burst balloons. Choosing the first balloon to burst breaks the problem, because the neighbours change. Instead, choose which balloon bursts last in the range. Its neighbours are then fixed, the range edges, and the two sides become independent.",
 ]},

{"html": H("Family 7 and 8: ", "trees", " and bitmasks") + row(
   col(box("green", "DP on trees", "post-order: each node returns a <b style=\"display:inline\">small tuple</b> to its parent", 0),
       code("""§0 // house robber III: {robThis, skipThis}
§0 int[] go(Node n) {
§0   if (n == null) return new int[]{0, 0};
§0   int[] l = go(n.left), r = go(n.right);
§0   int rob  = n.val + l[1] + r[1];
§0   int skip = max(l) + max(r);
§0   return new int[]{rob, skip};
§0 }""", 24), gap=16, style="flex:1"),
   col(box("purple", "bitmask DP", "state includes a <b style=\"display:inline\">set</b> as bits: <code>mask</code> = which items are used", 1),
       box("gray", "travelling salesman", "<code>dp[mask][last]</code> · O(2ⁿ · n²) · only for n ≤ ~20", 1),
       note("Small n (≤ 20) and \"visit all\" → bitmask", 2, "margin-top:10px"), gap=16, style="width:640px"), top=True),
 "steps": [
  "Two less common families. DP on trees. Do a post-order traversal, so children are solved before their parent. Each node returns a small tuple. In house robber three, a node returns two numbers: the best if we rob it, and the best if we skip it. Rob it, and its children must be skipped. Skip it, and each child takes its better option.",
  "Bitmask DP. When the state must include a set of things already used, store the set as bits in an integer. The travelling salesman state is the mask of visited cities, plus the city you're at now. That's two to the n states, times n choices each.",
  "Exponential, so it only works for small inputs. If n is at most about twenty, and the problem says visit all, or assign each, think bitmask.",
 ]},

{"html": H("Family 9: state ", "machines") + sub("Stock trading with a cooldown: which state are you in at the end of each day?") +
   graph({"free": (130, 150), "hold": (470, 150), "cool": (300, 330)},
         [("free", "hold"), ("hold", "cool"), ("cool", "free")], w=620, h=430, directed=True, r=60,
         colors={"free": ("#dcfce7", "#16a34a"), "hold": ("#dbeafe", "#2563eb"), "cool": ("#fee2e2", "#dc2626")}, step=0) +
   code("""§1 hold = max(hold, free - price);   // keep holding, or buy
§1 cool = hold_before + price;        // sell today
§1 free = max(free, cool_before);     // rest, or cooldown ends""", 28, style="margin-top:6px"),
 "steps": [
  "The last family: state machines. Stock problems look scary, but they're just a few states per day. With a cooldown, at the end of each day you either hold a share, are in cooldown because you just sold, or are free to buy.",
  "Write one variable per state, and one line per arrow. Hold is the best of keeping your share, or buying today from free. Cool means you sold today. Free is the best of resting, or coming out of cooldown. A transaction limit or a fee just changes the states and arrows. Draw the machine first, then the code follows.",
 ]},

{"html": H("Is it ", "DP", "? Which family?") + table(["Clue", "State"], [
     (["moving on a grid, count or cheapest path", "a cell <code>dp[r][c]</code>"], 0),
     (["longest increasing / chain / nesting", "ends at <code>i</code>"], 0),
     (["two strings: common, edit, match", "prefixes <code>dp[i][j]</code>"], 1),
     (["merge / split / burst a range", "a range <code>dp[i][j]</code>, by length"], 1),
     (["tree: choose nodes with a rule", "tuple returned per node"], 2),
     (["n ≤ 20, visit or assign all", "<code>dp[mask][…]</code>"], 2),
     (["buy / sell / cooldown / k transactions", "one variable per state"], 2)], size=28) +
   note("Still stuck? Write the brute-force recursion: its <u>parameters</u> are the state", 3),
 "steps": [
  "So here's how to pick a family. A grid with counts or cheapest paths: the state is a cell. Longest increasing, or chains and nesting: the state is the element the sequence ends at.",
  "Two strings: prefixes of each. Merging, splitting or bursting a range: the range itself, filled by length.",
  "A tree with a choice at each node: a tuple per node. Small n with visit all or assign all: a bitmask. And buy, sell, cooldown: one variable per state.",
  "And if none of these fits, fall back on part one's advice. Write the plain recursion first. Whatever changes between calls, its parameters, is your state.",
 ]},

quiz([
  ("LIS: why is the answer max(dp), not dp[n−1]?", "the best run can <b style=\"display:inline\">end anywhere</b>", "blue",
   "Quiz time. In longest increasing subsequence, why is the answer the maximum over dp, and not the last cell?",
   "Because dp of i is the best run ending at i, and the best run can end anywhere."),
  ("Edit distance: the characters match. Cost?", "free: take the <b style=\"display:inline\">diagonal</b>", "green",
   "In edit distance, the current characters match. What does that cell cost?",
   "Nothing. Take the diagonal value, the answer without both characters."),
  ("Interval DP: in what order do you fill?", "by range <b style=\"display:inline\">length</b>, short first", "orange",
   "In interval DP, what order do you fill the table in?",
   "By the length of the range, shortest first, because long ranges are built from short ones."),
]),

recap(["Grid: a cell, from the cells you arrive from",
       "LIS: ends at i · O(n log n) with tails + binary search",
       "Two strings: prefixes · match → diagonal",
       "Intervals: a range, by length, try every split",
       "Trees: tuples in post-order · bitmask for n ≤ 20",
       "Stocks: one variable per state, one line per arrow"],
  "Let's recap part two. Grid DP: the state is a cell, built from the cells you arrive from. Increasing subsequences: the state is where it ends, and tails with binary search makes it n log n. Two strings use prefixes, and a match goes diagonal. Intervals use a range, filled by length, trying every split. Trees return tuples in post-order, and small n with visit all means a bitmask. And stock problems are a state machine: one variable per state. That completes the DP families. Now practise the problems listed in your notes!"),
]
