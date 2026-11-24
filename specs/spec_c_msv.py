from conc import *

TAG = "Spring · Microservices"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Microservices.mp4"

SLIDES = [
title_slide(0, "Microservices", "Splitting an app into services, and the problems that come with it",
  "Welcome. Today's concept: microservices with Spring Cloud.",
  "Microservices are popular in job descriptions, and often misunderstood. Splitting an app solves some problems and creates new ones: finding each other, configuration, failures spreading, and data spread across databases. By the end you'll know when to split, central configuration, service discovery and load balancing, the gateway, distributed tracing, circuit breakers, data per service and sagas.",
  pill="SPRING · CONCEPT"),

{"html": H("Monolith vs ", "microservices") + row(
   box("blue", "a monolith", "one deployable · in-process calls · one database · simple to run and debug", 0, "flex:1"),
   box("purple", "microservices", "small services around business capabilities · each deploys and scales alone", 1, "flex:1"),
   box("red", "the bill", "network calls fail · distributed data · many things to deploy and watch", 2, "flex:1"), top=True) +
   note("Start with a modular monolith · split when teams or scaling demand it", 3),
 "steps": [
  "A monolith is one deployable unit. Calls between modules are in process, there's one database, and it's simple to run, test and debug.",
  "Microservices split the system by business capability: orders, payments, users. Each service has its own team, deploys independently, and scales on its own.",
  "But every call is now over the network and can fail, data lives in several databases, and there are many more things to deploy and monitor.",
  "A good default: start with a well structured modular monolith, and split off services when team size or scaling actually demands it.",
 ]},

{"html": H("Config and ", "discovery") + row(
   col(box("blue", "Config Server", "one place for every service's config · backed by git · per profile", 0),
       box("green", "Eureka registry", "services register on startup · send heartbeats · ask where others are", 1),
       box("purple", "client-side load balancing", "<code>@LoadBalanced</code> picks an instance · round robin", 2), gap=14, style="width:600px"),
   code("""§0 spring.config.import: configserver:http://config:8888
§1 eureka.client.service-url.defaultZone: http://eureka:8761/eureka
§2 @Bean @LoadBalanced
§2 RestClient.Builder lb() { return RestClient.builder(); }
§2 client.get().uri("http://payment-service/api/pay/{id}", id)
§2       .retrieve().body(Payment.class);""", 22, style="flex:1"), top=True),
 "steps": [
  "With many services, configuration moves to a config server, usually backed by a git repository. Each service imports its settings on startup.",
  "Instances come and go, so hard coded addresses don't work. Each service registers with Eureka, keeps sending heartbeats, and asks the registry where others are.",
  "Mark a rest client builder as load balanced, and you can call a service by name. Spring Cloud looks up its instances and spreads calls across them, round robin by default.",
 ]},

{"html": H("The API ", "gateway") + graph(
   {"client": (90, 210), "gateway": (360, 210), "orders": (680, 80), "payments": (680, 210), "users": (680, 340)},
   [("client", "gateway"), ("gateway", "orders"), ("gateway", "payments"), ("gateway", "users")],
   colors={"gateway": ("#ede9fe", "#7c3aed")}, w=820, h=420, directed=True, step=0, r=62) +
   note("One entry point: routing · auth · rate limits · CORS · request ids", 1),
 "steps": [
  "Clients shouldn't know about every service. Spring Cloud Gateway gives them one entry point, and routes each path to the right service.",
  "It's also the natural place for concerns every request shares: checking the token, rate limiting, CORS, and adding a request id.",
 ]},

{"html": H("Distributed ", "tracing") + row(
   code("""§0 traceparent: 00-4bf92f35…-00f067aa…-01
§0 gateway   ████████████████████████  210 ms
§0  orders     ███████████████████     170 ms
§1   payments     ████████████         120 ms   ← slow
§0   users      ██                      15 ms""", 25, style="flex:1"),
   col(box("blue", "trace id", "one id for the whole request, passed in a header", 0),
       box("green", "span", "one hop · start, duration, service", 0),
       box("purple", "tools", "Micrometer Tracing → OpenTelemetry → Zipkin / Jaeger / Tempo", 2), gap=14, style="width:560px"), top=True),
 "steps": [
  "A request now crosses several services. Distributed tracing gives it one trace id, passed along in a header, and every hop records a span with its timing. Laid out like this, you see the request's whole journey.",
  "And the slow part jumps out: payments took a hundred and twenty of the two hundred and ten milliseconds.",
  "In Spring Boot, Micrometer tracing creates the spans and exports them through OpenTelemetry to Zipkin, Jaeger or Tempo. The trace id also goes into the logs.",
 ]},

{"html": H("Circuit ", "breakers") + row(graph(
   {"CLOSED": (110, 230), "OPEN": (380, 80), "HALF": (560, 330)},
   [("CLOSED", "OPEN"), ("OPEN", "HALF"), ("HALF", "CLOSED")],
   colors={"CLOSED": ("#dcfce7", "#16a34a"), "OPEN": ("#fee2e2", "#dc2626"), "HALF": ("#fef3c7", "#d97706")},
   labels={"OPEN": "fail fast", "HALF": "half-open: a few trial calls", "CLOSED": "calls pass"},
   w=720, h=440, directed=True, step=0, r=62),
   col(box("blue", "the states", "too many failures → OPEN · after a wait → HALF-OPEN · trials pass → CLOSED", 1),
       box("green", "with it", "timeouts · a fallback (cached / default answer) · retries with backoff", 2), gap=14, style="flex:1"), top=True),
 "steps": [
  "When payments is slow, every caller waits, their threads pile up, and the failure spreads. A circuit breaker, from Resilience4j, stops that.",
  "Normally it's closed and calls pass. When the failure rate crosses a threshold, it opens, and calls fail immediately without touching payments. After a wait, it goes half open and lets a few trial calls through. If they succeed, it closes again.",
  "Combine it with timeouts, a fallback such as a cached or default answer, and a few retries with backoff.",
 ]},

{"html": H("Data per service and ", "sagas") + row(
   col(box("blue", "database per service", "no shared tables · others ask through the API or events", 0),
       box("red", "no global transaction", "order + payment + stock can't commit together", 1),
       box("green", "a saga", "a chain of local transactions · each failure triggers a <b style=\"display:inline\">compensation</b>", 2), gap=14, style="width:620px"),
   code("""§2 1  orders:   create order (PENDING)
§2 2  payments: charge card          ✓
§2 3  stock:    reserve items        ✗ out of stock
§3 ↩  payments: refund card          (compensate)
§3 ↩  orders:   mark CANCELLED""", 25, style="flex:1"), top=True) +
   note("Testing: one service alone with WireMock / Testcontainers · contract tests between them", 4),
 "steps": [
  "Each service owns its data. No other service reads its tables. They ask through its API, or listen to its events.",
  "That means there's no single database transaction across services. You can't commit the order, the payment and the stock reservation together.",
  "A saga replaces it: a sequence of local transactions. Create the order, charge the card, reserve the stock.",
  "If a step fails, run compensating actions for the steps already done. Refund the card, cancel the order.",
  "Test each service on its own, with fakes like WireMock for its neighbours, and contract tests to make sure services still agree.",
 ]},

quiz([
  ("Circuit open: what happens to calls?", "they <b style=\"display:inline\">fail fast</b>: no call is made", "red",
   "Quiz time. When a circuit breaker is open, what happens to calls?",
   "They fail immediately, without calling the failing service."),
  ("@LoadBalanced lets you call…?", "a service by <b style=\"display:inline\">name</b>", "purple",
   "What does load balanced let you do?",
   "Call a service by its name. Spring Cloud picks an instance."),
  ("No cross-service transaction: so…?", "a <b style=\"display:inline\">saga</b> with compensations", "green",
   "There's no transaction across services. What do you use instead?",
   "A saga of local transactions, with compensating actions."),
]),

recap(["Start modular · split when you need to",
       "Config Server · Eureka · @LoadBalanced by name",
       "Gateway: one entry, shared concerns",
       "Tracing: trace id + spans across services",
       "Circuit breaker: closed → open → half-open",
       "Data per service · sagas with compensations"],
  "Let's recap. Start with a modular monolith, and split when teams or scaling demand it. A config server centralises settings, Eureka tracks instances, and load balanced clients call services by name. A gateway gives clients one entry point. Tracing follows a request across services with one trace id. Circuit breakers fail fast instead of letting failures spread. And each service owns its data, with sagas and compensations instead of global transactions. Now practise with the examples in your notes!"),
]
