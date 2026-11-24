from conc import *

TAG = "DSA · Graphs, Part 1"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Graphs (Part 1).mp4"

N = {"A": (60, 80), "B": (230, 40), "C": (230, 220), "D": (400, 130), "E": (560, 130), "F": (90, 330), "G": (300, 330)}
EDG = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("F", "G")]
BLUE, GREEN, ORANGE, PURPLE, GREY = ("#dbeafe", "#2563eb"), ("#dcfce7", "#16a34a"), ("#ffedd5", "#ea580c"), ("#f3e8ff", "#9333ea"), ("#f1f5f9", "#64748b")
LV = {"A": ORANGE, "B": BLUE, "C": BLUE, "D": GREEN, "E": PURPLE}

SLIDES = [
title_slide(0, "Graphs", "Part 1 · vocabulary, representation, BFS, DFS, cycles, topological sort",
  "Welcome to graphs, part one.",
  "Graphs model anything with connections. Roads between cities, friends, course prerequisites, even cells in a grid. In this part: the vocabulary, how to store a graph, the two traversals, BFS and DFS, and what you build on them. Components, cycle detection, topological sort, and bipartite checks.",
  pill="DSA · CONCEPT"),

{"html": H("The ", "vocabulary") + row(
   graph(N, EDG, {"E": ORANGE, "F": GREY, "G": GREY}, w=620, h=380),
   col(table(["Term", "Meaning"], [
     (["vertex · edge", "a thing · a connection"], 0),
     (["directed · weighted", "one-way edges · edges with a cost"], 1),
     (["path · cycle", "a route · a route back to its start"], 1),
     (["component", "vertices all reachable from each other"], 2),
     (["tree · DAG", "connected, no cycles · directed, no cycles"], 2)], size=27), style="flex:1"), top=True),
 "steps": [
  "A graph is vertices, the things, and edges, the connections between them. Here, seven vertices and six edges.",
  "Edges can be directed, going one way only, like a one-way street. And weighted, carrying a cost, like a distance. A path is a route along edges. A cycle is a path that comes back to its start, like A, B, D, C, and back to A.",
  "A connected component is a group of vertices that can all reach each other. This picture has two: A to E, and F with G. A tree is a connected graph with no cycles. And a DAG is a directed graph with no cycles. Prerequisites and build orders are DAGs.",
 ]},

{"html": H("The one big difference from ", "trees") + row(
   box("green", "tree", "following child pointers can never loop back → no <code>visited</code> needed", 0, "flex:1"),
   box("red", "graph", "cycles exist → without <code>visited</code>, a traversal <b style=\"display:inline\">runs forever</b>", 1, "flex:1")) +
   note("Every graph traversal = a tree traversal + a <u>visited</u> set", 2),
 "steps": [
  "You already know tree traversals. In a tree, following child pointers can never bring you back to a node you've seen. So you never need to track what you visited.",
  "In a general graph, cycles exist. A, B, D, C, A. Without remembering where you've been, a traversal walks that loop forever.",
  "So here's the key idea. Every graph traversal is a tree traversal, plus a visited set. BFS is level order plus visited. DFS is preorder plus visited.",
 ]},

{"html": H("Storing a ", "graph") + table(["Representation", "Space", "Is u–v an edge?", "Best for"], [
     (["<b>adjacency list</b>", "O(V + E)", "O(degree)", "almost everything"], 0),
     (["adjacency matrix", "O(V²)", "<b>O(1)</b>", "dense graphs, small V"], 1),
     (["edge list", "O(E)", "O(E)", "algorithms that loop over edges"], 1)], size=29) +
   code("""§2 List<List<Integer>> adj = new ArrayList<>();
§2 for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
§2 for (int[] e : edges) {
§2   adj.get(e[0]).add(e[1]);
§2   adj.get(e[1]).add(e[0]);      // leave out for a directed graph
§2 }""", 28, style="margin-top:24px"),
 "steps": [
  "How do you store one? The default is an adjacency list. For each vertex, a list of its neighbours. Space is V plus E, and listing a vertex's neighbours is fast.",
  "An adjacency matrix is a V by V grid of true and false. Checking one edge is instant, but it costs V squared space, so it's for dense or small graphs. And an edge list is just the edges, for algorithms that loop over every edge.",
  "Problems usually give you n, and a list of edges. These five lines turn them into an adjacency list. They start almost every graph solution, so memorise them. For a directed graph, add each edge only one way.",
 ]},

{"html": H("BFS: level by ", "level") + row(
   graph({k: v for k, v in N.items() if k in "ABCDE"}, EDG[:5], LV, w=620, h=290,
         labels={"A": "0", "B": "1", "C": "1", "D": "2", "E": "3"}),
   col(box("blue", "a queue", "first everything 1 edge away, then 2, then 3", 0),
       box("green", "shortest paths", "in an <b style=\"display:inline\">unweighted</b> graph, the first visit is along a shortest path", 1), gap=18, style="width:600px"), top=True) +
   note("Mark visited when you <u>enqueue</u>, not when you dequeue", 2),
 "steps": [
  "Breadth first search explores level by level, using a queue. Start at A, at distance zero. Then everything one edge away, B and C. Then two away, D. Then E. It's level order traversal, plus visited.",
  "And that gives BFS its superpower. In an unweighted graph, the first time BFS reaches a vertex, it got there by a shortest path. Fewest edges. So shortest path questions in unweighted graphs and grids are BFS.",
  "One detail. Mark a vertex visited when you add it to the queue, not when you take it out. Otherwise the same vertex can be queued many times by different neighbours.",
 ]},

{"html": H("DFS: as deep as ", "possible") + row(
   code("""§0 void dfs(int u) {
§0   visited[u] = true;
§0   for (int v : adj.get(u))
§0     if (!visited[v]) dfs(v);
§0 }""", 30, style="flex:1"),
   col(box("purple", "one branch fully, then back", "recursion, or an explicit stack", 0),
       box("orange", "deep graphs", "recursion can overflow → use a <code>Deque</code> as a stack", 1), gap=18, style="width:600px"), top=True) +
   table(["Use BFS for", "Use DFS for"], [
     (["shortest paths (unweighted)", "cycles, topological order"], 2),
     (["nearest / spreading (levels)", "exploring everything, paths, backtracking"], 2)], size=29),
 "steps": [
  "Depth first search goes as deep as possible down one branch before backing up. It's preorder traversal, plus visited. Recursively, it's just four lines.",
  "Recursion has a limit though. On a very deep graph, like a long chain, Java's stack overflows. Then use an explicit stack instead.",
  "So when do you use which? BFS for shortest paths in unweighted graphs, and anything spreading out in levels. DFS for cycles, topological order, and exploring every path. For simply visiting everything, either works.",
 ]},

{"html": H("Components and ", "grids") + row(
   col(box("blue", "count components", "for each unvisited vertex: <b style=\"display:inline\">count++</b>, then traverse from it", 0),
       box("green", "a grid is a graph", "each cell is a vertex · up, down, left, right are edges", 1), gap=18, style="flex:1"),
   col(cells(["1", "1", "0", "0"], mark={0: "#dbeafe", 1: "#dbeafe"}, size=36),
       cells(["1", "0", "0", "1"], mark={0: "#dbeafe", 3: "#dcfce7"}, size=36),
       cells(["0", "0", "1", "1"], mark={2: "#dcfce7", 3: "#dcfce7"}, size=36),
       '<div data-step="1" style="font-size:30px;color:#374151;text-align:center">2 islands</div>', gap=10, style="width:420px"), top=True) +
   note("Multi-source BFS: put <u>every</u> start in the queue at once (rotting oranges, nearest exit)", 2),
 "steps": [
  "Most graph problems are a traversal plus a little bookkeeping. To count connected components, loop over every vertex. Each time you find one not yet visited, that's a new component. Count it, and traverse from it to mark the whole group.",
  "And a grid is a graph in disguise. Each cell is a vertex, and its neighbours up, down, left, and right are its edges. Counting islands of ones is just counting components. Two here.",
  "A neat variant is multi-source BFS. When something spreads from several places at once, like rotting oranges, put every starting cell in the queue at the beginning. The levels then give the time for everything to be reached.",
 ]},

{"html": H("Detecting ", "cycles") + row(
   box("blue", "undirected", "a visited neighbour that <b style=\"display:inline\">isn't my parent</b> → cycle<br><small>the edge you came along doesn't count</small>", 0, "flex:1"),
   box("purple", "directed: three colours", "white = unvisited · <b style=\"display:inline\">grey</b> = on the current path · black = done<br><small>reaching a <b style=\"display:inline\">grey</b> vertex = a back edge = a cycle</small>", 1, "flex:1")) +
   note("Directed: two paths can <u>merge</u> without a cycle, so \"visited\" isn't enough", 2),
 "steps": [
  "Cycle detection works differently in the two kinds of graph. Undirected first. During DFS, every edge looks like it goes back to where you came from, and that one doesn't count. So a cycle is a visited neighbour that isn't your parent.",
  "In a directed graph, use three colours. White is unvisited. Grey means on the current DFS path, still being explored. Black means finished. If DFS reaches a grey vertex, it found a way back into its own path. That's a cycle.",
  "Why not just visited? Because in a directed graph, two separate paths can lead to the same vertex without any cycle. Seeing a finished vertex again is fine. Only reaching one still on the current path means a cycle.",
 ]},

{"html": H("Topological ", "sort") + row(
   graph({"Java": (80, 70), "DSA": (80, 250), "Spring": (330, 70), "React": (330, 300), "Project": (560, 160)},
         [("Java", "Spring"), ("Java", "DSA"), ("Spring", "Project"), ("React", "Project"), ("DSA", "Project")],
         {"Java": GREEN}, w=620, h=360, directed=True, r=50),
   col(box("blue", "an order for a DAG", "every edge <code>u → v</code> has u before v", 0),
       box("green", "Kahn's algorithm", "take a vertex with <b style=\"display:inline\">in-degree 0</b>, output it, remove its edges, repeat", 1),
       box("red", "fewer than n output?", "the rest are stuck in a <b style=\"display:inline\">cycle</b>", 2), gap=16, style="width:600px"), top=True),
 "steps": [
  "A topological order lists the vertices of a DAG so every edge goes forwards. Every prerequisite comes before what needs it. Like a valid order to take courses, or build modules.",
  "Kahn's algorithm finds one. Count each vertex's incoming edges, its in-degree. Any vertex with in-degree zero has no prerequisites left, so output it, and remove its edges, which may free up others. Put the free ones in a queue, and repeat.",
  "And it detects cycles for free. Vertices in a cycle wait on each other forever, so their in-degree never reaches zero. If fewer than n vertices come out, there's a cycle. That's exactly the course schedule question.",
 ]},

{"html": H("Bipartite ", "graphs") + row(
   graph({"1": (80, 80), "2": (280, 80), "3": (80, 260), "4": (280, 260)},
         [("1", "2"), ("2", "4"), ("4", "3"), ("3", "1")], {"1": BLUE, "4": BLUE, "2": ORANGE, "3": ORANGE}, w=360, h=330),
   col(box("blue", "two colours", "every edge joins <b style=\"display:inline\">different</b> colours", 0),
       box("orange", "how to check", "BFS or DFS: colour each neighbour the opposite colour · a clash → not bipartite", 1),
       box("red", "equivalent", "bipartite ⇔ <b style=\"display:inline\">no odd-length cycle</b>", 2), gap=16, style="flex:1"), top=True),
 "steps": [
  "A graph is bipartite if you can colour its vertices with two colours, so every edge joins different colours. Like splitting people into two teams, where every rivalry crosses between teams.",
  "To check, traverse with BFS or DFS, giving each neighbour the opposite colour to the current vertex. If you ever find a neighbour that already has the same colour, it's not bipartite. And loop over every vertex, because the graph may have several components.",
  "There's a neat equivalent. A graph is bipartite exactly when it has no odd-length cycle. A triangle can never be two-coloured.",
 ]},

quiz([
  ("Why does a graph traversal need <code>visited</code>?", "<b style=\"display:inline\">cycles</b> would loop forever", "blue",
   "Quiz time. Why does a graph traversal need a visited set, when a tree traversal doesn't?",
   "Because graphs can have cycles, and without visited you'd loop forever."),
  ("Shortest path, unweighted graph?", "<b style=\"display:inline\">BFS</b>", "green",
   "Which traversal finds shortest paths in an unweighted graph?",
   "BFS. The first time it reaches a vertex is along a shortest path."),
  ("Directed cycle: what do you look for?", "reaching a <b style=\"display:inline\">grey</b> vertex (on the path)", "purple",
   "In directed cycle detection, what exactly signals a cycle?",
   "Reaching a grey vertex, one still on the current DFS path."),
]),

recap(["Graph traversal = tree traversal + visited",
       "Adjacency list by default: O(V + E)",
       "BFS: queue, levels, shortest paths (unweighted)",
       "DFS: deep first · components · grids are graphs",
       "Cycles: not-parent (undirected) · grey (directed)",
       "Topo sort: in-degree 0 first · bipartite: two colours"],
  "Let's recap part one. A graph traversal is a tree traversal plus visited. Store graphs as adjacency lists. BFS uses a queue, goes level by level, and gives shortest paths in unweighted graphs. DFS goes deep, and both count components, including on grids. Detect cycles with the parent rule in undirected graphs, and grey vertices in directed ones. Topological sort takes in-degree zero vertices first, and bipartite means two colours. Next time, part two: weighted shortest paths, minimum spanning trees, and more!"),
]
