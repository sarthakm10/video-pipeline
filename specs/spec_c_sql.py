from conc import *

TAG = "Spring · SQL Essentials"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring SQL Essentials.mp4"

SLIDES = [
title_slide(0, "SQL Essentials", "The SQL a backend developer writes every week, on PostgreSQL",
  "Welcome. Today's concept: SQL essentials.",
  "Even with JPA, you'll read and write SQL constantly: to debug a slow page, write a report, or answer an interview question. By the end you'll know how a query is evaluated, null and case, grouping with having, joins, subqueries and common table expressions, window functions, indexes and explain, transactions and ACID, and normalisation.",
  pill="SPRING · CONCEPT"),

{"html": H("Tables and ", "changes") + code("""§0 CREATE TABLE users (
§0   id    BIGSERIAL PRIMARY KEY,
§0   email TEXT NOT NULL UNIQUE,
§0   age   INT CHECK (age >= 0)
§0 );
§1 INSERT INTO users (email, age) VALUES ('a@x.com', 25);
§1 UPDATE users SET age = 26 WHERE id = 1;     -- forget WHERE → every row
§1 DELETE FROM users WHERE id = 1;
§2 INSERT INTO users (email, age) VALUES ('a@x.com', 30)
§2   ON CONFLICT (email) DO UPDATE SET age = EXCLUDED.age;   -- upsert""", 26),
 "steps": [
  "DDL defines structure. A table has columns with types, and constraints the database enforces: a primary key, not null, unique, and checks.",
  "DML changes rows: insert, update and delete. Always double check the where clause. Without it, every row changes.",
  "An upsert inserts a row, or updates it if a unique key already exists. In PostgreSQL that's on conflict do update.",
 ]},

{"html": H("How a query is ", "evaluated") + code("§0 FROM/JOIN → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT", 28) + row(
   code("""§1 SELECT dept, COUNT(*) AS n, AVG(salary)
§1 FROM employees
§1 WHERE active
§1 GROUP BY dept
§1 HAVING COUNT(*) > 5
§1 ORDER BY n DESC;""", 25, style="flex:1"),
   col(box("blue", "WHERE vs HAVING", "WHERE filters rows · HAVING filters <b style=\"display:inline\">groups</b>", 1),
       box("orange", "why aliases fail in WHERE", "SELECT runs after WHERE", 2), gap=14, style="width:600px"), top=True, style="margin-top:22px"),
 "steps": [
  "You write select first, but the database evaluates it in a different order: from and joins, then where, group by, having, select, order by, and finally limit.",
  "Where filters individual rows before grouping. Having filters whole groups after aggregation, so it can use count and average. Here: departments with more than five active employees.",
  "That order also explains a classic error. A column alias from select can't be used in where, because select hasn't run yet. Order by runs later, so it can.",
 ]},

{"html": H("NULL and ", "CASE") + row(
   col(box("red", "NULL is unknown", "<code>NULL = NULL</code> is not true · use <code>IS NULL</code>", 0),
       box("orange", "aggregates skip it", "<code>COUNT(col)</code> skips NULL · <code>COUNT(*)</code> doesn't", 1),
       box("blue", "NOT IN trap", "<code>x NOT IN (1, NULL)</code> → no rows ever", 2), gap=14, style="width:640px"),
   code("""§1 COALESCE(phone, 'none')
§3 SELECT name,
§3   CASE WHEN age < 18 THEN 'minor'
§3        WHEN age < 65 THEN 'adult'
§3        ELSE 'senior' END AS band
§3 FROM users;""", 25, style="flex:1"), top=True),
 "steps": [
  "Null means unknown, so comparing anything to null, even null, gives unknown, not true. Use is null and is not null.",
  "Aggregates skip nulls. Count of a column counts non null values, while count star counts rows. Coalesce replaces null with a default.",
  "And a nasty trap: not in a list containing null returns no rows at all, because every comparison becomes unknown. Prefer not exists.",
  "Case is SQL's if else. It's an expression, so it works in select, order by, and even inside aggregates.",
 ]},

{"html": H("", "Joins") + row(
   col(table(["user", "orders"], [
     (["Asha", "#1, #2"], 0), (["Ravi", "#3"], 0), (["Meera", "none"], 0)], size=28), style="width:420px"),
   table(["Join", "Keeps"], [
     (["INNER", "only matching pairs · Meera disappears"], 1),
     (["LEFT", "every user · Meera with NULL order"], 2),
     (["FULL", "everything from both sides"], 3),
     (["CROSS", "every pair (3 × 3)"], 3)], size=27), top=True, gap=40) +
   note("Users with no orders: LEFT JOIN … WHERE o.id IS NULL", 4),
 "steps": [
  "A join combines rows from two tables on a condition. Three users, three orders. Asha has two orders, Ravi one, Meera none.",
  "An inner join keeps only matching pairs: three rows, and Meera disappears.",
  "A left join keeps every row from the left table. Meera appears once, with nulls for the order columns.",
  "A full join keeps unmatched rows from both sides. A cross join pairs everything with everything, nine rows.",
  "The classic question, users with no orders, is a left join where the order id is null.",
 ]},

{"html": H("Subqueries, EXISTS and ", "CTEs") + row(
   code("""§0 SELECT * FROM users u
§0 WHERE EXISTS (SELECT 1 FROM orders o
§0               WHERE o.user_id = u.id);
§1 WITH big_spenders AS (
§1   SELECT user_id, SUM(total) AS spent
§1   FROM orders GROUP BY user_id
§1   HAVING SUM(total) > 1000
§1 )
§1 SELECT u.name, b.spent
§1 FROM users u JOIN big_spenders b ON b.user_id = u.id;
§2 SELECT email FROM customers UNION SELECT email FROM leads;""", 24, style="flex:1"),
   col(box("blue", "EXISTS", "stops at the first match · safe with NULLs", 0),
       box("green", "CTE (WITH)", "a named step · reads top to bottom", 1),
       box("purple", "set operations", "<code>UNION</code> removes duplicates · <code>UNION ALL</code> keeps them", 2), gap=14, style="width:520px"), top=True),
 "steps": [
  "A subquery is a query inside another. Exists checks whether any matching row exists, and stops at the first one. It's also safe with nulls, unlike not in.",
  "A common table expression, written with with, names an intermediate result. Complex queries become a series of readable steps.",
  "Set operations stack results. Union removes duplicates, which costs a sort, so use union all when duplicates are fine.",
 ]},

{"html": H("Window ", "functions") + row(
   code("""§0 SELECT name, dept, salary,
§0   RANK()  OVER (PARTITION BY dept ORDER BY salary DESC) AS r,
§1   SUM(salary) OVER (ORDER BY hired) AS running_total,
§2   LAG(salary) OVER (ORDER BY hired) AS previous
§0 FROM employees;""", 25, style="flex:1"),
   col(box("blue", "vs GROUP BY", "rows <b style=\"display:inline\">stay</b> · each gets a value from its window", 0),
       box("green", "ranking", "<code>ROW_NUMBER</code> 1,2,3 · <code>RANK</code> 1,1,3 · <code>DENSE_RANK</code> 1,1,2", 0),
       box("purple", "running / neighbours", "<code>SUM … OVER</code> · <code>LAG</code> · <code>LEAD</code>", 1), gap=14, style="width:560px"), top=True) +
   note("Top 3 per department: rank in a CTE, then WHERE r &lt;= 3", 3),
 "steps": [
  "Window functions compute across related rows without collapsing them. Group by turns a department into one row. A window keeps every employee and adds a value. Here, a rank within each department. Row number gives one, two, three. Rank gives ties the same number and skips. Dense rank doesn't skip.",
  "Sum over an ordering gives a running total.",
  "Lag and lead read the previous or next row, perfect for day over day changes.",
  "The classic interview query, top three per department, ranks inside a CTE, then filters on the rank.",
 ]},

{"html": H("Indexes and ", "EXPLAIN") + row(
   col(box("blue", "an index", "a sorted B-tree on columns · finds rows in O(log n) instead of scanning", 0),
       box("green", "composite (a, b)", "helps <code>a</code> and <code>a + b</code> · not <code>b</code> alone", 1),
       box("red", "the costs", "slower writes · more storage · unused if you wrap the column", 2), gap=14, style="width:600px"),
   code("""§0 CREATE INDEX idx_orders_user ON orders (user_id);
§3 EXPLAIN ANALYZE
§3 SELECT * FROM orders WHERE user_id = 42;
§3 -- Seq Scan   → reads every row
§3 -- Index Scan → jumps to the matches
§2 WHERE lower(email) = …   -- skips an index on email""", 23, style="flex:1"), top=True),
 "steps": [
  "An index is a sorted structure, usually a B tree, so the database can jump to matching rows instead of scanning the whole table.",
  "A composite index on a then b works like a phone book sorted by surname then first name. It helps queries on a, or on a and b, but not on b alone.",
  "Indexes slow down writes and take space. And wrapping the column in a function, like lower of email, stops a plain index from being used.",
  "Explain analyze shows the plan the database actually ran. A sequential scan on a big table, where you expected an index scan, is the first thing to look for.",
 ]},

{"html": H("Transactions and ", "normalisation") + row(
   col(table(["ACID", "Means"], [
     (["Atomic", "all or nothing"], 0),
     (["Consistent", "constraints hold after commit"], 0),
     (["Isolated", "concurrent transactions don't interfere"], 0),
     (["Durable", "committed survives a crash"], 0)], size=27), style="width:820px"),
   col(box("blue", "1NF", "one value per cell · no repeating groups", 1),
       box("green", "2NF / 3NF", "every column depends on the key, the whole key, nothing but the key", 1),
       box("orange", "denormalise", "on purpose, for read speed · accept duplication", 2), gap=14, style="flex:1"), top=True),
 "steps": [
  "A transaction groups statements into one unit, with four guarantees. Atomic: all or nothing. Consistent: constraints hold. Isolated: concurrent transactions don't see each other's half done work. Durable: once committed, it survives a crash.",
  "Normalisation removes duplication. First normal form, one value per cell. Second and third, every column depends on the key, the whole key, and nothing but the key. So a customer's address lives in one row, not in every order.",
  "Sometimes you denormalise on purpose, copying data to make reads faster, and accept the cost of keeping copies in sync.",
 ]},

quiz([
  ("WHERE or HAVING to filter on COUNT(*)?", "<b style=\"display:inline\">HAVING</b>: it filters groups", "blue",
   "Quiz time. To filter on count star, do you use where or having?",
   "Having. It runs after grouping, so aggregates exist."),
  ("Users with no orders?", "<b style=\"display:inline\">LEFT JOIN</b> … WHERE o.id IS NULL", "green",
   "How do you find users with no orders?",
   "Left join orders, and keep rows where the order id is null."),
  ("Index on (a, b): helps WHERE b = ?", "<b style=\"display:inline\">no</b>: leftmost column first", "red",
   "Does an index on a, b help a query that filters only on b?",
   "No. A composite index needs its leftmost column."),
]),

recap(["Evaluation: FROM → WHERE → GROUP BY → HAVING → SELECT",
       "NULL: IS NULL · COUNT(*) vs COUNT(col) · avoid NOT IN",
       "INNER vs LEFT join · anti-join with IS NULL",
       "EXISTS · CTEs · UNION ALL",
       "Windows: RANK / running SUM / LAG, rows stay",
       "Indexes + EXPLAIN · ACID · normalisation"],
  "Let's recap. SQL is evaluated from, where, group by, having, then select. Null is unknown, so use is null, and avoid not in. Inner joins keep matches, left joins keep every left row, and is null finds the missing ones. Exists, CTEs and union all structure bigger queries. Window functions rank and total without collapsing rows. And indexes, explain, ACID and normalisation keep it fast and correct. Now practise with the exercises in your notes!"),
]
