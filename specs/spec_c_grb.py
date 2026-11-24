from conc import *

TAG = "DSA · Graphs, Part 2"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Graphs (Part 2).mp4"

N = {"A": (90, 200), "B": (330, 70), "C": (330, 330), "D": (570, 200)}
E = [("A", "B", 4), ("A", "C", 1), ("C", "B", 2), ("B", "D", 1), ("C", "D", 5)]


def wgraph(colors=None, labels=None, step=None, nodes=N, edges=E, w=660, h=420):
    """graph() plus a weight label on each edge."""
    svg = graph(nodes, [(a, b) for a, b, _ in edges], colors=colors, w=w, h=h, step=step, labels=labels)
    marks = "".join(
        f'<rect x="{(nodes[a][0] + nodes[b][0]) / 2 - 20:.0f}" y="{(nodes[a][1] + nodes[b][1]) / 2 - 20:.0f}" width="40" height="38" rx="8" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>'
        f'<text x="{(nodes[a][0] + nodes[b][0]) / 2:.0f}" y="{(nodes[a][1] + nodes[b][1]) / 2 + 10:.0f}" text-anchor="middle" font-size="28" font-weight="700" font-family="Segoe UI">{wt}</text>'
        for a, b, wt in edges)
    return svg.replace("</svg>", marks + "</svg>")


DONE = ("#dcfce7", "#16a34a")

SLIDES = [
title_slide(0, "Graphs", "Part 2: weighted shortest paths, spanning trees, and choosing the right algorithm",
  "Welcome to part two of graphs.",
  "In part one, every edge cost the same, so BFS found shortest paths. Today, edges have weights. We'll see Dijkstra, 0-1 BFS, Bellman-Ford and Floyd-Warshall for shortest paths, Prim and Kruskal for minimum spanning trees, then implicit graphs, strongly connected components and bridges. And at the end, a table to choose between them.",
  pill="DSA · CONCEPT · PART 2"),

{"html": H("Why BFS isn't enough any ", "more") + row(
   wgraph(),
   col(box("red", "BFS: fewest edges", "A → B directly: 1 edge, cost <b style=\"display:inline\">4</b>", 0),
       box("green", "cheapest path", "A → C → B: 2 edges, cost <b style=\"display:inline\">3</b>", 1),
       box("blue", "the fix", "always expand the <b style=\"display:inline\">closest</b> unfinished vertex next", 2), gap=18, style="flex:1"), top=True),
 "steps": [
  "Why do we need new algorithms? BFS finds the path with the fewest edges. From A to B, that's the direct edge, which costs four.",
  "But going A to C to B uses two edges, and costs only three. With weights, fewest edges and cheapest aren't the same thing.",
  "The fix: instead of a plain queue, always expand the vertex that's currently closest to the start. That's Dijkstra's algorithm.",
 ]},

{"html": H("", "Dijkstra") + row(
   col(wgraph(),
       box("green", "", "popped vertices are final: nothing cheaper can come later", 3), gap=10, style="width:660px"),
   col(box("gray", "1 · pop A (0)", "relax: B = 4, C = 1", 0),
       box("gray", "2 · pop C (1)", "B: 1 + 2 = <b style=\"display:inline\">3</b> &lt; 4 → update · D = 6", 1),
       box("gray", "3 · pop B (3)", "D: 3 + 1 = <b style=\"display:inline\">4</b> &lt; 6 → update", 2),
       box("green", "4 · pop D (4)", "done: A 0 · C 1 · B 3 · D 4", 3), gap=16, style="flex:1"), top=True),
 "steps": [
  "Here's Dijkstra on that graph. Distances start at infinity, except A at zero. Pop the closest vertex, A, and relax its edges. B becomes four, C becomes one.",
  "Now the closest unfinished vertex is C, at one. Through C, B costs one plus two, three, which beats four. So update it. D becomes six.",
  "Next is B, at three. Through B, D costs three plus one, four. Better than six, update.",
  "Finally pop D at four. Every vertex is done. A zero, C one, B three, D four.",
 ]},

{"html": H("Dijkstra in ", "code") + code("""§0 PriorityQueue<int[]> pq = new PriorityQueue<>((x, y) -> x[1] - y[1]);
§0 dist[src] = 0;  pq.add(new int[]{src, 0});
§0 while (!pq.isEmpty()) {
§0   int[] top = pq.poll();  int u = top[0];
§1   if (top[1] > dist[u]) continue;          // stale entry: skip it
§0   for (int[] e : adj.get(u)) {             // e = {v, w}
§0     if (dist[u] + e[1] < dist[e[0]]) {     // relax
§0       dist[e[0]] = dist[u] + e[1];
§0       pq.add(new int[]{e[0], dist[e[0]]});
§0     }
§0   }
§0 }""", 28) + row(box("blue", "time", "O((V + E) log V)", 2, "flex:1"),
                   box("red", "needs", "<b style=\"display:inline\">no negative</b> edges", 2, "flex:1"), style="margin-top:22px"),
 "steps": [
  "In code, it's BFS with a priority queue ordered by distance. Pop the closest, relax each edge: if going through u is cheaper, update the distance and push the neighbour.",
  "One detail. A vertex can sit in the queue several times with old distances. When you pop an entry that's worse than the known distance, it's stale. Skip it.",
  "It runs in V plus E, times log V. And it has one hard requirement: no negative edges. Once a vertex is popped, Dijkstra assumes nothing can make it cheaper. A negative edge breaks that promise.",
 ]},

{"html": H("Special and negative ", "weights") + row(
   box("green", "weights only 0 or 1 → 0-1 BFS", "a <b style=\"display:inline\">deque</b>: 0-edges go to the front, 1-edges to the back · O(V + E)", 0, "flex:1"),
   box("orange", "negative edges → Bellman-Ford", "relax <b style=\"display:inline\">every</b> edge V − 1 times · O(V · E)<br>still improving on round V? <b style=\"display:inline\">negative cycle</b>", 1, "flex:1")) +
   row(box("purple", "all pairs, small V → Floyd-Warshall", "<code>dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])</code> for every k · O(V³)", 2, "flex:1"), style="margin-top:24px") +
   note("At most k stops? Bellman-Ford with <u>k + 1</u> rounds", 3),
 "steps": [
  "Some weight patterns have their own tools. If every edge weighs zero or one, use a deque instead of a priority queue. A zero edge goes to the front, a one edge to the back. That's linear, faster than Dijkstra.",
  "With negative edges, use Bellman-Ford. Relax every edge, V minus one times. A shortest path has at most V minus one edges, so that's enough. And if anything still improves on the V-th round, there's a negative cycle, and no shortest path exists.",
  "If you need the distance between every pair, and the graph is small, use Floyd-Warshall. For each middle vertex k, check whether going through k is shorter. Three loops, V cubed.",
  "And an interview favourite: cheapest flight with at most k stops. Dijkstra struggles with that limit. Bellman-Ford with k plus one rounds handles it naturally.",
 ]},

{"html": H("Minimum spanning ", "trees") + row(
   col(box("blue", "spanning tree", "connects all V vertices with V − 1 edges, no cycles", 0),
       box("green", "minimum", "the smallest total weight", 0),
       box("orange", "not a shortest-path tree", "MST minimises the <b style=\"display:inline\">total</b>, not the distance from one source", 1), gap=18, style="flex:1"),
   wgraph(colors={"A": DONE, "B": DONE, "C": DONE, "D": DONE}, step=2,
          edges=[("A", "C", 1), ("C", "B", 2), ("B", "D", 1)]), top=True) +
   note("Cheapest way to connect all the cities with cable", 2),
 "steps": [
  "Now a different question. A spanning tree connects every vertex using exactly V minus one edges, with no cycles. The minimum spanning tree is the one with the smallest total weight.",
  "Don't confuse it with shortest paths. The MST minimises the total cost of all edges, not the distance from one starting vertex.",
  "On our graph, the MST uses A to C, C to B, and B to D. Total weight four. Think of it as the cheapest way to connect every city with cable.",
 ]},

{"html": H("Kruskal and ", "Prim") + row(
   box("purple", "Kruskal: edges first", "sort all edges by weight · take an edge if it joins <b style=\"display:inline\">two different</b> components (Union-Find) · O(E log E)", 0, "flex:1"),
   box("blue", "Prim: grow one tree", "start anywhere · repeatedly add the cheapest edge leaving the tree (priority queue) · O(E log V)", 1, "flex:1"), top=True) +
   table(["", "Kruskal", "Prim"], [
     (["works on", "an edge list", "adjacency lists"], 2),
     (["good for", "sparse graphs", "dense graphs"], 2),
     (["tool", "Union-Find", "priority queue"], 2)], size=29) +
   note("Both are greedy, and both are correct by the <u>cut property</u>", 3),
 "steps": [
  "Two algorithms build an MST. Kruskal goes edge by edge. Sort every edge by weight, then take each one, unless it would join two vertices that are already connected, which would make a cycle. Union-Find answers that check almost instantly.",
  "Prim grows a single tree. Start from any vertex, and keep adding the cheapest edge that leaves the tree. A priority queue gives you that edge, just like in Dijkstra.",
  "Kruskal suits an edge list and sparse graphs. Prim suits adjacency lists and dense graphs.",
  "Both are greedy, and greedy is safe here because of the cut property. The cheapest edge crossing any split of the vertices always belongs to some MST.",
 ]},

{"html": H("Hidden graphs and ", "deeper", " structure") + row(
   col(box("green", "implicit graphs", "no edge list given · vertices are <b style=\"display:inline\">states</b><br>word ladder: words differing by one letter · lock: turn one wheel", 0),
       box("blue", "cloning a graph", "DFS or BFS + a <code>HashMap&lt;old, copy&gt;</code> so each node is copied once", 1), gap=18, style="flex:1"),
   col(box("purple", "strongly connected components", "directed: every vertex reaches every other · <b style=\"display:inline\">Kosaraju</b>: DFS order, reverse edges, DFS again", 2),
       box("red", "bridges", "an edge whose removal disconnects the graph · <b style=\"display:inline\">Tarjan</b>: discovery time + low-link", 3), gap=18, style="flex:1"), top=True),
 "steps": [
  "Some graphs are never given to you. In an implicit graph, the vertices are states, and the edges are the moves between them. In word ladder, each word is a vertex, and words one letter apart are connected. Generate neighbours on the fly, and run BFS.",
  "Cloning a graph is a traversal plus a map from each original node to its copy. The map does double duty. It finds copies you've already made, and it stops you looping forever on cycles.",
  "Two harder ideas, worth recognising. In a directed graph, a strongly connected component is a group where every vertex can reach every other. Kosaraju finds them with two DFS passes, the second on the reversed graph.",
  "And a bridge is an edge whose removal splits the graph. Tarjan's algorithm finds them in one DFS, using discovery times and the lowest time each subtree can reach. That's critical connections in a network.",
 ]},

{"html": H("Choosing the ", "algorithm") + table(["Situation", "Use", "Time"], [
     (["unweighted shortest path", "BFS", "O(V + E)"], 0),
     (["weights 0 / 1", "0-1 BFS", "O(V + E)"], 0),
     (["non-negative weights", "Dijkstra", "O((V + E) log V)"], 1),
     (["negative edges · at most k stops", "Bellman-Ford", "O(V · E)"], 1),
     (["all pairs, V ≤ ~400", "Floyd-Warshall", "O(V³)"], 2),
     (["connect everything cheapest", "Kruskal / Prim", "O(E log E)"], 2),
     (["dependencies · ordering", "topological sort", "O(V + E)"], 3)], size=29),
 "steps": [
  "So how do you choose? Unweighted: BFS. Weights of zero or one: zero one BFS. Both linear.",
  "Non-negative weights: Dijkstra. Negative edges, or a limit on the number of stops: Bellman-Ford.",
  "Every pair of vertices on a small graph: Floyd-Warshall. Connecting everything at minimum cost: Kruskal or Prim.",
  "And from part one, anything about dependencies or ordering is a topological sort. Read the constraints, especially the edge weights and the size of V. They usually decide it for you.",
 ]},

quiz([
  ("Dijkstra with a negative edge?", "can be <b style=\"display:inline\">wrong</b>: use Bellman-Ford", "red",
   "Quiz time. Can you run Dijkstra on a graph with a negative edge?",
   "No. It can give wrong answers, because a popped vertex might get cheaper later. Use Bellman-Ford."),
  ("Bellman-Ford still improves on round V. Meaning?", "a <b style=\"display:inline\">negative cycle</b>", "orange",
   "Bellman-Ford keeps improving a distance on round V. What does that mean?",
   "There's a negative cycle, so no shortest path exists."),
  ("MST vs shortest-path tree?", "MST minimises the <b style=\"display:inline\">total</b> weight", "green",
   "What's the difference between a minimum spanning tree and a shortest path tree?",
   "The MST minimises the total weight of all edges. A shortest path tree minimises each vertex's distance from one source."),
]),

recap(["Weights → always expand the closest vertex (Dijkstra)",
       "Skip stale queue entries · no negative edges",
       "0/1 weights → deque · negatives → Bellman-Ford",
       "All pairs, small V → Floyd-Warshall",
       "MST: Kruskal (sort + Union-Find) or Prim (heap)",
       "Implicit graphs: states as vertices, then BFS"],
  "Let's recap part two. With weights, always expand the closest vertex. That's Dijkstra. Skip stale queue entries, and never use it with negative edges. Zero one weights use a deque. Negative edges use Bellman-Ford, which also detects negative cycles. All pairs on a small graph: Floyd-Warshall. Minimum spanning trees: Kruskal with sorting and Union-Find, or Prim with a heap. And when no graph is given, the states are your vertices. Now practise the problems listed in your notes!"),
]
