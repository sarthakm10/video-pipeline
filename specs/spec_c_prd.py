from conc import *

TAG = "Spring · Production Features"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Production Features.mp4"

SLIDES = [
title_slide(0, "Production Features", "Logs, health checks, metrics and docs: how you know your app is alive and well",
  "Welcome. Today's concept: production features in Spring Boot.",
  "Your app works on your laptop. In production, nobody can attach a debugger, so the app has to explain itself. By the end you'll know the three pillars of observability, logging with SLF4J and request ids, Actuator and how to secure it, liveness versus readiness, metrics with Micrometer and Prometheus, OpenAPI docs, virtual threads, and graceful shutdown.",
  pill="SPRING · CONCEPT"),

{"html": H("The three pillars of ", "observability") + row(
   box("blue", "logs", "what happened · one event at a time · <i>\"order 42 failed: card declined\"</i>", 0, "flex:1"),
   box("green", "metrics", "how much, how often · numbers over time · <i>p99 latency 180 ms</i>", 1, "flex:1"),
   box("purple", "traces", "where the time went · one request across services", 2, "flex:1"), top=True) +
   note("Plus health checks: is it up, and can it take traffic?", 3),
 "steps": [
  "Observability means understanding a running system from the outside. It rests on three pillars. Logs record individual events, like one failed order.",
  "Metrics are numbers over time: request rate, error rate, latency. They're cheap to keep and perfect for dashboards and alerts.",
  "Traces follow one request across services, showing where the time went.",
  "On top of these, health checks tell the platform whether the app is up and ready for traffic.",
 ]},

{"html": H("Logging with ", "SLF4J") + row(
   code("""§0 private static final Logger log =
§0     LoggerFactory.getLogger(OrderService.class);
§1 log.info("Order {} placed for {}", id, user);   // placeholders
§1 log.debug("Cart: {}", cart);                    // off in prod
§1 log.error("Payment failed for {}", id, ex);     // stack trace
§2 logging:
§2   level:
§2     root: INFO
§2     com.shop.orders: DEBUG""", 24, style="flex:1"),
   col(box("blue", "SLF4J + Logback", "an API and the engine behind it · Boot's default", 0),
       box("green", "placeholders", "<code>{}</code> skips building the string when the level is off", 1),
       box("orange", "levels", "TRACE · DEBUG · INFO · WARN · ERROR · per package", 2), gap=14, style="width:560px"), top=True),
 "steps": [
  "Code logs through SLF4J, a facade, and Spring Boot plugs in Logback as the engine. Declare one logger per class.",
  "Use curly brace placeholders, not string concatenation. If the level is off, the message is never built. Pass the exception as the last argument to get its stack trace.",
  "Levels go from trace to error, and you set them per package in configuration. In production, info at the root, with debug turned on only where you're investigating.",
 ]},

{"html": H("Request ids and JSON ", "logs") + row(
   code("""§0 class RequestIdFilter extends OncePerRequestFilter {
§0   protected void doFilterInternal(…) {
§0     String id = Optional.ofNullable(req.getHeader("X-Request-Id"))
§0                         .orElse(UUID.randomUUID().toString());
§0     MDC.put("requestId", id);
§0     try { chain.doFilter(req, res); }
§0     finally { MDC.remove("requestId"); }
§0   }
§0 }
§2 logging.structured.format.console=ecs""", 22, style="flex:1"),
   col(box("blue", "MDC", "a per-thread map · every log line includes the id", 0),
       box("orange", "clear it", "threads are reused · <code>finally</code> removes it", 1),
       box("green", "JSON logs", "one object per line · searchable fields in Loki / ELK", 2), gap=14, style="width:520px"), top=True),
 "steps": [
  "When a hundred requests interleave, how do you find all the lines for one of them? A filter gives every request an id, reusing the caller's header if present, and puts it in the MDC, a per thread map that the log pattern prints on every line.",
  "Threads are reused for other requests, so always remove it in a finally block. Async work on another thread needs the id copied across.",
  "In production, write logs as JSON, one object per line. Spring Boot has structured logging built in. Log tools can then search by request id, user or level.",
 ]},

{"html": H("Actuator ", "endpoints") + row(
   table(["Endpoint", "Shows"], [
     (["<code>/actuator/health</code>", "UP / DOWN · DB, disk, custom checks"], 0),
     (["<code>/actuator/info</code>", "version, git commit, build time"], 0),
     (["<code>/actuator/metrics</code>", "JVM, HTTP, pool numbers"], 0),
     (["<code>/actuator/loggers</code>", "change a log level at runtime"], 1),
     (["<code>/actuator/env</code>", "config values · <b>secrets masked</b>"], 2)], size=26),
   code("""§3 management:
§3   endpoints.web.exposure.include:
§3     health, info, prometheus
§3   endpoint.health.show-details:
§3     when-authorized
§3   server.port: 8081""", 23, style="width:520px"), top=True) +
   note("Expose only what you need · secure the rest · ideally on a separate port", 3),
 "steps": [
  "Spring Boot Actuator adds production endpoints. Health reports up or down, including the database and disk. Info shows the version and git commit. Metrics exposes JVM and HTTP numbers.",
  "Loggers lets you change a log level on a running app, without a restart. Very handy during an incident.",
  "Env shows configuration, which is why values that look like secrets are masked.",
  "These endpoints reveal a lot, so expose only what you need, show health details only to authorised users, and ideally serve them on a separate management port that isn't public.",
 ]},

{"html": H("Liveness vs ", "readiness") + row(
   box("red", "liveness", "is the process healthy? · <b style=\"display:inline\">no</b> → restart it · don't include the DB", 0, "flex:1"),
   box("green", "readiness", "can it take traffic now? · <b style=\"display:inline\">no</b> → stop sending requests", 1, "flex:1"), top=True) +
   code("""§2 /actuator/health/liveness     → Kubernetes livenessProbe
§2 /actuator/health/readiness    → Kubernetes readinessProbe
§3 management.endpoint.health.group.readiness.include=readinessState,db""", 25, style="margin-top:22px") +
   note("A DB outage in liveness → every pod restarts → nothing improves", 4),
 "steps": [
  "Kubernetes asks two different questions. Liveness: is this process stuck? If it fails, the container is restarted.",
  "Readiness: can it serve traffic right now? If it fails, the pod stays alive but is taken out of the load balancer, for example while warming up or shutting down.",
  "Spring Boot exposes both as health groups, ready to point the probes at.",
  "You can add checks to a group. The database belongs in readiness, if anywhere.",
  "Never in liveness. If the database goes down, every pod fails liveness and restarts, which fixes nothing and adds a restart storm.",
 ]},

{"html": H("Metrics with ", "Micrometer") + row(
   code("""§0 Counter.builder("orders.placed")
§0     .tag("type", "express")
§0     .register(registry).increment();
§1 Timer.builder("payment.call").register(registry)
§1     .record(() -> gateway.charge(amount));
§2 # GET /actuator/prometheus
§2 orders_placed_total{type="express"} 42.0
§2 http_server_requests_seconds_count{status="500"} 3.0""", 23, style="flex:1"),
   col(box("blue", "Micrometer", "a metrics facade · like SLF4J for numbers", 0),
       box("green", "counter · gauge · timer", "count events · current value · durations + percentiles", 1),
       box("purple", "Prometheus", "scrapes the endpoint · Grafana draws dashboards and alerts", 2), gap=14, style="width:540px"), top=True) +
   note("Tags: few values only · never a user id (high cardinality)", 3),
 "steps": [
  "Micrometer is to metrics what SLF4J is to logs: one API, many backends. A counter counts events, with tags to break it down.",
  "A gauge reports a current value, like queue size. A timer records durations and can publish percentiles. Spring already times every HTTP request for you.",
  "Prometheus scrapes the actuator prometheus endpoint every few seconds, and Grafana turns that into dashboards and alerts.",
  "Keep tag values to a small set. A tag per user id creates millions of series and can take down the metrics system.",
 ]},

{"html": H("Docs, virtual threads and ", "shutdown") + row(
   box("blue", "OpenAPI (springdoc)", "<code>/v3/api-docs</code> + Swagger UI · generated from controllers · <code>@Operation</code>", 0, "flex:1"),
   box("green", "virtual threads", "<code>spring.threads.virtual.enabled=true</code> · cheap blocking · the DB pool is still the limit", 1, "flex:1"),
   box("purple", "graceful shutdown", "stop new requests · finish in-flight ones · then exit", 2, "flex:1"), top=True) +
   code("""§2 server.shutdown: graceful
§2 spring.lifecycle.timeout-per-shutdown-phase: 20s""", 26, style="margin-top:22px"),
 "steps": [
  "Springdoc generates an OpenAPI description from your controllers, plus a Swagger UI page to try the endpoints. Annotations add summaries and examples.",
  "One property switches request handling to virtual threads. Blocking calls get cheap, but a pool of ten database connections still means only ten queries at once.",
  "Graceful shutdown stops accepting new requests, lets in flight ones finish within a timeout, and then exits. With rolling deployments, that means no user sees an error.",
 ]},

quiz([
  ("Why <code>log.info(\"{}\", x)</code> over <code>\"…\" + x</code>?", "the string isn't built when the level is <b style=\"display:inline\">off</b>", "blue",
   "Quiz time. Why use placeholders instead of string concatenation in log calls?",
   "If the level is off, the message is never built."),
  ("DB check in liveness or readiness?", "<b style=\"display:inline\">readiness</b>: never liveness", "green",
   "Does a database check belong in the liveness or the readiness probe?",
   "Readiness. In liveness, a database outage would restart every pod."),
  ("A metric tag per user id: problem?", "<b style=\"display:inline\">high cardinality</b>: millions of series", "red",
   "What's wrong with tagging a metric with the user id?",
   "High cardinality. It creates a series per user and overwhelms the metrics system."),
]),

recap(["Logs · metrics · traces + health checks",
       "SLF4J placeholders · levels per package",
       "MDC request id · JSON logs",
       "Actuator: expose little, secure the rest",
       "Liveness restarts · readiness removes from traffic",
       "Micrometer → Prometheus · graceful shutdown"],
  "Let's recap. Observability rests on logs, metrics and traces, plus health checks. Log through SLF4J with placeholders and per package levels. Put a request id in the MDC, and write JSON logs. Actuator exposes health, info and metrics, so expose little and secure the rest. Liveness failures restart a pod, readiness failures take it out of traffic. And Micrometer feeds Prometheus, while graceful shutdown finishes in flight requests. Now practise with the examples in your notes!"),
]
