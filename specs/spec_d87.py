from conc import *

TAG = "Day 87 · AWS Databases, Caching and Messaging"
TRACK = "Java Fullstack · Cloud"
FILE = "Day 87 AWS Databases Caching and Messaging.mp4"

SLIDES = [
title_slide(87, "AWS Databases, Caching & Messaging", "The managed versions of PostgreSQL, Redis and queues",
  "Welcome to day eighty seven: databases, caching and messaging on AWS.",
  "You already know PostgreSQL, Redis-style caching, and messaging from the Spring track. AWS runs all of them as managed services, so backups, patching and failover become settings instead of chores. By the end you'll know RDS and Aurora, ElastiCache and the cache aside pattern, SQS queues, SNS topics and fan out, and the Well Architected Framework.",
  pill="DAY 87 · CLOUD"),

{"html": H("RDS: managed ", "databases") + row(
   col(box("blue", "RDS", "PostgreSQL, MySQL… · AWS patches, backs up, monitors", 0),
       box("green", "Multi-AZ", "a standby in another AZ · automatic failover · for <b style=\"display:inline\">availability</b>", 1),
       box("purple", "read replicas", "async copies · spread reads · for <b style=\"display:inline\">scale</b>", 2),
       box("orange", "Aurora", "AWS's compatible engine · storage across 3 AZs · fast replicas", 3), gap=14, style="width:640px"),
   graph({"app": (110, 210), "primary": (380, 110), "standby": (380, 330), "replica": (640, 110)},
         [("app", "primary"), ("primary", "standby"), ("primary", "replica")],
         colors={"primary": ("#dbeafe", "#2563eb"), "standby": ("#f3f4f6", "#6b7280"), "replica": ("#ede9fe", "#7c3aed")},
         labels={"standby": "sync · other AZ", "replica": "async · reads"}, w=740, h=440, directed=True, step=1, r=58), top=True),
 "steps": [
  "RDS runs a database like PostgreSQL for you. AWS handles patching, automated backups with point in time restore, and monitoring. You still design the schema and the queries.",
  "Multi AZ keeps a synchronous standby in another availability zone. If the primary fails, RDS fails over automatically within a minute or two. This is about availability, not speed.",
  "Read replicas are asynchronous copies you can send read queries to. They scale reads, but may lag slightly behind.",
  "Aurora is AWS's own engine, compatible with PostgreSQL and MySQL, with storage replicated across three zones and faster replicas.",
 ]},

{"html": H("ElastiCache and cache-", "aside") + row(
   code("""§1 ProjectDto find(long id) {
§1   String hit = redis.get("project:" + id);
§1   if (hit != null) return parse(hit);             // fast path
§1   ProjectDto p = repo.load(id);                    // miss → DB
§1   redis.setex("project:" + id, 600, toJson(p));    // TTL 10 min
§1   return p;
§1 }
§2 // on update: write the DB, then DELETE the key""", 23, style="flex:1"),
   col(box("blue", "ElastiCache", "managed Redis / Valkey or Memcached", 0),
       box("green", "Redis", "data structures · persistence · replication · locks, sessions", 0),
       box("gray", "Memcached", "simple key-value · multi-threaded · nothing else", 0),
       box("orange", "invalidation", "delete on write · TTL as a safety net", 2), gap=14, style="width:500px"), top=True),
 "steps": [
  "ElastiCache runs Redis, its open source fork Valkey, or Memcached. Redis has rich data structures, replication and persistence, so it also does sessions, rate limits and distributed locks. Memcached is a simple, fast key value store.",
  "The usual pattern is cache aside. Look in the cache first. On a miss, read the database, then store the result with an expiry time.",
  "When data changes, write the database and delete the cache key, so the next read loads the fresh value. The expiry time is a safety net for anything you forget.",
 ]},

{"html": H("SQS: ", "queues") + row(
   col(box("blue", "Standard", "near-unlimited throughput · at-least-once · best-effort order", 0),
       box("green", "FIFO", "exactly-once processing · strict order per group · lower throughput", 0),
       box("orange", "visibility timeout", "a received message is hidden · not deleted in time → it reappears", 1),
       box("red", "dead-letter queue", "after N failed receives → park it for inspection", 2), gap=14, style="width:600px"),
   code("""§1 receive (long polling, wait 20 s)
§1    → process
§1    → deleteMessage        // only after success!
§3 limits: 256 KB per message
§3         kept up to 14 days""", 25, style="flex:1"), top=True),
 "steps": [
  "SQS is a fully managed queue. Standard queues have almost unlimited throughput, deliver at least once, and keep order on a best effort basis. FIFO queues keep strict order within a message group and avoid duplicates, at lower throughput.",
  "A consumer receives a message, which becomes invisible for the visibility timeout. It processes it, then deletes it. If it crashes or takes too long, the message reappears for another consumer. So consumers must be idempotent.",
  "After a number of failed attempts, a redrive policy moves the message to a dead letter queue for inspection.",
  "Use long polling to cut empty responses. Messages are at most two hundred and fifty six kilobytes, so for bigger payloads, put the data in S3 and send its key.",
 ]},

{"html": H("SNS and ", "fan-out") + graph(
   {"orders": (100, 190), "SNS": (360, 190), "email": (660, 70), "stock": (660, 190), "audit": (660, 310)},
   [("orders", "SNS"), ("SNS", "email"), ("SNS", "stock"), ("SNS", "audit")],
   colors={"SNS": ("#ede9fe", "#7c3aed")}, w=780, h=400, directed=True, step=0, r=60) + row(
   box("purple", "SNS", "publish once · push to every subscriber", 0, "flex:1"),
   box("blue", "fan-out", "SNS → several SQS queues · each consumer at its own pace", 1, "flex:1"),
   box("green", "vs Kafka", "SQS/SNS: simple, managed · Kafka (MSK): replay, streams, ordering", 2, "flex:1"), top=True, style="margin-top:16px"),
 "steps": [
  "SNS is publish subscribe. A publisher sends a message to a topic once, and SNS pushes it to every subscriber: queues, Lambda functions, email or SMS.",
  "The classic pattern is fan out: an SNS topic delivering into several SQS queues. Each service gets its own copy and processes it at its own pace, and the queue buffers it if the service is down.",
  "Compared with Kafka: SQS and SNS are simpler and fully managed. Kafka, available as MSK, gives you replay, stream processing and ordered partitions.",
 ]},

{"html": H("The Well-Architected ", "Framework") + table(["Pillar", "Asks"], [
     (["Operational Excellence", "can you deploy, observe and fix it easily?"], 0),
     (["Security", "least privilege · encryption · traceability"], 0),
     (["Reliability", "Multi-AZ · backups tested · recovers by itself"], 1),
     (["Performance Efficiency", "right instance types · caching · scale out"], 1),
     (["Cost Optimisation", "pay for what you use · right-size · Savings Plans"], 2),
     (["Sustainability", "use less: efficient code, scale down when idle"], 2)], size=27),
 "steps": [
  "AWS sums up good design in the Well Architected Framework, with six pillars. Operational excellence: can you deploy, observe and fix things easily? Security: least privilege, encryption and traceability.",
  "Reliability: multiple zones, tested backups, recovery without humans. Performance efficiency: the right resources, caching, and scaling out.",
  "Cost optimisation: pay only for what you use. And sustainability: use less, by writing efficient code and scaling down when idle. Interviewers love it when you frame trade offs in these terms.",
 ]},

quiz([
  ("Multi-AZ or read replica to survive an AZ outage?", "<b style=\"display:inline\">Multi-AZ</b>", "blue",
   "Quiz time. Multi AZ or a read replica, to survive an availability zone outage?",
   "Multi AZ. Read replicas are for scaling reads."),
  ("When do you delete an SQS message?", "<b style=\"display:inline\">after</b> processing succeeds", "orange",
   "When should a consumer delete an SQS message?",
   "Only after processing succeeds. Otherwise it reappears and is retried."),
  ("One event, three services each need it?", "SNS → three SQS queues (<b style=\"display:inline\">fan-out</b>)", "purple",
   "One event must reach three services. What's the pattern?",
   "Fan out: publish to SNS, with one SQS queue per service."),
]),

recap(["RDS: managed DB · Multi-AZ = availability",
       "Read replicas = read scale · Aurora",
       "ElastiCache Redis · cache-aside, delete on write",
       "SQS: visibility timeout · delete after success · DLQ",
       "SNS fan-out to SQS queues",
       "Well-Architected: 6 pillars"],
  "Let's recap. RDS manages your database, with Multi AZ for availability and read replicas for scale, and Aurora as AWS's own engine. ElastiCache runs Redis, used with cache aside and deleting keys on writes. SQS hides received messages until they're deleted after success, with dead letter queues for failures. SNS fans one message out to several queues. And the Well Architected Framework's six pillars frame every trade off. Tomorrow: monitoring and security."),
]
