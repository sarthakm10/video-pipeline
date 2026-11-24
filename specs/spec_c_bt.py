from conc import *

TAG = "DSA · Backtracking"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Backtracking.mp4"

G = ("#f3f4f6", "#6b7280")
OK = ("#dcfce7", "#16a34a")
CUT = ("#fee2e2", "#dc2626")

SLIDES = [
title_slide(0, "Backtracking", "Choose, explore, un-choose: a DFS over decisions",
  "Welcome. Today's concept: backtracking.",
  "Generate every subset. Every combination that sums to a target. Every way to split a string into palindromes. These questions ask you to build answers one choice at a time, and to try every possibility. Backtracking is the template for that. By the end you'll know the template, the difference between subsets, combinations and permutations, how to handle reuse and duplicates, and how pruning keeps it fast enough.",
  pill="DSA · CONCEPT"),

{"html": H("The ", "template") + row(
   code("""§0 void bt(int start, List<Integer> path) {
§1   if (isAnswer(path)) res.add(new ArrayList<>(path));
§2   for (int i = start; i < n; i++) {
§2     path.add(a[i]);              // choose
§2     bt(i + 1, path);             // explore
§3     path.remove(path.size() - 1); // un-choose
§2   }
§0 }""", 27, style="flex:1"),
   col(box("blue", "path", "the choices made so far", 0),
       box("green", "copy on save", "<code>new ArrayList&lt;&gt;(path)</code>: path keeps changing", 1),
       box("purple", "loop = the options", "each one is a branch of the tree", 2),
       box("red", "undo", "put everything back for the next branch", 3), gap=14, style="width:560px"), top=True),
 "steps": [
  "Every backtracking solution has the same shape. A recursive function, and a path holding the choices made so far.",
  "If the path is a valid answer, save it. But save a copy. The path object keeps changing as the search goes on, so saving the object itself would leave you with a list of empty lists.",
  "Then loop over the options for the next choice. Each option is a branch. Choose it by adding it to the path, then explore by recursing.",
  "After the recursive call returns, un-choose. Remove the last element, so the path is exactly as it was before this branch. That's the back in backtracking. Choose, explore, un-choose.",
 ]},

{"html": H("The decision ", "tree") + sub("Subsets of [1, 2, 3]") +
   graph({"{ }": (460, 50), "1": (200, 170), "2": (460, 170), "3": (720, 170),
          "1,2": (110, 300), "1,3": (290, 300), "2,3": (460, 300), "1,2,3": (110, 430)},
         [("{ }", "1"), ("{ }", "2"), ("{ }", "3"), ("1", "1,2"), ("1", "1,3"), ("2", "2,3"), ("1,2", "1,2,3")],
         w=900, h=480, r=44, step=0,
         colors={k: OK for k in ["{ }", "1", "2", "3", "1,2", "1,3", "2,3", "1,2,3"]}) +
   note("Every node is a subset · <code>start = i + 1</code> means we never look back → no duplicates like {2,1}", 1),
 "steps": [
  "Draw the search as a tree. Each node is a path, and each edge is a choice. For subsets, the root is the empty set. From it we can pick one, two or three. From one, we can add two or three. And so on.",
  "For subsets, every node in the tree is an answer, so we save at every call. And since each level starts from i plus one, we only ever add bigger indices. So we get one two, but never two one. Eight nodes, eight subsets.",
 ]},

{"html": H("Subsets, combinations, ", "permutations") + table(["Question", "Save when…", "Next start", "Count"], [
     (["subsets", "every node", "<code>i + 1</code>", "2ⁿ"], 0),
     (["combinations of size k", "<code>path.size() == k</code>", "<code>i + 1</code>", "C(n, k)"], 1),
     (["permutations", "<code>path.size() == n</code>", "always 0, skip <b>used</b>", "n!"], 2),
     (["combination sum, reuse allowed", "<code>remaining == 0</code>", "<code>i</code> (not i + 1)", "—"], 3)], size=29) +
   note("Order matters → permutations (a <code>used[]</code> array) · order doesn't → a start index", 4),
 "steps": [
  "Three question types use the same template, with small changes. Subsets save at every node, and the next level starts at i plus one. Two to the n answers.",
  "Combinations of size k are the same tree, but only save when the path has k elements.",
  "Permutations are different, because order matters. One two and two one are both answers. So every level loops from zero, and a used array skips elements already in the path. n factorial answers.",
  "And when an element can be reused, like coins in combination sum, recurse with i instead of i plus one. The same element can be picked again, but you still never go backward, so the same combination isn't found twice in a different order.",
  "The rule of thumb. If order matters, use a used array. If it doesn't, use a start index.",
 ]},

{"html": H("Duplicates in the ", "input") + sub("Subsets of [1, 2, 2] without repeating {1, 2}") + row(
   col(box("orange", "step 1 · sort", "equal values become neighbours", 0),
       box("green", "step 2 · skip", "at the <b style=\"display:inline\">same level</b>, use a value only once", 1),
       box("blue", "i &gt; start, not i &gt; 0", "the same value at a <b style=\"display:inline\">deeper</b> level is fine: {2, 2}", 2), gap=18, style="width:600px"),
   code("""§0 Arrays.sort(a);
§1 for (int i = start; i < n; i++) {
§1   if (i > start && a[i] == a[i - 1]) continue;
§1   path.add(a[i]);
§1   bt(i + 1, path);
§1   path.remove(path.size() - 1);
§1 }""", 26, style="flex:1"), top=True),
 "steps": [
  "When the input has duplicates, like one, two, two, the plain template finds the subset one two twice, once with each two. The fix has two parts. First, sort, so equal values sit next to each other.",
  "Second, in the loop, skip a value if it equals the one before it. Within one level, choosing the first two or the second two would build identical subtrees, so try only the first.",
  "The condition is i greater than start, not i greater than zero. That only skips repeats at the same level. Going one level deeper, picking the second two after the first is allowed, which is how we still get the subset two two.",
 ]},

{"html": H("Pruning: cut dead ", "branches") + sub("Combination sum: pick from [2, 3, 6, 7] to reach 7") +
   graph({"7": (440, 50), "5": (180, 180), "4": (380, 180), "1": (580, 180), "0 ✓": (760, 180),
          "3": (100, 320), "2": (260, 320), "−2 ✗": (440, 320)},
         [("7", "5"), ("7", "4"), ("7", "1"), ("7", "0 ✓"), ("5", "3"), ("5", "2"), ("4", "−2 ✗")],
         w=880, h=380, r=42, step=0, directed=True,
         colors={"7": G, "5": G, "4": G, "1": G, "0 ✓": OK, "3": G, "2": G, "−2 ✗": CUT}) +
   row(box("red", "prune", "sorted input + <code>a[i] &gt; remaining</code> → <code>break</code>, not <code>continue</code>", 1, "flex:1"),
       box("green", "why it matters", "same worst case, but real inputs finish fast", 2, "flex:1"), style="margin-top:10px"),
 "steps": [
  "Each node here is the amount still remaining. Picking seven reaches zero, an answer. Picking six from seven leaves one, picking six from four would leave minus two. That branch is dead.",
  "Pruning means not walking into dead branches at all. Sort the candidates first. Then, as soon as a candidate is bigger than what remains, every candidate after it is too. So break out of the loop, instead of continuing.",
  "Pruning doesn't change the worst case on paper, but it removes huge parts of the tree in practice. Good pruning is often the difference between a solution that passes and one that times out.",
 ]},

{"html": H("Beyond lists: strings and ", "grids") + row(
   box("blue", "palindrome partitioning", "choice = where to cut next · keep cutting only if the piece is a palindrome", 0, "flex:1"),
   box("purple", "generate parentheses", "choice = '(' or ')' · <code>open &lt; n</code> · <code>close &lt; open</code>", 1, "flex:1"),
   box("green", "word search", "DFS on the grid · mark the cell visited, <b style=\"display:inline\">unmark</b> on the way back", 2, "flex:1"), top=True) +
   note("Same template: the path can be a string, a grid mark, or a counter", 3),
 "steps": [
  "The template isn't limited to picking numbers. In palindrome partitioning, each choice is where to make the next cut. Only recurse if the piece you cut off is a palindrome, which prunes everything else.",
  "In generate parentheses, each choice is an open or a close bracket. You can open while you have openings left, and close only if more are open than closed. Those two rules mean every result is valid, with no checking at the end.",
  "And in word search, you walk the grid letter by letter. Mark a cell as visited before exploring its neighbours, and unmark it afterwards. That unmarking is the un-choose step.",
  "So the path can be a list, a string, a set of marks on a grid, or just counters. The rhythm is always the same.",
 ]},

{"html": H("Cost and common ", "bugs") + table(["Bug", "Symptom"], [
     (["saving <code>path</code> instead of a copy", "a list full of empty lists"], 0),
     (["forgetting to un-choose", "paths keep growing, wrong answers"], 0),
     (["<code>i + 1</code> vs <code>i</code> mixed up", "reuse missing, or infinite recursion"], 1),
     (["skip with <code>i &gt; 0</code> instead of <code>i &gt; start</code>", "valid answers like {2, 2} missing"], 1)], size=30) +
   note("Time ≈ number of answers × cost to build each one · it's exponential by nature", 2),
 "steps": [
  "The common bugs. Saving the path instead of a copy gives you a list of empty lists, because by the end the path is empty again. Forgetting to remove the last choice makes paths keep growing.",
  "Mixing up i and i plus one either loses reuse, or recurses forever on the same element. And skipping duplicates with i greater than zero, instead of i greater than start, throws away valid answers.",
  "As for cost, backtracking is exponential by nature, because the number of answers is. A good estimate is the number of answers times the work to build each one. That's why these problems have small inputs.",
 ]},

quiz([
  ("Why add new ArrayList<>(path)?", "path keeps <b style=\"display:inline\">changing</b> after you save it", "red",
   "Quiz time. Why save a new array list of the path, instead of the path itself?",
   "Because the same path object keeps changing, and is empty again at the end."),
  ("Combination sum, reuse allowed: recurse with?", "<code>i</code>, not <code>i + 1</code>", "blue",
   "In combination sum, each candidate can be used many times. Do you recurse with i, or i plus one?",
   "With i, so the same candidate can be picked again."),
  ("Permutations: start index or used[]?", "<b style=\"display:inline\">used[]</b>: order matters", "purple",
   "For permutations, do you use a start index, or a used array?",
   "A used array. Order matters, so every level loops over everything, skipping what's already in the path."),
]),

recap(["Choose → explore → un-choose",
       "Save a copy of the path",
       "Subsets/combinations: start index · permutations: used[]",
       "Reuse allowed → recurse with i",
       "Duplicates: sort, skip when i > start",
       "Prune with break on sorted input"],
  "Let's recap. Backtracking is choose, explore, un-choose. Always save a copy of the path. Subsets and combinations use a start index, and permutations use a used array. If elements can be reused, recurse with i. For duplicates, sort and skip equal values at the same level, with i greater than start. And prune dead branches early, with break on sorted input. Now practise the problems listed in your notes!"),
]
