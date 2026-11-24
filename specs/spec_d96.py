from conc import *

TAG = "Day 96 · Revision: SQL and System Design"
TRACK = "Java Fullstack · Revision"
FILE = "Day 96 Revision SQL and System Design.mp4"

SLIDES = [
title_slide(96, "Revision: SQL & System Design", "Queries on paper, and how databases keep data safe",
  "Welcome to day ninety six: the last technical revision day, on SQL and system design.",
  "We'll write the classic interview queries, revisit indexes and the explain plan, then go deeper on transactions than before: isolation levels, how PostgreSQL uses MVCC so readers and writers don't block each other, and optimistic versus pessimistic locking. We'll finish with a quick pass over the system design ideas from days ninety one and ninety two.",
  pill="DAY 96 · REVISION"),

{"html": H("Three classic ", "queries") + code("""§0 -- second highest salary
§0 SELECT MAX(salary) FROM emp WHERE salary < (SELECT MAX(salary) FROM emp);
§1 -- running total
§1 SELECT day, amount, SUM(amount) OVER (ORDER BY day) AS running FROM sales;
§2 -- compare with the previous day
§2 SELECT day, amount, amount - LAG(amount) OVER (ORDER BY day) AS change FROM sales;""", 23) +
   note("Window functions keep every row · GROUP BY collapses them", 3),
 "steps": [
  "The second highest salary: the largest salary below the maximum. Or rank with dense rank and pick rank two, which also handles the Nth highest.",
  "A running total is a sum used as a window function, ordered by day. Each row adds its amount to everything before it.",
  "To compare with the previous row, LAG fetches the value from the row before, so you can subtract.",
  "The key idea: window functions keep every row and add a computed column, while group by collapses rows into one per group.",
 ]},

{"html": H("Indexes and ", "EXPLAIN") + row(
   col(box("blue", "B-tree index", "sorted · finds a row in O(log n) instead of scanning", 0),
       box("green", "composite (a, b)", "helps <code>a</code> and <code>a + b</code> · not <code>b</code> alone: leftmost first", 1),
       box("orange", "the cost", "every index slows writes and takes space", 1), gap=14, style="width:560px"),
   code("""§2 EXPLAIN ANALYZE
§2 SELECT * FROM orders WHERE customer_id = 42;
§2
§2 Seq Scan on orders  (rows=1000000)      -- ⚠ no index used
§3 Index Scan using idx_orders_customer    -- ✓ after
§3   (actual time=0.03 ms, rows=12)""", 22, style="flex:1"), top=True),
 "steps": [
  "An index is usually a B tree: a sorted structure that finds rows in logarithmic time instead of scanning the whole table.",
  "A composite index on a and b is sorted by a first, then b. It helps queries on a, or on a and b, but not on b alone. And every index slows down inserts and updates, so don't index everything.",
  "Explain analyze shows the plan the database chose. A sequential scan over a million rows on a selective filter means a missing index.",
  "After adding one, you see an index scan, and the time drops from a full scan to a fraction of a millisecond.",
 ]},

{"html": H("Isolation ", "levels") + table(["Level", "Dirty read", "Non-repeatable read", "Phantom"], [
     (["READ UNCOMMITTED", "possible", "possible", "possible"], 0),
     (["READ COMMITTED (Postgres default)", "—", "possible", "possible"], 1),
     (["REPEATABLE READ", "—", "—", "possible*"], 2),
     (["SERIALIZABLE", "—", "—", "—"], 2)], size=26) +
   note("* Postgres blocks phantoms here too · higher = safer, more conflicts", 3),
 "steps": [
  "Isolation decides what concurrent transactions see of each other. A dirty read sees uncommitted data. A non repeatable read gets a different value when reading the same row twice. A phantom is a new row appearing when the same query runs again. Read uncommitted allows all three.",
  "Read committed, the default in PostgreSQL and most databases, never shows uncommitted data, but values can change between two reads.",
  "Repeatable read keeps every row you've read stable for the whole transaction. Serializable makes transactions behave as if they ran one after another.",
  "PostgreSQL's repeatable read actually prevents phantoms too. Higher levels are safer, but cause more conflicts and retries.",
 ]},

{"html": H("MVCC: readers don't block ", "writers") + row(
   code("""§0 row #7, version 1   balance = 100   (created by tx 10)
§1 tx 20 UPDATE    → version 2   balance = 80    (created by tx 20)
§1                   version 1 is kept, marked "ended by tx 20"
§2 tx 15 (started earlier) reads row #7 → sees version 1: 100
§2 tx 25 (started later)   reads row #7 → sees version 2: 80
§3 VACUUM later removes version 1 when no one can see it""", 22, style="flex:1"),
   col(box("blue", "MVCC", "multi-version concurrency control · an update writes a new version", 0),
       box("green", "snapshots", "each transaction sees the versions committed when it started", 2),
       box("purple", "so", "reads never wait for writes · writes never wait for reads", 2),
       box("gray", "cleanup", "old versions pile up → VACUUM", 3), gap=14, style="width:500px"), top=True),
 "steps": [
  "How can PostgreSQL let people read while others write? With MVCC, multi version concurrency control. Instead of changing a row in place, an update writes a new version of it.",
  "Here transaction twenty updates the balance from a hundred to eighty. The old version isn't deleted, just marked as ended by transaction twenty.",
  "Each transaction reads from a snapshot, seeing only versions that were committed when it started. So an older transaction still sees a hundred, and a newer one sees eighty. Readers never wait for writers, and writers never wait for readers.",
  "Old versions pile up, so a background process called vacuum removes them once no transaction can see them. Two writers on the same row still conflict, and that's where locking comes in.",
 ]},

{"html": H("Optimistic vs pessimistic ", "locking") + row(
   col(box("green", "optimistic", "no lock · check a version at save time · conflict → retry", 0),
       code("""§0 @Version private long version;
§0 -- UPDATE … SET …, version = 4
§0 --   WHERE id = 7 AND version = 3
§0 -- 0 rows → OptimisticLockException""", 21), gap=14, style="flex:1"),
   col(box("red", "pessimistic", "lock the row while you work · others wait", 1),
       code("""§1 SELECT * FROM seat WHERE id = 7
§1   FOR UPDATE;
§1 @Lock(LockModeType.PESSIMISTIC_WRITE)""", 21), gap=14, style="flex:1"), top=True) +
   note("Conflicts rare → optimistic · conflicts likely (last seat, hot counter) → pessimistic", 2),
 "steps": [
  "Optimistic locking takes no lock at all. Each row has a version column. An update says: change this row only if the version is still three, and set it to four. If someone else saved first, zero rows change, JPA throws an optimistic lock exception, and you retry or tell the user.",
  "Pessimistic locking locks the row while you work, with select for update, or the pessimistic write lock mode in JPA. Anyone else wanting that row waits.",
  "So: when conflicts are rare, like editing a profile, use optimistic locking. When they're likely, like booking the last seat, lock pessimistically.",
 ]},

{"html": H("System design in one ", "slide") + table(["Explain…", "In one breath"], [
     (["CAP", "during a partition: consistency (bank) or availability (feed)"], 0),
     (["cache-aside", "check cache → miss → DB → fill · delete on write + TTL"], 0),
     (["write-through", "write cache and DB together · fresh reads, slower writes"], 1),
     (["consistent hashing", "a ring · adding a server moves ~1/N keys · virtual nodes"], 1),
     (["sharding", "split by a key · scales writes · avoid cross-shard queries"], 2),
     (["queue vs stream", "a task for one worker vs events many can replay"], 2)], size=27),
 "steps": [
  "Finally, the system design ideas in one breath each. CAP: during a network partition, choose consistency, like a bank, or availability, like a news feed. Cache aside: check the cache, on a miss read the database and fill the cache, and delete keys on writes.",
  "Write through updates cache and database together. Consistent hashing places servers on a ring, so adding one moves only about one over N keys.",
  "Sharding splits data by a key to scale writes. And a queue holds tasks for one worker, while a stream keeps events that many consumers can replay. If any of these took you more than a minute, put it on your weak list.",
 ]},

quiz([
  ("Composite index (a, b): helps <code>WHERE b = 5</code>?", "<b style=\"display:inline\">no</b>: leftmost column first", "orange",
   "Quiz time. There's a composite index on a and b. Does it help a query filtering only on b?",
   "No. An index is used from its leftmost column."),
  ("In MVCC, does a reader wait for a writer?", "<b style=\"display:inline\">no</b>: it reads its snapshot", "blue",
   "With MVCC, does a reader wait for a writer on the same row?",
   "No. It reads the version from its snapshot."),
  ("Booking the last seat: which locking?", "<b style=\"display:inline\">pessimistic</b> (SELECT … FOR UPDATE)", "red",
   "Many users try to book the last seat at once. Optimistic or pessimistic locking?",
   "Pessimistic, because conflicts are very likely."),
]),

recap(["2nd highest · SUM OVER · LAG",
       "B-tree · composite index: leftmost first · EXPLAIN",
       "READ COMMITTED default · higher = safer, more conflicts",
       "MVCC: new versions + snapshots · VACUUM",
       "Optimistic (@Version) vs pessimistic (FOR UPDATE)",
       "CAP · caching · consistent hashing · sharding"],
  "Let's recap. You can write the second highest salary, a running total with sum over, and a previous row comparison with LAG. Indexes are B trees, used from their leftmost column, and explain shows whether they're used. Read committed is the usual default, and higher levels trade conflicts for safety. MVCC writes new row versions and gives each transaction a snapshot, so readers and writers don't block each other. Use optimistic locking when conflicts are rare, and pessimistic when they're likely. Tomorrow: behavioral interviews."),
]
