from conc import *

TAG = "Day 92 · System Design Fundamentals, Part 2"
TRACK = "Java Fullstack · System Design"
FILE = "Day 92 System Design Fundamentals Part 2.mp4"

SLIDES = [
title_slide(92, "System Design Fundamentals II", "Sharding, rate limiting, consistent hashing and Bloom filters",
  "Welcome to day ninety two: system design fundamentals, part two.",
  "Yesterday's building blocks get you a long way. Today we look inside four techniques that keep coming up when systems get big: how to shard data, how to limit request rates, consistent hashing, which lets you add servers without reshuffling everything, and Bloom filters, which answer \"have I seen this?\" in very little memory. Then a framework for answering any design question.",
  pill="DAY 92 · SYSTEM DESIGN"),

{"html": H("Sharding ", "strategies") + table(["Strategy", "How", "Watch out for"], [
     (["range", "users A–M → shard 1, N–Z → shard 2", "hot ranges (everyone signs up today)"], 0),
     (["hash", "<code>hash(userId) % N</code>", "range queries hit every shard · changing N moves almost everything"], 1),
     (["directory", "a lookup table: key → shard", "the table is a dependency · but moving data is easy"], 2)], size=26) +
   note("Pick a key that spreads load and keeps one request on one shard (e.g. tenantId)", 3),
 "steps": [
  "Sharding by range puts consecutive keys together, like users A to M on one shard. Range queries are easy, but a popular range becomes a hot spot.",
  "Hashing the key spreads load evenly. But range queries now hit every shard, and with hash modulo N, changing the number of shards moves almost every key.",
  "A directory keeps a lookup table from key to shard. Moving data is easy, but the directory itself must be fast and highly available.",
  "The shard key matters most. Choose one that spreads load and keeps a typical request on a single shard, like a tenant or user id.",
 ]},

{"html": H("Rate ", "limiting") + row(
   col(table(["Algorithm", "Behaviour"], [
     (["token bucket", "refills steadily · allows short bursts"], 0),
     (["leaky bucket", "processes at a fixed rate · smooths bursts"], 1),
     (["fixed window", "N per minute · a burst at the boundary doubles it"], 2),
     (["sliding window", "counts over the last 60 s · accurate, more memory"], 2)], size=26), style="width:780px"),
   code("""§3 -- token bucket in Redis, per user
§3 tokens = min(cap, tokens + elapsed * rate)
§3 if tokens >= 1: tokens -= 1 → allow
§3 else → 429 Too Many Requests
§3          Retry-After: 2""", 21, style="flex:1"), top=True),
 "steps": [
  "Rate limiting protects a service from abuse and overload. A token bucket refills at a steady rate up to a cap. Each request spends a token, so short bursts are allowed, which suits most APIs.",
  "A leaky bucket processes requests at a fixed rate, smoothing bursts out.",
  "A fixed window counts requests per minute, but a burst at the end of one minute and the start of the next lets through double. A sliding window fixes that at the cost of more memory.",
  "With several servers, keep the counters in Redis, updated atomically. Over the limit, reply four twenty nine, with a retry after header.",
 ]},

{"html": H("Consistent ", "hashing") + row(
   graph({"A": (300, 70), "B": (520, 260), "C": (120, 300), "k1": (500, 85), "k2": (380, 350), "k3": (150, 140)},
         [("A", "B"), ("B", "C"), ("C", "A")],
         colors={"A": ("#dbeafe", "#2563eb"), "B": ("#dbeafe", "#2563eb"), "C": ("#dbeafe", "#2563eb"),
                 "k1": ("#fef3c7", "#d97706"), "k2": ("#fef3c7", "#d97706"), "k3": ("#fef3c7", "#d97706")},
         labels={"k1": "→ B", "k2": "→ C", "k3": "→ A"}, w=640, h=420, step=0, r=40),
   col(box("blue", "the ring", "servers and keys hashed onto a circle · a key goes to the next server clockwise", 0),
       box("green", "add a server", "only keys between it and its neighbour move · ~1/N", 1),
       box("purple", "virtual nodes", "each server at many points · even spread", 2),
       box("gray", "used in", "DynamoDB · Cassandra · CDNs · load balancers", 2), gap=14, style="flex:1"), top=True),
 "steps": [
  "Consistent hashing places both servers and keys on a ring of hash values. Each key belongs to the next server going clockwise.",
  "Add a server, and only the keys between it and its neighbour move, about one over N of them, instead of nearly all of them with hash modulo N. Removing a server is just as gentle.",
  "With only a few servers, the ring is uneven, so each server is placed at many points, called virtual nodes. This idea powers DynamoDB, Cassandra, CDNs and sticky load balancing.",
 ]},

{"html": H("Bloom ", "filters") + col(
   cells([0, 1, 0, 1, 0, 0, 1, 0, 0, 1], None, None, 0, "bits", size=34, mark={1: "#bbf7d0", 3: "#bbf7d0", 6: "#bbf7d0", 9: "#bbf7d0"}), gap=14) + row(
   box("blue", "add", "set k bits chosen by k hash functions", 0, "flex:1"),
   box("green", "check", "any bit 0 → <b style=\"display:inline\">definitely not</b> · all 1 → <b style=\"display:inline\">probably</b>", 1, "flex:1"),
   box("purple", "use it", "skip a DB / disk lookup · \"username taken?\" · \"seen this URL?\"", 2, "flex:1"), top=True, style="margin-top:22px") +
   note("No false negatives · some false positives · can't delete (plain version)", 3),
 "steps": [
  "A Bloom filter is a bit array plus a few hash functions. To add an item, hash it with each function, and set those bits.",
  "To check an item, look at its bits. If any is zero, the item was definitely never added. If all are one, it was probably added, but they could have been set by other items.",
  "That makes it a cheap pre check. Before hitting a database or disk, ask the filter. Databases like Cassandra use them to skip files, and crawlers to skip seen URLs.",
  "So: no false negatives, a tunable rate of false positives, and a plain Bloom filter can't delete items.",
 ]},

{"html": H("A framework for any ", "design") + table(["Step", "Do"], [
     (["1 · requirements", "features in / out · users, QPS, data size · latency, availability"], 0),
     (["2 · API", "the main endpoints and their payloads"], 1),
     (["3 · high level", "boxes and arrows: clients, LB, services, DB, cache, queue"], 1),
     (["4 · data", "schema, SQL or NoSQL, shard key"], 2),
     (["5 · deep dive", "the hardest part · bottlenecks · scale and failures"], 2)], size=27) +
   note("Talk trade-offs out loud · estimate with round numbers", 3),
 "steps": [
  "To answer any design question, follow a framework. Start with requirements: what's in and out of scope, and numbers like users, requests per second and data size, plus latency and availability goals.",
  "Sketch the API, then the high level design: clients, load balancer, services, database, cache and queues.",
  "Choose the data model and storage, including a shard key if needed. Then deep dive into the hardest part, its bottlenecks, and how it scales and fails.",
  "Throughout, say the trade offs out loud, and estimate with round numbers. Interviewers grade the reasoning, not a perfect diagram.",
 ]},

quiz([
  ("hash % N, add a shard: how many keys move?", "almost <b style=\"display:inline\">all</b> of them", "red",
   "Quiz time. With hash modulo N, you add one shard. How many keys move?",
   "Almost all of them. Consistent hashing moves only about one over N."),
  ("Token bucket allows bursts?", "<b style=\"display:inline\">yes</b>, up to the bucket size", "blue",
   "Does a token bucket allow bursts?",
   "Yes, up to the bucket's capacity, then at the refill rate."),
  ("Bloom filter says \"not present\": sure?", "<b style=\"display:inline\">yes</b>: no false negatives", "green",
   "A Bloom filter says an item isn't present. Can you trust it?",
   "Yes. There are no false negatives."),
]),

recap(["Sharding: range · hash · directory · pick the key well",
       "Rate limits: token bucket, sliding window · 429",
       "Consistent hashing: ~1/N keys move · virtual nodes",
       "Bloom filter: definitely not / probably yes",
       "Framework: requirements → API → design → data → deep dive",
       "Say trade-offs out loud"],
  "Let's recap. Shard by range, hash or directory, and choose the shard key carefully. Rate limit with a token bucket or sliding window, and answer four twenty nine. Consistent hashing moves only about one over N keys when servers change, helped by virtual nodes. A Bloom filter says definitely not, or probably yes, in very little memory. And answer designs with a framework: requirements, API, high level, data, and a deep dive, saying the trade offs out loud. Next: practice designs."),
]
