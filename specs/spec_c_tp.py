from conc import *

TAG = "DSA · Two Pointers"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Two Pointers.mp4"
A = [1, 2, 4, 7, 11, 15]


def lr(l, r, step, label, found=False):
    mark = {l: "#bfdbfe", r: "#fecaca"}
    if found:
        mark = {l: "#bbf7d0", r: "#bbf7d0"}
    return cells(A, None, None, step, label, size=40, mark=mark)


SLIDES = [
title_slide(0, "Two Pointers", "Two indices, each moving one way: O(n²) pair checks become one O(n) pass",
  "Welcome. Today's concept: two pointers.",
  "Many array and string questions ask about pairs: two numbers that add up to something, two ends that should match, a fast reader and a slow writer. Checking every pair is quadratic. With two pointers that only move one way, it's linear. By the end, you'll know the three shapes of the pattern, why it never misses the answer, and when it doesn't apply.",
  pill="DSA · CONCEPT"),

{"html": H("The three ", "shapes") + row(
   box("blue", "1 · opposite ends", "<code>l = 0</code>, <code>r = n − 1</code>, walk inward<br>pair sum · palindrome · reverse", 0, "flex:1"),
   box("green", "2 · same direction", "a fast <b style=\"display:inline\">read</b> pointer and a slow <b style=\"display:inline\">write</b> pointer<br>remove duplicates · move zeroes", 1, "flex:1"),
   box("purple", "3 · two arrays", "one pointer in each array<br>merge · intersect", 2, "flex:1"), top=True) +
   note("Every pointer only moves <u>forward</u> (or only inward) → O(n) total", 3),
 "steps": [
  "Two pointers comes in three shapes. The first: opposite ends. One pointer starts at the left, one at the right, and they walk toward each other. That's for pair sums in sorted arrays, palindromes, and reversing.",
  "The second: same direction. A fast pointer reads every element, and a slow pointer marks where the next kept element should be written. That's for removing duplicates or moving zeroes in place.",
  "The third: two arrays, one pointer in each. That's how you merge two sorted arrays, or find their intersection.",
  "What they share: every pointer moves only one way, and never goes back. So in total, the pointers make at most a linear number of moves.",
 ]},

{"html": H("Opposite ends: pair ", "sum") + sub("Sorted array, find two numbers that add up to 15") +
   col(lr(0, 5, 0, "1 + 15 = 16 &gt; 15 → r−−"),
       lr(0, 4, 1, "1 + 11 = 12 &lt; 15 → l++"),
       lr(1, 4, 2, "2 + 11 = 13 &lt; 15 → l++"),
       lr(2, 4, 3, "4 + 11 = <b>15</b> ✅", True), gap=16) +
   note("Too big → move <u>right</u> in · too small → move <u>left</u> in", 4),
 "steps": [
  "Here's the first shape. A sorted array, and we want two numbers that add up to fifteen. Left starts at one, right at fifteen. One plus fifteen is sixteen. Too big.",
  "To make the sum smaller, move right inward. Now one plus eleven is twelve. Too small.",
  "To make it bigger, move left inward. Two plus eleven is thirteen. Still too small, so move left again.",
  "Four plus eleven. Fifteen. Found it, in four steps instead of checking all fifteen pairs.",
  "The rule is always the same. If the sum is too big, move the right pointer in, which can only make it smaller. If it's too small, move the left pointer in. Sorting is what makes each move meaningful.",
 ]},

{"html": H("Why it never ", "misses") + row(
   col(box("orange", "sum too big at (l, r)", "<code>a[l] + a[r] &gt; target</code>", 0),
       box("red", "so r pairs with nothing", "every <code>a[l']</code> with <code>l' ≥ l</code> is even bigger → all those sums are too big", 1),
       box("green", "safe to drop r", "we threw away a whole column of pairs, none of them the answer", 2), gap=18, style="flex:1"),
   code("""// sorted: a[l] ≤ a[l+1] ≤ … ≤ a[r]
§1 a[l]   + a[r] > target
§1 a[l+1] + a[r] > target
§1 a[l+2] + a[r] > target
§1 ...""", 28, style="width:640px"), top=True) +
   note("Each move rules out <u>n pairs at once</u>: that's where O(n²) → O(n) comes from", 3),
 "steps": [
  "Why is it safe to skip pairs? Say the sum at left and right is too big.",
  "The array is sorted, so every element from left onward is at least a of left. Pairing any of them with a of right gives a sum that's at least as big. Too big, every time. So a of right can't be part of any answer with the remaining elements.",
  "That means moving right inward throws away a whole row of pairs, and none of them was the answer. The same argument works the other way when the sum is too small.",
  "That's the real reason it's fast. Each pointer move rules out many pairs at once, not just one. So n squared pairs are covered in n moves.",
 ]},

{"html": H("Same direction: read and ", "write") + sub("Move all zeroes to the end, keeping the order") +
   col(cells([0, 1, 0, 3, 12], None, None, 0, "start · w = 0", size=40),
       cells([1, 0, 0, 3, 12], None, None, 1, "read 1 → write at 0, w = 1", size=40, mark={0: "#bbf7d0"}),
       cells([1, 3, 0, 0, 12], None, None, 2, "read 3 → write at 1, w = 2", size=40, mark={0: "#bbf7d0", 1: "#bbf7d0"}),
       cells([1, 3, 12, 0, 0], None, None, 3, "read 12 → write at 2, w = 3", size=40, mark={0: "#bbf7d0", 1: "#bbf7d0", 2: "#bbf7d0"}), gap=16) +
   note("<code>w</code> = how many elements we've <u>kept</u> so far", 4),
 "steps": [
  "Now the second shape. Move every zero to the end, keeping the other numbers in order, in place. Use a read pointer that visits every element, and a write pointer w, starting at zero.",
  "The reader finds one, which we keep. Swap it to position w, and move w forward.",
  "The reader skips the zero, then finds three. Swap it to position one. w moves to two.",
  "Then twelve goes to position two. Now everything before w is kept, in order, and the zeroes have drifted to the end.",
  "That's the idea behind every read and write problem. The write pointer counts how many elements you've kept. Remove duplicates, remove an element, compress a string: same pattern, different keep rule.",
 ]},

{"html": H("Two arrays: ", "merge") + row(
   col(cells([1, 4, 7], None, None, 0, "a", size=40, mark={0: "#bfdbfe"}),
       cells([2, 3, 9], None, None, 0, "b", size=40, mark={0: "#fecaca"}),
       cells([1, 2, 3, 4, 7, 9], None, None, 1, "out", size=40), gap=16),
   code("""§0 while (i < a.length && j < b.length)
§0   out[k++] = a[i] <= b[j] ? a[i++] : b[j++];
§1 // then copy whatever is left""", 28, style="flex:1"), top=True) +
   box("orange", "in-place merge into the bigger array?", "fill from the <b style=\"display:inline\">back</b>: biggest first, so you never overwrite unread values", 2, "margin-top:28px"),
 "steps": [
  "The third shape: one pointer in each sorted array. Compare the two front elements, take the smaller one, and move only that pointer forward.",
  "When one array runs out, copy whatever is left of the other. That's the merge step of merge sort, in linear time.",
  "One twist interviewers like. If the first array has empty space at the end, and you must merge into it in place, fill from the back. Compare the largest elements and write them at the end. That way you never overwrite a value you haven't read yet.",
 ]},

{"html": H("3Sum: fix one, then ", "two pointers") + code("""§0 sort(a);
§0 for (int i = 0; i < n - 2; i++) {
§2   if (i > 0 && a[i] == a[i - 1]) continue;      // skip duplicate anchors
§1   int l = i + 1, r = n - 1;
§1   while (l < r) {
§1     int s = a[i] + a[l] + a[r];
§1     if (s == 0) { record(); l++; r--; /* skip duplicates */ }
§1     else if (s < 0) l++; else r--;
§1   }
§0 }""", 30) + note("O(n log n) sort + O(n²) loops · k-Sum adds one loop per extra number", 3),
 "steps": [
  "Two pointers also stacks. For three numbers that sum to zero, sort first, then fix one number as an anchor.",
  "For each anchor, the other two must sum to minus the anchor. That's just the pair sum from earlier, on the part of the array to the right. Opposite ends, moving inward.",
  "The tricky part is duplicates. Skip an anchor that equals the previous one, and after a match, move both pointers past repeated values. Otherwise the same triple is reported twice.",
  "Overall that's quadratic, much better than cubic. Four sum adds one more loop on top. Each extra number costs one more factor of n.",
 ]},

{"html": H("Greedy moves: ", "water") + row(
   box("blue", "container with most water", "area = width × shorter wall<br>move the <b style=\"display:inline\">shorter</b> wall inward: the taller one can't help while the short one limits it", 0, "flex:1"),
   box("green", "trapping rain water", "water above i = min(maxLeft, maxRight) − h[i]<br>move the side with the <b style=\"display:inline\">smaller max</b>: its water level is already known", 1, "flex:1")) +
   box("purple", "Dutch flag: three pointers", "<code>low</code> · <code>mid</code> · <code>high</code> sort 0s, 1s and 2s in one pass", 2, "margin-top:26px"),
 "steps": [
  "Some two pointer problems need a greedy argument for which side to move. Container with most water: the area is the width times the shorter wall. Moving the taller wall inward can never help, because the short wall still limits the height, and the width shrinks. So always move the shorter wall.",
  "Trapping rain water is similar. The water above a bar is the smaller of the highest wall on its left and on its right, minus its height. Whichever side has the smaller maximum, its water level is already decided. So compute it, and move that side.",
  "And sometimes you need three pointers. To sort an array of zeros, ones and twos in one pass, low marks where the next zero goes, high where the next two goes, and mid scans the unknown middle.",
 ]},

{"html": H("When to use it, and when ", "not") + table(["Clue", "Choice"], [
     (["sorted array · find a pair or triple", "opposite ends"], 0),
     (["in place · remove / keep / compress", "read and write pointers"], 0),
     (["two sorted inputs", "one pointer each"], 1),
     (["unsorted, need original indices", "<b>HashMap</b> (Two Sum), not two pointers"], 2),
     (["contiguous range with a condition", "<b>sliding window</b> (a two pointer cousin)"], 2)], size=30) +
   pts([("Use <code>l &lt; r</code>, not <code>l &lt;= r</code>, for pairs", 3), ("Skip duplicates <u>after</u> a match, not before", 3),
        ("Sorting costs O(n log n) and loses the original indices", 3)], size=31, style="margin-top:22px"),
 "steps": [
  "So how do you choose? A sorted array where you look for a pair or triple: opposite ends. Rearranging in place, keeping some elements and dropping others: read and write pointers.",
  "Two sorted inputs: one pointer in each.",
  "But if the array is unsorted and you need the original indices, like the classic Two Sum, sorting would lose them. Use a hash map instead. And if the question is about a contiguous range, that's a sliding window, which is really two pointers moving in the same direction.",
  "Three common bugs. For pairs, loop while left is less than right, not less or equal, or an element pairs with itself. Skip duplicates after recording a match. And remember sorting costs n log n, and loses the original positions.",
 ]},

quiz([
  ("Sorted pair sum is too small. Which pointer moves?", "<b style=\"display:inline\">left</b> moves right, to grow the sum", "blue",
   "Quiz time. In a sorted pair sum, the current sum is too small. Which pointer moves?",
   "The left pointer moves right, because that's the only way to make the sum bigger."),
  ("Two Sum on an unsorted array, return indices?", "<b style=\"display:inline\">HashMap</b>: sorting loses indices", "red",
   "Two Sum on an unsorted array, and you must return the original indices. Two pointers?",
   "No. Sorting would lose the indices, so use a hash map in one pass."),
  ("Container with most water: which wall moves?", "the <b style=\"display:inline\">shorter</b> one", "green",
   "Container with most water. Which wall do you move inward?",
   "The shorter one. Moving the taller wall can never increase the area."),
]),

recap(["Three shapes: opposite ends · read/write · two arrays",
       "Pointers only move one way → O(n)",
       "Each move rules out a whole row of pairs",
       "Write pointer = count of kept elements",
       "3Sum: sort, fix one, pair-sum the rest, skip duplicates",
       "Unsorted + indices → HashMap · contiguous → window"],
  "Let's recap. Two pointers has three shapes: opposite ends, read and write, and one pointer per array. Pointers only move one way, so it's linear. In a sorted array, each move safely rules out a whole row of pairs. The write pointer counts what you've kept. For three sum, sort, fix one number, run the pair sum on the rest, and skip duplicates. And if the array is unsorted and you need indices, use a hash map. Now practise the problems listed in your notes!"),
]
