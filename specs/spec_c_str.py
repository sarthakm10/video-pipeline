from conc import *

TAG = "Java · Streams API"
TRACK = "Java Fullstack · Java"
FILE = "Java Streams API.mp4"

SLIDES = [
title_slide(0, "Streams API", "Describe what you want from a collection, not how to loop over it",
  "Welcome. Today's concept: the Java Streams API.",
  "Streams let you process a collection as a pipeline: filter this, transform that, collect the result. The code says what you want, and Java handles the looping. By the end you'll understand how a pipeline is built, why it's lazy, the key operations including flat map and reduce, the collectors that do grouping and counting, and the pitfalls that catch people in interviews.",
  pill="JAVA · CONCEPT"),

{"html": H("Loop vs ", "stream") + row(
   code("""§0 List<String> out = new ArrayList<>();
§0 for (String n : names) {
§0   if (n.length() > 3) {
§0     out.add(n.toUpperCase());
§0   }
§0 }""", 28, style="flex:1"),
   code("""§1 List<String> out = names.stream()
§1     .filter(n -> n.length() > 3)
§1     .map(String::toUpperCase)
§1     .toList();""", 28, style="flex:1"), top=True) +
   row(box("blue", "a stream is not a collection", "it stores <b style=\"display:inline\">nothing</b> · it describes a computation over a source", 2, "flex:1"),
       box("orange", "single use", "after a terminal operation it's consumed: <code>IllegalStateException</code>", 2, "flex:1"), style="margin-top:24px"),
 "steps": [
  "Here's a familiar loop. Keep the names longer than three letters, and upper case them. It works, but you have to read it carefully to see what it does.",
  "The stream version reads like the requirement. Filter, then map, then collect into a list. No temporary list to manage, no index.",
  "Two facts to keep straight. A stream is not a collection. It holds no data. It describes a computation over a source, like a list. And a stream can be used only once. After its terminal operation, it's consumed, and using it again throws an illegal state exception.",
 ]},

{"html": H("The ", "pipeline") + row(
   box("blue", "1 · source", "<code>list.stream()</code> · <code>Arrays.stream(a)</code> · <code>Stream.of(…)</code> · <code>IntStream.range(0, n)</code>", 0, "flex:1"),
   box("purple", "2 · intermediate ops", "<code>filter</code> · <code>map</code> · <code>sorted</code> · <code>distinct</code> · <code>limit</code><br>return a <b style=\"display:inline\">new stream</b>, lazy", 1, "flex:1"),
   box("green", "3 · terminal op", "<code>toList</code> · <code>collect</code> · <code>count</code> · <code>forEach</code> · <code>reduce</code><br>produces the result, <b style=\"display:inline\">runs</b> the pipeline", 2, "flex:1"), top=True) +
   note("Zero or more intermediate ops, exactly <u>one</u> terminal op", 3),
 "steps": [
  "Every stream pipeline has three parts. A source: a collection, an array, some values, or a range of numbers.",
  "Then intermediate operations, like filter, map, sorted and distinct. Each one returns a new stream, and none of them does any work yet.",
  "Finally, one terminal operation: collect to a list, count, for each, reduce. That's what produces the result, and it's the moment the pipeline actually runs.",
  "So the shape is always: one source, any number of intermediate steps, and exactly one terminal step.",
 ]},

{"html": H("", "Laziness") + row(
   code("""§0 Stream.of("a", "bb", "ccc", "dddd")
§0     .filter(s -> { print("filter " + s); return s.length() > 1; })
§0     .map(s -> { print("map " + s); return s.toUpperCase(); })
§1     .findFirst();""", 27, style="flex:1"),
   col(box("gray", "without findFirst()", "prints <b style=\"display:inline\">nothing</b>", 0),
       box("green", "with it", "filter a · filter bb · map bb · <b style=\"display:inline\">stop</b>", 1), gap=16, style="width:520px"), top=True) +
   pts([("Elements flow through the pipeline <u>one at a time</u>, not stage by stage", 2),
        ("Short-circuiting ops (<code>findFirst</code>, <code>anyMatch</code>, <code>limit</code>) stop early", 2),
        ("So infinite streams work: <code>Stream.iterate(1, x -&gt; x * 2).limit(10)</code>", 3)], size=31, style="margin-top:22px"),
 "steps": [
  "Laziness is the most important idea in streams. This pipeline prints a message in filter and in map. Without the find first at the end, it prints nothing at all. No terminal operation, no work.",
  "With find first, it prints: filter a, filter b b, map b b, and then it stops. It never even looks at c c c.",
  "Notice the order. Elements go through the whole pipeline one at a time. It's not all filtering first, then all mapping. And short circuiting operations, like find first, any match and limit, stop as soon as they have their answer.",
  "That's why infinite streams work. Stream dot iterate makes an endless sequence, and limit cuts it off. Laziness means only the needed elements are ever produced.",
 ]},

{"html": H("map vs ", "flatMap") + row(
   col(box("blue", "map: one in, one out", "<code>[\"hi\", \"yo\"]</code> → <code>map(String::length)</code> → <code>[2, 2]</code>", 0),
       box("purple", "flatMap: one in, many out, flattened", "<code>[[1, 2], [3]]</code> → <code>flatMap(List::stream)</code> → <code>[1, 2, 3]</code>", 1), gap=18, style="flex:1"),
   code("""§2 // all unique words in a list of sentences
§2 sentences.stream()
§2     .flatMap(s -> Arrays.stream(s.split(" ")))
§2     .distinct()
§2     .toList();""", 24, style="width:740px"), top=True),
 "steps": [
  "Map transforms each element into exactly one new element. Two words in, two lengths out.",
  "Flat map transforms each element into a stream of elements, and then flattens all those streams into one. A list of lists becomes one list. One in, many out.",
  "A classic use: every unique word from a list of sentences. Each sentence becomes a stream of words, flat map joins them, and distinct removes repeats. Whenever you see nested lists, think flat map.",
 ]},

{"html": H("", "reduce") + row(
   col(cells([1, 2, 3, 4], None, None, 0, "values", size=40),
       cells([0, 1, 3, 6, 10], None, None, 1, "acc", size=40, mark={4: "#bbf7d0"}), gap=16),
   code("""§0 int sum = nums.stream()
§0     .reduce(0, (a, b) -> a + b);  // 0 = identity
§2 Optional<Integer> max = nums.stream()
§2     .reduce(Integer::max);        // → Optional""", 25, style="flex:1"), top=True) +
   note("The identity must not change the result: <u>0 for +</u>, <u>1 for ×</u>", 3),
 "steps": [
  "Reduce combines all the elements into one value. It takes an identity, the starting value, and an accumulator that merges the running result with the next element.",
  "Start at zero. Zero plus one is one. Plus two is three. Plus three is six. Plus four is ten.",
  "Without an identity, reduce returns an optional, because an empty stream has no answer. That's how you'd find a maximum.",
  "And the identity must be neutral, leaving any value unchanged. Zero for addition, one for multiplication. Use zero for multiplication and every product is zero. In practice, prefer the ready-made sum, max and count when they exist.",
 ]},

{"html": H("", "Collectors") + table(["Collector", "Result"], [
     (["<code>toList()</code> · <code>toSet()</code>", "a list or a set"], 0),
     (["<code>toMap(k, v)</code>", "a map · <b>throws</b> on duplicate keys unless you pass a merge function"], 0),
     (["<code>joining(\", \")</code>", "one string"], 1),
     (["<code>groupingBy(f)</code>", "<code>Map&lt;key, List&gt;</code>"], 1),
     (["<code>groupingBy(f, counting())</code>", "<code>Map&lt;key, Long&gt;</code>: a frequency count"], 2),
     (["<code>partitioningBy(pred)</code>", "<code>Map&lt;Boolean, List&gt;</code>: always both keys"], 2)], size=28) +
   code("""§3 Map<Character, Long> freq = s.chars().mapToObj(c -> (char) c)
§3     .collect(Collectors.groupingBy(c -> c, Collectors.counting()));""", 26, style="margin-top:20px"),
 "steps": [
  "Collect turns a stream into a container, using a collector. To list and to set are the simple ones. To map builds a map, but watch out: two elements with the same key throw an exception, unless you pass a merge function.",
  "Joining builds one string with a separator. Grouping by groups elements by a key, into a map from each key to a list.",
  "Grouping by with a second collector changes what's stored per key. With counting, you get a frequency map. Partitioning by splits on a true or false test, and always has both keys, even if one list is empty.",
  "That frequency count is a DSA classic. Turn a string into characters, then group by each character, and count. One line instead of a loop with get or default.",
 ]},

{"html": H("Primitive and parallel ", "streams") + row(
   col(box("blue", "IntStream · LongStream · DoubleStream", "no boxing · <code>sum()</code>, <code>average()</code>, <code>max()</code> built in", 0),
       box("gray", "converting", "<code>mapToInt(String::length)</code> · <code>boxed()</code> back to objects", 0), gap=16, style="flex:1"),
   col(box("green", ".parallel(): worth it when", "lots of data · CPU-heavy · splits easily (arrays, ranges) · no shared state", 1),
       box("red", "not worth it when", "small data · I/O · <code>LinkedList</code> · order-sensitive · shared mutable state", 2), gap=16, style="flex:1"), top=True) +
   note("Parallel streams share one ForkJoinPool: <u>measure</u> before you switch", 3),
 "steps": [
  "Stream of Integer boxes every number into an object. Primitive streams, int stream, long stream and double stream, avoid that, and give you sum, average and max directly. Map to int converts, and boxed converts back.",
  "Calling parallel splits the work across cores. It helps with lots of data, CPU heavy work, a source that splits easily like an array or a range, and no shared state between elements.",
  "It hurts with small data, I/O, a linked list that can't be split, operations that depend on order, or lambdas that change shared variables. That last one gives wrong answers, not just slow ones.",
  "And every parallel stream in the application shares one common fork join pool. So measure before switching. Parallel is not automatically faster.",
 ]},

{"html": H("", "Pitfalls") + table(["Trap", "Fix"], [
     (["reusing a stream", "create a new one from the source"], 0),
     (["<code>forEach</code> that adds to an outside list", "use <code>collect</code> / <code>toList()</code>"], 0),
     (["side effects inside <code>map</code> or <code>filter</code>", "keep lambdas pure"], 1),
     (["<code>toMap</code> with duplicate keys", "pass a merge function"], 1),
     (["<code>.toList()</code> result modified", "it's <b>unmodifiable</b>: use <code>Collectors.toList()</code>"], 2),
     (["checked exceptions in a lambda", "wrap them, or use a loop"], 2)], size=29) +
   note("Simple loop with early exits, indices or checked exceptions? A <u>loop</u> is fine", 3),
 "steps": [
  "Let's go through the common traps. Reusing a stream fails, so create a new one. And using for each to add into an outside list is fighting the API. Use collect instead.",
  "Keep lambdas pure. Side effects inside map or filter break with laziness and with parallel streams. And to map with duplicate keys throws, unless you give it a merge function.",
  "Stream dot to list, from Java sixteen, returns an unmodifiable list. Adding to it throws. And lambdas can't throw checked exceptions, so you have to wrap them.",
  "Finally, streams aren't always better. If you need indices, early breaks, or checked exceptions, a plain loop is clearer. Use whichever reads best.",
 ]},

quiz([
  ("A pipeline with no terminal operation does…?", "<b style=\"display:inline\">nothing</b>: streams are lazy", "blue",
   "Quiz time. What does a stream pipeline with no terminal operation do?",
   "Nothing at all. Intermediate operations are lazy, and only a terminal operation runs the pipeline."),
  ("List of lists → one list. Which op?", "<b style=\"display:inline\">flatMap</b>", "purple",
   "You have a list of lists and want one flat list. Which operation?",
   "Flat map. It turns each inner list into a stream and flattens them."),
  ("Count each character's frequency?", "<code>groupingBy(c -&gt; c, counting())</code>", "green",
   "How do you count how often each character appears, with streams?",
   "Grouping by the character itself, with counting as the second collector."),
]),

recap(["Source → intermediate ops → one terminal op",
       "Lazy: nothing runs without a terminal op",
       "Elements flow one at a time · short-circuit ops stop early",
       "map = one to one · flatMap = one to many, flattened",
       "reduce needs a neutral identity · groupingBy + counting",
       "Parallel only for big, CPU-heavy, stateless work"],
  "Let's recap. A stream pipeline is a source, intermediate operations, and exactly one terminal operation. It's lazy, so nothing runs until the terminal operation, and elements flow through one at a time. Map is one to one, and flat map is one to many, flattened. Reduce needs a neutral identity, and grouping by with counting gives you a frequency map. And use parallel streams only for big, CPU heavy work with no shared state. Now practise with the exercises in your notes!"),
]
