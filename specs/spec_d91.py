from conc import *

TAG = "Day 91 · System Design Fundamentals, Part 1"
TRACK = "Java Fullstack · System Design"
FILE = "Day 91 System Design Fundamentals Part 1.mp4"

SLIDES = [
title_slide(91, "System Design Fundamentals I", "CAP, scaling databases, caching, load balancing and queues",
  "Welcome to day ninety one: system design fundamentals, part one.",
  "System design interviews ask how you'd build something big, like a URL shortener or a chat app. There's no single right answer, but there is a shared vocabulary of building blocks and trade offs. By the end you'll know the CAP theorem and PACELC, how databases scale, caching strategies, load balancing algorithms, and when to use a queue versus an event stream.",
  pill="DAY 91 · SYSTEM DESIGN"),

{"html": H("The CAP ", "theorem") + row(
   col(box("blue", "Consistency", "every read sees the latest write", 0),
       box("green", "Availability", "every request gets an answer", 0),
       box("orange", "Partition tolerance", "keeps working when the network splits", 0), gap=14, style="width:520px"),
   col(box("red", "the real choice", "partitions <b style=\"display:inline\">will</b> happen → during one, pick C or A", 1),
       table(["System", "Leans"], [
         (["a bank balance", "CP: refuse rather than be wrong"], 2),
         (["a like counter, a feed", "AP: answer, catch up later"], 2),
         (["ZooKeeper · Cassandra", "CP · AP (tunable)"], 2)], size=26),
       box("purple", "PACELC", "<b style=\"display:inline\">E</b>lse, with no partition: trade <b style=\"display:inline\">L</b>atency vs <b style=\"display:inline\">C</b>onsistency", 3), gap=14, style="flex:1"), top=True),
 "steps": [
  "The CAP theorem talks about three properties of a distributed data store. Consistency: every read sees the latest write. Availability: every request gets a response. Partition tolerance: the system keeps working when the network between nodes breaks.",
  "Networks do fail, so partition tolerance isn't optional. The real choice is what to do during a partition: refuse some requests to stay consistent, or answer them and risk stale data.",
  "A bank balance should be CP: better to refuse than show the wrong amount. A like counter or a news feed can be AP: answer now, catch up later. ZooKeeper is CP, Cassandra leans AP, with tunable consistency.",
  "PACELC adds the everyday case. Even without a partition, there's a trade off between latency and consistency, because waiting for replicas takes time.",
 ]},

{"html": H("Scaling a ", "database") + row(
   box("blue", "vertical", "a bigger machine · simple · has a ceiling and a single point of failure", 0, "flex:1"),
   box("green", "read replicas", "copies for reads · writes still to one primary · replica lag", 1, "flex:1"),
   box("purple", "sharding", "split rows across databases by a key · scales writes · hard", 2, "flex:1"), top=True) +
   pts([("Usually in this order: index + tune queries → cache → replicas → shard", 3),
        ("Sharding costs: cross-shard joins, rebalancing, distributed transactions", 3)], size=30),
 "steps": [
  "The simplest way to scale a database is vertically: a bigger machine. It's easy, but there's a ceiling, and it's still one machine.",
  "Read replicas copy the data for read traffic. Most apps read far more than they write, so this goes a long way. Writes still go to one primary, and replicas can lag a little.",
  "Sharding splits the rows across several databases by a key, like user id. That finally scales writes, but it's hard.",
  "So go in order: fix indexes and queries, add a cache, add replicas, and shard only when you must. Sharding brings cross shard joins, rebalancing and distributed transactions.",
 ]},

{"html": H("Caching ", "strategies") + table(["Strategy", "How", "Trade-off"], [
     (["cache-aside", "app reads cache → on miss, DB → fill cache", "simple · first read slow · may be stale"], 0),
     (["write-through", "write cache and DB together", "fresh reads · slower writes"], 1),
     (["write-behind", "write cache now, DB later in batches", "fast writes · data loss risk"], 1),
     (["CDN", "copies at the edge, near users", "static files, images, cached API GETs"], 2)], size=27) +
   note("Hard part: invalidation · delete on write + a TTL · watch for a stampede on hot keys", 3),
 "steps": [
  "Caching keeps frequently read data in fast memory. Cache aside is the default: the app checks the cache, and on a miss reads the database and fills the cache.",
  "Write through writes to the cache and the database together, so reads are always fresh but writes are slower. Write behind writes to the cache immediately and to the database later in batches: fast, but you can lose data if the cache dies.",
  "A CDN caches content at edge locations near users, for static files, images, and cacheable API responses.",
  "The hard part is invalidation. Delete keys on writes, keep a TTL as a safety net, and protect hot keys from a stampede, when thousands of requests miss at once and all hit the database.",
 ]},

{"html": H("Load ", "balancing") + row(
   table(["Algorithm", "Good for"], [
     (["round robin", "equal servers, similar requests"], 0),
     (["least connections", "requests of very different length"], 1),
     (["IP / consistent hash", "the same client or key → the same server"], 2)], size=27),
   col(box("blue", "L4 vs L7", "L4: TCP, fast · L7: HTTP, routes by path, header, cookie", 0),
       box("green", "health checks", "unhealthy servers are taken out", 1),
       box("orange", "stateless servers", "sessions in Redis or a token → any server can answer", 3), gap=14, style="width:560px"), top=True),
 "steps": [
  "A load balancer spreads requests across servers. Round robin takes turns, which is fine when servers and requests are similar. It can work at layer four, on TCP connections, or at layer seven, on HTTP, routing by path or header.",
  "Least connections sends work to the least busy server, better when some requests take much longer than others. Health checks remove broken servers.",
  "Hashing the client or a key sends the same one to the same server, which helps caching.",
  "But the best design keeps servers stateless. Store sessions in Redis or in a token, and then any server can handle any request, and you scale by just adding more.",
 ]},

{"html": H("Queues vs event ", "streams") + row(
   box("blue", "a queue (SQS, RabbitMQ)", "a task for <b style=\"display:inline\">one</b> worker · deleted when done · retries, DLQ", 0, "flex:1"),
   box("purple", "a stream (Kafka, Kinesis)", "an event log for <b style=\"display:inline\">many</b> readers · kept · replayable · ordered per partition", 1, "flex:1"), top=True) +
   table(["Use case", "Pick"], [
     (["send this email, resize this image", "queue"], 2),
     (["order placed → email, stock, analytics, audit", "stream (or SNS fan-out)"], 2),
     (["rebuild a view by replaying history", "stream"], 2)], size=27),
 "steps": [
  "Both decouple services, but differently. A queue holds tasks. Each message goes to one worker, and is deleted once handled, with retries and a dead letter queue.",
  "A stream is a log of events. Many independent consumers read it, the events are kept, can be replayed, and are ordered within a partition.",
  "So: a job to do, like sending one email, use a queue. A fact that many services care about, like order placed, use a stream, or SNS fan out. And if you need to rebuild data by replaying history, only a stream can do that.",
 ]},

quiz([
  ("During a partition, CAP makes you choose…?", "<b style=\"display:inline\">consistency</b> or <b style=\"display:inline\">availability</b>", "blue",
   "Quiz time. During a network partition, what does CAP make you choose between?",
   "Consistency or availability."),
  ("Reads overwhelm the DB: first step after indexes?", "a <b style=\"display:inline\">cache</b>, then read replicas", "green",
   "Reads are overwhelming the database, and indexes are fine. What next?",
   "Add a cache, then read replicas. Shard last."),
  ("Make any server able to handle any request?", "keep servers <b style=\"display:inline\">stateless</b>", "purple",
   "How do you let any server handle any request?",
   "Keep servers stateless, with sessions in Redis or a token."),
]),

recap(["CAP: during a partition, pick C or A · PACELC",
       "Scale DB: tune → cache → replicas → shard",
       "Cache-aside · write-through · write-behind · CDN",
       "Invalidation: delete on write + TTL",
       "LB: round robin, least connections, hashing",
       "Queue = task for one · stream = events for many"],
  "Let's recap. CAP says that during a partition you choose consistency or availability, and PACELC adds latency versus consistency the rest of the time. Scale a database by tuning, caching, replicas, and sharding last. Know cache aside, write through, write behind and CDNs, and invalidate on writes with a TTL. Load balancers use round robin, least connections or hashing, in front of stateless servers. And queues hold tasks for one worker, while streams hold events for many. Next: scaling techniques."),
]
