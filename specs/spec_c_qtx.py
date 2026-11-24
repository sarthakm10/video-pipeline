from conc import *

TAG = "Spring · Queries and Transactions"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Queries and Transactions.mp4"

SLIDES = [
title_slide(0, "Queries & Transactions", "Ask the database the right question, and keep changes all-or-nothing",
  "Welcome to queries and transactions.",
  "Spring Data can write simple queries for you from a method name. When that's not enough, you write JPQL or SQL yourself. And once several changes have to succeed or fail together, you need transactions. By the end you'll know derived queries, JPQL and native queries, projections, paging, how at transactional really works, propagation, rollback rules, the proxy trap, isolation levels, and optimistic versus pessimistic locking.",
  pill="SPRING · CONCEPT"),

{"html": H("Derived ", "queries") + code("""§0 interface TaskRepository extends JpaRepository<Task, Long> {
§0   List<Task> findByDoneFalse();
§1   List<Task> findByOwnerEmailAndPriorityGreaterThan(String email, int p);
§2   Optional<Task> findFirstByOrderByDueAsc();
§2   long countByDone(boolean done);
§2   boolean existsByTitle(String title);
§0 }""", 27) + row(
   box("blue", "the name is the query", "<code>find…By</code> + properties + keywords: <code>And</code>, <code>Between</code>, <code>Like</code>, <code>In</code>, <code>OrderBy</code>", 0, "flex:1"),
   box("orange", "checked at startup", "a typo in a property name → the app <b style=\"display:inline\">fails to start</b>", 1, "flex:1"),
   box("red", "know when to stop", "a name longer than a sentence → write a <code>@Query</code>", 3, "flex:1"), style="margin-top:22px"),
 "steps": [
  "Spring Data JPA can write queries for you from the method name. Find by done false becomes a select with where done equals false. No SQL, no implementation.",
  "You combine properties with keywords: and, or, greater than, between, like, in, order by. And the names are checked when the app starts. Misspell a property, and the app refuses to start, which is much better than failing in production.",
  "Besides find, there's count by, exists by, delete by, and find first or find top for limiting results.",
  "But know when to stop. If the method name gets longer than a sentence, it's time to write the query yourself.",
 ]},

{"html": H("JPQL, native SQL, ", "projections") + code("""§0 @Query("SELECT t FROM Task t WHERE t.owner.email = :email AND t.done = false")
§0 List<Task> openFor(@Param("email") String email);
§1 @Query(value = "SELECT * FROM tasks WHERE title ILIKE '%' || :q || '%'", nativeQuery = true)
§1 List<Task> search(@Param("q") String q);
§2 record TaskSummary(Long id, String title) {}
§2 @Query("SELECT new com.app.TaskSummary(t.id, t.title) FROM Task t")
§2 List<TaskSummary> summaries();""", 24) + row(
   box("blue", "JPQL", "queries <b style=\"display:inline\">entities and fields</b>, not tables · portable", 0, "flex:1"),
   box("purple", "native", "real SQL for database-specific features · not portable", 1, "flex:1"),
   box("green", "projection", "select only the columns you need → less data, no tracking", 2, "flex:1"), style="margin-top:20px"),
 "steps": [
  "When a name isn't enough, write a query with at query. This is JPQL. It looks like SQL, but it talks about entities and their fields, not tables and columns. So t dot owner dot email follows the relationship for you.",
  "When you need a database specific feature, write native SQL, with native query equals true. It's powerful, but ties you to that database.",
  "And if you only need a few columns, don't load whole entities. Select into a record. That's a projection. Less data travels, and Hibernate doesn't have to track those objects for changes.",
 ]},

{"html": H("Paging and ", "sorting") + row(
   code("""§0 Page<Task> page = repo.findByDone(false,
§0     PageRequest.of(0, 20, Sort.by("due").descending()));
§1 page.getContent();       // the 20 rows
§1 page.getTotalElements(); // runs a COUNT query
§2 Slice<Task> slice = ...; // just "is there a next page?"
§3 @GetMapping
§3 Page<TaskResponse> list(Pageable pageable)  // ?page=0&size=20&sort=due,desc""", 24, style="flex:1"),
   col(box("blue", "Pageable", "page number + size + sort", 0),
       box("orange", "Page", "content + totals · costs an extra <code>COUNT</code>", 1),
       box("green", "Slice", "no count · fine for infinite scroll", 2),
       box("purple", "from the URL", "Spring builds the Pageable from query parameters", 3), gap=14, style="width:520px"), top=True),
 "steps": [
  "Never return a whole table. Any repository method can take a pageable: a page number, a page size, and a sort. Pages start at zero.",
  "Returning a page gives you the rows, plus the total number of elements and pages. But computing the total costs an extra count query.",
  "If you only need to know whether there's a next page, like for infinite scrolling, return a slice instead. No count query.",
  "In a controller, just add a pageable parameter. Spring builds it from query parameters like page, size and sort.",
 ]},

{"html": H("How @Transactional ", "works") + row(
   col(box("blue", "a proxy wraps your bean", "<b style=\"display:inline\">begin</b> → call your method → <b style=\"display:inline\">commit</b>, or rollback on an exception", 0),
       box("green", "all or nothing", "move money: debit and credit both happen, or neither does", 1),
       box("purple", "readOnly = true", "a hint: no dirty checking, maybe a read replica", 2), gap=16, style="flex:1"),
   code("""§0 @Service
§0 class TransferService {
§1   @Transactional
§1   void transfer(long from, long to, long cents) {
§1     accounts.debit(from, cents);
§1     accounts.credit(to, cents);  // throws → rollback
§1   }
§2   @Transactional(readOnly = true)
§2   Report monthly() { … }
§0 }""", 25, style="width:780px"), top=True) +
   note("Put it on <u>service</u> methods: one business action = one transaction", 3),
 "steps": [
  "At transactional works through a proxy. Spring wraps your bean in another object. When someone calls the method, the proxy begins a transaction, calls your code, and commits. If an exception escapes, it rolls back instead.",
  "That gives all or nothing behaviour. When moving money, the debit and the credit both happen, or neither does. If the credit fails, the debit is undone.",
  "Read only equals true is a hint for queries. Hibernate can skip dirty checking, and some setups route those queries to a read replica.",
  "Put transactional on service methods, not controllers or repositories. One business action is one transaction.",
 ]},

{"html": H("Rollback rules and the proxy ", "trap") + row(
   col(box("red", "rolls back on", "<code>RuntimeException</code> and <code>Error</code> only", 0),
       box("orange", "checked exceptions", "<b style=\"display:inline\">commit</b> by default · use <code>rollbackFor = Exception.class</code>", 0),
       box("purple", "self-invocation", "<code>this.save()</code> skips the proxy → <b style=\"display:inline\">no transaction</b>", 1),
       box("gray", "also ignored", "<code>private</code> methods · catching the exception yourself", 2), gap=16, style="width:640px"),
   code("""§1 public void importAll(List<Row> rows) {
§1   for (Row r : rows) save(r);
§1   // = this.save(r): no proxy, no transaction
§1 }
§1 @Transactional
§1 public void save(Row r) { … }""", 26, style="flex:1"), top=True),
 "steps": [
  "Two rules trip people up. First, by default, a transaction rolls back only on runtime exceptions and errors. A checked exception, like an IO exception, still commits. If you want a rollback, say rollback for equals exception dot class.",
  "Second, the proxy trap. Here, import all calls save on the same object. That call goes through this, not through the proxy, so the transactional annotation on save is silently ignored. The fix is to put the annotation on the outer method, or move save into another bean.",
  "For the same reason, transactional on a private method does nothing. And if you catch the exception inside the method, the proxy never sees it, so it commits.",
 ]},

{"html": H("Propagation and ", "isolation") + table(["Propagation", "Meaning"], [
     (["<code>REQUIRED</code> (default)", "join the current transaction, or start one"], 0),
     (["<code>REQUIRES_NEW</code>", "pause the caller's, run my own · e.g. an audit log that must survive"], 0),
     (["<code>MANDATORY</code> · <code>NEVER</code> · <code>SUPPORTS</code>", "must have one · must not · either"], 0)], size=27) +
   table(["Isolation", "Prevents"], [
     (["<code>READ_COMMITTED</code> (Postgres default)", "dirty reads"], 1),
     (["<code>REPEATABLE_READ</code>", "+ the same row changing under you"], 1),
     (["<code>SERIALIZABLE</code>", "+ phantoms · as if one at a time · slowest"], 1)], size=27),
 "steps": [
  "Propagation decides what happens when a transactional method calls another one. The default, required, joins the transaction that's already running, or starts one if there isn't one. Requires new pauses the caller's transaction and runs its own, which commits independently. That's useful for an audit log that must be saved even if the main work fails. Mandatory, never and supports are rarer.",
  "Isolation decides how much concurrent transactions can see of each other. Read committed, the Postgres default, never shows uncommitted data. Repeatable read also guarantees that a row you've read won't change under you. Serializable behaves as if transactions ran one at a time. Stronger isolation means fewer anomalies, but more waiting and more retries.",
 ]},

{"html": H("Locking: optimistic vs ", "pessimistic") + row(
   col(box("green", "optimistic: @Version", "no lock · <code>UPDATE … WHERE version = 3</code> · 0 rows → <code>OptimisticLockException</code>", 0),
       box("blue", "use when", "conflicts are <b style=\"display:inline\">rare</b> · web apps, edit forms · answer 409, let the user retry", 1), gap=16, style="flex:1"),
   col(box("red", "pessimistic: FOR UPDATE", "<code>@Lock(PESSIMISTIC_WRITE)</code> · others <b style=\"display:inline\">wait</b>", 2),
       box("orange", "use when", "conflicts are <b style=\"display:inline\">frequent</b> and costly · stock counts, seat booking", 3), gap=16, style="flex:1"), top=True) +
   note("Two users edit the same task: the second save fails instead of silently overwriting", 1),
 "steps": [
  "When two users edit the same row, someone's change can be silently lost. Optimistic locking prevents that without locks. Add a version field with at version. Every update checks the version it read, and increments it. If someone else updated first, zero rows match, and Hibernate throws an optimistic lock exception.",
  "It suits cases where conflicts are rare, like web edit forms. Return a four oh nine, and let the user reload and retry. The second save fails, instead of silently overwriting the first.",
  "Pessimistic locking locks the row when you read it, with select for update. Other transactions wait until you commit.",
  "It suits cases where conflicts are frequent and expensive, like decrementing stock or booking the last seat. The cost is waiting, and the risk of deadlocks, so keep those transactions short.",
 ]},

quiz([
  ("A checked exception escapes @Transactional. Rollback?", "<b style=\"display:inline\">no</b>, it commits · add rollbackFor", "red",
   "Quiz time. A checked exception escapes a transactional method. Does it roll back?",
   "No. By default only runtime exceptions and errors roll back. Use rollback for."),
  ("this.save() with @Transactional on save. Transaction?", "<b style=\"display:inline\">no</b>: the proxy is bypassed", "purple",
   "A method calls this dot save, and save is transactional. Is there a transaction?",
   "No. Self invocation skips the proxy, so the annotation is ignored."),
  ("Edit forms, rare conflicts: which locking?", "<b style=\"display:inline\">optimistic</b> (@Version)", "green",
   "Users editing records in a web form, conflicts are rare. Which kind of locking?",
   "Optimistic locking with a version field. Answer four oh nine when it fails."),
]),

recap(["Derived queries from names · @Query when they get long",
       "JPQL = entities · native = real SQL · projections = less data",
       "Pageable in, Page or Slice out",
       "@Transactional = a proxy: begin, commit, rollback",
       "Checked exceptions commit · self-calls skip the proxy",
       "@Version for rare conflicts · FOR UPDATE for hot rows"],
  "Let's recap. Spring Data derives simple queries from method names, and at query handles the rest: JPQL for entities, native SQL when you need it, and projections to load less. Take a pageable and return a page or a slice. At transactional works through a proxy that begins, commits, or rolls back. Remember that checked exceptions commit by default, and calls through this skip the proxy. And use a version field for rare conflicts, and select for update for hot rows. Now practise with the examples in your notes!"),
]
