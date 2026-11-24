from conc import *

TAG = "Day 94 · Revision: Java and Collections"
TRACK = "Java Fullstack · Revision"
FILE = "Day 94 Revision Java and Collections.mp4"

SLIDES = [
title_slide(94, "Revision: Java & Collections", "The core Java questions every backend interview asks",
  "Welcome to day ninety four: revision, starting with core Java and collections.",
  "No new topics today. Instead we go back over the questions interviewers ask most, so you can answer them out loud, without notes. We'll cover how to revise well, the object oriented basics, how a HashMap really works, an LRU cache in a few lines, thread safety including the happens before rule, and streams. Pause after each question and try answering before I do.",
  pill="DAY 94 · REVISION"),

{"html": H("How to ", "revise") + row(
   box("blue", "clear the backlog", "Backlog &amp; Stats lists every unchecked topic and \"What I Missed\" note", 0, "flex:1"),
   box("green", "answer out loud", "under a minute per question · then check with the flashcards", 1, "flex:1"),
   box("orange", "find your weak five", "write them down · give each one a slot before the interviews", 2, "flex:1"), top=True) +
   note("If you can't start an answer within a minute, it goes on the weak list", 2),
 "steps": [
  "Start with your backlog. The Backlog and Stats page in the sidebar collects every topic you haven't ticked and every What I Missed note. Most take fifteen minutes to clear.",
  "Then answer questions out loud, in under a minute each. Reading an answer feels like knowing it. Saying it is what an interview actually tests. Check yourself with the flashcards afterwards.",
  "Finally, write down your five weakest topics and give each one a slot in the remaining days. If you can't start an answer within a minute, it belongs on that list.",
 ]},

{"html": H("OOP and ", "equality") + table(["Question", "Answer in one breath"], [
     (["Four OOP pillars?", "encapsulation · inheritance · polymorphism · abstraction"], 0),
     (["<code>==</code> vs <code>equals()</code>?", "same object vs same value"], 1),
     (["Override <code>equals</code>, must you override…?", "<code>hashCode</code>: equal objects need equal hash codes"], 1),
     (["Why is <code>String</code> immutable?", "safe to share in the pool, as map keys, across threads"], 2),
     (["Abstract class vs interface?", "shared state and code vs a contract many classes can sign"], 2)], size=27),
 "steps": [
  "The four pillars: encapsulation hides data behind methods, inheritance reuses a parent's code, polymorphism lets one call behave differently per object, and abstraction shows what something does, not how.",
  "Double equals compares references: is it the very same object? The equals method compares values. And if you override equals, you must override hash code too, because equal objects must land in the same hash bucket.",
  "Strings are immutable, so the JVM can share them in the string pool and use them safely as map keys and across threads. An abstract class can hold state and shared code. An interface is a contract that any class can sign, even one that already extends something else.",
 ]},

{"html": H("HashMap ", "internals") + row(
   code("""§0 put(key, value)
§0   → h = hash(key)   → index = h & (n - 1)
§1   → bucket empty?   store it
§1   → else walk it:   equals()? replace : append
§2   → 8+ in a bucket  → becomes a red-black tree
§3   → size > 0.75 × n → double the table, rehash""", 24, style="flex:1"),
   col(box("blue", "average O(1)", "a good hashCode spreads keys over buckets", 0),
       box("purple", "worst case", "one crowded bucket · O(log n) once it's a tree", 2),
       box("red", "mutable keys", "change a key after put → its hash changes → lost", 3), gap=14, style="width:500px"), top=True),
 "steps": [
  "This is the most asked collections question. A HashMap is an array of buckets. To put a key, it hashes the key and uses the hash to pick a bucket.",
  "If the bucket is empty, the entry goes straight in. If not, it walks the entries there: if one equals the key, the value is replaced, otherwise the new entry is added.",
  "When one bucket collects eight or more entries, it turns into a red black tree, so even a bad hash degrades to log n, not linear time.",
  "When the map is three quarters full, the table doubles and every entry is rehashed. And never change a key after putting it: its hash changes, and the map can't find it any more.",
 ]},

{"html": H("An LRU cache in eight ", "lines") + row(
   code("""§0 class LruCache<K, V> extends LinkedHashMap<K, V> {
§0   private final int capacity;
§1   LruCache(int capacity) {
§1     super(16, 0.75f, true);        // true = access order
§1     this.capacity = capacity;
§1   }
§2   @Override
§2   protected boolean removeEldestEntry(Map.Entry<K, V> e) {
§2     return size() > capacity;      // evict the least recent
§2   }
§0 }""", 22, style="flex:1"),
   col(box("blue", "access order", "every get moves the entry to the end", 1),
       box("green", "removeEldestEntry", "asked after each put · true → drop the oldest", 2),
       box("orange", "from scratch", "HashMap + doubly linked list · both O(1)", 3), gap=14, style="width:480px"), top=True),
 "steps": [
  "Least recently used caches come up constantly. In Java, a LinkedHashMap almost gives you one for free.",
  "Pass true as the third constructor argument, and the map keeps access order: every get moves that entry to the end, so the front is always the least recently used.",
  "Then override remove eldest entry. The map calls it after every put, and returning true drops the oldest entry once you're over capacity.",
  "If the interviewer says no LinkedHashMap, build the same thing yourself: a HashMap from key to node, plus a doubly linked list for the order. Both operations stay constant time.",
 ]},

{"html": H("Thread safety and ", "happens-before") + row(
   col(code("""§0 count++   // read → add 1 → write
§0 // two threads read 5 → both write 6""", 23),
       table(["Tool", "Gives you"], [
         (["<code>synchronized</code>", "one thread at a time + visibility"], 1),
         (["<code>AtomicInteger</code>", "lock-free atomic counters"], 1),
         (["<code>volatile</code>", "visibility only · not atomic"], 2),
         (["<code>ConcurrentHashMap</code>", "safe map · locks per bucket · no null keys"], 2)], size=25), gap=16, style="flex:1"),
   col(box("purple", "happens-before", "if A happens-before B, B sees everything A wrote", 3),
       box("blue", "you get it from", "unlock → next lock · volatile write → next read · start() and join()", 3),
       box("red", "without it", "another thread may see a stale value, forever", 3), gap=14, style="width:500px"), top=True),
 "steps": [
  "Why isn't count plus plus thread safe? Because it's three steps: read, add one, write. Two threads can both read five and both write six, losing an update.",
  "Synchronized lets one thread in at a time, and also makes its writes visible to the next thread. AtomicInteger does the same for counters, without locks.",
  "Volatile only guarantees visibility, not atomicity, so a volatile count plus plus is still broken. ConcurrentHashMap is the thread safe map: it locks small parts of the table instead of the whole thing, and it rejects null keys and values.",
  "Behind all of this is the Java memory model's happens before rule. If action A happens before action B, then B sees everything A wrote. You get that ordering from releasing and then taking the same lock, from a volatile write and a later read, and from starting or joining a thread. Without it, a thread may keep seeing a stale value.",
 ]},

{"html": H("Streams and choosing a ", "collection") + row(
   code("""§0 orders.stream()                        // source
§0   .filter(o -> o.total() > 100)         // intermediate (lazy)
§0   .map(Order::customer)
§0   .distinct()
§0   .toList();                           // terminal: runs it all""", 22, style="flex:1"),
   col(table(["Need", "Pick"], [
     (["index access, append", "<code>ArrayList</code>"], 1),
     (["key → value, fast", "<code>HashMap</code>"], 1),
     (["keys kept sorted", "<code>TreeMap</code>"], 2),
     (["stack or queue", "<code>ArrayDeque</code>"], 2),
     (["always take the smallest", "<code>PriorityQueue</code>"], 2)], size=25), style="width:560px"), top=True),
 "steps": [
  "A stream pipeline has a source, intermediate operations like filter and map, and a terminal operation like toList. Intermediate operations are lazy: nothing runs until the terminal operation asks for results.",
  "Interviewers also love asking which collection you'd pick. Index access and appending: ArrayList. Fast lookup by key: HashMap.",
  "Keys kept in sorted order: TreeMap. A stack or a queue: ArrayDeque, not the old Stack class. And when you always need the smallest item next: a PriorityQueue.",
 ]},

quiz([
  ("Two equal objects, different hashCodes: what breaks?", "<b style=\"display:inline\">HashMap / HashSet</b> lookups", "red",
   "Quiz time. Two objects are equal, but have different hash codes. What breaks?",
   "Hash based collections. The map looks in the wrong bucket and can't find the key."),
  ("Is <code>volatile int count; count++</code> safe?", "<b style=\"display:inline\">no</b>: visible, not atomic", "orange",
   "Is a volatile count plus plus thread safe?",
   "No. Volatile makes the value visible, but the increment is still three separate steps."),
  ("LinkedHashMap flag for an LRU cache?", "<b style=\"display:inline\">accessOrder = true</b>", "blue",
   "What turns a LinkedHashMap into the start of an LRU cache?",
   "Access order set to true, plus overriding remove eldest entry."),
]),

recap(["Revise out loud · list your weak five",
       "== vs equals · equals needs hashCode",
       "HashMap: hash → bucket → tree at 8 → resize at 0.75",
       "LRU: LinkedHashMap(access order) + removeEldestEntry",
       "count++ isn't atomic · volatile = visibility · happens-before",
       "Streams are lazy · pick the right collection"],
  "Let's recap. Revise by answering out loud, and keep a list of your five weakest topics. Double equals compares references, equals compares values, and overriding equals means overriding hash code. A HashMap hashes to a bucket, turns crowded buckets into trees, and resizes at three quarters full. An LRU cache is a LinkedHashMap in access order with remove eldest entry. Count plus plus isn't atomic, volatile only gives visibility, and happens before tells you when one thread sees another's writes. Tomorrow: revising Spring, Kafka and the cloud."),
]
