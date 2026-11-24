from conc import *

TAG = "Java · Multithreading and Concurrency, Part 2"
TRACK = "Java Fullstack · Java"
FILE = "Java Multithreading and Concurrency (Part 2).mp4"

SLIDES = [
title_slide(0, "Multithreading", "Part 2: locks, atomics, thread pools, CompletableFuture and virtual threads",
  "Welcome to part two of multithreading and concurrency.",
  "In part one we used the basic tools: threads, synchronized, volatile, wait and notify. They work, but real code rarely creates threads by hand. Today we move to the java dot util dot concurrent toolkit: explicit locks, atomic variables, thread pools, completable futures, concurrent collections, synchronizers, and Java twenty-one's virtual threads.",
  pill="JAVA · CONCEPT · PART 2"),

{"html": H("Explicit locks: ", "ReentrantLock") + row(
   code("""§0 private final Lock lock = new ReentrantLock();
§0
§0 void transfer() {
§0   lock.lock();
§0   try {
§0     // critical section
§1   } finally {
§1     lock.unlock();        // ALWAYS in finally
§1   }
§0 }""", 28, style="flex:1"),
   col(box("blue", "what synchronized can't do", "", 2),
       box("green", "tryLock(timeout)", "give up instead of waiting forever → no deadlock", 2),
       box("purple", "lockInterruptibly()", "a waiting thread can be interrupted", 2),
       box("orange", "new ReentrantLock(true)", "fair: longest waiter goes first", 2), gap=14, style="width:600px"), top=True),
 "steps": [
  "First, explicit locks. A reentrant lock does the same job as synchronized, but you call lock and unlock yourself.",
  "Which means you must always unlock in a finally block. If the critical section throws and you skip unlock, every other thread waits forever.",
  "So why use it? Because it can do things synchronized can't. Try lock with a timeout lets a thread give up instead of waiting forever, which is a clean way to avoid deadlock. Lock interruptibly lets a waiting thread be cancelled. And a fair lock serves threads in the order they arrived.",
 ]},

{"html": H("Many readers, one ", "writer") + row(
   col(box("green", "readLock()", "many threads can hold it <b style=\"display:inline\">at once</b>", 0),
       box("red", "writeLock()", "exclusive: no readers, no other writer", 0),
       box("gray", "good for", "a cache read far more often than it's written", 1), gap=16, style="flex:1"),
   col(box("purple", "Condition", "named wait queues on one lock: <code>notFull.await()</code> · <code>notEmpty.signal()</code>", 2),
       box("blue", "vs wait / notify", "one queue per object, and <code>notifyAll</code> wakes everyone", 2), gap=16, style="flex:1"), top=True),
 "steps": [
  "A read write lock has two locks inside. Any number of threads can hold the read lock together, because reading doesn't change anything. The write lock is exclusive. No readers, and no other writer.",
  "That's a big win for data that's read far more often than it's written, like a cache or configuration.",
  "Locks also give you conditions. A condition is a named wait queue. A bounded buffer can have one queue for not full, and another for not empty, so a producer only wakes consumers, and the other way round. With wait and notify there's just one queue per object.",
 ]},

{"html": H("Atomics and ", "CAS") + row(
   code("""§0 AtomicInteger count = new AtomicInteger();
§0 count.incrementAndGet();          // thread-safe count++
§2
§2 // what it does inside, roughly:
§2 do {
§2   old = value;
§2 } while (!compareAndSet(old, old + 1));""", 28, style="flex:1"),
   col(box("blue", "compare-and-swap", "\"set it to new, <b style=\"display:inline\">only if</b> it's still old\": one CPU instruction", 1),
       box("green", "lock-free", "no blocking · a loser just retries", 2),
       box("orange", "heavy contention?", "<code>LongAdder</code> spreads the count over cells", 3), gap=16, style="width:600px"), top=True),
 "steps": [
  "Remember count plus plus from part one? Read, add, write, and threads could interleave. An atomic integer fixes it without any lock. Increment and get is a thread safe plus plus.",
  "Underneath is compare and swap. It says: set the value to new, but only if it's still old. If another thread changed it in between, nothing happens and it reports failure. The CPU does this as one instruction.",
  "So the loop is simple. Read the old value, try to swap in old plus one, and if someone beat you, try again. No thread ever blocks, so it's called lock free.",
  "When many threads hammer one counter, they keep failing and retrying. Long adder solves that by keeping several cells and adding them up when you read.",
 ]},

{"html": H("Thread ", "pools") + row(
   col(box("red", "new Thread() per task", "creating threads is expensive · 10 000 tasks = 10 000 threads", 0),
       box("green", "ExecutorService", "a few <b style=\"display:inline\">worker threads</b> take tasks from a queue", 1), gap=18, style="width:600px"),
   code("""§1 ExecutorService pool = Executors.newFixedThreadPool(4);
§2 Future<Integer> f = pool.submit(() -> compute());
§2 int result = f.get();        // blocks until it's done
§3 pool.shutdown();             // stop taking new tasks""", 27, style="flex:1"), top=True) +
   table(["Factory", "Good for"], [
     (["<code>newFixedThreadPool(n)</code>", "CPU work, n ≈ number of cores"], 3),
     (["<code>newCachedThreadPool()</code>", "many short tasks (unbounded threads!)"], 3),
     (["<code>newScheduledThreadPool(n)</code>", "delays and repeating tasks"], 3)], size=27),
 "steps": [
  "Creating a thread per task is expensive. Each thread has its own stack, and ten thousand tasks would mean ten thousand threads.",
  "A thread pool keeps a few worker threads alive, and they take tasks from a queue. You don't manage threads at all, you submit work to an executor service.",
  "Submit returns a future, a handle to a result that isn't ready yet. Get blocks until it is.",
  "And always shut the pool down when you're done, or its threads keep the program alive. The factory methods give common shapes: a fixed pool for CPU work, a cached pool for many short tasks, and a scheduled pool for delays and repeating jobs.",
 ]},

{"html": H("ThreadPoolExecutor, the ", "real", " knobs") + table(["Parameter", "Meaning"], [
     (["<code>corePoolSize</code>", "threads kept alive even when idle"], 0),
     (["<code>workQueue</code>", "where tasks wait when all core threads are busy"], 0),
     (["<code>maximumPoolSize</code>", "extra threads, only once the queue is <b>full</b>"], 1),
     (["<code>keepAliveTime</code>", "how long those extra threads may sit idle"], 1),
     (["<code>RejectedExecutionHandler</code>", "queue full and at max: abort, caller runs, discard…"], 2)], size=29) +
   note("Order: core threads → queue → extra threads → reject", 3),
 "steps": [
  "Interviewers often ask how a thread pool really works. Every factory method builds a thread pool executor with five main settings. Core pool size is the number of threads it keeps, even when idle. The work queue is where tasks wait while those threads are busy.",
  "Maximum pool size allows extra threads, but here's the surprise. They're only created once the queue is full. Keep alive time is how long those extra threads can stay idle before they're removed.",
  "And when the queue is full and the pool is at its maximum, the rejection handler decides: throw an exception, run the task on the caller's thread, or drop it.",
  "So the order is: core threads first, then the queue, then extra threads, then rejection. One consequence: with an unbounded queue, the maximum size never matters at all.",
 ]},

{"html": H("", "CompletableFuture") + code("""§0 CompletableFuture.supplyAsync(() -> fetchUser(id))       // runs on a pool
§1   .thenApply(user -> user.email())                         // transform
§1   .thenCompose(email -> sendAsync(email))                  // chain another async call
§2   .thenCombine(loadPrefs(id), (sent, prefs) -> report(sent, prefs))
§3   .exceptionally(ex -> fallback())                         // handle any failure
§3   .thenAccept(System.out::println);""", 27) + row(
   box("blue", "Future", "you must block on <code>get()</code>", 1, "flex:1"),
   box("green", "CompletableFuture", "describe what happens <b style=\"display:inline\">next</b>, without blocking", 1, "flex:1"),
   box("purple", "allOf / anyOf", "wait for all, or the first, of many", 2, "flex:1"), style="margin-top:24px"),
 "steps": [
  "A plain future has one problem. The only way to use its result is to block on get. Completable future lets you describe what should happen next, instead. Supply async runs a task on a pool.",
  "Then apply transforms the result when it arrives. Then compose chains another asynchronous call, like map versus flat map in streams. So instead of blocking, you build a pipeline.",
  "Then combine waits for two independent futures and merges their results. All of waits for many, any of for the first.",
  "And exceptionally handles a failure anywhere earlier in the chain, so one error doesn't silently disappear. This is how modern Java writes non-blocking code, like calling several services in parallel.",
 ]},

{"html": H("Concurrent ", "collections") + table(["Instead of", "Use", "Why"], [
     (["<code>HashMap</code> + synchronized", "<code>ConcurrentHashMap</code>", "fine-grained locking, no null keys or values"], 0),
     (["<code>if (!map.containsKey(k)) map.put(k, v)</code>", "<code>map.merge</code> / <code>computeIfAbsent</code>", "check-then-act in <b>one</b> atomic call"], 1),
     (["wait / notify buffer", "<code>BlockingQueue</code>", "<code>put</code> waits when full, <code>take</code> when empty"], 2),
     (["<code>ArrayList</code> read by many", "<code>CopyOnWriteArrayList</code>", "reads lock-free, every write copies"], 3)], size=27),
 "steps": [
  "The collections package has thread safe versions of the usual structures. Concurrent hash map replaces a synchronized hash map. It locks only small parts of the table, so many threads work at once. And it doesn't allow null keys or values.",
  "One trap: each call is atomic, but two calls together aren't. Check if a key exists, then put, is a race. Use merge or compute if absent, which do the check and the update in one atomic call.",
  "Blocking queue gives you producer consumer for free. Put waits when the queue is full, and take waits when it's empty. No wait and notify needed.",
  "And copy on write array list is for lists read constantly and changed rarely. Reads need no lock, but every write copies the whole array.",
 ]},

{"html": H("", "Synchronizers") + row(
   box("blue", "CountDownLatch", "wait until N things have happened · <code>countDown()</code> / <code>await()</code> · <b style=\"display:inline\">one-shot</b>", 0, "flex:1"),
   box("green", "CyclicBarrier", "N threads wait for <b style=\"display:inline\">each other</b>, then all go · reusable", 1, "flex:1"),
   box("orange", "Semaphore", "N permits · at most N threads inside · e.g. 10 DB connections", 2, "flex:1"), top=True) +
   code("""§0 CountDownLatch ready = new CountDownLatch(3);
§0 // each of 3 services, when started:  ready.countDown();
§0 ready.await();    // main thread continues once all 3 are up""", 28, style="margin-top:26px"),
 "steps": [
  "Synchronizers coordinate threads. A count down latch waits until N things have happened. Workers call count down, and a thread calling await continues once the count reaches zero. Like waiting for three services to start. It can't be reset.",
  "A cyclic barrier makes N threads wait for each other. Nobody passes until everyone arrives, then they all continue, and it can be reused for the next round.",
  "And a semaphore holds N permits. Acquire takes one, release gives it back. So at most N threads can be inside at once, like limiting how many threads use ten database connections.",
 ]},

{"html": H("Virtual threads (", "Java 21", ")") + row(
   col(box("gray", "platform thread", "one OS thread · ~1 MB stack · thousands at most", 0),
       box("green", "virtual thread", "managed by the JVM · tiny · <b style=\"display:inline\">millions</b> are fine", 0),
       box("blue", "the trick", "on a blocking call it <b style=\"display:inline\">unmounts</b> and frees its carrier thread", 1), gap=16, style="flex:1"),
   col(code("""§2 try (var ex = Executors
§2        .newVirtualThreadPerTaskExecutor()) {
§2   ex.submit(() -> callService());
§2 }""", 22),
       box("orange", "great for", "I/O-bound work: HTTP calls, DB queries", 3),
       box("red", "no help for", "CPU-bound work · and don't pool them", 3), gap=16, style="width:700px"), top=True),
 "steps": [
  "Finally, virtual threads, final in Java twenty one. A normal platform thread is an operating system thread with a big stack, so you can only have a few thousand. A virtual thread is managed by the JVM, and is tiny. Millions are fine.",
  "The trick is what happens when one blocks, waiting for a database or an HTTP call. It unmounts from the real carrier thread, which goes off to run other virtual threads. So waiting costs almost nothing.",
  "Using them is easy. Create a virtual thread per task executor, and submit work as usual. One cheap thread per request, written in plain blocking style.",
  "They shine for input output bound work, like servers making lots of calls. They don't make CPU heavy work faster, because the cores are still the limit. And don't pool them. They're cheap, so just create a new one per task.",
 ]},

quiz([
  ("Why unlock() in a finally block?", "an exception would leave it <b style=\"display:inline\">locked forever</b>", "red",
   "Quiz time. Why must unlock go in a finally block?",
   "Because if the critical section throws, the lock would never be released, and every other thread would wait forever."),
  ("When are threads beyond core size created?", "only when the <b style=\"display:inline\">queue is full</b>", "orange",
   "In a thread pool executor, when are threads beyond the core size created?",
   "Only when the work queue is full. Core threads first, then the queue, then extra threads."),
  ("Virtual threads for CPU-heavy work?", "no gain: they help <b style=\"display:inline\">I/O-bound</b> work", "blue",
   "Do virtual threads speed up CPU heavy work?",
   "No. They help when threads spend their time waiting on input and output. CPU work is still limited by the cores."),
]),

recap(["ReentrantLock: tryLock, fair, unlock in finally",
       "ReadWriteLock: many readers or one writer",
       "Atomics: CAS loop, lock-free · LongAdder under contention",
       "Pools: core → queue → extra threads → reject",
       "CompletableFuture: chain, combine, handle errors",
       "ConcurrentHashMap.merge · BlockingQueue · virtual threads for I/O"],
  "Let's recap part two. Reentrant lock adds try lock and fairness, and always unlocks in finally. A read write lock allows many readers or one writer. Atomics use compare and swap, with no locking. Thread pools go core threads, then the queue, then extra threads, then rejection. Completable future chains and combines async work and handles errors. Use concurrent hash map's merge for check then act, blocking queue for producer consumer, and virtual threads for I/O heavy work. That completes multithreading. Now practise with the questions in your notes!"),
]
