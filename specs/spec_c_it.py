from conc import *

TAG = "Java · Iterator, Fail-Fast and Fail-Safe"
TRACK = "Java Fullstack · Java"
FILE = "Java Iterator Fail Fast and Fail Safe.mp4"

SLIDES = [
title_slide(0, "Iterators", "What for-each really does, and why changing a list while looping throws",
  "Welcome. Today's concept: iterators, and fail fast versus fail safe.",
  "Every for each loop over a collection is secretly an iterator. Knowing that explains one of the most common Java exceptions, concurrent modification exception, and a classic interview question about fail fast and fail safe. By the end you'll know iterable and iterator, how to make your own class iterable, list iterator, mod count, safe ways to remove while looping, and which collections behave how.",
  pill="JAVA · CONCEPT"),

{"html": H("Iterable and ", "Iterator") + row(
   col(box("blue", "Iterable&lt;T&gt;", "can <b style=\"display:inline\">produce</b> an iterator: <code>iterator()</code> · anything for-each accepts", 0),
       box("green", "Iterator&lt;T&gt;", "one pass over it: <code>hasNext()</code> · <code>next()</code> · <code>remove()</code>", 0),
       box("orange", "the cursor", "sits <b style=\"display:inline\">between</b> elements · <code>next()</code> jumps over one and returns it", 2), gap=16, style="width:680px"),
   code("""§1 for (String s : names) print(s);
§1 // compiles to:
§1 Iterator<String> it = names.iterator();
§1 while (it.hasNext()) {
§1   String s = it.next();
§1   print(s);
§1 }""", 26, style="flex:1"), top=True) +
   note("<code>remove()</code> deletes the element last returned by <code>next()</code> · twice in a row → IllegalStateException", 3),
 "steps": [
  "Two interfaces. An iterable is something that can hand out an iterator. Every collection is one, and so is anything a for each loop accepts. An iterator is a single pass over it: has next, next, and an optional remove.",
  "A for each loop over a collection is just this. The compiler asks for an iterator, and loops while has next is true, calling next each time. Arrays are the exception: those compile to an index loop.",
  "Picture the iterator's cursor sitting between elements. Next jumps over one element and returns it.",
  "Remove deletes the element that next just returned. Calling it twice without a next in between, or before the first next, throws an illegal state exception.",
 ]},

{"html": H("Make your own class ", "iterable") + code("""§0 record Range(int from, int to) implements Iterable<Integer> {
§0   public Iterator<Integer> iterator() {
§1     return new Iterator<>() {
§1       int cur = from;                               // state lives here
§1       public boolean hasNext() { return cur < to; }
§1       public Integer next() {
§2         if (!hasNext()) throw new NoSuchElementException();
§1         return cur++;
§1       }
§1     };
§0   }
§0 }
§3 for (int i : new Range(2, 5)) print(i);   // 2 3 4 · no array stored""", 26),
 "steps": [
  "To make your own class work with for each, implement iterable, and return a new iterator from the iterator method.",
  "The iterator holds the position. Each call to iterator returns a fresh one, so two loops over the same range don't interfere.",
  "Next must throw no such element exception when there's nothing left. That's part of the contract.",
  "And now for each works. This range never stores its numbers, it computes them one at a time. Iterators can be lazy, or even infinite.",
 ]},

{"html": H("ListIterator: both ", "ways") + row(
   code("""§0 ListIterator<String> it = list.listIterator();
§0 while (it.hasNext()) {
§0   String s = it.next();
§1   if (s.isBlank()) it.remove();
§1   else if (s.equals("x")) it.set("y");
§1   else if (s.equals("a")) it.add("a2");     // inserted after "a"
§0 }
§2 while (it.hasPrevious()) print(it.previous());""", 25, style="flex:1"),
   col(box("blue", "for lists only", "<code>hasPrevious</code> · <code>previous</code> · <code>nextIndex</code>", 0),
       box("green", "edit as you go", "<code>remove</code> · <code>set</code> · <code>add</code>, all safely", 1),
       box("purple", "walk back", "from the end: <code>list.listIterator(list.size())</code>", 2), gap=16, style="width:560px"), top=True),
 "steps": [
  "Lists offer a richer iterator, the list iterator. It can also move backwards, and tell you the index of the next element.",
  "It can change the list as it goes. Remove the current element, replace it with set, or insert a new one with add, all without breaking the iteration.",
  "To walk a list backwards, start the list iterator at the size, and call previous.",
 ]},

{"html": H("ConcurrentModificationException and ", "modCount") + row(
   code("""§0 for (String s : list)
§0   if (s.startsWith("x")) list.remove(s);    // 💥 CME
§1 // inside ArrayList's iterator:
§1 if (modCount != expectedModCount)
§1   throw new ConcurrentModificationException();""", 25, style="flex:1"),
   col(box("blue", "modCount", "the list counts structural changes · the iterator remembers the count it started with", 1),
       box("red", "next() checks", "counts differ → someone changed the list behind my back → throw", 1),
       box("orange", "best effort", "remove the <b style=\"display:inline\">second-to-last</b> element → <code>hasNext()</code> is false → no exception, last element skipped", 2), gap=14, style="width:680px"), top=True) +
   note("Nothing to do with threads: one thread is enough", 3),
 "steps": [
  "Here's the classic bug. Loop over a list with for each, and remove from the list inside the loop. You get a concurrent modification exception.",
  "Here's how it's detected. The list keeps a mod count, increased by every add or remove. The iterator copies it when it's created. On every next, it compares them. If they differ, the list was changed behind its back, so it fails fast rather than return garbage.",
  "It's best effort, not a guarantee. Remove the second to last element, and the size shrinks so that has next returns false. The loop just ends, no exception, and the last element is silently skipped.",
  "And despite the name, this has nothing to do with threads. One thread is enough.",
 ]},

{"html": H("Removing while ", "iterating") + table(["Way", "Code"], [
     (["<b>removeIf</b> (best)", "<code>list.removeIf(s -&gt; s.startsWith(\"x\"));</code>"], 0),
     (["the iterator's remove", "<code>if (…) it.remove();</code>"], 1),
     (["index loop, backwards", "<code>for (int i = n − 1; i &gt;= 0; i−−) if (…) list.remove(i);</code>"], 2),
     (["collect, then remove / new list", "<code>list.stream().filter(…).toList()</code>"], 3)], size=29) +
   note("Maps too: <code>map.entrySet().removeIf(e -&gt; e.getValue() == 0)</code>", 4),
 "steps": [
  "So how do you remove safely? The best way is remove if. It's one line, and it's linear for array lists.",
  "Or use an explicit iterator and call its own remove. That keeps the counts in sync.",
  "An index loop works too, if you go backwards, so removing doesn't shift the elements you haven't visited yet.",
  "Or don't modify in place at all: filter into a new list.",
  "Maps work the same way, through their entry set.",
 ]},

{"html": H("Fail-fast vs ", "fail-safe") + table(["Collection", "Iterator", "While another change happens"], [
     (["ArrayList · HashMap · HashSet", "<b>fail-fast</b>", "throws CME (best effort)"], 0),
     (["<code>Collections.synchronizedList</code>", "<b>still fail-fast</b>", "lock it yourself while iterating"], 1),
     (["CopyOnWriteArrayList", "<b>snapshot</b>", "sees the list as it was · writes copy the array"], 2),
     (["ConcurrentHashMap", "<b>weakly consistent</b>", "never throws · may or may not see new changes"], 2)], size=28) +
   note("\"Fail-safe\" = works on a copy or tolerates change · costs memory or freshness", 3),
 "steps": [
  "The ordinary collections, array list, hash map and hash set, have fail fast iterators. Change the collection outside the iterator, and they throw.",
  "A synchronized wrapper doesn't change that. Its iterator is still fail fast, and the documentation says you must hold its lock while iterating.",
  "The concurrent collections are the so called fail safe ones. Copy on write array list iterates over a snapshot: you see the list as it was when the loop began. Concurrent hash map's iterators are weakly consistent: they never throw, and may or may not reflect changes made during the loop.",
  "The trade off: copying costs memory and makes writes expensive, and weak consistency means you might not see the latest data.",
 ]},

{"html": H("Maps, Spliterator and ", "Enumeration") + row(
   box("blue", "iterating a map", "<code>entrySet()</code> gives key and value · <code>keySet()</code> + <code>get</code> = two lookups · or <code>map.forEach((k, v) -&gt; …)</code>", 0, "flex:1"),
   box("green", "Spliterator (Java 8)", "<code>tryAdvance</code> · <code>trySplit</code> into halves → how parallel streams divide work", 1, "flex:1"),
   box("gray", "Enumeration", "the pre-1.2 iterator: <code>Vector</code>, <code>Hashtable</code> · no <code>remove</code> · legacy", 2, "flex:1"), top=True) +
   note("Practice: BST Iterator (a stack, O(h)) · Peeking Iterator (cache the next) · Flatten Nested List", 3),
 "steps": [
  "To loop over a map, use the entry set, which gives you each key and value together. Looping over keys and calling get does a second lookup for every entry. Or use map dot for each with a lambda.",
  "Java eight added the spliterator, an iterator that can split itself in half. That's how parallel streams divide work between threads.",
  "And enumeration is the original iterator, from vector and hashtable. It has no remove, and only shows up in legacy code.",
  "Iterator design problems are popular practice: a binary search tree iterator backed by a stack, a peeking iterator that caches the next value, and flattening a nested list.",
 ]},

quiz([
  ("What does for-each over a List compile to?", "an <b style=\"display:inline\">Iterator</b> loop: hasNext / next", "blue",
   "Quiz time. What does a for each loop over a list compile to?",
   "An iterator loop, calling has next and next."),
  ("list.remove(x) inside for-each?", "<b style=\"display:inline\">ConcurrentModificationException</b> (usually)", "red",
   "What happens if you call list dot remove inside a for each loop over that list?",
   "Usually a concurrent modification exception, because mod count changed."),
  ("Iterate while another thread writes, no exception?", "<b style=\"display:inline\">CopyOnWriteArrayList</b> / ConcurrentHashMap", "green",
   "You need to iterate while other threads keep writing, with no exceptions. What do you use?",
   "Copy on write array list, or concurrent hash map."),
]),

recap(["Iterable hands out Iterators · for-each uses one",
       "Iterator: hasNext · next · remove (the last returned)",
       "modCount mismatch → ConcurrentModificationException",
       "Remove safely: removeIf · it.remove() · backwards index",
       "Fail-fast: ArrayList, HashMap (synchronized ones too)",
       "Fail-safe: COW snapshot · CHM weakly consistent"],
  "Let's recap. An iterable hands out iterators, and for each uses one under the hood. An iterator has has next, next, and remove, which deletes the last element returned. Changing a collection outside its iterator changes mod count, and the next call throws. To remove safely, use remove if, the iterator's own remove, or a backwards index loop. The ordinary collections are fail fast, and the concurrent ones are fail safe. Now practise with the examples in your notes!"),
]
