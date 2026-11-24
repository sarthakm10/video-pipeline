from conc import *

TAG = "Java · Comparator and Comparable"
TRACK = "Java Fullstack · Java"
FILE = "Java Comparator and Comparable.mp4"

SLIDES = [
title_slide(0, "Comparator & Comparable", "How Java decides which object comes first",
  "Welcome. Today's concept: Comparable and Comparator.",
  "Sorting numbers is easy, because Java knows that two is less than five. But how should it sort students, or tasks, or intervals? You have to tell it. By the end you'll know the compare contract, the difference between Comparable and Comparator, how to build multi-key comparators, where they're used in collections, and the subtraction bug that interviewers love.",
  pill="JAVA · CONCEPT"),

{"html": H("The compare ", "contract") + row(
   col(box("blue", "compare(a, b) returns", "", 0),
       box("green", "negative", "a comes <b style=\"display:inline\">before</b> b", 0),
       box("gray", "zero", "a and b are <b style=\"display:inline\">equal</b> for ordering", 0),
       box("orange", "positive", "a comes <b style=\"display:inline\">after</b> b", 0), gap=14, style="width:560px"),
   pts([("Only the <u>sign</u> matters, not the size", 1),
        ("Antisymmetric: sign(a, b) = −sign(b, a)", 2),
        ("Transitive: a &lt; b and b &lt; c → a &lt; c", 2),
        ("Consistent: same inputs, same answer", 2),
        ("Break the rules → <code>Comparison method violates its general contract!</code>", 3)], size=31, style="flex:1"), top=True),
 "steps": [
  "Everything starts with one method: compare a, b. It returns a negative number if a should come before b, zero if they're equal for ordering, and a positive number if a should come after b.",
  "Only the sign matters. Minus one and minus a thousand mean exactly the same thing.",
  "A comparison must also follow some rules. Swap the arguments and the sign flips. If a is before b and b is before c, then a is before c. And the same inputs always give the same answer.",
  "Break those rules, and sorting can fail at runtime with a famous error: comparison method violates its general contract.",
 ]},

{"html": H("Comparable: the ", "natural", " order") + row(
   code("""§0 record Student(String name, int marks)
§0     implements Comparable<Student> {
§0   public int compareTo(Student o) {
§0     return Integer.compare(marks, o.marks);
§0   }
§0 }
§1 Collections.sort(list);     // uses compareTo""", 27, style="flex:1"),
   col(box("blue", "inside the class", "<code>java.lang</code> · one method: <code>compareTo(o)</code>", 0),
       box("green", "one natural order", "String: alphabetical · Integer: numeric · LocalDate: by date", 1),
       box("orange", "keep it consistent with equals", "<code>compareTo == 0</code> ⇔ <code>equals</code>", 2), gap=16, style="width:600px"), top=True),
 "steps": [
  "Comparable is the natural order, written inside the class itself. Implement comparable, and write one method, compare to, which compares this object with another.",
  "Now collections dot sort, tree set and tree map all know how to order students. Built in types already have a natural order. Strings are alphabetical, integers numeric, dates chronological.",
  "A class gets only one natural order. And it should agree with equals: compare to returns zero exactly when equals is true. We'll see later why that matters.",
 ]},

{"html": H("Comparator: any order you ", "want") + code("""§0 // 1. a class               2. an anonymous class
§0 // 3. a lambda
§1 Comparator<Student> byName = (a, b) -> a.name().compareTo(b.name());
§2 // 4. a factory method: the modern way
§2 Comparator<Student> byName2 = Comparator.comparing(Student::name);
§3 list.sort(byName);    // or: list.sort(Comparator.comparing(Student::name))""", 28) + row(
   box("blue", "Comparable", "inside the class · one natural order · <code>compareTo(o)</code>", 3, "flex:1"),
   box("green", "Comparator", "outside the class · as many orders as you like · <code>compare(a, b)</code>", 3, "flex:1"), style="margin-top:24px"),
 "steps": [
  "Comparator is an ordering that lives outside the class. You can have as many as you want: by name, by marks, by age. It used to be a separate class or an anonymous class.",
  "Since Java eight, it's usually a lambda. Two students in, a number out.",
  "Even better, use the factory method comparing, with a method reference to the key. It reads exactly like the intent: compare by name.",
  "So the difference: comparable sits inside the class and gives one natural order. Comparator sits outside, and gives any order, even for classes you can't edit.",
 ]},

{"html": H("Multi-key sorting: ", "thenComparing") + code("""§0 Comparator<Student> c = Comparator
§0     .comparingInt(Student::marks).reversed()      // 1. highest marks first
§1     .thenComparing(Student::name);                // 2. tie → alphabetical""", 30) +
   table(["Pair", "Step 1: marks (desc)", "Step 2: name"], [
     (["Riya(90) vs Dev(85)", "90 &gt; 85 → <b>Riya first</b>", "not needed"], 2),
     (["Riya(90) vs Asha(90)", "tie", "Asha &lt; Riya → <b>Asha first</b>"], 3)], size=29) +
   note("<code>thenComparing</code> only runs when the earlier keys are <u>tied</u>", 3),
 "steps": [
  "Real sorts often have several keys. Highest marks first: comparing int on marks, then reversed.",
  "And if two students have the same marks, sort them by name. Then comparing adds that second key.",
  "Riya with ninety against Dev with eighty five. The first key already decides it: Riya first. The second key is never checked.",
  "Riya and Asha both have ninety. The first key ties, so then comparing looks at names. Asha comes first. The rule: each later key only matters when every earlier key is tied.",
 ]},

{"html": H("reversed() and ", "nulls") + row(
   col(box("orange", "careful with reversed()", "it reverses <b style=\"display:inline\">everything chained before it</b>", 0),
       code("""§0 comparing(A).thenComparing(B).reversed()
§0 // → A desc AND B desc""", 25),
       code("""§1 comparing(A, reverseOrder()).thenComparing(B)
§1 // → only A desc""", 25), gap=16, style="flex:1"),
   col(box("red", "a null element", "<code>compare</code> throws <code>NullPointerException</code>", 2),
       code("""§2 Comparator.nullsFirst(naturalOrder())
§2 comparing(Student::city,
§2           nullsLast(naturalOrder()))""", 25), gap=16, style="width:640px"), top=True),
 "steps": [
  "Reversed has a trap. It reverses the whole comparator built so far. So comparing A, then B, then reversed, sorts both A and B descending.",
  "To reverse only one key, pass reverse order as that key's comparator instead.",
  "And nulls. A normal comparator throws a null pointer exception on a null. Wrap it with nulls first or nulls last, either for the whole element or just for one key, like a missing city.",
 ]},

{"html": H("Where comparators are ", "used") + row(
   col(box("blue", "sorting", "<code>list.sort(c)</code> · <code>Arrays.sort(arr, c)</code> (objects only)", 0),
       box("green", "PriorityQueue", "min-heap by default · max-heap: <code>new PriorityQueue&lt;&gt;(Comparator.reverseOrder())</code>", 1), gap=16, style="flex:1"),
   col(box("red", "TreeSet / TreeMap", "<code>compare == 0</code> means <b style=\"display:inline\">duplicate</b> → the element is silently dropped", 2),
       code("""§2 new TreeSet<>(comparing(Student::marks))
§2 // Riya(90) and Asha(90): only one survives!""", 25), gap=16, style="flex:1"), top=True) +
   note("For a TreeSet, add a tie-breaker so different objects never compare as 0", 3),
 "steps": [
  "Where do comparators show up? Sorting, of course: list dot sort and arrays dot sort. Note that arrays of primitives can't take a comparator, only arrays of objects.",
  "Priority queues use one to decide what's on top. By default it's a min heap. For a max heap, pass reverse order. This is the heart of every top k problem.",
  "Tree set and tree map have a subtle rule. They don't use equals. If compare returns zero, they treat the two objects as duplicates, and silently drop one. Sort students by marks only, and two students with ninety means one disappears.",
  "So for a tree set or tree map, always add a tie breaker, like the name or an id, so different objects never compare as zero. That's why comparable should be consistent with equals.",
 ]},

{"html": H("The subtraction ", "bug") + row(
   code("""§0 (a, b) -> a - b                   // looks fine…
§1 a = Integer.MAX_VALUE, b = -1
§1 a - b = overflow → negative!      // says a < b ❌
§2 (a, b) -> Integer.compare(a, b)   // ✅ always safe""", 28, style="flex:1"),
   col(box("red", "why it breaks", "int subtraction can <b style=\"display:inline\">overflow</b> and flip the sign", 1),
       box("green", "use instead", "<code>Integer.compare</code> · <code>comparingInt</code> · <code>Long.compare</code>", 2), gap=16, style="width:560px"), top=True) +
   note("Comparing strings for \"largest number\"? <code>(a, b) -&gt; (b + a).compareTo(a + b)</code>", 3),
 "steps": [
  "Now the bug interviewers love. A comparator written as a minus b looks correct, and usually works.",
  "But take the biggest integer, and minus one. The true difference is bigger than any int can hold, so it overflows and becomes negative. The comparator now says the biggest integer comes first in ascending order. Wrong, and only for extreme values, so tests rarely catch it.",
  "Always use integer dot compare, or comparing int, which compare without subtracting.",
  "And comparators aren't always about size. To arrange numbers into the largest possible number, compare the two concatenations, b plus a against a plus b. The comparator is the whole solution.",
 ]},

quiz([
  ("Comparable or Comparator for a class you can't edit?", "<b style=\"display:inline\">Comparator</b>: it lives outside", "green",
   "Quiz time. You need to sort a class you can't edit. Comparable or Comparator?",
   "Comparator. It lives outside the class, so you don't need to change it."),
  ("TreeSet by marks: two students with 90?", "one is <b style=\"display:inline\">dropped</b> (compare == 0)", "red",
   "A tree set sorted only by marks gets two students with ninety. What happens?",
   "One of them is silently dropped, because compare returned zero and the set treats them as duplicates."),
  ("Why not <code>(a, b) -&gt; a - b</code>?", "<b style=\"display:inline\">overflow</b> flips the sign", "orange",
   "Why shouldn't you write a comparator as a minus b?",
   "Because the subtraction can overflow and flip the sign. Use integer dot compare."),
]),

recap(["compare: negative before · 0 equal · positive after",
       "Comparable: inside, one natural order",
       "Comparator: outside, any number of orders",
       "comparing(…).thenComparing(…) · careful with reversed()",
       "TreeSet/TreeMap: compare == 0 means duplicate",
       "Never a − b: use Integer.compare"],
  "Let's recap. Compare returns negative for before, zero for equal, and positive for after. Comparable lives inside the class and gives one natural order. Comparator lives outside, and you can have as many as you like. Build multi-key orders with comparing and then comparing, and be careful what reversed reverses. In tree sets and tree maps, compare equals zero means a duplicate. And never compare by subtracting. Use integer dot compare. Now practise the problems in your notes!"),
]
