from conc import *

TAG = "Spring · Capstone"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Capstone.mp4"

SLIDES = [
title_slide(0, "The Capstone", "One Task Tracker that ties every Spring topic together",
  "Welcome. Today's concept: the capstone project.",
  "Each Spring topic so far was learned on its own. The capstone puts them in one application, a task tracker for teams, and the interesting part is how the pieces fit. By the end you'll know its architecture, what happens to one request from start to finish, the design trade offs behind it, what real production would still need, and how to present it in an interview.",
  pill="SPRING · CONCEPT"),

{"html": H("What it ", "is") + row(
   col(box("blue", "the product", "a REST API for teams · projects, tasks, tags, search, reports, an audit trail", 0),
       box("green", "the size", "17 endpoints · 39 tests across the pyramid", 0), gap=14, style="width:560px"),
   table(["Layer", "Choice"], [
     (["web", "Spring MVC on virtual threads · ProblemDetail errors"], 1),
     (["data", "PostgreSQL · Flyway · JPA writes · JdbcTemplate reports"], 1),
     (["security", "JWT for the API · session login for the browser"], 2),
     (["extras", "Caffeine cache · Micrometer · springdoc"], 2)], size=26), top=True),
 "steps": [
  "The capstone is a task tracker for teams: projects, tasks, tags, search, reports, and an audit trail. Seventeen endpoints, covered by thirty nine tests.",
  "It runs Spring MVC on virtual threads, PostgreSQL with Flyway migrations, JPA for writes and plain JDBC template for reports.",
  "Security uses JWT for the API and a session login for the browser, plus a Caffeine cache, Micrometer metrics, and generated API docs.",
 ]},

{"html": H("The ", "architecture") + col(
   box("gray", "filters", "RequestIdFilter → security chains → RateLimitFilter", 0),
   box("blue", "controllers", "<code>@Valid</code> DTO records in · DTOs out · <code>GlobalExceptionHandler</code> → ProblemDetail", 1),
   box("green", "services", "<code>@Transactional</code> · <code>@PreAuthorize</code> · <code>@Audited</code> · <code>@CacheEvict</code> · events", 2),
   box("purple", "repositories", "Spring Data JPA · JdbcTemplate for reports · PostgreSQL", 3), gap=12) +
   note("Dependencies point only downward · entities never leave the service layer", 4),
 "steps": [
  "Every request first passes the filters: a request id for the logs, the security chains that authenticate it, and a rate limiter.",
  "Controllers take validated DTO records and return DTOs. One global exception handler turns every error into a standard problem detail response.",
  "Services hold the business rules, and that's where the cross cutting annotations live: transactions, authorisation, auditing, cache eviction, and events.",
  "Repositories talk to PostgreSQL, with Spring Data for entities and JDBC template for report queries.",
  "Packages depend only downward, and entities never leave the service layer.",
 ]},

{"html": H("One request, end to ", "end") + row(
   code("""§0 POST /api/projects/7/tasks   Authorization: Bearer eyJ…
§0 { "title": "Write release notes", "due": "2026-12-01" }
§1 RequestIdFilter      → MDC requestId = 9f2c…
§1 JwtFilter            → user = asha, role = MEMBER
§1 RateLimitFilter      → 1 token spent
§2 TaskController       → @Valid CreateTaskRequest ✓
§3 @PreAuthorize        → asha is in project 7 ✓
§3 @Transactional       → INSERT task · INSERT audit
§4 AFTER_COMMIT event   → @Async notification
§5 201 Created   Location: /api/tasks/42""", 22, style="flex:1"),
   col(box("blue", "filters", "who, which request, how fast", 1),
       box("green", "validation", "bad input → 400 ProblemDetail, nothing touched", 2),
       box("purple", "transaction", "task + audit row commit together", 3),
       box("orange", "after commit", "side effects only for committed work", 4), gap=14, style="width:480px"), top=True),
 "steps": [
  "Let's follow one request. A member posts a new task to project seven, with a bearer token.",
  "The filters run first. The request gets an id for every log line, the JWT is checked and becomes the current user, and the rate limiter spends one token.",
  "The controller validates the body. A missing title would stop here with a four hundred, before any business code runs.",
  "In the service, pre authorize checks the user belongs to the project. Then one transaction inserts the task and its audit row together.",
  "After the commit, an event triggers an async notification, so a rolled back request never sends one.",
  "The response is two oh one created, with a location header pointing at the new task.",
 ]},

{"html": H("Design ", "trade-offs") + table(["Decision", "Instead of", "Cost"], [
     (["DTO records at the API", "returning entities", "mapping code"], 0),
     (["Flyway + <code>ddl-auto: validate</code>", "<code>ddl-auto: update</code>", "SQL written by hand"], 0),
     (["optimistic locking <code>@Version</code>", "pessimistic locks", "clients handle 409"], 1),
     (["JWT for the API", "server sessions", "logout is hard · short lifetime"], 1),
     (["events AFTER_COMMIT", "direct calls", "lost on a crash → outbox"], 2),
     (["Caffeine + in-memory rate limit", "Redis", "<b>wrong with many instances</b>"], 2)], size=26),
 "steps": [
  "Every choice has a cost, and being able to say it is what interviewers look for. DTOs keep the API stable, at the cost of mapping code. Flyway migrations make schema changes reviewed and repeatable, with Hibernate only validating.",
  "Optimistic locking with a version column avoids holding locks while people edit, but clients must handle a conflict. JWTs scale without session storage, but logging out is hard, so tokens are short lived.",
  "After commit events decouple side effects, but can be lost in a crash, which the transactional outbox fixes. And the local cache and rate limiter are simple, but wrong as soon as you run several instances.",
 ]},

{"html": H("What real production still ", "needs") + row(
   col(box("blue", "scale-out", "Redis for cache and rate limits · ShedLock for <code>@Scheduled</code>", 0),
       box("green", "data", "backups + restore drills · backward-compatible migrations", 1),
       box("purple", "observability", "distributed tracing · dashboards and alerts", 2), gap=14, style="flex:1"),
   col(box("orange", "resilience", "retries with backoff + a circuit breaker on outbound calls", 2),
       box("red", "security", "HTTPS everywhere · vault secrets · dependency + image scanning", 3),
       box("gray", "time", "replace the fixed <code>Clock</code> bean with <code>Clock.systemUTC()</code>", 3), gap=14, style="flex:1"), top=True),
 "steps": [
  "A good engineer knows what's missing. To run many instances, the cache and rate limits move to Redis, and scheduled jobs need a lock.",
  "Data needs backups that are actually restored in drills, and migrations that work while old and new versions run side by side.",
  "Add distributed tracing, dashboards and alerts, and wrap outbound calls in retries and a circuit breaker.",
  "And security hardening: HTTPS everywhere, secrets in a vault, scanning of dependencies and images. Even the clock: the notes fix time for predictable output, and production needs the real one.",
 ]},

{"html": H("Presenting it in an ", "interview") + row(
   col(pts([("<b>What</b>: a task API for teams, in one sentence", 0),
        ("<b>Stack</b>: Boot 4, PostgreSQL, JWT, Caffeine, Docker", 0),
        ("<b>Architecture</b>: controller → service → repository", 0),
        ("<b>One problem, deep</b>: problem → options → choice → result", 1),
        ("<b>Quality</b>: 39 tests · bugs the end-to-end run caught", 2),
        ("<b>Next</b>: tracing, Redis, a resilience layer", 2)], size=30), style="flex:1"),
   col(box("purple", "good deep dives", "N+1: 9 queries → 1 · <code>@Version</code> → 409 · CDS: 14.5 s → 8.5 s", 1),
       box("blue", "expect", "\"walk me through a request\" · \"how would you scale it?\"", 3), gap=14, style="width:600px"), top=True),
 "steps": [
  "Prepare a two minute walk through. What it is, in one sentence. The stack. The layered architecture.",
  "Then one interesting problem, told as problem, options, choice and result. For example, the project page made nine queries, and a fetch join made it one, guarded by a test.",
  "Mention quality: the test pyramid, and the bugs the end to end run caught that per feature tests missed. Then what you'd do next.",
  "Expect follow ups like: walk me through a request, and how would you scale it to ten instances. You now have answers to both.",
 ]},

quiz([
  ("Why send the notification AFTER_COMMIT?", "rolled-back work <b style=\"display:inline\">never</b> notifies", "purple",
   "Quiz time. Why is the notification sent after commit?",
   "So a rolled back request never sends a notification."),
  ("Two people edit the same task?", "<b style=\"display:inline\">@Version</b> → 409 → reload", "orange",
   "What happens when two people edit the same task at once?",
   "The version column detects it, the second gets a four oh nine, and reloads."),
  ("Scale to 10 instances: first change?", "cache + rate limit → <b style=\"display:inline\">Redis</b>", "blue",
   "What has to change first to run ten instances?",
   "The cache and rate limiter move to a shared store like Redis, and scheduled jobs get a lock."),
]),

recap(["Task Tracker: 17 endpoints, 39 tests",
       "Filters → controllers → services → repositories",
       "One request: id, JWT, rate limit, validate, authorise",
       "One transaction · AFTER_COMMIT side effects · 201",
       "Every choice has a cost: say it",
       "Pitch: what, stack, architecture, one deep problem"],
  "Let's recap. The task tracker has seventeen endpoints and thirty nine tests. Requests pass filters, controllers, services and repositories, with dependencies pointing down. One request gets an id, a user, a rate limit check, validation and authorisation, then one transaction, with side effects after commit, and a two oh one. Every design choice has a cost, and you should name it. And in an interview: what, stack, architecture, and one problem told in depth. Now explore the full project in your notes!"),
]
