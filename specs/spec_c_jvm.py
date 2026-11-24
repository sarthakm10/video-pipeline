from conc import *

TAG = "Java · JVM Internals and GC"
TRACK = "Java Fullstack · Java"
FILE = "Java JVM Internals and GC.mp4"

SLIDES = [
title_slide(0, "JVM Internals & GC", "What happens between java Main and your code running, and who cleans up after it",
  "Welcome. Today's concept: JVM internals and garbage collection.",
  "You never free memory in Java, and your code gets faster the longer it runs. Both come from the JVM. Interviewers love asking how. By the end you'll know the JVM's parts, class loading and class loaders, where data lives at runtime, the JIT compiler, how garbage is found and collected, the main collectors, reference types, memory leaks, and the flags and tools to diagnose problems.",
  pill="JAVA · CONCEPT"),

{"html": H("The JVM's ", "parts") + row(
   box("blue", "class loader subsystem", ".class files → loaded, linked, initialised", 0, "flex:1"),
   box("green", "runtime data areas", "heap · metaspace · one stack per thread · PC registers", 1, "flex:1"),
   box("purple", "execution engine", "interpreter · JIT compiler · garbage collector", 2, "flex:1"), top=True) +
   note("javac → bytecode (.class) → the JVM runs it on any OS", 3),
 "steps": [
  "The JVM has three big parts. The class loader subsystem finds class files and prepares them.",
  "The runtime data areas are the memory: the heap, metaspace, and a stack for each thread.",
  "And the execution engine runs the bytecode, with an interpreter, a just in time compiler, and the garbage collector.",
  "Java compiles to bytecode, not machine code, and the JVM on each operating system runs it. That's write once, run anywhere.",
 ]},

{"html": H("Class loading and ", "delegation") + row(
   col(box("blue", "load", "read the bytes · create a <code>Class</code> object", 0),
       box("orange", "link", "verify the bytecode · prepare static fields (defaults) · resolve references", 0),
       box("green", "initialise", "run static initialisers · on <b style=\"display:inline\">first active use</b>", 0), gap=14, style="flex:1"),
   col(box("purple", "bootstrap", "java.lang, java.util … (the JDK core)", 1),
       box("purple", "platform", "other JDK modules", 1),
       box("purple", "application", "your classpath / JARs", 1),
       box("gray", "parent delegation", "ask the parent first · a fake <code>java.lang.String</code> can't replace the real one", 2), gap=14, style="flex:1"), top=True) +
   note("ClassNotFoundException = lookup by name failed · NoClassDefFoundError = missing at run time", 3, "margin-top:14px;font-size:30px"),
 "steps": [
  "A class goes through three steps. Loading reads its bytes. Linking verifies the bytecode is safe, gives static fields their default values, and resolves references. Initialising runs static initialisers, and happens lazily, the first time the class is actually used.",
  "Three class loaders do the loading. Bootstrap loads the JDK's core classes, platform loads the other JDK modules, and application loads your code and its JARs.",
  "Each loader asks its parent first. So core classes always come from the JDK, and a malicious java dot lang dot string on your classpath can never replace the real one.",
  "Two errors to tell apart. Class not found exception: code asked for a class by name, like with class for name, and it wasn't there. No class def found error: it existed when you compiled, but is missing, or failed to initialise, at runtime.",
 ]},

{"html": H("Where data ", "lives") + row(
   code("""§0 void handle() {
§0   int count = 3;                 // stack: primitive local
§1   User u = new User("Asha");     // stack: reference · heap: the object
§2   String s = "hi";               // heap: string pool
§0 }""", 25, style="flex:1"),
   col(box("blue", "stack (per thread)", "one frame per call: locals + operand stack · gone on return", 0),
       box("green", "heap (shared)", "every object and array · managed by the GC", 1),
       box("purple", "metaspace", "class metadata · native memory, not the heap", 2), gap=14, style="width:640px"), top=True) +
   note("Heap: young (Eden + 2 survivors) and old · <code>new</code> is a pointer bump in a thread-local buffer (TLAB)", 3),
 "steps": [
  "Each thread has its own stack. Every method call pushes a frame holding its local variables. Primitives live right there, and the frame disappears when the method returns.",
  "Objects always live on the heap, shared by all threads. A local variable only holds a reference to one. The garbage collector manages the heap.",
  "Class metadata lives in metaspace, which uses native memory rather than the heap. String literals are pooled on the heap.",
  "The heap is split into a young generation, Eden plus two survivor spaces, and an old generation. Allocation is very cheap: each thread has its own buffer in Eden, so new is often just bumping a pointer.",
 ]},

{"html": H("The JIT ", "compiler") + row(
   box("gray", "interpreter", "starts running bytecode immediately", 0, "flex:1"),
   box("blue", "C1", "hot methods → quick compile with profiling", 1, "flex:1"),
   box("green", "C2", "very hot → heavily optimised machine code", 1, "flex:1"), top=True) +
   pts([("<b style=\"display:inline\">inlining</b>: copy small methods into the caller", 2),
        ("<b style=\"display:inline\">escape analysis</b>: an object that never escapes needs no heap allocation", 2),
        ("loop unrolling · dead code removal · deoptimise if an assumption breaks", 2)], size=31) +
   note("Why Java benchmarks need a warm-up: JMH", 3),
 "steps": [
  "When a program starts, the interpreter runs bytecode right away, but slowly.",
  "The JVM counts calls. Hot methods are compiled to machine code by C one, quickly. The hottest are recompiled by C two, using the profile it gathered. This is tiered compilation.",
  "C two's optimisations go beyond a static compiler. It inlines small methods, removes allocations for objects that never escape a method, unrolls loops, and if an assumption later turns out wrong, it throws the compiled code away and starts again.",
  "That's why Java gets faster as it runs, and why benchmarks need a warm up. Use JMH rather than timing a loop yourself.",
 ]},

{"html": H("How GC finds ", "garbage") + row(
   graph({"root": (90, 80), "A": (300, 80), "B": (510, 80), "C": (300, 250), "X": (620, 250), "Y": (800, 250)},
         [("root", "A"), ("A", "B"), ("A", "C"), ("X", "Y"), ("Y", "X")], w=880, h=330, directed=True, r=40, step=0,
         colors={"root": ("#bfdbfe", "#2563eb"), "X": ("#fecaca", "#dc2626"), "Y": ("#fecaca", "#dc2626")},
         labels={"X": "cycle, unreachable"}),
   col(box("blue", "GC roots", "locals on stacks · static fields · active threads · JNI refs", 0),
       box("green", "mark", "everything reachable from a root is alive · the rest is garbage, <b style=\"display:inline\">even cycles</b>", 1),
       box("orange", "then", "sweep · compact · or copy the live objects elsewhere", 2), gap=14, style="flex:1"), top=True) +
   note("Stop-the-world pauses: the app halts while (part of) this runs", 3),
 "steps": [
  "The collector starts from GC roots: local variables on every thread's stack, static fields, active threads, and native references.",
  "It marks everything reachable from them. Whatever isn't marked is garbage. Unlike reference counting, a cycle like x and y here, pointing at each other but unreachable, is still collected.",
  "Then the space is reclaimed. Sweeping frees dead objects in place, compacting slides live objects together, and copying moves live objects to a fresh area.",
  "Some of this needs the application paused, a stop the world pause. Modern collectors work hard to keep those pauses short.",
 ]},

{"html": H("Generations and ", "collectors") + row(
   col(box("blue", "most objects die young", "minor GC: copy Eden's survivors · after a few, promote to old", 0),
       box("orange", "old generation", "collected less often · major / full GC", 0), gap=14, style="width:600px"),
   table(["Collector", "Best for"], [
     (["Serial", "tiny heaps, one CPU"], 1),
     (["Parallel", "throughput: batch jobs"], 1),
     (["<b>G1</b> (default)", "balance · regions · pause target"], 2),
     (["<b>ZGC</b>", "sub-millisecond pauses · huge heaps"], 2)], size=28), top=True) +
   note("Throughput vs latency vs memory: pick two", 3),
 "steps": [
  "Most objects die young: request objects, temporary strings. So the heap is split by age. Minor collections clean Eden often and cheaply, copying the few survivors. Objects that survive several rounds are promoted to the old generation, which is collected less often.",
  "Serial uses one thread, for tiny heaps. Parallel uses all cores and maximises throughput, but with longer pauses.",
  "G1 is the default. It splits the heap into regions, and collects the ones with the most garbage first, aiming for a pause target. ZGC does almost everything concurrently, with pauses under a millisecond even on huge heaps.",
  "Every collector trades throughput, pause time and memory. You can't have the best of all three.",
 ]},

{"html": H("References, leaks and ", "errors") + row(
   table(["Reference", "Cleared when", "Use"], [
     (["strong", "never, while reachable", "normal code"], 0),
     (["soft", "memory runs low", "caches"], 0),
     (["weak", "next GC", "<code>WeakHashMap</code>, metadata"], 0),
     (["phantom", "after finalising", "cleanup (<code>Cleaner</code>)"], 0)], size=26),
   col(box("red", "leaks still happen", "static collections that only grow · listeners never removed · <code>ThreadLocal</code> in pools · unclosed resources", 1),
       box("orange", "OutOfMemoryError", "heap space · metaspace · too many threads", 2),
       box("purple", "StackOverflowError", "recursion too deep · <code>-Xss</code> or iterate", 2), gap=14, style="width:680px"), top=True),
 "steps": [
  "Not all references are equal. Strong references keep objects alive. Soft references are cleared only when memory runs low, useful for caches. Weak references are cleared at the next collection, as in weak hash map. Phantom references signal that an object is gone, for cleanup.",
  "Java can still leak memory. The GC only frees unreachable objects, so anything you keep a reference to stays. Classic cases: static collections that only grow, listeners that are never removed, thread locals in pooled threads, and unclosed resources.",
  "Out of memory errors name what ran out: heap space, metaspace, or native threads. A stack overflow error usually means recursion that's too deep.",
 ]},

{"html": H("Flags and ", "tools") + row(
   code("""§0 -Xms512m -Xmx2g          # initial / max heap
§0 -Xss1m                   # stack per thread
§0 -XX:+UseZGC              # pick a collector
§0 -XX:MaxGCPauseMillis=200 # G1 pause target
§1 -Xlog:gc*                # GC logging
§1 -XX:+HeapDumpOnOutOfMemoryError""", 25, style="flex:1"),
   col(box("blue", "jcmd", "one tool for heap dumps, thread dumps, flags", 2),
       box("green", "JFR + Mission Control", "low-overhead recording of GC, allocation, locks", 2),
       box("purple", "heap dump → Eclipse MAT / VisualVM", "who holds the memory?", 2), gap=14, style="width:640px"), top=True) +
   note("Containers: size the heap as a share of the limit with <code>-XX:MaxRAMPercentage</code>", 3),
 "steps": [
  "The flags you'll meet most: initial and maximum heap size, stack size per thread, choosing a collector, and a pause target for G1.",
  "In production, turn on GC logging, and dump the heap automatically on an out of memory error, so you can investigate afterwards.",
  "For diagnosis, jcmd takes heap and thread dumps. Java flight recorder records GC, allocation and lock behaviour with very little overhead. And a heap dump opened in Eclipse MAT shows exactly which objects hold the memory.",
  "In containers, the JVM respects the container's memory limit. Size the heap as a percentage of it, with max RAM percentage.",
 ]},

quiz([
  ("Two objects point at each other, nothing else does. Collected?", "<b style=\"display:inline\">yes</b>: unreachable from any GC root", "green",
   "Quiz time. Two objects point at each other, and nothing else points at them. Are they collected?",
   "Yes. They're unreachable from any GC root, so the cycle doesn't matter."),
  ("Where does <code>new User()</code> live?", "the <b style=\"display:inline\">heap</b> · the reference is on the stack", "blue",
   "Where does a new user object live?",
   "On the heap. The local variable holding the reference is on the stack."),
  ("Why does parent delegation exist?", "core classes can't be <b style=\"display:inline\">replaced</b>", "purple",
   "Why do class loaders delegate to their parent first?",
   "So the JDK's core classes always win, and can't be replaced by fakes."),
]),

recap(["Class loading: load → link → initialise, parent first",
       "Stack per thread (frames) · heap shared (objects)",
       "JIT: interpreter → C1 → C2, gets faster as it runs",
       "GC: reachable from roots = alive, cycles included",
       "Young dies fast · G1 default · ZGC for tiny pauses",
       "Leaks = references you forgot · jcmd, JFR, heap dumps"],
  "Let's recap. Classes are loaded, linked and initialised, with loaders asking their parents first. Each thread has a stack of frames, and objects live on the shared heap. The JIT compiles hot code, so Java speeds up as it runs. The garbage collector keeps whatever is reachable from GC roots, and frees the rest, cycles included. Most objects die young, G1 is the default, and ZGC keeps pauses tiny. Leaks are references you forgot to drop. Now practise with the examples in your notes!"),
]
