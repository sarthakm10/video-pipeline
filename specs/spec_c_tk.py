from conc import *

TAG = "DSA · Top K and K-Way Merge"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Top K and K Way Merge.mp4"

SLIDES = [
title_slide(0, "Top K & K-Way Merge", "A small heap that remembers only what matters",
  "Welcome. Today's concept: top K problems, and K way merge.",
  "The K largest numbers. The K most frequent words. The K closest points. Merge K sorted lists. All of these are solved with a heap, but the clever part is which heap, and how big. By the end you'll know Java's priority queue, why the top K largest uses a min heap, how to break ties, quickselect, and how one heap merges K sorted lists.",
  pill="DSA · CONCEPT"),

{"html": H("PriorityQueue in ", "Java") + row(
   code("""§0 PriorityQueue<Integer> min = new PriorityQueue<>();
§0 PriorityQueue<Integer> max =
§0     new PriorityQueue<>(Comparator.reverseOrder());
§1 pq.offer(x);    // add       O(log n)
§1 pq.peek();      // smallest  O(1)
§1 pq.poll();      // remove it O(log n)
§2 new PriorityQueue<int[]>((a, b) -> Integer.compare(a[1], b[1]));""", 25, style="flex:1"),
   col(box("blue", "a binary heap", "the smallest element is always at the top", 0),
       box("green", "offer / poll", "O(log n) · peek O(1)", 1),
       box("orange", "not sorted", "iterating gives heap order, <b style=\"display:inline\">not</b> sorted order", 2), gap=16, style="width:520px"), top=True),
 "steps": [
  "Java's priority queue is a binary heap. By default it's a min heap: the smallest element is always at the top. For a max heap, pass comparator dot reverse order.",
  "Adding with offer and removing with poll both cost log n. Peeking at the top is constant.",
  "For arrays or objects, pass a comparator that says what to order by. Use Integer dot compare rather than subtracting, which can overflow. And remember: iterating over a priority queue does not give sorted order. Only polling one by one does.",
 ]},

{"html": H("Top K largest: a ", "min-heap") + sub("K = 3 largest of [5, 1, 9, 3, 7, 6]") +
   col(cells([1, 5, 9], None, None, 0, "first 3 → heap", size=40, mark={0: "#fde68a"}),
       cells([3, 5, 9], None, None, 1, "3 beats top 1 → poll 1", size=40, mark={0: "#fde68a"}),
       cells([5, 7, 9], None, None, 2, "7 beats top 3 → poll 3", size=40, mark={0: "#fde68a"}),
       cells([6, 7, 9], None, None, 3, "6 beats top 5 → done", size=40, mark={0: "#bbf7d0", 1: "#bbf7d0", 2: "#bbf7d0"}), gap=14) +
   note("The top of the min-heap = the <u>weakest</u> of the current K = the bar to beat", 4),
 "steps": [
  "Find the three largest numbers. The surprise: use a min heap, not a max heap. Fill it with the first three numbers. The smallest, one, sits on top.",
  "Three arrives. It's bigger than the heap's smallest, one. So one can't be in the top three any more. Add three, and poll the smallest out.",
  "Seven beats the current smallest, three. Three goes.",
  "Six beats five. At the end, the heap holds six, seven and nine. The three largest.",
  "Why a min heap? Its top is the weakest of your current top K. It's the bar a new number has to beat. And the heap never grows past K.",
 ]},

{"html": H("Why it's ", "fast") + table(["Approach", "Time", "Space"], [
     (["sort everything", "O(n log n)", "O(1) – O(n)"], 0),
     (["max-heap of all n, poll K times", "O(n + K log n)", "O(n)"], 1),
     (["<b>min-heap of size K</b>", "<b>O(n log K)</b>", "<b>O(K)</b>"], 2),
     (["quickselect", "O(n) average · O(n²) worst", "O(1)"], 3)], size=31) +
   note("K much smaller than n, or a stream that never ends → the size-K heap wins", 4),
 "steps": [
  "Compare the options. Sorting everything is n log n, and does far more work than needed.",
  "Putting all n into a max heap and polling K times works, but stores everything.",
  "The size K min heap does n operations of log K each, and only stores K items. When K is small, log K is tiny.",
  "Quickselect, coming up, is linear on average, but can degrade to quadratic.",
  "And there's one case only the heap handles: a stream. Numbers keep arriving, and you can't sort something that never ends. A heap of size K always holds the current answer.",
 ]},

{"html": H("Top K frequent and ", "ties") + row(
   code("""§0 Map<String,Integer> count = new HashMap<>();
§0 for (String w : words) count.merge(w, 1, Integer::sum);
§1 PriorityQueue<String> pq = new PriorityQueue<>(
§1     (a, b) -> !count.get(a).equals(count.get(b))
§1         ? Integer.compare(count.get(a), count.get(b)) // fewer first
§2         : b.compareTo(a));               // then reverse alphabetical
§1 for (String w : count.keySet()) {
§1   pq.offer(w);
§1   if (pq.size() > k) pq.poll();
§1 }""", 23, style="flex:1"),
   col(box("blue", "1 · count", "a HashMap of frequencies", 0),
       box("green", "2 · heap of size K", "ordered by count, weakest on top", 1),
       box("orange", "3 · ties", "the comparator must put the <b style=\"display:inline\">loser</b> on top", 2),
       box("purple", "4 · output", "polls come out weakest first → <b style=\"display:inline\">reverse</b>", 3), gap=14, style="width:520px"), top=True),
 "steps": [
  "Top K frequent elements adds one step. First count frequencies with a hash map.",
  "Then run the same size K min heap over the distinct words, ordered by count.",
  "Ties are the tricky part. If the answer should list equal counts alphabetically, then the word that loses a tie is the later one. The heap's top must be the loser, so for equal counts, compare in reverse alphabetical order. Get this backwards and the wrong word survives.",
  "Polling gives the weakest first, so reverse the result at the end. Bucket sort by frequency is a linear alternative when counts are bounded by n.",
 ]},

{"html": H("Quickselect: average ", "O(n)") + row(
   col(box("blue", "partition", "pick a pivot, put smaller left, bigger right · the pivot lands in its <b style=\"display:inline\">final</b> place", 0),
       box("green", "recurse one side", "the Kth position is left or right of the pivot · ignore the other half", 1),
       box("red", "worst case O(n²)", "bad pivots · pick a <b style=\"display:inline\">random</b> pivot", 2), gap=16, style="flex:1"), top=True) +
   cells([3, 1, 2, 5, 9, 7, 6], None, None, 0, "pivot 5 → index 3", size=38, mark={3: "#fde68a"}, style="margin-top:20px") +
   note("n + n/2 + n/4 + … ≈ 2n → linear on average", 3),
 "steps": [
  "Quickselect borrows quicksort's partition step. Pick a pivot, and move smaller elements to its left and bigger ones to its right. The pivot is now exactly where it would be in sorted order.",
  "If that's the position you want, you're done. Otherwise, the answer is on one side only, so recurse into that side and ignore the other half. That's the difference from quicksort, which sorts both halves.",
  "Bad pivots, like always the largest, make it quadratic. A random pivot makes that very unlikely.",
  "On average, each step halves the work: n, plus n over two, plus n over four, which adds up to about two n. Linear.",
 ]},

{"html": H("K-way ", "merge") + sub("Merge K sorted lists") + row(
   col(cells([1, 4, 7], None, None, 0, "list A", size=38, mark={0: "#bfdbfe"}),
       cells([2, 5, 8], None, None, 0, "list B", size=38, mark={0: "#bfdbfe"}),
       cells([3, 6, 9], None, None, 0, "list C", size=38, mark={0: "#bfdbfe"}),
       cells([1, 2, 3, 4, "…"], None, None, 2, "output", size=38), gap=14),
   col(box("blue", "heap of heads", "one entry per list: its current smallest", 0),
       box("green", "poll, then push the next", "take the smallest head, push that list's next element", 1),
       box("purple", "cost", "N total elements · heap size K → O(N log K)", 3), gap=16, style="flex:1"), top=True),
 "steps": [
  "Now K way merge. You have K sorted lists, and want one sorted output. Put the head of each list into a min heap. The heap holds one candidate per list.",
  "Poll the smallest. That's the next output element. Then push the next element from the same list, so that list stays represented.",
  "Repeat until the heap is empty. One, two, three, four, and so on.",
  "The heap never holds more than K entries, so each of the N elements costs log K. Store the list index with each value, so you know which list to advance.",
 ]},

{"html": H("Same pattern, other ", "shapes") + table(["Problem", "Heap holds…"], [
     (["Kth smallest in a sorted matrix", "one cell per row · advance along the row"], 0),
     (["K pairs with smallest sums", "pairs · push (i, j+1) after (i, j)"], 1),
     (["smallest range covering K lists", "one per list + track the current <b>max</b>"], 2),
     (["Kth largest in a stream", "size-K min-heap · answer = <code>peek()</code>"], 3)], size=30),
 "steps": [
  "The K way merge idea shows up in disguise. In a matrix whose rows are sorted, each row is a sorted list. Put the first cell of every row in the heap, and poll K times.",
  "For K pairs with the smallest sums from two arrays, each row is a fixed i, and the pairs i j form a sorted list. After polling a pair, push its neighbour.",
  "For the smallest range covering one number from each list, keep one element per list, and also track the current maximum. The range is from the heap's minimum to that maximum. Advance the minimum's list and update.",
  "And for the Kth largest in a stream, keep the size K min heap from before. After every new number, the answer is simply the top.",
 ]},

quiz([
  ("K largest elements: min-heap or max-heap?", "<b style=\"display:inline\">min-heap</b> of size K", "blue",
   "Quiz time. To keep the K largest elements, min heap or max heap?",
   "A min heap of size K. Its top is the weakest of the K, the one a new number must beat."),
  ("Cost of top K with a size-K heap?", "<b style=\"display:inline\">O(n log K)</b>", "green",
   "What's the time cost of top K with a heap of size K?",
   "n log K, and only K extra space."),
  ("Merge K sorted lists: heap size?", "<b style=\"display:inline\">K</b>: one head per list", "purple",
   "When merging K sorted lists, how big does the heap get?",
   "At most K. It holds one current element from each list."),
]),

recap(["PriorityQueue = min-heap · reverseOrder for max",
       "K largest → min-heap of size K, top = the bar",
       "O(n log K) time, O(K) space · works on streams",
       "Ties: the comparator puts the loser on top",
       "Quickselect: O(n) average, random pivot",
       "K-way merge: heap of heads, O(N log K)"],
  "Let's recap. Java's priority queue is a min heap, and reverse order makes it a max heap. For the K largest, keep a min heap of size K. Its top is the bar to beat. That's n log K time and K space, and it works on streams. For ties, make the comparator put the loser on top. Quickselect is linear on average with a random pivot. And K way merge keeps one head per list in a heap. Now practise the problems listed in your notes!"),
]
