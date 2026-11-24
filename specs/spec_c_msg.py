from conc import *

TAG = "Spring · Messaging"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Messaging.mp4"

SLIDES = [
title_slide(0, "Messaging with Kafka", "Let services talk without waiting for each other, and without losing messages",
  "Welcome. Today's concept: messaging, with Kafka and RabbitMQ.",
  "When one service calls another directly, both must be up, and the caller waits. Messaging puts a broker in between. By the end you'll know why messaging helps, Kafka's topics, partitions, offsets and consumer groups, Kafka versus RabbitMQ, producing and consuming in Spring, the dual write problem and the outbox, delivery guarantees and idempotent consumers, retries and dead letter topics, and ordering with keys.",
  pill="SPRING · CONCEPT"),

{"html": H("Why ", "messaging") + row(
   box("red", "direct calls", "orders → email, stock, analytics · one is down → the order fails · the caller waits", 0, "flex:1"),
   box("green", "through a broker", "orders publishes <i>OrderPlaced</i> once · each service reads it at its own pace", 1, "flex:1"), top=True) +
   pts([("Decoupled: the producer doesn't know the consumers", 2),
        ("Buffered: a spike waits in the broker, nothing is dropped", 2),
        ("Cost: eventual consistency, harder debugging, one more system", 3)], size=30),
 "steps": [
  "Imagine the order service calls email, stock and analytics directly. If any of them is down or slow, placing an order fails or crawls.",
  "With a broker, the order service publishes one event, order placed, and returns. Each other service reads it whenever it's ready.",
  "The producer doesn't know who consumes. A traffic spike waits in the broker instead of overwhelming the consumers.",
  "The cost: data becomes consistent eventually, not instantly, debugging spans systems, and there's one more piece of infrastructure to run.",
 ]},

{"html": H("Kafka: topics, partitions, ", "offsets") + col(
   cells(["o1", "o4", "o7", "o9"], None, None, 0, "partition 0", size=34),
   cells(["o2", "o5", "o8"], None, None, 0, "partition 1", size=34),
   cells(["o3", "o6"], None, None, 0, "partition 2", size=34, mark={1: "#bbf7d0"}), gap=12) + row(
   box("blue", "a topic", "an append-only log, split into partitions", 0, "flex:1"),
   box("green", "an offset", "a message's position · consumers store how far they read", 1, "flex:1"),
   box("purple", "retention", "messages stay (e.g. 7 days) after being read · replay is possible", 2, "flex:1"), top=True, style="margin-top:20px"),
 "steps": [
  "A Kafka topic is an append only log, split into partitions so it can be spread over brokers and read in parallel. Here, orders spread over three partitions.",
  "Each message has an offset, its position in the partition. A consumer simply remembers the offset it has reached, and commits it.",
  "Reading doesn't delete anything. Messages are kept for a retention period, so a new service can replay history from the beginning.",
 ]},

{"html": H("Consumer ", "groups") + graph(
   {"P0": (450, 80), "P1": (450, 210), "P2": (450, 340), "A1": (110, 130), "A2": (110, 300), "B1": (800, 210)},
   [("P0", "A1"), ("P1", "A1"), ("P2", "A2"), ("P0", "B1"), ("P1", "B1"), ("P2", "B1")],
   colors={"A1": ("#dbeafe", "#2563eb"), "A2": ("#dbeafe", "#2563eb"), "B1": ("#dcfce7", "#16a34a")},
   labels={"A2": "group: email", "B1": "group: analytics", "P2": "topic: orders"},
   w=900, h=420, directed=True, step=0, r=40) +
   note("Inside a group: each partition → one consumer · more consumers than partitions sit idle", 1),
 "steps": [
  "Consumers join a group. Every group gets every message, so email and analytics each see all orders.",
  "Inside one group, each partition is assigned to exactly one consumer, which shares the work. So the partition count caps a group's parallelism: a fourth email consumer would sit idle.",
 ]},

{"html": H("Kafka vs ", "RabbitMQ") + table(["", "Kafka", "RabbitMQ"], [
     (["model", "a replayable log", "queues · a message is gone once acked"], 0),
     (["routing", "by topic + key", "exchanges: direct, topic, fanout"], 0),
     (["strength", "huge throughput · event streams · replay", "flexible routing · per-message work"], 1),
     (["ordering", "per partition", "per queue, one consumer"], 1),
     (["Spring", "<code>KafkaTemplate</code> · <code>@KafkaListener</code>", "<code>RabbitTemplate</code> · <code>@RabbitListener</code>"], 2)], size=27),
 "steps": [
  "Kafka is a log: messages stay and can be replayed. RabbitMQ is a classic queue: once a consumer acknowledges a message, it's gone. Rabbit routes through exchanges, by exact key, by pattern, or to everyone.",
  "Kafka shines for very high throughput event streams and replay. RabbitMQ shines for flexible routing and task queues.",
  "Spring supports both with the same style: a template to send, and a listener annotation to receive.",
 ]},

{"html": H("Producing and consuming in ", "Spring") + code("""§0 record OrderPlaced(long orderId, long userId, BigDecimal total) { }
§0 kafka.send("orders", String.valueOf(o.userId()), event);   // topic, key, value
§1 @KafkaListener(topics = "orders", groupId = "email")
§1 void on(OrderPlaced e) {
§1   mailer.sendConfirmation(e.orderId());
§1 }
§2 spring.kafka.consumer.properties.spring.json.trusted.packages: com.shop.events
§3 spring.kafka.consumer.value-deserializer: ErrorHandlingDeserializer""", 23) +
   note("A poison pill (unreadable message) must not block the partition forever", 3),
 "steps": [
  "Events are small immutable records. Kafka template sends one to a topic, with a key and a value serialised as JSON.",
  "A Kafka listener method receives them. Spring deserialises the JSON, calls the method, and commits the offset afterwards.",
  "For JSON, list the packages you trust, so the consumer won't instantiate arbitrary classes.",
  "And wrap the deserialiser in an error handling one. Otherwise a single message that can't be parsed, a poison pill, fails forever and blocks the whole partition.",
 ]},

{"html": H("Dual writes and the ", "outbox") + row(
   col(box("red", "the dual write", "save the order, then send the event · a crash in between → order saved, event lost", 0),
       box("green", "the outbox", "same transaction: INSERT order + INSERT outbox row", 1),
       box("blue", "a relay", "a poller or CDC (Debezium) publishes outbox rows, then marks them sent", 2), gap=14, style="width:640px"),
   code("""§1 @Transactional
§1 void place(Order o) {
§1   orders.save(o);
§1   outbox.save(new OutboxEvent(
§1       "orders", o.key(), toJson(o)));
§1 }
§2 @Scheduled(fixedDelay = 1000)
§2 void relay() { /* send unsent rows */ }""", 24, style="flex:1"), top=True),
 "steps": [
  "Saving to the database and sending to Kafka are two separate systems. If the app crashes between them, the order exists but the event never goes out. Or the other way round.",
  "The transactional outbox fixes it. In the same database transaction as the order, insert a row into an outbox table. Both commit, or neither does.",
  "A relay then publishes outbox rows to Kafka and marks them sent, either by polling, or by reading the database log with a change data capture tool like Debezium.",
 ]},

{"html": H("Delivery, retries and ", "ordering") + row(
   col(box("orange", "at-least-once", "the usual guarantee · duplicates <b style=\"display:inline\">will</b> happen", 0),
       box("green", "idempotent consumer", "store processed event ids · skip ones already seen", 1),
       box("red", "retries → DLT", "retry with backoff · then park it in <code>orders.DLT</code>", 2),
       box("blue", "keys keep order", "same key → same partition → in order", 3), gap=14, style="width:600px"),
   code("""§1 if (processed.existsById(e.eventId())) return;
§1 handle(e);
§1 processed.save(new Processed(e.eventId()));
§2 @RetryableTopic(attempts = "4",
§2     backoff = @Backoff(delay = 1000, multiplier = 2))
§3 kafka.send("orders", userId, event);   // key = userId""", 23, style="flex:1"), top=True),
 "steps": [
  "In practice, Kafka gives at least once delivery. If a consumer crashes after handling a message but before committing the offset, it receives it again. So duplicates will happen.",
  "Make consumers idempotent. Record each processed event id, ideally in the same transaction as the work, and skip ids you've seen.",
  "When handling fails, retry with growing delays. After the last attempt, move the message to a dead letter topic for a human to inspect, so it doesn't block the others.",
  "Order is only guaranteed within a partition. Messages with the same key go to the same partition, so use the user or order id as the key when order matters. And test all this with an embedded broker, or a real Kafka in Testcontainers.",
 ]},

quiz([
  ("4 consumers in a group, 3 partitions?", "one sits <b style=\"display:inline\">idle</b>", "blue",
   "Quiz time. A group has four consumers and the topic has three partitions. What happens?",
   "One consumer sits idle. Partitions cap the parallelism."),
  ("Save to DB, then send: the risk?", "a crash between → <b style=\"display:inline\">lost event</b> · use an outbox", "red",
   "You save to the database, then send to Kafka. What's the risk?",
   "A crash between the two loses the event. Use a transactional outbox."),
  ("At-least-once delivery means consumers must be…?", "<b style=\"display:inline\">idempotent</b>", "green",
   "With at least once delivery, what must consumers be?",
   "Idempotent, so a duplicate has no extra effect."),
]),

recap(["A broker decouples and buffers services",
       "Topic → partitions → offsets · replayable",
       "Each group sees all · one consumer per partition",
       "KafkaTemplate · @KafkaListener · poison pills",
       "Dual write → transactional outbox",
       "At-least-once → idempotent · DLT · keys for order"],
  "Let's recap. A broker decouples services and absorbs spikes. Kafka topics are split into partitions, where offsets track progress and messages can be replayed. Every group sees every message, and within a group each partition has one consumer. Spring sends with Kafka template and receives with Kafka listener, and must handle poison pills. Avoid dual writes with a transactional outbox. And since delivery is at least once, make consumers idempotent, use dead letter topics, and keys for ordering. Now practise with the examples in your notes!"),
]
