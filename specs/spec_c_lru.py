from conc import *

TAG = "DSA · LRU and LFU Cache"
TRACK = "Java Fullstack · DSA"
FILE = "DSA LRU and LFU Cache.mp4"

S = ("#e5e7eb", "#6b7280")

SLIDES = [
title_slide(0, "LRU & LFU Cache", "A hash map for speed, a linked list for order: every operation in O(1)",
  "Welcome. Today's concept: LRU and LFU caches.",
  "Designing a cache is one of the most common interview questions, because it combines two data structures into something neither can do alone. By the end you'll know eviction policies, why LRU needs a hash map plus a doubly linked list, the operations in constant time, Java's linked hash map shortcut, how LFU adds frequencies, and what real caches do about threads.",
  pill="DSA · CONCEPT"),

{"html": H("Caches and ", "eviction") + row(
   box("blue", "a cache is small", "fixed capacity · when it's full, something must <b style=\"display:inline\">leave</b>", 0, "flex:1"),
   box("green", "LRU", "evict the <b style=\"display:inline\">least recently used</b> · recent use predicts the next use", 1, "flex:1"),
   box("orange", "LFU", "evict the <b style=\"display:inline\">least frequently used</b> · ties → least recent", 2, "flex:1"), top=True) +
   note("The goal: <code>get</code> and <code>put</code> both in O(1)", 3),
 "steps": [
  "A cache keeps a small amount of data close at hand, like recent database rows. It has a fixed capacity, so when it's full and something new arrives, something must leave. The eviction policy decides what.",
  "LRU, least recently used, evicts the entry that hasn't been touched for the longest time. The bet is that what you used recently, you'll use again soon.",
  "LFU, least frequently used, evicts the entry used the fewest times, breaking ties by recency.",
  "And the interview requirement: get and put must both run in constant time.",
 ]},

{"html": H("Why hash map + doubly linked ", "list") +
   graph({"head": (90, 110), "C": (380, 110), "A": (670, 110), "B": (960, 110), "tail": (1250, 110)},
         [("head", "C"), ("C", "A"), ("A", "B"), ("B", "tail")], w=1340, h=200, r=54, step=0,
         colors={"head": S, "tail": S, "C": ("#bbf7d0", "#16a34a"), "B": ("#fecaca", "#dc2626")},
         labels={"C": "most recent", "B": "evict next"}) +
   table(["Need", "Structure"], [
     (["find a key in O(1)", "<b>HashMap</b>: key → node"], 1),
     (["move a node to the front in O(1)", "<b>doubly</b> linked: the node knows prev and next"], 2),
     (["find the eviction victim in O(1)", "it's always <code>tail.prev</code>"], 2)], size=29),
 "steps": [
  "Keep the entries in a list ordered by recency. The front is the most recently used, the back is the next to be evicted. Two dummy nodes, head and tail, mean you never handle an empty list or an end node specially.",
  "A list alone needs linear time to find a key. So add a hash map from each key to its node. Now finding is constant.",
  "And because the list is doubly linked, a node you've found can unlink itself in constant time, using its own prev and next pointers. The victim is always just before the tail.",
 ]},

{"html": H("LRU in ", "code") + code("""§0 int get(int key) {
§0   Node n = map.get(key);
§0   if (n == null) return -1;
§0   remove(n); addFront(n);              // just used → most recent
§0   return n.value;
§0 }
§1 void put(int key, int value) {
§1   Node n = map.get(key);
§1   if (n != null) { n.value = value; remove(n); addFront(n); return; }
§2   if (map.size() == capacity) {
§2     Node lru = tail.prev; remove(lru);
§2     map.remove(lru.key);               // why the node stores its key
§2   }
§1   n = new Node(key, value); map.put(key, n); addFront(n);
§1 }""", 25) + note("<code>remove</code> and <code>addFront</code> are four pointer changes each", 3),
 "steps": [
  "Get looks the key up in the map. If it's there, unlink the node and add it at the front, because it was just used. Then return its value.",
  "Put has two cases. If the key exists, update the value, and move it to the front, since updating also counts as use. Otherwise, create a node, put it in the map, and add it at the front.",
  "Before inserting a new key into a full cache, evict the node just before the tail. Remove it from the list, and from the map. That's why each node stores its own key: to know which map entry to delete.",
  "Remove and add front are a few pointer assignments each, so everything is constant time.",
 ]},

{"html": H("The LinkedHashMap ", "shortcut") + code("""§0 class LRUCache<K, V> extends LinkedHashMap<K, V> {
§0   private final int capacity;
§0   LRUCache(int capacity) {
§1     super(capacity, 0.75f, true);        // true = access order
§0     this.capacity = capacity;
§0   }
§2   @Override protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
§2     return size() > capacity;            // evict after each put
§2   }
§0 }""", 27) + note("In an interview, write it by hand first, then mention this", 3),
 "steps": [
  "Java already has this structure. Linked hash map is a hash map with a doubly linked list running through its entries.",
  "Passing true as the third constructor argument switches from insertion order to access order. Every get moves the entry to the end.",
  "Then override remove eldest entry. After each put, Java asks whether to drop the oldest entry, and you answer yes when the size is over capacity. That's a full LRU cache in a few lines.",
  "Interviewers usually want the hand built version first, to see the pointer work. Mention this afterwards, as what you'd use in real code.",
 ]},

{"html": H("LFU: add ", "frequencies") + row(
   col(box("blue", "key → node", "value + frequency", 0),
       box("purple", "freq → list of keys", "one LRU-ordered list per frequency", 0),
       box("orange", "minFreq", "the smallest frequency present", 1), gap=16, style="width:620px"),
   col(box("green", "get / update", "move the key from list <code>f</code> to list <code>f + 1</code> · if list <code>minFreq</code> emptied → <code>minFreq++</code>", 2),
       box("red", "evict", "the least recent key in list <code>minFreq</code>", 3),
       box("gray", "new key", "goes into list 1 · <code>minFreq = 1</code>", 4), gap=16, style="flex:1"), top=True),
 "steps": [
  "LFU needs more bookkeeping. One map from each key to its node, which holds the value and a use count. A second map from each frequency to a list of keys with that frequency, each kept in LRU order.",
  "And one number: the minimum frequency currently in the cache.",
  "When a key is used, move it from its frequency's list to the next one. If that leaves the minimum frequency's list empty, the minimum goes up by one.",
  "To evict, take the least recent key from the list at the minimum frequency. That handles ties by recency.",
  "A brand new key has been used once, so it goes into list one, and the minimum frequency resets to one. Every step is still constant time.",
 ]},

{"html": H("Real caches and ", "threads") + row(
   box("red", "not thread-safe", "two threads moving nodes at once corrupt the list · <code>synchronized</code> works but serialises everything", 0, "flex:1"),
   box("blue", "Caffeine", "the go-to Java cache · W-TinyLFU · expiry, size limits, stats", 1, "flex:1"),
   box("green", "Redis", "<code>allkeys-lru</code> / <code>allkeys-lfu</code> · approximates by sampling a few keys", 2, "flex:1"), top=True) +
   pts([("follow-ups: add a TTL · count hit rate · cap by memory, not entries", 3),
        ("bugs: forgetting <code>map.remove</code> on evict · not moving on update · capacity 0", 3)], size=31),
 "steps": [
  "The hand built cache isn't thread safe. Two threads moving nodes at the same time can corrupt the list. Making every method synchronized is correct but turns the cache into a bottleneck.",
  "In real Java code, use Caffeine. It's fast, concurrent, and uses a smarter policy called W tiny LFU, with expiry and statistics built in.",
  "Redis offers LRU and LFU eviction too, but approximates them by sampling a few keys rather than keeping an exact list, which saves memory.",
  "Expect follow ups like adding a time to live, or tracking the hit rate. And watch the classic bugs: not removing the evicted key from the map, not moving a node when its value is updated, and a capacity of zero.",
 ]},

quiz([
  ("Why a doubly linked list?", "unlink a found node in <b style=\"display:inline\">O(1)</b>", "blue",
   "Quiz time. Why does LRU need a doubly linked list, not a singly linked one?",
   "So a node found through the map can unlink itself in constant time, using its own prev pointer."),
  ("Why does each node store its key?", "to <code>map.remove</code> it on <b style=\"display:inline\">eviction</b>", "orange",
   "Why does each node store its own key?",
   "So when it's evicted from the list, you know which map entry to remove."),
  ("LFU tie between two keys?", "evict the <b style=\"display:inline\">least recent</b> one", "purple",
   "In LFU, two keys have the same lowest frequency. Which goes?",
   "The least recently used of them."),
]),

recap(["LRU: evict the least recently used",
       "HashMap (find) + doubly linked list (order)",
       "Dummy head and tail · victim = tail.prev",
       "LinkedHashMap(cap, 0.75f, true) + removeEldestEntry",
       "LFU: freq → LRU list, plus minFreq",
       "Real code: Caffeine · Redis approximates"],
  "Let's recap. LRU evicts the least recently used entry. A hash map finds nodes, and a doubly linked list keeps them in recency order, so get and put are both constant time. Dummy head and tail nodes keep the code simple, and the victim is always just before the tail. Java's linked hash map in access order does it for you. LFU adds a list per frequency and tracks the minimum. And in real code, reach for Caffeine. Now practise the problems listed in your notes!"),
]
