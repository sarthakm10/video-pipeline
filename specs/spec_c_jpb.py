from conc import *

TAG = "Spring · Data Access with JDBC and JPA, Part 2"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Data Access with JDBC and JPA (Part 2).mp4"

SLIDES = [
title_slide(0, "Data Access", "Part 2: relationships, lazy loading, the N+1 problem, and repositories",
  "Welcome to data access with JDBC and JPA, part two.",
  "In part one, we mapped single entities and saw how the persistence context tracks them. But real data is connected: a user has tasks, a task has tags. By the end of this part you'll know how to map relationships, who owns a relationship, cascades, lazy versus eager loading, the lazy initialization exception, the famous N plus one problem and its fixes, the second level cache, and Spring Data repositories.",
  pill="SPRING · CONCEPT · PART 2"),

{"html": H("Mapping ", "relationships") + code("""§0 @Entity class Task {
§0   @ManyToOne(fetch = FetchType.LAZY)        // many tasks → one user
§0   @JoinColumn(name = "owner_id")            // the foreign key lives HERE
§0   private User owner;
§0 }
§1 @Entity class User {
§1   @OneToMany(mappedBy = "owner")            // the inverse side
§1   private List<Task> tasks = new ArrayList<>();
§1 }
§2 @ManyToMany @JoinTable(name = "task_tags")  // a join table
§2 private Set<Tag> tags = new HashSet<>();""", 26) + row(
   box("blue", "owning side", "has the foreign key · its changes are saved", 3, "flex:1"),
   box("orange", "mappedBy side", "just a view · keep both sides in sync in code", 3, "flex:1"), style="margin-top:18px"),
 "steps": [
  "Relationships are fields with annotations. Many tasks belong to one user, so task has a many to one field. The join column says the foreign key, owner id, lives in the tasks table.",
  "The user can also see its tasks, with one to many, mapped by owner. Mapped by says: the other side owns this relationship, I'm just a view of it.",
  "Many to many needs a join table, like task tags. Use a set for it.",
  "This owning side idea matters. Only changes to the owning side, the one with the foreign key, are written to the database. If you only add a task to user dot tasks, nothing is saved. Write helper methods that update both sides together.",
 ]},

{"html": H("Cascades and ", "orphans") + row(
   col(box("blue", "cascade", "pass an operation from parent to children: <code>PERSIST</code>, <code>REMOVE</code>, <code>ALL</code>", 0),
       box("green", "orphanRemoval = true", "a child removed from the collection is <b style=\"display:inline\">deleted</b>", 1),
       box("red", "careful", "cascade only down a true parent → child ownership · never <code>REMOVE</code> on <code>@ManyToOne</code>", 2), gap=16, style="flex:1"),
   code("""§0 @OneToMany(mappedBy = "order",
§0            cascade = CascadeType.ALL,
§1            orphanRemoval = true)
§0 private List<OrderLine> lines;
§1 order.getLines().remove(line);  // → DELETE""", 26, style="width:720px"), top=True),
 "steps": [
  "Cascade passes operations from a parent to its children. Persist an order with cascade all, and its order lines are saved too. Remove the order, and its lines go with it.",
  "Orphan removal goes further. Remove a line from the collection, and it's deleted from the database, because a line can't exist without its order.",
  "Use cascades only for real ownership, where children belong entirely to one parent. Never cascade remove from a many to one. Deleting one task would delete its user, and then all of that user's other tasks.",
 ]},

{"html": H("Lazy vs ", "eager") + row(
   col(box("green", "LAZY", "load the related data only when you <b style=\"display:inline\">touch</b> it · a proxy stands in", 0),
       box("orange", "EAGER", "always load it, even when you don't need it", 0),
       box("blue", "defaults", "<code>@ManyToOne</code>, <code>@OneToOne</code>: EAGER · collections: LAZY · <b style=\"display:inline\">make everything LAZY</b>", 1), gap=16, style="flex:1"),
   col(box("red", "LazyInitializationException", "a lazy field is touched <b style=\"display:inline\">after</b> the persistence context closed", 2),
       box("purple", "fix", "fetch what you need inside the transaction, map to a DTO · don't turn on open-in-view as a crutch", 3), gap=16, style="width:640px"), top=True),
 "steps": [
  "Fetching decides when related data is loaded. Lazy means only when you touch it. Until then, a proxy object stands in. Eager means always, whether you need it or not.",
  "The defaults are inconsistent: to one relationships are eager, collections are lazy. The common advice is to make everything lazy, and load what each use case needs explicitly.",
  "Lazy loading has a classic failure. Touch a lazy field after the transaction has ended, often while Jackson writes the response, and you get a lazy initialization exception. There's no open session left to load it.",
  "The fix is to load what you need inside the transaction, and map it to a DTO before returning. Spring's open in view setting hides the problem by keeping the session open, but it causes surprise queries. Turn it off.",
 ]},

{"html": H("The N+1 ", "problem") + row(
   code("""§0 List<Task> tasks = repo.findAll();           // 1 query
§1 for (Task t : tasks)
§1   System.out.println(t.getOwner().getName()); // +1 query EACH
§2 // 100 tasks → 101 queries""", 25, style="flex:1"),
   col(box("green", "JOIN FETCH", "<code>SELECT t FROM Task t JOIN FETCH t.owner</code> → 1 query", 3),
       box("blue", "@EntityGraph", "<code>@EntityGraph(attributePaths = \"owner\")</code> on the repository method", 3),
       box("purple", "batch size", "<code>hibernate.default_batch_fetch_size=50</code> → IN (…) batches", 4),
       box("orange", "or a DTO projection", "select only the columns you need", 4), gap=14, style="width:640px"), top=True),
 "steps": [
  "Here's the most famous JPA performance bug. Load all tasks: one query.",
  "Then, for each task, print the owner's name. The owner is lazy, so each access fires its own query.",
  "A hundred tasks means a hundred and one queries. It's fast in development with five rows, and painfully slow in production.",
  "The main fixes load the owners together with the tasks. Join fetch in a JPQL query, or an entity graph on the repository method. Either way, one query.",
  "Or set a batch fetch size, so Hibernate loads lazy owners fifty at a time with an in clause. Or skip entities entirely with a DTO projection. Turn on SQL logging in development, so you see N plus one when it happens.",
 ]},

{"html": H("Second-level ", "cache") + row(
   box("blue", "first-level", "the persistence context · <b style=\"display:inline\">one</b> transaction · always on", 0, "flex:1"),
   box("green", "second-level", "shared across transactions · opt-in per entity · Caffeine, Ehcache, Redis", 1, "flex:1"),
   box("orange", "use for", "read-mostly reference data: countries, categories", 2, "flex:1"), top=True) +
   note("A cache you add is a cache you must keep correct · measure before caching", 3),
 "steps": [
  "Part one showed the first level cache: the persistence context, scoped to one transaction, always on.",
  "Hibernate also has an optional second level cache, shared across transactions, and enabled per entity. A provider like Caffeine or Redis stores it.",
  "It suits data that's read constantly and changes rarely, like countries or categories.",
  "But every cache can serve stale data, especially with several servers. Measure first, and add caching only where it clearly helps.",
 ]},

{"html": H("Spring Data ", "repositories") + row(
   code("""§0 interface TaskRepository extends JpaRepository<Task, Long> {
§1   List<Task> findByOwnerId(long ownerId);
§2   @EntityGraph(attributePaths = "owner")
§2   List<Task> findByDoneFalse();
§0 }
§0 repo.save(task); repo.findById(7L); repo.deleteById(7L);""", 25, style="flex:1"),
   col(box("blue", "you write an interface", "Spring generates the class at startup", 0),
       box("green", "for free", "save · findById · findAll · delete · count · paging", 0),
       box("purple", "derived queries", "covered in Queries & Transactions", 1),
       box("red", "exceptions", "SQL errors → <code>DataIntegrityViolationException</code> etc. (translated)", 3), gap=14, style="width:560px"), top=True),
 "steps": [
  "Spring Data JPA removes the boilerplate. Declare an interface extending JPA repository, with the entity type and the id type. At startup, Spring generates the implementation. Save, find by id, find all, delete, count and paging come for free.",
  "Add methods by name, and Spring derives the query. The queries and transactions video covers these in depth.",
  "And you can fix N plus one right on the method, with an entity graph.",
  "Database errors are translated into Spring's own exception hierarchy. A unique constraint violation becomes a data integrity violation exception, whatever the database. Your advice can map it to a four oh nine.",
 ]},

quiz([
  ("Which side of a relationship is saved?", "the <b style=\"display:inline\">owning</b> side (has the FK)", "blue",
   "Quiz time. In a bidirectional relationship, which side's changes are written to the database?",
   "The owning side, the one with the foreign key. The mapped by side is just a view."),
  ("100 tasks, 101 queries. Name it and fix it.", "<b style=\"display:inline\">N+1</b> · JOIN FETCH / @EntityGraph", "red",
   "Loading a hundred tasks fires a hundred and one queries. What is it, and how do you fix it?",
   "The N plus one problem. Fix it with join fetch, an entity graph, or batch fetching."),
  ("LazyInitializationException: cause?", "touched a lazy field <b style=\"display:inline\">after</b> the session closed", "orange",
   "What causes a lazy initialization exception?",
   "Accessing a lazy field after the persistence context has closed. Load what you need inside the transaction."),
]),

recap(["@ManyToOne + @JoinColumn owns the FK · mappedBy is the view",
       "Cascade only parent → child · orphanRemoval deletes orphans",
       "Make relationships LAZY · map to DTOs in the transaction",
       "N+1: JOIN FETCH, @EntityGraph or batch size",
       "2nd-level cache: read-mostly data only",
       "JpaRepository: an interface, implemented for you"],
  "Let's recap part two. The many to one side with the join column owns the foreign key, and mapped by is only a view. Cascade from parent to child only, and orphan removal deletes children you drop. Make relationships lazy, and map to DTOs inside the transaction to avoid lazy initialization errors. Fix N plus one with join fetch, an entity graph, or a batch size. Use the second level cache only for read mostly data. And JPA repository gives you a full repository from just an interface. Now practise with the examples in your notes!"),
]
