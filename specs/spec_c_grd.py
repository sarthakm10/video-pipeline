from conc import *

TAG = "DSA · Greedy"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Greedy.mp4"

SLIDES = [
title_slide(0, "Greedy", "Take the best-looking step now, and never look back, when you can prove it's safe",
  "Welcome. Today's concept: greedy algorithms.",
  "A greedy algorithm makes the choice that looks best right now, and never reconsiders it. When it works, it's simple and fast. When it doesn't, it's confidently wrong. By the end you'll know what makes a greedy choice safe, how to break a wrong one with a counterexample, the classic patterns: intervals, reach, matching, two passes and counting, and how to tell greedy problems from DP problems.",
  pill="DSA · CONCEPT"),

{"html": H("What greedy ", "means") + row(
   col(box("blue", "one local choice per step", "usually after sorting · no going back, no table", 0),
       box("green", "when it's right", "a <b style=\"display:inline\">greedy choice</b> is part of some optimal answer, and what's left is the same problem, smaller", 1),
       box("orange", "fast", "often O(n log n) for the sort + O(n)", 2), gap=16, style="flex:1"),
   col(box("red", "coins 1, 3, 4 · make 6", "greedy: 4 + 1 + 1 = <b style=\"display:inline\">3 coins</b>", 3),
       box("green", "optimal", "3 + 3 = <b style=\"display:inline\">2 coins</b> → greedy fails → DP", 3), gap=16, style="width:560px"), top=True),
 "steps": [
  "A greedy algorithm makes one locally best choice at each step, often after sorting, and never undoes it. No backtracking, no DP table.",
  "It's correct when two things hold. The greedy choice is part of at least one optimal answer. And after making it, what's left is a smaller copy of the same problem.",
  "When that holds, greedy is very fast. Typically a sort plus one pass.",
  "But it's easy to fool yourself. Coins of one, three and four, make six. Greedy takes the biggest coin first: four, one, one. Three coins. The best is three plus three. Two coins. One counterexample, and greedy is out. This is a DP problem.",
 ]},

{"html": H("Proving it: the exchange ", "argument") + row(
   box("purple", "1 · take any optimal answer", "suppose it does <b style=\"display:inline\">not</b> start with the greedy choice", 0, "flex:1"),
   box("blue", "2 · swap", "replace its first choice with the greedy one", 1, "flex:1"),
   box("green", "3 · show it's no worse", "still valid, same or better value → greedy is safe", 2, "flex:1"), top=True) +
   note("Can't prove it in an interview? Try hard to <u>break</u> it with a tiny example first", 3),
 "steps": [
  "How do you know a greedy choice is safe? The standard proof is an exchange argument. Take any optimal answer that doesn't make the greedy choice.",
  "Swap its first choice for the greedy one.",
  "Then show the result is still valid, and no worse. So there's always an optimal answer that starts greedily.",
  "In an interview, a full proof is rarely expected. But do spend a minute trying to break your rule with a tiny example. If you can't, explain the swap intuition. If you can, switch to DP.",
 ]},

{"html": H("Reach: jump ", "game") + sub("Can you reach the end? Each value = max jump from there") +
   col(cells([2, 3, 1, 1, 4], None, None, 0, "nums", size=40),
       cells([2, 4, 4, 4, 8], None, None, 1, "farthest so far", size=40, mark={4: "#bbf7d0"}),
       cells([3, 2, 1, 0, 4], None, None, 2, "other input: stuck", size=40, mark={3: "#fecaca"}), gap=16) +
   code("""§1 int far = 0;
§1 for (int i = 0; i < n; i++) {
§2   if (i > far) return false;        // can't even get here
§1   far = Math.max(far, i + nums[i]);
§1 }
§1 return true;""", 26, style="margin-top:20px"),
 "steps": [
  "Jump game. Each value is the maximum jump from that position. Can you reach the end?",
  "Don't explore every jump. Just track the farthest index reachable so far. Two, then four from index one, and so on. Four is the last index, so yes.",
  "If you ever stand at an index beyond the farthest reachable, you're stuck. Here, every path lands on the zero at index three. One pass, constant space. Jump game two, the minimum number of jumps, extends this into BFS-like levels: each jump covers the range reachable with one more jump.",
 ]},

{"html": H("Matching and ", "partitioning") + table(["Problem", "Greedy rule"], [
     (["assign cookies", "sort both · give the smallest cookie that satisfies the least greedy child"], 0),
     (["boats (limit 2 people)", "sort · pair the heaviest with the lightest if they fit"], 1),
     (["partition labels", "record each letter's <b>last</b> index · cut when i reaches the farthest last"], 2),
     (["gas station", "total gas ≥ total cost → a start exists · reset the start where the tank goes negative"], 3)], size=27),
 "steps": [
  "Many greedy problems are about matching. Assign cookies: sort children and cookies, and give each child the smallest cookie that's big enough. Big cookies are saved for greedier children.",
  "Boats that carry two people within a weight limit: sort, and try pairing the heaviest person with the lightest. If they don't fit, the heaviest goes alone, since nobody fits with them.",
  "Partition labels: record the last position of every letter. Walk the string, tracking the farthest last position seen. When you reach it, cut. The part can't be shorter, or a letter would be split.",
  "Gas station: if the total gas is at least the total cost, some start works. Walk once, and whenever the tank goes negative, the start must be after this point, so reset it.",
 ]},

{"html": H("Two passes and ", "counting") + row(
   col(box("blue", "candy", "each child with a higher rating than a neighbour gets more", 0),
       cells([1, 0, 2], None, None, 0, "ratings", size=36),
       cells([1, 1, 2], None, None, 1, "pass 1: left → right", size=36),
       cells([2, 1, 2], None, None, 2, "pass 2 + max: sum 5", size=36, mark={0: "#bbf7d0"}), gap=12, style="flex:1"),
   col(box("purple", "task scheduler", "the most frequent task sets the frame: <code>(maxCount − 1) × (n + 1) + tiesAtMax</code>", 3),
       box("green", "answer", "<code>max(tasks.length, frame)</code>", 3), gap=16, style="width:600px"), top=True),
 "steps": [
  "Some rules involve both neighbours, which one pass can't handle. In candy, a child with a higher rating than a neighbour must get more candy. Start everyone at one.",
  "Pass left to right: if a child beats the left neighbour, give one more than them.",
  "Then pass right to left, doing the same with the right neighbour, and keep the larger of the two values. Each pass satisfies one side, and the maximum satisfies both.",
  "Other greedy problems are really counting. In the task scheduler, the most frequent task decides the shape: gaps of n between its copies. Count the frame that creates, and the answer is the larger of that and the number of tasks.",
 ]},

{"html": H("Greedy or ", "DP?") + table(["Problem", "Greedy?", "Why"], [
     (["fractional knapsack", "✅ best value per kg first", "you can take part of an item"], 0),
     (["0/1 knapsack", "❌ DP", "whole items only: a good ratio can waste space"], 0),
     (["coin change, any coins", "❌ DP", "1, 3, 4 → 6 breaks it"], 1),
     (["activity selection", "✅ earliest end first", "exchange argument works"], 1),
     (["Dijkstra · Kruskal · Prim · Huffman", "✅ greedy inside", "proven greedy choices"], 2)], size=28) +
   note("Tiny counterexample found → DP · choices independent and provable → greedy", 3),
 "steps": [
  "The classic contrast is knapsack. If you can take part of an item, greedy by value per kilo is optimal. If items are all or nothing, a great ratio item can leave useless empty space, and you need DP.",
  "Coin change with arbitrary coins is DP, as we saw. Activity selection, picking the most non overlapping intervals, is greedy by earliest end.",
  "And some famous algorithms are greedy at heart. Dijkstra always finalises the closest node. Kruskal and Prim always take the cheapest safe edge. Huffman always merges the two rarest symbols.",
  "The practical test: try to find a tiny counterexample. If you find one, it's DP. If choices don't affect each other, and an exchange argument works, it's greedy.",
 ]},

quiz([
  ("Coins {1, 3, 4}, amount 6: greedy works?", "<b style=\"display:inline\">no</b>: 4+1+1 vs 3+3 → DP", "red",
   "Quiz time. Coins one, three and four, amount six. Does greedy work?",
   "No. Greedy gives three coins, but three plus three is two. Use DP."),
  ("Jump game: what do you track?", "the <b style=\"display:inline\">farthest</b> reachable index", "blue",
   "In jump game, what single value do you track?",
   "The farthest index reachable so far."),
  ("Candy: why two passes?", "each pass fixes <b style=\"display:inline\">one</b> neighbour", "purple",
   "In the candy problem, why do you need two passes?",
   "Each pass satisfies the rule for one side, and taking the maximum satisfies both."),
]),

recap(["Greedy: best local choice, never undone",
       "Safe when an exchange argument works",
       "One tiny counterexample → switch to DP",
       "Reach: track the farthest index",
       "Matching: sort, pair extremes or smallest fit",
       "Two-sided rules → two passes"],
  "Let's recap. Greedy makes the best local choice and never undoes it. It's safe when an exchange argument shows the greedy choice fits some optimal answer. One tiny counterexample means switch to DP. For reach problems, track the farthest index. For matching, sort and pair extremes, or give the smallest thing that fits. And rules involving both neighbours need two passes. Now practise the problems listed in your notes!"),
]
