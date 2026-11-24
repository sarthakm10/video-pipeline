from conc import *

TAG = "DSA · Union-Find"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Union Find.mp4"

R = ("#fde68a", "#d97706")
N = ("#fff", "#374151")

SLIDES = [
title_slide(0, "Union-Find", "Which group is this in? Merge two groups. Both in almost O(1)",
  "Welcome. Today's concept: union find, also called the disjoint set union.",
  "Some problems keep merging things into groups, and keep asking whether two things are in the same group. Friends of friends, connected computers, cities joined by roads. Union find answers both questions in nearly constant time. By the end you'll know how groups become trees, the two optimisations that make it fast, counting components, detecting cycles, Kruskal's algorithm, and when to choose it over BFS or DFS.",
  pill="DSA · CONCEPT"),

{"html": H("Sets as ", "trees") + row(
   graph({"0": (120, 70), "1": (60, 200), "2": (180, 200), "3": (420, 70), "4": (420, 200), "5": (620, 120)},
         [("1", "0"), ("2", "0"), ("4", "3")], w=700, h=270, directed=True, r=36, step=0,
         colors={"0": R, "3": R, "5": R}),
   col(box("blue", "parent[]", "each item points to a parent · a root points to itself", 0),
       box("orange", "the root names the group", "<code>find(x)</code> walks up to the root", 1),
       box("green", "same group?", "<code>find(a) == find(b)</code>", 2), gap=16, style="flex:1"), top=True) +
   code("""§1 int find(int x) { while (parent[x] != x) x = parent[x]; return x; }
§3 void union(int a, int b) { parent[find(a)] = find(b); }   // root under root""", 27, style="margin-top:20px"),
 "steps": [
  "Union find stores each group as a tree, using one array. Every item points to a parent. A root points to itself. Here there are three groups: zero, one and two; three and four; and five on its own.",
  "The root is the group's name. To find which group an item is in, follow parents up until you reach the root.",
  "Two items are in the same group if they have the same root.",
  "To merge two groups, find both roots, and point one root at the other. One assignment joins two whole trees.",
 ]},

{"html": H("Optimisation 1: path ", "compression") + row(
   col(graph({"a": (90, 50), "b": (90, 150), "c": (90, 250), "d": (90, 350)},
             [("d", "c"), ("c", "b"), ("b", "a")], w=200, h=410, directed=True, r=34, step=0, colors={"a": R}),
       style=""),
   col(box("red", "the problem", "unlucky unions build a <b style=\"display:inline\">chain</b> → find is O(n)", 0),
       box("green", "the fix", "while finding, point every node on the path <b style=\"display:inline\">straight at the root</b>", 1),
       code("""§1 int find(int x) {
§1   if (parent[x] != x) parent[x] = find(parent[x]);
§1   return parent[x];
§1 }""", 28),
       box("blue", "next time", "d, c and b are one step from the root", 2), gap=16, style="flex:1"), top=True),
 "steps": [
  "Without care, trees can become long chains. Then find walks the whole chain, which is linear.",
  "Path compression fixes it while finding. On the way back from the root, set each node's parent directly to the root. It's one extra assignment in a recursive find.",
  "After one find from d, the nodes d, c and b all point straight at a. Every later find from them is one step.",
 ]},

{"html": H("Optimisation 2: union by ", "size") + row(
   col(box("orange", "attach the smaller tree under the bigger", "the depth grows only when sizes are equal", 0),
       box("green", "both together", "amortised <b style=\"display:inline\">O(α(n))</b> per operation · α(n) ≤ 4 for any real n", 1), gap=18, style="width:560px"),
   code("""§0 boolean union(int a, int b) {
§0   int ra = find(a), rb = find(b);
§2   if (ra == rb) return false;    // already together
§0   if (size[ra] < size[rb]) {        // ra = the bigger
§0     int t = ra; ra = rb; rb = t;
§0   }
§0   parent[rb] = ra;  size[ra] += size[rb];
§0   count--;                       // one group fewer
§0   return true;
§0 }""", 26, style="flex:1"), top=True) +
   note("<code>union</code> returning false = the two were already connected", 2),
 "steps": [
  "The second optimisation decides which root goes under which. Always attach the smaller tree under the bigger one. Rank, a bound on height, works the same way. Trees then stay shallow.",
  "With both optimisations, each operation costs the inverse Ackermann function of n, which is at most four for any input you'll ever see. Effectively constant.",
  "One more detail. Make union return false when both items already share a root. That single boolean is what cycle detection uses. And keep a count of groups, decreasing it on every successful union.",
 ]},

{"html": H("Components and ", "cycles") + row(
   box("blue", "count components", "start with <code>count = n</code> · every successful union: <code>count--</code>", 0, "flex:1"),
   box("red", "detect a cycle", "adding edge (a, b) when <code>find(a) == find(b)</code> → that edge closes a cycle", 1, "flex:1"),
   box("green", "Kruskal's MST", "sort edges by weight · keep an edge only if <code>union</code> succeeds", 2, "flex:1"), top=True) +
   graph({"1": (160, 80), "2": (420, 80), "3": (420, 260), "4": (160, 260)},
         [("1", "2"), ("2", "3"), ("3", "4"), ("4", "1")], w=600, h=330, r=38, step=1,
         colors={"1": ("#fee2e2", "#dc2626"), "4": ("#fee2e2", "#dc2626")}, labels={"4": "edge 4–1: same root → cycle"}),
 "steps": [
  "Three classic uses. Counting connected components: start with n groups, and every successful union reduces the count by one.",
  "Detecting a cycle in an undirected graph: add edges one by one. If an edge joins two nodes that already share a root, there was already a path between them, so this edge closes a cycle. That's redundant connection.",
  "And Kruskal's minimum spanning tree: sort edges by weight, and keep each edge only if its union succeeds. Union find is exactly the tool Kruskal needs.",
 ]},

{"html": H("Beyond integers and ", "graphs") + row(
   box("purple", "items aren't 0..n−1", "map each name/email to an index with a <code>HashMap</code> · or keep <code>Map&lt;String,String&gt; parent</code>", 0, "flex:1"),
   box("blue", "grids", "cell (r, c) → index <code>r * cols + c</code> · union with neighbours", 1, "flex:1"),
   box("orange", "weighted DSU", "store a ratio/offset to the parent · <code>a / b = 2</code>, <code>b / c = 3</code> → <code>a / c = 6</code>", 2, "flex:1"), top=True) +
   note("Accounts merge · number of islands · evaluate division", 3),
 "steps": [
  "Items don't have to be numbers. When they're emails or names, map each one to an index with a hash map, or keep the parent links in a map directly.",
  "On a grid, give each cell a number, row times columns plus column, and union each land cell with its land neighbours. The number of islands is the component count.",
  "Weighted union find stores extra information on each link, like a ratio to the parent. Path compression multiplies the ratios along the path. That's how you evaluate chains of divisions.",
  "These are the shapes behind accounts merge, number of islands two, and evaluate division.",
 ]},

{"html": H("Union-Find or ", "BFS/DFS?") + table(["Situation", "Better choice"], [
     (["edges keep arriving, connectivity asked in between", "<b>union-find</b>"], 0),
     (["count components / detect a cycle, undirected", "either · DSU is shorter"], 0),
     (["shortest path, distances, the actual path", "<b>BFS / DFS</b>"], 1),
     (["directed graphs, topological order", "<b>DFS / Kahn</b> · DSU ignores direction"], 1),
     (["edges are <b>removed</b>", "neither directly · reverse time, then union"], 2)], size=29),
 "steps": [
  "When to choose it? Union find shines when edges keep arriving and connectivity questions come in between. A graph search would have to rerun each time.",
  "BFS or DFS is better when you need distances, the actual path, or anything about direction. Union find only knows who is connected, not how, and it ignores edge direction.",
  "And union find can't split groups. If edges are removed, a common trick is to process the operations backwards in time, so removals become additions.",
 ]},

quiz([
  ("Adding edge (a, b) and find(a) == find(b)?", "this edge makes a <b style=\"display:inline\">cycle</b>", "red",
   "Quiz time. You add the edge a b, and a and b already have the same root. What does that mean?",
   "They were already connected, so this edge closes a cycle."),
  ("The two optimisations?", "<b style=\"display:inline\">path compression</b> + union by size/rank", "blue",
   "What are the two optimisations that make union find fast?",
   "Path compression, and union by size or rank."),
  ("Need the shortest path. Union-find?", "<b style=\"display:inline\">no</b>: use BFS", "green",
   "You need the shortest path between two nodes. Is union find the right tool?",
   "No. It only knows whether they're connected. Use BFS."),
]),

recap(["parent[] makes trees · the root names the group",
       "find: walk to the root · union: root under root",
       "Path compression + union by size → almost O(1)",
       "union false → already connected → a cycle",
       "count-- on each union → components",
       "Distances or direction → BFS/DFS instead"],
  "Let's recap. Union find stores groups as trees in a parent array, and the root names the group. Find walks up to the root, and union points one root at another. Path compression and union by size make both almost constant time. When union finds the two already connected, that edge is a cycle. Decrease a counter on each union to count components. And when you need distances or direction, use BFS or DFS instead. Now practise the problems listed in your notes!"),
]
