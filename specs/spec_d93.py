from conc import *

TAG = "Day 93 · System Design Practice"
TRACK = "Java Fullstack · System Design"
FILE = "Day 93 System Design Practice.mp4"

SLIDES = [
title_slide(93, "System Design Practice", "Four classic interview designs, walked through with the framework",
  "Welcome to day ninety three: system design practice.",
  "Now we apply the framework to the designs interviewers ask most: a URL shortener, a notification system, a chat application, and search autocomplete. For each one, we'll focus on the key decisions and trade offs, not every box. By the end you'll have a pattern you can reuse for designs you've never seen.",
  pill="DAY 93 · SYSTEM DESIGN"),

{"html": H("URL shortener: the ", "core") + row(
   col(box("blue", "requirements", "shorten · redirect fast · 100:1 reads to writes · links last years", 0),
       box("green", "the key", "a counter → base62 · 7 chars = 3.5 trillion codes", 1),
       box("orange", "or hashing", "hash(url) → first 7 chars · check collisions", 1), gap=14, style="width:600px"),
   code("""§2 POST /api/links {"url": "https://…"}  → 201 {"code": "aZ3k9Qx"}
§2 GET  /aZ3k9Qx  → 302 Location: https://…
§3 links(code PK, url, owner, created_at, expires_at)""", 23, style="flex:1"), top=True),
 "steps": [
  "A URL shortener turns a long link into a short code, and redirects. Reads outnumber writes about a hundred to one, redirects must be fast, and links live for years.",
  "The heart is generating codes. A global counter, encoded in base sixty two, gives unique, short codes. Seven characters cover three and a half trillion links. Alternatively, hash the URL and take the first characters, checking for collisions.",
  "The API is two calls: create a link, and a redirect.",
  "The data is a simple key value lookup from code to URL, which fits any database well, SQL or NoSQL.",
 ]},

{"html": H("URL shortener: ", "scale") + row(
   box("blue", "301 vs 302", "301: browsers cache it, fewer hits · 302: every click reaches you → analytics", 0, "flex:1"),
   box("green", "cache the hot links", "Redis in front · most clicks go to few links", 1, "flex:1"),
   box("purple", "counter at scale", "each server reserves a block of 1,000 ids", 2, "flex:1"), top=True) +
   note("Analytics: write click events to a stream, aggregate later, keep the redirect fast", 3),
 "steps": [
  "A permanent redirect, three oh one, is cached by browsers, so fewer requests reach you. A temporary one, three oh two, means every click comes through, which you need for analytics.",
  "A few links get most of the clicks, so cache them in Redis in front of the database.",
  "A single counter would be a bottleneck, so each server reserves a block of ids at a time and hands them out locally.",
  "For analytics, don't slow the redirect. Write a click event to a stream, and aggregate it later.",
 ]},

{"html": H("Notification ", "system") + graph(
   {"apps": (100, 210), "API": (330, 210), "queue": (560, 210), "email": (820, 80), "push": (820, 210), "SMS": (820, 340)},
   [("apps", "API"), ("API", "queue"), ("queue", "email"), ("queue", "push"), ("queue", "SMS")],
   colors={"queue": ("#ede9fe", "#7c3aed")}, labels={"API": "prefs · limits", "queue": "per priority"},
   w=920, h=420, directed=True, step=0, r=54) + row(
   box("blue", "priorities", "OTPs ahead of marketing · separate queues", 1, "flex:1"),
   box("orange", "reliability", "retries with backoff · DLQ · idempotency key", 2, "flex:1"),
   box("green", "respect users", "preferences · quiet hours · per-user rate limit", 2, "flex:1"), top=True, style="margin-top:12px"),
 "steps": [
  "A notification system takes requests from other services, checks preferences and limits, and puts work on queues. Workers per channel send email, push and SMS through providers.",
  "Use separate queues by priority, so a one time password never waits behind a marketing blast.",
  "Providers fail, so retry with backoff, park failures in a dead letter queue, and use an idempotency key so a retry never sends twice. And respect users: preferences, quiet hours, and a per user rate limit.",
 ]},

{"html": H("Chat ", "application") + row(
   col(box("blue", "WebSockets", "a long-lived connection per user · server pushes messages", 0),
       box("green", "routing", "user → which gateway server · stored in Redis · pub/sub between servers", 1),
       box("purple", "ordering", "a sequence number per conversation · clients sort and dedupe", 2),
       box("orange", "receipts + presence", "sent ✓ · delivered ✓✓ · read · heartbeats for online", 3), gap=14, style="width:640px"),
   code("""§2 messages(
§2   conversation_id,   -- partition key
§2   seq,               -- sort key
§2   sender_id, body, sent_at
§2 )
§3 offline? → store + push notification
§3 reconnect → fetch seq > last seen""", 24, style="flex:1"), top=True),
 "steps": [
  "Chat needs messages pushed instantly, so each online user keeps a WebSocket connection open to a gateway server.",
  "Users are spread over many gateways. Keep a map from user to gateway in Redis, and pass messages between servers with pub sub.",
  "For ordering, give each message a sequence number within its conversation. Store messages partitioned by conversation and sorted by sequence, a great fit for Cassandra or DynamoDB.",
  "Receipts track sent, delivered and read. Presence uses heartbeats. Offline users get a push notification, and on reconnect they fetch everything after the last sequence they saw.",
 ]},

{"html": H("Search ", "autocomplete") + row(
   col(box("blue", "a trie", "prefix → node · keep the top 5 completions at each node", 0),
       box("green", "ranking", "by frequency from search logs · rebuilt offline, e.g. hourly", 1),
       box("purple", "speed", "cache popular prefixes · CDN / browser cache · debounce typing", 2), gap=14, style="width:620px"),
   code("""§0 "ja"   → java, javascript, jaipur, jam, jacket
§0 "jav"  → java, javascript, java 21, javelin
§1 search logs → batch job → new trie → swap in
§2 client: wait ~150 ms after typing stops""", 24, style="flex:1"), top=True) +
   note("Reads must be ~instant · writes can lag by an hour", 3),
 "steps": [
  "Autocomplete suggests completions as you type. A trie maps each prefix to a node, and storing the top few completions at every node makes lookups instant.",
  "Rankings come from search logs. A batch job recounts frequencies and builds a new trie, say hourly, then swaps it in.",
  "Popular prefixes are cached, even at the CDN, and the client waits until typing pauses before asking.",
  "The trade off: reads must feel instant, while suggestions may lag an hour behind. That's fine for this product.",
 ]},

quiz([
  ("Shortener needs click analytics: 301 or 302?", "<b style=\"display:inline\">302</b>: every click reaches you", "blue",
   "Quiz time. A URL shortener needs click analytics. Three oh one or three oh two?",
   "Three oh two, so every click reaches your servers."),
  ("OTP stuck behind a marketing blast: fix?", "separate <b style=\"display:inline\">priority</b> queues", "orange",
   "One time passwords are stuck behind a marketing blast. The fix?",
   "Separate queues by priority."),
  ("Chat message order per conversation?", "a <b style=\"display:inline\">sequence number</b> per conversation", "purple",
   "How do you keep chat messages in order?",
   "Give each message a sequence number within its conversation."),
]),

recap(["Shortener: counter → base62 · cache hot links",
       "301 caches · 302 counts clicks",
       "Notifications: queues by priority · retries · idempotency",
       "Chat: WebSockets · Redis routing · seq per conversation",
       "Autocomplete: trie with top-k · rebuilt offline",
       "Same framework every time"],
  "Let's recap. A URL shortener generates codes from a counter in base sixty two, and caches hot links. Three oh one redirects are cached, three oh two let you count clicks. Notifications go through priority queues, with retries and idempotency keys. Chat uses WebSockets, routing in Redis, and a sequence number per conversation. Autocomplete serves top completions from a trie rebuilt offline. And every time, the same framework guides you. Well done: that completes the cloud and system design days."),
]
