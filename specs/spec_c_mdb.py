from conc import *

TAG = "Spring · MongoDB"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring MongoDB.mp4"

SLIDES = [
title_slide(0, "MongoDB with Spring Data", "Documents instead of rows: when it fits, and how to model it",
  "Welcome. Today's concept: NoSQL with Spring Data MongoDB.",
  "Not all data fits neatly into tables. MongoDB stores whole documents, which can be a better fit, or a painful mistake. By the end you'll know the document model, embedding versus referencing, mapping and its traps, repositories and MongoTemplate queries, aggregation pipelines, indexes, atomicity and locking, schema evolution, and when to pick MongoDB over SQL.",
  pill="SPRING · CONCEPT"),

{"html": H("The document ", "model") + row(
   code("""§0 {
§0   "_id": ObjectId("665f…"),
§0   "title": "Launch plan",
§0   "owner": { "name": "Asha", "email": "asha@x.com" },
§0   "tags": ["q4", "marketing"],
§0   "tasks": [
§0     { "title": "Draft copy", "done": true },
§0     { "title": "Book venue", "done": false }
§0   ]
§0 }""", 25, style="flex:1"),
   col(box("blue", "a document", "JSON-like (BSON) · nested objects and arrays", 0),
       box("green", "a collection", "a group of documents · no fixed schema", 1),
       box("purple", "one read", "the whole project, with its tasks, in one fetch · no joins", 2), gap=14, style="width:560px"), top=True),
 "steps": [
  "MongoDB stores documents: JSON like objects, saved as binary BSON, with nested objects and arrays. One project document can hold its owner, its tags, and its tasks.",
  "Documents live in collections. The database doesn't enforce a schema, so documents in one collection can differ.",
  "The win: the whole project, with its tasks, comes back in one read, with no joins. Data that's used together is stored together.",
 ]},

{"html": H("Embed or ", "reference?") + row(
   box("green", "embed", "owned by the parent · read together · bounded size · e.g. an order's lines", 0, "flex:1"),
   box("blue", "reference", "shared, large or growing without limit · e.g. users, comments", 1, "flex:1"), top=True) +
   code("""§0 @Document("orders") class Order { List<OrderLine> lines; }     // embedded
§1 @Document("projects") class Project {
§1   @DocumentReference(lazy = true) User owner;                 // stores the id
§1 }""", 24, style="margin-top:22px") +
   note("The 16 MB document limit · unbounded arrays are a classic mistake", 2),
 "steps": [
  "The core design question is embed or reference. Embed data that belongs to the parent, is read with it, and stays bounded, like the lines of an order.",
  "Reference data that's shared, large, or grows without limit, like users who own many projects. Document reference stores the id and loads the other document when needed.",
  "A document can be at most sixteen megabytes, so an array that grows forever, like every comment ever posted, belongs in its own collection.",
 ]},

{"html": H("Mapping and its ", "traps") + row(
   code("""§0 @Document("tasks")
§0 class Task {
§0   @Id String id;                         // ObjectId as a string
§0   @Field("t") String title;              // stored as "t"
§0   @Indexed TaskStatus status;
§1   Instant dueAt;                         // stored as a UTC date
§2   @Version Long version;
§0 }""", 25, style="flex:1"),
   col(box("blue", "@Document", "a class ↔ a collection · <code>@Id</code> ↔ <code>_id</code>", 0),
       box("red", "the LocalDate trap", "BSON has one date type, a UTC instant · LocalDate shifts by the zone", 1),
       box("green", "@Version", "optimistic locking, as in JPA", 2), gap=14, style="width:560px"), top=True),
 "steps": [
  "Mapping looks like JPA. Document maps a class to a collection, and the id field maps to underscore id, usually an ObjectId. Field can rename a property in storage.",
  "Watch out for dates. BSON has one date type, a UTC instant. A local date is converted using the server's time zone, so in some zones the stored date shifts by a day. Prefer instants, or store dates as strings.",
  "And a version field gives optimistic locking, just like JPA.",
 ]},

{"html": H("Repositories and ", "MongoTemplate") + code("""§0 interface TaskRepository extends MongoRepository<Task, String> {
§0   List<Task> findByStatusAndTagsContaining(TaskStatus s, String tag);
§0 }
§1 Query q = new Query(Criteria.where("status").is(OPEN)
§1                    .and("dueAt").lt(Instant.now()));
§1 List<Task> overdue = mongo.find(q, Task.class);
§2 mongo.updateFirst(Query.query(Criteria.where("_id").is(id)),
§2     new Update().set("status", DONE).inc("version", 1), Task.class);""", 23) +
   note("A partial update changes one field on the server · no read-modify-write race", 3),
 "steps": [
  "Mongo repository works like Spring Data JPA. Derived query methods are generated from their names.",
  "For dynamic queries, Mongo template takes a query built from criteria. Here: open tasks that are overdue.",
  "Updates can be partial. Set one field, increment another, directly on the server.",
  "That's important: instead of reading a document, changing it, and saving the whole thing back, which can overwrite someone else's change, the server applies just your change.",
 ]},

{"html": H("Aggregation ", "pipelines") + row(
   code("""§0 Aggregation.newAggregation(
§0   match(Criteria.where("status").is(DONE)),
§1   unwind("tags"),
§2   group("tags").count().as("n"),
§3   sort(Sort.by(DESC, "n")),
§3   limit(5)
§0 );""", 26, style="flex:1"),
   col(box("blue", "$match", "filter · like WHERE · put it first, it can use indexes", 0),
       box("green", "$unwind", "one document per array element", 1),
       box("purple", "$group", "like GROUP BY · count, sum, avg", 2),
       box("orange", "$sort · $limit · $lookup", "order · cut · join another collection", 3), gap=14, style="width:560px"), top=True),
 "steps": [
  "Aggregation pipelines are MongoDB's answer to SQL reports. Documents flow through stages. Match filters, like where. Put it first, so it can use an index.",
  "Unwind turns one document with three tags into three documents, one per tag.",
  "Group collects them, like group by, here counting tasks per tag.",
  "Then sort and limit give the top five tags. And lookup can join another collection when you need to.",
 ]},

{"html": H("Indexes, atomicity and ", "transactions") + row(
   col(box("blue", "indexes", "<code>@Indexed</code> · <code>@CompoundIndex</code> · same left-prefix rule as SQL", 0),
       box("red", "the auto-index trap", "off by default · create indexes explicitly or in a migration", 1),
       box("green", "atomic per document", "one document's update is all or nothing", 2),
       box("purple", "transactions", "multi-document · need a replica set · use sparingly", 3), gap=14, style="flex:1"),
   col(box("orange", "schema evolution", "no migrations forced · old and new shapes coexist · version field or lazy upgrade on read", 4),
       box("gray", "testing", "Testcontainers MongoDB · <code>@DataMongoTest</code>", 4), gap=14, style="width:560px"), top=True),
 "steps": [
  "Indexes work much like SQL, including the left prefix rule for compound indexes.",
  "But Spring Data no longer creates indexes from annotations automatically. If you don't create them explicitly, queries silently scan the whole collection.",
  "A write to a single document is atomic, which is another reason to embed data that changes together.",
  "Multi document transactions exist, but need a replica set and cost performance. Needing them a lot suggests the data is really relational.",
  "Without a fixed schema, old and new document shapes coexist. Handle that with a schema version field, or upgrade documents as you read them. Test against a real MongoDB in Testcontainers.",
 ]},

{"html": H("MongoDB or ", "SQL?") + table(["Pick", "When"], [
     (["<b>MongoDB</b>", "self-contained aggregates read whole · varying shapes · catalogues, content, events"], 0),
     (["<b>SQL</b>", "many relationships · joins · multi-row transactions · reports across entities"], 1),
     (["either", "a good model matters more than the engine"], 2)], size=29) +
   note("Most business data is relational · default to PostgreSQL unless documents clearly fit", 2),
 "steps": [
  "MongoDB fits when data forms self contained aggregates that are read whole, or when shapes vary: product catalogues, content, event logs.",
  "SQL fits when entities have many relationships, you need joins, transactions across many rows, and reports that cut across entities.",
  "Either way, a good data model matters more than the engine. And since most business data is relational, PostgreSQL is a sensible default unless documents are clearly a better fit.",
 ]},

quiz([
  ("Embed or reference a user's comments (thousands)?", "<b style=\"display:inline\">reference</b>: unbounded growth", "blue",
   "Quiz time. A user can write thousands of comments. Embed them in the user, or reference them?",
   "Reference them. Unbounded arrays hit the document limit."),
  ("Is a single-document update atomic?", "<b style=\"display:inline\">yes</b>, always", "green",
   "Is an update to a single document atomic?",
   "Yes. A single document's update is all or nothing."),
  ("@Indexed but queries still scan?", "auto-index is <b style=\"display:inline\">off</b>: create them", "red",
   "You annotated a field with indexed, but queries still scan the collection. Why?",
   "Automatic index creation is off. Create the indexes explicitly."),
]),

recap(["Documents: nested data read in one fetch",
       "Embed owned + bounded · reference shared + growing",
       "Dates are UTC instants · @Version locking",
       "Repositories · Criteria queries · partial updates",
       "Pipelines: $match → $group → $sort",
       "Create indexes yourself · default to SQL if relational"],
  "Let's recap. MongoDB stores documents, so data used together comes back in one read. Embed what's owned and bounded, reference what's shared or grows. Dates are stored as UTC instants, and version gives optimistic locking. Use repositories, criteria queries and partial updates. Aggregation pipelines match, group and sort. And create indexes yourself, keep single document atomicity in mind, and default to SQL when the data is relational. Now practise with the examples in your notes!"),
]
