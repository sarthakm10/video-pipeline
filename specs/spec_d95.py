from conc import *

TAG = "Day 95 · Revision: Spring, Kafka and Cloud"
TRACK = "Java Fullstack · Revision"
FILE = "Day 95 Revision Spring Kafka and Cloud.mp4"

SLIDES = [
title_slide(95, "Revision: Spring, Kafka & Cloud", "The backend stack you'll actually be hired to work on",
  "Welcome to day ninety five: revising Spring, Kafka and the cloud.",
  "Today is the backend half of your revision. We'll go over the Spring traps interviewers love, the JWT flow and auto configuration, then go deeper on Kafka than before: consumer lag, rebalancing and Kafka Streams. We'll add two ideas that often come with microservices, CQRS and event sourcing, and finish with rapid fire AWS and design pattern questions.",
  pill="DAY 95 · REVISION"),

{"html": H("Two Spring ", "traps") + row(
   code("""§0 @Service class OrderService {
§0   public void placeAll(List<Order> os) {
§0     os.forEach(this::place);    // self-call: no proxy → no transaction!
§0   }
§0   @Transactional public void place(Order o) { … }
§0 }
§2 // N+1: 1 query for 100 orders + 100 for their items
§2 @Query("select o from Order o join fetch o.items")""", 22, style="flex:1"),
   col(box("red", "self-invocation", "<code>this.place()</code> skips the proxy · move it to another bean", 0),
       box("orange", "checked exceptions", "don't roll back by default · <code>rollbackFor = Exception.class</code>", 1),
       box("blue", "N+1 fixes", "<code>JOIN FETCH</code> · <code>@EntityGraph</code> · <code>@BatchSize</code>", 2), gap=14, style="width:480px"), top=True),
 "steps": [
  "Transactional works through a proxy that wraps your bean. When a method calls another method on this, the call never goes through the proxy, so no transaction starts. The fix is to put the transactional method in a different bean.",
  "Second trap: by default, only unchecked exceptions roll back. A checked exception commits the transaction, unless you add roll back for.",
  "And the N plus one problem: one query loads a hundred orders, then a lazy collection fires one more query per order. Fix it with join fetch, an entity graph, or batch size.",
 ]},

{"html": H("Spring ", "rapid-fire") + table(["Question", "Answer"], [
     (["JWT flow?", "login → signed token · client sends <code>Bearer</code> · a filter verifies each request"], 0),
     (["Bean lifecycle?", "create → inject → <code>@PostConstruct</code> → use → <code>@PreDestroy</code>"], 1),
     (["How does auto-config decide?", "<code>@ConditionalOnClass</code> · <code>@ConditionalOnMissingBean</code> · properties"], 1),
     (["<code>@WebMvcTest</code> vs <code>@SpringBootTest</code>?", "web layer only, fast vs the whole app"], 2),
     (["Constructor or field injection?", "constructor: final fields, easy to test"], 2)], size=27),
 "steps": [
  "JWT: logging in returns a signed token. The client sends it as a bearer header, and a filter checks the signature and expiry on every request, with no session on the server.",
  "A bean is created, its dependencies are injected, post construct runs, it's used, and pre destroy runs at shutdown. Auto configuration creates beans only when conditions hold: a class is on the classpath, you haven't defined your own bean, or a property is set.",
  "Web MVC test loads only the web layer, so it's fast. Spring Boot test starts the whole application. And prefer constructor injection: fields can be final, and tests can pass mocks directly.",
 ]},

{"html": H("Kafka: lag and ", "rebalancing") + row(
   col(code("""§0 partition 0:  end offset 1,200
§0               committed  1,150   → lag 50
§0 partition 1:  end offset   900
§0               committed    300   → lag 600 ⚠""", 23),
       box("blue", "consumer lag", "how far a group is behind · growing lag = consumers too slow", 0),
       box("green", "fix lag", "more partitions + consumers · faster processing · batch", 1), gap=14, style="flex:1"),
   col(box("orange", "rebalance", "a consumer joins, leaves or misses <code>max.poll.interval</code> → partitions reassigned", 2),
       box("red", "the cost", "eager: everyone stops · duplicates if offsets weren't committed", 2),
       box("purple", "calmer rebalances", "cooperative-sticky assignor · static membership", 3), gap=14, style="width:560px"), top=True),
 "steps": [
  "Consumer lag is how far a consumer group is behind: the newest offset in a partition minus the offset the group has committed. Here partition one is six hundred messages behind. Lag that keeps growing means consumers can't keep up.",
  "To fix it, add partitions and consumers, since one partition is read by only one consumer in a group, or make processing faster, for example by batching.",
  "A rebalance reassigns partitions when a consumer joins, leaves, or takes longer than max poll interval between polls. In the classic eager style, every consumer stops, and uncommitted work is processed again, so you get duplicates.",
  "The cooperative sticky assignor moves only the partitions that must move, and static membership lets a restarting consumer keep its partitions, so rolling deploys don't trigger rebalances.",
 ]},

{"html": H("Delivery guarantees and Kafka ", "Streams") + row(
   col(table(["Guarantee", "How", "Risk"], [
     (["at-most-once", "commit, then process", "lost messages"], 0),
     (["at-least-once", "process, then commit", "duplicates → idempotent consumer"], 0),
     (["exactly-once", "transactions · read-process-write", "Kafka to Kafka only"], 1)], size=25), style="flex:1"),
   col(box("blue", "Kafka Streams", "a Java library · runs inside your app · no extra cluster", 2),
       box("green", "KStream vs KTable", "every event vs the latest value per key", 2),
       box("purple", "state", "counts, joins, windows · stored locally, backed up to Kafka", 3), gap=14, style="width:520px"), top=True),
 "steps": [
  "At most once commits the offset before processing, so a crash loses messages. At least once processes first and commits after, so a crash repeats messages, which is why consumers must be idempotent. This is what most systems use.",
  "Exactly once uses Kafka transactions, so reading, processing and writing results commit together. It only covers Kafka to Kafka: a call to an external system can still happen twice.",
  "Kafka Streams is a Java library for processing streams inside your own application, with no separate cluster. A KStream is every event, while a KTable keeps the latest value for each key, like a table built from a changelog.",
  "It supports stateful operations like counts, joins and time windows. The state lives in a local store and is backed up to a Kafka topic, so another instance can take over.",
 ]},

{"html": H("CQRS and event ", "sourcing") + graph(
   {"cmd": (90, 90), "write": (330, 90), "events": (570, 90), "read": (810, 90), "query": (1040, 90)},
   [("cmd", "write"), ("write", "events"), ("events", "read"), ("query", "read")],
   colors={"write": ("#dbeafe", "#2563eb"), "events": ("#ede9fe", "#7c3aed"), "read": ("#dcfce7", "#16a34a")},
   labels={"cmd": "change data", "write": "rules + validation", "events": "append-only log", "read": "shaped for screens", "query": "read data"},
   w=1130, h=230, directed=True, step=0, r=56) + row(
   box("blue", "CQRS", "separate models for writes and reads · scale them apart", 0, "flex:1"),
   box("purple", "event sourcing", "store the events, not the current state · replay to rebuild", 1, "flex:1"),
   box("orange", "the price", "reads lag behind · more moving parts · use only when needed", 2, "flex:1"), top=True, style="margin-top:10px"),
 "steps": [
  "CQRS means command query responsibility segregation: one model handles commands that change data, with all the business rules, and a separate model answers queries, shaped exactly for the screens that read it. Each side can be scaled and stored differently.",
  "Event sourcing goes further: instead of storing the current state, you store every event that happened, like order placed and item added, in an append only log. Current state is rebuilt by replaying them, and you get a full audit history for free.",
  "The cost: read models update a moment later, there are more moving parts, and changing event formats is tricky. Use them for complex domains or strong audit needs, not for a simple CRUD app.",
 ]},

{"html": H("AWS and patterns: ", "rapid-fire") + row(
   col(table(["AWS question", "Answer"], [
     (["EC2, Fargate or Lambda?", "servers · containers · functions"], 0),
     (["Give an app access?", "an IAM <b>role</b>, never keys"], 0),
     (["Database subnet?", "private"], 0),
     (["Terraform workflow?", "init → plan → apply"], 0)], size=25), style="flex:1"),
   col(table(["Description", "Pattern"], [
     (["wraps an object to add behaviour", "Decorator"], 1),
     (["swap algorithms at run time", "Strategy"], 1),
     (["notify many on a change", "Observer"], 2),
     (["step-by-step object creation", "Builder"], 2),
     (["make one interface fit another", "Adapter"], 2)], size=25), style="width:640px"), top=True),
 "steps": [
  "Quick AWS checks. EC2 gives you servers, Fargate runs containers, Lambda runs functions on demand. Apps get permissions through IAM roles, never stored keys. Databases live in private subnets. And Terraform runs init, plan, then apply.",
  "Now name the pattern. Wraps an object to add behaviour: decorator. Interchangeable algorithms chosen at run time: strategy.",
  "Notify many listeners when something changes: observer. Build a complex object step by step: builder. Make one interface fit another: adapter.",
 ]},

quiz([
  ("<code>this.save()</code> on a <code>@Transactional</code> method: transaction?", "<b style=\"display:inline\">no</b>: the proxy is skipped", "red",
   "Quiz time. A method calls this dot save, and save is transactional. Does a transaction start?",
   "No. Self invocation skips the proxy."),
  ("Lag keeps growing on one partition: why?", "consumers are <b style=\"display:inline\">too slow</b> for the traffic", "orange",
   "Consumer lag keeps growing. What does it tell you?",
   "The consumers can't keep up with the incoming messages."),
  ("Store every change and replay to rebuild state?", "<b style=\"display:inline\">event sourcing</b>", "purple",
   "You store every change as an event, and replay them to rebuild state. What's that called?",
   "Event sourcing."),
]),

recap(["@Transactional: self-calls and checked exceptions",
       "N+1 → JOIN FETCH, @EntityGraph, @BatchSize",
       "Lag = end offset − committed · rebalances cause duplicates",
       "At-least-once + idempotent consumers · Kafka Streams",
       "CQRS: split reads and writes · event sourcing: store events",
       "Roles not keys · name the pattern"],
  "Let's recap. Transactional fails on self calls and doesn't roll back checked exceptions by default. Fix N plus one with join fetch, an entity graph or batch size. Consumer lag is the newest offset minus the committed one, and rebalances can cause duplicates, softened by cooperative and static membership. Most systems use at least once delivery with idempotent consumers, and Kafka Streams processes streams inside your app. CQRS splits reads from writes, and event sourcing stores events instead of state. Tomorrow: revising SQL and system design."),
]
