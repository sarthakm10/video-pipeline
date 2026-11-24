from conc import *

TAG = "DSA · Two Heaps"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Two Heaps.mp4"

SLIDES = [
title_slide(0, "Two Heaps", "A max-heap for the small half, a min-heap for the big half: the middle is always on top",
  "Welcome. Today's concept: two heaps.",
  "Numbers arrive one at a time, and after each one you need the median. Sorting after every number is far too slow. The trick is to split the numbers into a smaller half and a bigger half, each kept in its own heap, so the middle is always sitting on top. By the end you'll know the two invariants, how to add and rebalance, sliding window medians, and how the same idea solves IPO.",
  pill="DSA · CONCEPT"),

{"html": H("The ", "idea") + row(
   col(box("blue", "low: a max-heap", "the smaller half · its top = the <b style=\"display:inline\">largest</b> small number", 0),
       box("green", "high: a min-heap", "the bigger half · its top = the <b style=\"display:inline\">smallest</b> big number", 0),
       box("purple", "the median", "odd count → <code>low.peek()</code> · even → average of both tops", 1), gap=16, style="flex:1"),
   cells([1, 3, 4, "|", 6, 8], None, None, 0, "sorted", size=40, mark={2: "#bfdbfe", 4: "#bbf7d0"}), top=True) +
   note("The two tops are the two middle numbers: O(1) to read", 2),
 "steps": [
  "Split the numbers into two halves. The smaller half goes into a max heap, so its top is the largest of the small numbers. The bigger half goes into a min heap, so its top is the smallest of the big numbers.",
  "Those two tops sit right in the middle. With an odd count, keep the extra number in the low heap, and the median is its top. With an even count, average the two tops.",
  "So the median is always readable in constant time. The work is in keeping the halves correct as numbers arrive.",
 ]},

{"html": H("Two ", "invariants") + row(
   box("orange", "1 · order", "every number in low ≤ every number in high<br><code>low.peek() &lt;= high.peek()</code>", 0, "flex:1"),
   box("purple", "2 · size", "<code>low.size() == high.size()</code> or one more<br>(low holds the extra)", 1, "flex:1"), top=True) +
   code("""§2 void add(int x) {
§2   low.offer(x);                    // 1. always into low
§2   high.offer(low.poll());          // 2. its largest moves up: order fixed
§3   if (high.size() > low.size())    // 3. too many in high?
§3     low.offer(high.poll());        //    move the smallest back
§2 }
§4 double median() {
§4   return low.size() > high.size() ? low.peek()
§4        : (low.peek() + (double) high.peek()) / 2;
§4 }""", 27, style="margin-top:22px"),
 "steps": [
  "Two rules must always hold. First, order: everything in low is less than or equal to everything in high.",
  "Second, size: the heaps are equal, or low has one more.",
  "Adding a number keeps both rules with a simple dance. Always push into low first. Then move low's largest into high. Whatever was in the wrong place has now crossed over, so the order rule holds.",
  "Then, if high got bigger than low, move high's smallest back. Now the size rule holds too. Each add is a few heap operations, so log n.",
  "And the median reads the tops. Note the cast to double, so the average of two ints isn't truncated.",
 ]},

{"html": H("Watch it ", "run") + table(["add", "low (max-heap)", "high (min-heap)", "median"], [
     (["5", "5", "—", "5"], 0),
     (["2", "2", "5", "3.5"], 1),
     (["8", "2, 5", "8", "5"], 2),
     (["1", "1, 2", "5, 8", "3.5"], 3),
     (["9", "1, 2, 5", "8, 9", "5"], 4)], size=30),
 "steps": [
  "Let's run it. Add five. It goes into low, crosses to high, then comes back because high is bigger. Low holds five. The median is five.",
  "Add two. It ends up in low, five stays in high. Equal sizes, so the median is the average, three point five.",
  "Add eight. Eight goes high, and five comes back down to keep low one bigger. The median is five.",
  "Add one. It stays low, and five moves up. The median is two plus five over two, three point five.",
  "Add nine. Low gets five back as its extra element. Median five. Every step was log n, and the answer was always on top.",
 ]},

{"html": H("Sliding window ", "median") + row(
   col(box("blue", "add the new element", "same as before", 0),
       box("red", "remove the one leaving", "a heap can't remove from the middle quickly", 1),
       box("green", "lazy deletion", "remember it in a map · delete only when it reaches the <b style=\"display:inline\">top</b>", 2),
       box("purple", "or", "two <code>TreeMap</code>s / <code>TreeSet</code>s with indices: O(log k) removal", 3), gap=14, style="flex:1"),
   box("orange", "sizes count only live elements", "track a <code>balance</code> by hand, because the heaps still hold the 'deleted' ones", 2, "width:520px"), top=True),
 "steps": [
  "Now the window version: the median of every window of size k. Adding the new element is the same as before.",
  "But the element leaving the window must be removed, and a heap can't remove from its middle efficiently. Priority queue's remove is linear.",
  "The common trick is lazy deletion. Note the outgoing number in a hash map. Leave it in the heap, and only throw it away when it reaches a heap's top. Since only tops matter for the median, that's enough. The catch: heap sizes now include dead entries, so track the real balance yourself.",
  "The alternative is two sorted sets, like tree sets of value and index pairs, which can remove any element in log k.",
 ]},

{"html": H("Two heaps as a ", "gate") + sub("IPO: start with capital w, finish at most k projects, maximise capital") + row(
   col(box("gray", "min-heap by cost", "projects you <b style=\"display:inline\">can't</b> afford yet", 0),
       box("green", "max-heap by profit", "projects you <b style=\"display:inline\">can</b> afford", 0), gap=16, style="width:520px"),
   code("""§1 for (int i = 0; i < k; i++) {
§1   while (!byCost.isEmpty() && byCost.peek()[0] <= w)
§1     byProfit.offer(byCost.poll());   // now affordable
§2   if (byProfit.isEmpty()) break;
§2   w += byProfit.poll()[1];           // take the best
§1 }""", 26, style="flex:1"), top=True) +
   note("One heap waits at the gate, the other picks the best that passed", 3),
 "steps": [
  "Two heaps aren't only for medians. In the IPO problem, you start with some capital, and can do at most k projects. Each needs a minimum capital, and adds a profit. Keep all projects in a min heap by cost. Those are the ones still locked.",
  "Before each pick, move every project you can now afford into a max heap by profit.",
  "Then take the most profitable one. Your capital grows, which unlocks more projects for the next round. If nothing is affordable, stop.",
  "So one heap is a gate, releasing items as a threshold rises, and the other picks the best of what's been released.",
 ]},

{"html": H("Recognise it, avoid the ", "traps") + pts([
     ("“median of a stream” · “middle of a changing set” → two heaps", 0),
     ("any percentile: change the size rule (e.g. low holds 90%)", 1),
     ("int overflow: <code>(a + b) / 2</code> → <code>(a + (double) b) / 2</code>", 2),
     ("max-heap: <code>Collections.reverseOrder()</code>, not <code>(a, b) -> b - a</code>", 2),
     ("static data? just sort once", 3)], size=33),
 "steps": [
  "The signal is a median, or any middle value, of data that keeps changing.",
  "It also generalises. For the ninetieth percentile, change the size rule so low holds ninety percent of the elements.",
  "Two classic bugs. Adding two large ints overflows, so convert to double before adding. And building a max heap with b minus a can also overflow. Use reverse order.",
  "And if the data doesn't change, don't bother. Sort once and read the middle.",
 ]},

quiz([
  ("Which heap holds the smaller half?", "a <b style=\"display:inline\">max</b>-heap: its top is the middle", "blue",
   "Quiz time. Which kind of heap holds the smaller half of the numbers?",
   "A max heap, so its top is the largest small number, right at the middle."),
  ("Odd count: where's the median?", "<code>low.peek()</code> (low holds the extra)", "purple",
   "With an odd number of elements, where's the median?",
   "On top of the low heap, which holds the extra element."),
  ("Cost per add?", "<b style=\"display:inline\">O(log n)</b> · median O(1)", "green",
   "What does each add cost, and reading the median?",
   "Each add is log n, and reading the median is constant."),
]),

recap(["low = max-heap (small half) · high = min-heap (big half)",
       "Order: low.peek() ≤ high.peek()",
       "Size: equal, or low has one more",
       "Add: into low → move top to high → rebalance",
       "Window: lazy deletion, or two TreeSets",
       "Gate pattern: min-heap by cost, max-heap by profit"],
  "Let's recap. Two heaps split the data: a max heap for the smaller half, and a min heap for the bigger half. Keep the order rule, low's top at most high's top, and the size rule, equal or low one bigger. To add, push into low, move its top to high, and rebalance. For sliding windows, use lazy deletion or sorted sets. And the gate pattern uses one heap to release items and another to pick the best. Now practise the problems listed in your notes!"),
]
