from conc import *

TAG = "Java · Multithreading, Part 1"
TRACK = "Java Fullstack · Java"
FILE = "Java Multithreading and Concurrency (Part 1).mp4"

SLIDES = [
title_slide(0, "Multithreading", "Part 1 · threads, races, synchronized, volatile, wait/notify, deadlock",
  "Welcome to multithreading and concurrency, part one.",
  "Threads let a program do several things at once, but they bring a whole new class of bugs. Lost updates, stale values, and deadlocks. In this part: what a thread is, how to start one, its lifecycle, why races happen, and the tools that fix them. Synchronized, volatile, wait and notify. And finally, deadlock.",
  pill="JAVA · CONCEPT"),

{"html": H("Process vs ", "thread") + row(
   col(box("gray", "JVM process", "", 0, "text-align:center"),
       box("orange", "heap (shared)", "objects · arrays · static fields", 0),
       row(box("blue", "main", "own stack", 1, "flex:1"), box("blue", "worker-1", "own stack", 1, "flex:1"),
           box("blue", "worker-2", "own stack", 1, "flex:1"), gap=14), gap=14, style="width:820px"),
   col(box("green", "locals → safe", "each thread's stack is private", 2),
       box("red", "objects → need care", "the heap is shared by every thread", 2), gap=18, style="flex:1"), top=True),
 "steps": [
  "A process is a running program, with its own memory. A thread is a path of execution inside a process. One JVM process can run many threads.",
  "Here's the key. All threads share the process's heap. Objects, arrays, and static fields. But each thread has its own stack, holding its own local variables.",
  "That gives you a simple rule. Local variables live on a thread's own stack, so they're safe. Objects on the shared heap can be touched by several threads at once, so they're where every concurrency bug lives.",
 ]},

{"html": H("Concurrency vs ", "parallelism") + table(["", "Meaning", "Needs several cores?"], [
     (["<b>concurrency</b>", "several tasks <b>in progress</b>, taking turns", "no"], 0),
     (["<b>parallelism</b>", "several tasks running <b>at the same instant</b>", "yes"], 0)], size=31) +
   row(box("blue", "responsiveness", "the UI or server keeps answering", 1, "flex:1"),
       box("green", "throughput", "while one thread waits on I/O, another uses the CPU", 1, "flex:1"),
       box("purple", "speed", "split CPU-heavy work across cores", 1, "flex:1"), style="margin-top:26px") +
   note("Use the <u>highest-level tool</u> that works: executors and concurrent collections before raw threads", 2),
 "steps": [
  "Two words people mix up. Concurrency means several tasks are in progress at once, taking turns, even on one core. Parallelism means they run at the same instant, which needs several cores.",
  "Why use threads at all? Responsiveness: a server keeps answering while slow work runs. Throughput: while one thread waits for the disk or network, another uses the CPU. And speed: heavy work split across cores.",
  "But threads add bugs that only appear under load, and are hard to reproduce. So prefer the highest level tool that works. Executors and concurrent collections, before raw threads and locks.",
 ]},

{"html": H("Creating ", "threads") + row(
   code("""§0 // preferred: a Runnable (often a lambda)
§0 Thread t = new Thread(() -> work(), "worker");
§0 t.start();
§1 // need a result? a Callable, via an executor
§1 Callable<Integer> task = () -> 42;""", 27, style="flex:1"),
   col(box("red", "<code>run()</code>", "a <b style=\"display:inline\">plain method call</b> on the current thread", 2),
       box("green", "<code>start()</code>", "creates a <b style=\"display:inline\">new thread</b> that calls run()", 2),
       box("orange", "start() twice", "<code>IllegalThreadStateException</code>", 3), gap=16, style="width:520px"), top=True),
 "steps": [
  "There are three ways to define a thread's work. Extending Thread works, but implementing Runnable is preferred, because it keeps the task separate from the thread running it. And it's usually just a lambda.",
  "If the task needs to return a value, or throw a checked exception, use a Callable instead, submitted to an executor. That's in part two.",
  "Now the classic trap. Calling run directly doesn't create a thread. It's a plain method call, on the current thread. Only start creates a new thread, which then calls run.",
  "And a thread can only be started once. Calling start twice throws an illegal thread state exception.",
 ]},

{"html": H("The thread ", "lifecycle") + table(["State", "When"], [
     (["<code>NEW</code>", "created, <code>start()</code> not called yet"], 0),
     (["<code>RUNNABLE</code>", "running, <b>or</b> ready and waiting for a CPU"], 0),
     (["<code>BLOCKED</code>", "waiting to enter a <code>synchronized</code> block another thread holds"], 1),
     (["<code>WAITING</code>", "<code>wait()</code>, <code>join()</code> with no timeout"], 1),
     (["<code>TIMED_WAITING</code>", "<code>sleep(ms)</code>, <code>wait(ms)</code>, <code>join(ms)</code>"], 1),
     (["<code>TERMINATED</code>", "<code>run()</code> finished"], 2)], size=29) +
   note("<code>join()</code> waits for a thread · <code>interrupt()</code> politely asks it to stop", 3),
 "steps": [
  "A thread moves through six states. New, before start is called. Then runnable, which covers both running, and ready but waiting for a CPU. Java doesn't separate those two.",
  "Then three ways to wait. Blocked means waiting to get a lock that another thread holds. Waiting means waiting with no time limit, like wait or join. And timed waiting means waiting with a timeout, like sleep.",
  "And terminated, once run finishes, normally or with an exception.",
  "Two useful methods. Join makes one thread wait for another to finish. And interrupt politely asks a thread to stop. It's a request the thread checks for, not a forced kill.",
 ]},

{"html": H("Race ", "conditions") + sub("Two threads run <code>count++</code> at the same time") + table(["Step", "Thread A", "Thread B", "count"], [
     (["1", "reads 5", "", "5"], 0),
     (["2", "", "reads 5", "5"], 0),
     (["3", "adds 1 → 6", "", "5"], 1),
     (["4", "", "adds 1 → 6", "5"], 1),
     (["5", "writes 6", "", "6"], 2),
     (["6", "", "writes 6", "<b>6 ❌ (not 7)</b>"], 2)], size=29) +
   note("<code>count++</code> is three steps: <u>read, add, write</u>", 3),
 "steps": [
  "A race condition is when the result depends on the timing of threads. The classic example is two threads each running count plus plus. Here, both read five.",
  "Both add one, each in its own copy. Both now hold six.",
  "And both write six. One increment is lost. Run this a hundred thousand times on two threads, and you'll get a different wrong answer every run.",
  "The reason is that count plus plus looks like one step, but it's three. Read, add, write. Another thread can slip in between them.",
 ]},

{"html": H("Two kinds of ", "race") + row(
   box("red", "read-modify-write", "read a value, change it, write it back<br><code>count++</code> · <code>balance -= amount</code>", 0, "flex:1"),
   box("orange", "check-then-act", "check a condition, then act on it<br><code>if (!map.containsKey(k)) map.put(k, v);</code>", 1, "flex:1")) +
   row(box("blue", "fix 1: make it atomic", "a lock (<code>synchronized</code>) or an atomic class (<code>AtomicInteger</code>)", 2, "flex:1"),
       box("green", "fix 2: don't share", "each thread its own data, or immutable data", 2, "flex:1"), style="margin-top:22px") +
   note("Code that touches shared mutable state = a <u>critical section</u>", 3),
 "steps": [
  "Races come in two shapes. Read, modify, write. You read a value, change it, and write it back. Count plus plus, or subtracting from a balance.",
  "And check, then act. You check a condition, then act on it. If the map doesn't contain a key, put it. But another thread can insert the key between your check and your put.",
  "There are two fixes. Make the steps atomic, so no thread can slip in between. That's a lock, or an atomic class. Or avoid sharing entirely. Give each thread its own data, or make the data immutable.",
  "Any piece of code that touches shared, mutable state, and must not run in two threads at once, is called a critical section.",
 ]},

{"html": H("", "synchronized") + row(
   code("""§0 private final Object lock = new Object();
§0 void inc() {
§0   synchronized (lock) {     // one thread at a time
§0     count++;
§0   }
§0 }""", 28, style="flex:1"),
   col(box("blue", "locks an object", "never a method · different objects don't block each other", 1),
       box("purple", "static vs instance", "<code>static synchronized</code> locks the Class, instance locks <code>this</code>", 1),
       box("green", "reentrant + visible", "the holder can re-enter · releasing the lock publishes your writes", 2), gap=14, style="width:640px"), top=True) +
   note("Readers need the lock too · never lock on a <u>String literal</u>", 3),
 "steps": [
  "The basic fix is synchronized. Only one thread at a time can hold the lock, so the three steps of count plus plus run together. A private final lock object is safest, because outside code can't grab it.",
  "Two facts people get wrong. A lock belongs to an object, never a method. Two threads using two different counter objects don't block each other at all. And static synchronized locks the class, while instance synchronized locks this. They're different locks.",
  "Synchronized is reentrant: a thread holding a lock can enter another block on the same lock. And it gives visibility too. Releasing a lock publishes your writes, and acquiring it sees them.",
  "So readers need the lock as well, or they may see a stale value. And never lock on a string literal. Literals are shared across the whole JVM, so unrelated code could use the same lock.",
 ]},

{"html": H("", "volatile", " and visibility") + row(
   col(box("orange", "the visibility problem", "a thread may keep reading a <b style=\"display:inline\">cached</b> value and never see another thread's write", 0),
       code("""§1 volatile boolean running = true;
§1 // thread 1: while (running) { … }
§1 // thread 2: running = false;   // now seen""", 27), gap=18, style="flex:1"),
   col(table(["Guarantee", "volatile", "synchronized"], [
     (["visibility", "✅", "✅"], 2),
     (["ordering", "✅", "✅"], 2),
     (["atomic count++", "<b>❌</b>", "✅"], 2)], size=26), style="width:520px"), top=True) +
   note("<code>volatile</code> for flags · <code>synchronized</code> or <u>AtomicInteger</u> for counters", 3),
 "steps": [
  "There's a second, sneakier problem. Visibility. Without synchronisation, a thread may keep reading a cached copy of a field, and never see another thread change it. A loop waiting on a flag can spin forever.",
  "Volatile fixes that. Every read of a volatile field sees the latest write. So one thread can set running to false, and the other is guaranteed to see it.",
  "But compare the guarantees. Volatile gives visibility and ordering. It does not make compound actions atomic. Volatile count plus plus is still a race.",
  "So the rule is: volatile for simple flags, written by one thread and read by others. Synchronized, or an atomic integer, for counters.",
 ]},

{"html": H("wait, notify and producer-", "consumer") + row(
   code("""§0 synchronized void put(T item) throws InterruptedException {
§0   while (queue.size() == capacity) wait();   // full: wait
§0   queue.add(item);
§0   notifyAll();                               // wake consumers
§0 }""", 25, style="flex:1")) +
   table(["", "Thread.sleep()", "obj.wait()"], [
     (["releases the lock?", "<b>no</b>", "<b>yes</b>"], 1),
     (["needs synchronized?", "no", "yes"], 1),
     (["woken by", "time passing", "notify / notifyAll"], 1)], size=28) +
   note("Always wait in a <u>while</u> loop · in real code, use a <code>BlockingQueue</code>", 2),
 "steps": [
  "Sometimes a thread must wait for a condition, like a producer waiting for space in a full buffer. Wait releases the lock and sleeps. Notify all wakes the waiting threads, which then re-check the condition.",
  "Don't confuse wait with sleep. Sleep holds onto any lock it has, and just pauses for a time. Wait releases the lock, must be called while holding it, and is woken by notify.",
  "Two rules. Always wait inside a while loop, not an if, because a thread can wake up without the condition being true. And in real code, use a blocking queue, which does all of this for you.",
 ]},

{"html": H("", "Deadlock") + row(
   graph({"T1": (90, 90), "A": (330, 90), "T2": (330, 300), "B": (90, 300)},
         [("T1", "A"), ("A", "T2"), ("T2", "B"), ("B", "T1")], {"T1": ("#dbeafe", "#2563eb"), "T2": ("#dbeafe", "#2563eb"), "A": ("#ffedd5", "#ea580c"), "B": ("#ffedd5", "#ea580c")},
         w=430, h=390, directed=True, r=46),
   col(table(["Coffman condition", "Break it by"], [
     (["mutual exclusion", "lock-free / immutable data"], 1),
     (["hold and wait", "take all locks at once"], 1),
     (["no preemption", "<code>tryLock</code> with a timeout"], 1),
     (["<b>circular wait</b>", "<b>always lock in the same order</b>"], 2)], size=27), style="flex:1"), top=True) +
   note("Hung program? <code>jstack &lt;pid&gt;</code> shows \"Found one Java-level deadlock\"", 3),
 "steps": [
  "Deadlock. Thread one holds lock B, and waits for A. Thread two holds A, and waits for B. Each waits for the other, forever, doing nothing.",
  "Deadlock needs all four Coffman conditions at once. Mutual exclusion, hold and wait, no preemption, and circular wait. Break any one, and deadlock is impossible.",
  "The most common fix breaks circular wait. Always take locks in the same global order. If every thread locks A before B, no cycle can form.",
  "And if a program hangs, run j stack on its process I D. The thread dump says found one Java level deadlock, and shows which thread holds which lock. Two cousins to know: livelock, where threads keep politely reacting without progress, and starvation, where one thread never gets a turn.",
 ]},

quiz([
  ("<code>t.run()</code> vs <code>t.start()</code>?", "run = plain call · <b style=\"display:inline\">start = new thread</b>", "blue",
   "Quiz time. What's the difference between calling run and calling start on a thread?",
   "Run is a plain method call on the current thread. Start creates a new thread."),
  ("Is <code>volatile int count; count++</code> safe?", "<b style=\"display:inline\">No</b>: visibility, not atomicity", "red",
   "Is a volatile counter, incremented with plus plus, thread safe?",
   "No. Volatile gives visibility, not atomicity. Use an atomic integer or synchronized."),
  ("Most common deadlock fix?", "always lock in the <b style=\"display:inline\">same order</b>", "green",
   "What's the most common way to prevent deadlock?",
   "Always acquire locks in the same global order."),
]),

recap(["Threads share the heap, each has its own stack",
       "start() creates a thread · run() doesn't",
       "count++ = read, add, write → races",
       "synchronized: atomic + visible · locks an object",
       "volatile: visibility only · wait releases, sleep doesn't",
       "Deadlock: lock in one global order"],
  "Let's recap part one. Threads share the heap, but each has its own stack, so objects need care and locals are safe. Start creates a thread, run doesn't. Count plus plus is read, add, write, so it races. Synchronized makes code atomic and visible, and it locks an object. Volatile gives visibility only. Wait releases the lock, sleep doesn't. And prevent deadlock by always locking in the same order. Next time, part two: locks, atomics, thread pools, completable futures, and virtual threads!"),
]
