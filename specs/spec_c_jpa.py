from conc import *

TAG = "Spring · Data Access with JDBC and JPA, Part 1"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Data Access with JDBC and JPA (Part 1).mp4"

SLIDES = [
title_slide(0, "Data Access", "Part 1: connections, migrations, JDBC, and how JPA really tracks your objects",
  "Welcome to data access with JDBC and JPA, part one.",
  "Almost every backend reads and writes a database. Spring gives you several ways to do it, from writing SQL yourself to letting JPA generate it. By the end of this part you'll know the four approaches, how connections are pooled, how schema migrations work, how to use JdbcTemplate and JdbcClient, and the heart of JPA: entities, their lifecycle, and the persistence context that tracks every change.",
  pill="SPRING · CONCEPT · PART 1"),

{"html": H("Four ways to reach the ", "database") + table(["Approach", "You write", "Good for"], [
     (["plain <b>JDBC</b>", "SQL + connections + result sets + cleanup", "nothing, in Spring code"], 0),
     (["<b>JdbcTemplate</b> / <b>JdbcClient</b>", "SQL · Spring handles the rest", "reports, bulk work, full control"], 1),
     (["<b>JPA</b> (Hibernate)", "annotated classes · SQL is generated", "domain objects with relationships"], 2),
     (["<b>Spring Data JPA</b>", "an interface · even the queries are derived", "most CRUD services"], 2)], size=28) +
   note("They mix fine: JPA for the domain, JdbcClient for a heavy report", 3),
 "steps": [
  "There are four levels. Plain JDBC means writing SQL and also opening connections, walking through result sets, and closing everything in finally blocks. Lots of boilerplate, and easy to leak connections.",
  "Spring's JdbcTemplate and JdbcClient keep you writing SQL, but handle connections, cleanup and exceptions. Good when you want full control over the query.",
  "JPA, implemented by Hibernate, goes further. You annotate classes, and it generates the SQL. Spring Data JPA adds repositories on top, where you write just an interface.",
  "And they mix well in one app. JPA for everyday domain objects, and JdbcClient for a heavy report query that's easier in plain SQL.",
 ]},

{"html": H("Connections and ", "HikariCP") + row(
   col(box("red", "opening a connection", "TCP + login + setup: <b style=\"display:inline\">milliseconds</b>, every time", 0),
       box("green", "a connection pool", "keeps connections open and <b style=\"display:inline\">lends</b> them out · Boot's default: HikariCP", 1), gap=18, style="flex:1"),
   code("""§2 spring:
§2   datasource:
§2     url: jdbc:postgresql://db:5432/tasks
§2     username: app
§2     password: ${DB_PASSWORD}
§3     hikari:
§3       maximum-pool-size: 10""", 25, style="width:700px"), top=True) +
   note("Pool size is small on purpose: more connections ≠ faster", 3),
 "steps": [
  "Opening a database connection is slow. A network handshake, a login, session setup. Doing that for every request would waste milliseconds each time.",
  "So applications use a connection pool. It keeps a few connections open, and lends one to each piece of work, then takes it back. Spring Boot uses HikariCP by default, and creates the data source for you as soon as a driver is on the classpath.",
  "You only give it the URL, the user and the password. And the password comes from an environment variable, never hard coded.",
  "The pool size is deliberately small, ten by default. The database can only do so much at once, so more connections usually means more waiting, not more speed.",
 ]},

{"html": H("Schema migrations with ", "Flyway") + row(
   col(box("gray", "resources/db/migration/", "", 0),
       box("blue", "V1__create_tasks.sql", "", 0),
       box("blue", "V2__add_due_date.sql", "", 0),
       box("green", "flyway_schema_history", "records which versions ran, with checksums", 1), gap=12, style="width:620px"),
   col(box("purple", "at startup", "Flyway runs only the <b style=\"display:inline\">new</b> scripts, in order", 1),
       box("red", "never edit an applied file", "checksum mismatch → startup fails · add V3 instead", 2),
       box("orange", "ddl-auto", "<code>create</code> / <code>update</code> for demos only · <code>validate</code> or <code>none</code> in production", 3), gap=16, style="flex:1"), top=True),
 "steps": [
  "The database schema changes over time, and those changes must be versioned like code. Flyway does that with numbered SQL files. V one creates the tasks table. V two adds a due date.",
  "At startup, Flyway checks its history table, and runs only the scripts that haven't run yet, in order. Every environment ends up with exactly the same schema.",
  "The golden rule: never edit a migration that has already run. Flyway stores a checksum, and a changed file stops the app from starting. Fix things with a new migration instead.",
  "Hibernate can also create tables itself, with ddl auto. That's handy for demos, but in production set it to validate or none, and let Flyway own the schema.",
 ]},

{"html": H("Spring JDBC: ", "JdbcClient") + code("""§0 record Task(long id, String title, boolean done) {}
§0
§1 List<Task> open = jdbc.sql("SELECT id, title, done FROM tasks WHERE done = :done")
§1     .param("done", false)                 // a bind parameter, never string concat
§1     .query(Task.class)                    // map each row to a record
§1     .list();
§2 int rows = jdbc.sql("UPDATE tasks SET done = true WHERE id = :id")
§2     .param("id", 7).update();""", 26) + row(
   box("green", "Spring handles", "connections · closing · <b style=\"display:inline\">exception translation</b>", 3, "flex:1"),
   box("red", "bind parameters", "never build SQL with <code>+</code>: SQL injection", 3, "flex:1"), style="margin-top:22px"),
 "steps": [
  "Here's Spring JDBC with JdbcClient, the newer fluent API. JdbcTemplate does the same with older style methods.",
  "You write the SQL, with named parameters, and bind values with param. Then map each row, here straight into a record, and get a list. No connection handling, no result set loop.",
  "Updates work the same way, and return the number of rows affected.",
  "Spring opens and closes the connection, and translates database errors into its own exceptions, like duplicate key exception. And always use bind parameters. Gluing user input into SQL with a plus sign is how SQL injection happens.",
 ]},

{"html": H("JPA: map objects, not ", "rows") + row(
   code("""§0 @Entity
§0 @Table(name = "tasks")
§0 public class Task {
§1   @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
§1   private Long id;
§2   @Column(nullable = false, length = 200)
§2   private String title;
§2   @Enumerated(EnumType.STRING) private Priority priority;
§3   protected Task() {}      // JPA needs a no-arg constructor
§0 }""", 25, style="flex:1"),
   col(box("blue", "JPA", "the specification (<code>jakarta.persistence</code>)", 0),
       box("purple", "Hibernate", "the implementation Boot uses", 0),
       box("orange", "EnumType.STRING", "ORDINAL breaks if you reorder the enum", 2),
       box("gray", "no records", "entities must be mutable and proxyable", 3), gap=14, style="width:560px"), top=True),
 "steps": [
  "JPA is the specification, in jakarta dot persistence. Hibernate is the implementation Spring Boot uses. You describe the mapping with annotations: at entity, and the table name.",
  "Every entity needs an id. Generated value with identity lets the database assign it.",
  "Column sets constraints like not null and length. And store enums as strings. The default stores their position number, which silently breaks if someone reorders the enum.",
  "JPA also needs a no argument constructor, and the class must be mutable so Hibernate can fill it in and create proxies. That's why entities are classes, not records. Records are for DTOs.",
 ]},

{"html": H("The entity ", "lifecycle") +
   graph({"new": (110, 160), "managed": (420, 160), "detached": (730, 160), "removed": (420, 360)},
         [("new", "managed"), ("managed", "detached"), ("managed", "removed")], w=860, h=430, directed=True, r=62,
         colors={"new": ("#f3f4f6", "#6b7280"), "managed": ("#dcfce7", "#16a34a"),
                 "detached": ("#dbeafe", "#2563eb"), "removed": ("#fee2e2", "#dc2626")}, step=0) +
   row(box("gray", "new (transient)", "just <code>new Task()</code> · JPA doesn't know it", 0, "flex:1"),
       box("green", "managed", "after <code>persist</code> or <code>find</code> · <b style=\"display:inline\">changes are tracked</b>", 1, "flex:1"),
       box("blue", "detached", "the context closed · changes are <b style=\"display:inline\">ignored</b>", 2, "flex:1"),
       box("red", "removed", "<code>remove</code> · deleted on flush", 2, "flex:1"), style="margin-top:6px"),
 "steps": [
  "An entity object is always in one of four states. A new object, created with new, is transient. JPA doesn't know it exists.",
  "Persist it, or load it with find or a query, and it becomes managed. A managed entity is watched. Every change to it is tracked.",
  "When the persistence context closes, usually at the end of the transaction, the entity becomes detached. It's an ordinary object again, and changes to it are ignored, unless you merge it back. Remove marks a managed entity for deletion.",
 ]},

{"html": H("The persistence ", "context") + row(
   col(box("blue", "1 · first-level cache", "<code>find(Task, 7)</code> twice in one transaction → <b style=\"display:inline\">one</b> SELECT, the same object", 0),
       box("green", "2 · dirty checking", "change a managed entity → Hibernate notices and writes an UPDATE · <b style=\"display:inline\">no save() needed</b>", 1),
       box("orange", "3 · flush", "pending SQL is sent at commit, before a query, or on <code>flush()</code>", 2), gap=16, style="flex:1"),
   code("""§1 @Transactional
§1 void complete(long id) {
§1   Task t = em.find(Task.class, id);
§1   t.setDone(true);   // just change it
§1 }   // commit → UPDATE""", 25, style="width:640px"), top=True) +
   note("One persistence context per transaction · it's what makes JPA feel like magic", 3),
 "steps": [
  "Managed entities live in the persistence context. Think of it as a workspace for one transaction, and it does three things. First, it's a cache. Find the same task twice, and only one select is sent. You get the very same Java object.",
  "Second, dirty checking. It remembers each entity's original state. Change a field on a managed entity, and at commit Hibernate compares, notices the change, and writes the update. There's no save call in this method at all.",
  "Third, flushing. SQL isn't sent the moment you change something. It's queued, and flushed at commit, before a query that needs fresh data, or when you call flush yourself.",
  "That's the core of JPA. Normally there's one persistence context per transaction, and it's why JPA code looks like you're just changing Java objects. In part two: relationships, lazy loading, and the N plus one problem.",
 ]},

quiz([
  ("Why a connection pool?", "opening connections is <b style=\"display:inline\">slow</b>: reuse them", "blue",
   "Quiz time. Why does every app use a connection pool?",
   "Because opening a connection is slow, so a pool keeps a few open and reuses them."),
  ("A migration already ran. Need a fix?", "add a <b style=\"display:inline\">new</b> V3 file, never edit V2", "red",
   "A Flyway migration has already run, and it needs fixing. What do you do?",
   "Add a new migration. Editing an applied file changes its checksum, and startup fails."),
  ("Changed a managed entity, no save(). Saved?", "<b style=\"display:inline\">yes</b>: dirty checking at commit", "green",
   "You change a field on a managed entity inside a transaction, and never call save. Is it saved?",
   "Yes. Dirty checking notices the change, and Hibernate writes the update at commit."),
]),

recap(["JDBC → JdbcClient → JPA → Spring Data: less code each step",
       "HikariCP pools connections · small pool on purpose",
       "Flyway: numbered migrations, never edit an applied one",
       "JdbcClient: your SQL, bind parameters, no boilerplate",
       "Entity states: new · managed · detached · removed",
       "Persistence context: cache + dirty checking + flush"],
  "Let's recap part one. There are four levels, from plain JDBC up to Spring Data, each writing less code. HikariCP pools connections, and a small pool is on purpose. Flyway applies numbered migrations, and you never edit one that has run. JdbcClient runs your own SQL with bind parameters. JPA entities are new, managed, detached or removed. And the persistence context caches entities, detects changes, and flushes them as SQL. Next time, part two: relationships, fetching, the N plus one problem, and repositories!"),
]
