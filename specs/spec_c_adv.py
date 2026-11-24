from conc import *

TAG = "Spring · Advanced Spring"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Advanced Spring.mp4"

SLIDES = [
title_slide(0, "Advanced Spring", "AOP, @Async, scheduling, events, caching, RestClient and rate limiting",
  "Welcome. Today's concept: advanced Spring.",
  "Many Spring annotations look like magic. Put transactional, async or cacheable on a method, and behaviour appears. It's all one mechanism: proxies. By the end you'll know how proxies and AOP work, the self invocation trap, async methods and their thread pools, scheduling, application events, caching, calling other services with RestClient, and rate limiting.",
  pill="SPRING · CONCEPT"),

{"html": H("Proxies: the trick behind the ", "annotations") + row(
   col(box("gray", "caller", "<code>orderController</code>", 0),
       box("purple", "proxy", "before: start a transaction · time it · check the cache", 0),
       box("blue", "your bean", "<code>OrderService.place()</code>", 0),
       gap=14, style="width:520px"),
   col(box("green", "how it's made", "an interface → JDK proxy · a class → a CGLIB subclass", 1),
       box("orange", "consequence", "only <b style=\"display:inline\">public calls from outside</b> go through it", 2),
       gap=14, style="flex:1"), top=True) +
   note("@Transactional · @Async · @Cacheable · @PreAuthorize · @Retryable all work this way", 3),
 "steps": [
  "When a bean has an annotation like transactional, Spring doesn't inject the bean itself. It injects a proxy: an object with the same methods, that does extra work before and after calling your real bean.",
  "If the bean implements an interface, Spring can use a JDK dynamic proxy. Otherwise it generates a subclass with CGLIB, which is the default in Spring Boot.",
  "The consequence: only calls that arrive from outside, through the proxy, get the extra behaviour.",
  "Transactional, async, cacheable, pre authorize and retryable all work this way.",
 ]},

{"html": H("Aspect-oriented ", "programming") + row(
   code("""§0 @Target(METHOD) @Retention(RUNTIME)
§0 public @interface Timed { }
§1 @Aspect @Component
§1 class TimingAspect {
§2   @Around("@annotation(Timed)")
§2   Object time(ProceedingJoinPoint jp) throws Throwable {
§2     long t = System.nanoTime();
§2     try { return jp.proceed(); }               // the real call
§2     finally { log.info("{} took {} µs", jp.getSignature(),
§2                        (System.nanoTime() - t) / 1000); }
§2   }
§1 }""", 22, style="flex:1"),
   col(box("blue", "aspect", "a class of cross-cutting logic", 1),
       box("green", "pointcut", "which methods · <code>@annotation(Timed)</code> · <code>execution(* com.shop..*(..))</code>", 2),
       box("purple", "advice", "<code>@Before</code> · <code>@AfterReturning</code> · <code>@AfterThrowing</code> · <code>@Around</code>", 3), gap=14, style="width:540px"), top=True),
 "steps": [
  "AOP lets you write cross cutting logic, like timing, auditing or logging, once, and apply it to many methods. A common pattern starts with your own annotation.",
  "An aspect is a bean holding that logic.",
  "A pointcut picks the methods, here every method annotated with timed. Around advice wraps the call: proceed runs the real method, and the finally block logs how long it took.",
  "Other advice types run before, after a successful return, or after an exception. An audit aspect, for example, records the action after returning, so failed calls aren't audited.",
 ]},

{"html": H("The self-invocation ", "trap") + row(
   code("""§0 @Service
§0 class ReportService {
§0   public void runAll() {
§0     for (var r : reports)
§1       generate(r);              // this.generate → no proxy!
§0   }
§0   @Async @Transactional
§0   public void generate(Report r) { … }
§0 }""", 25, style="flex:1"),
   col(box("red", "what happens", "<code>this.generate()</code> runs synchronously, with no transaction", 1),
       box("green", "fixes", "move it to another bean · or inject the proxy of yourself", 2),
       box("orange", "also skipped", "private and final methods · calls during construction", 3), gap=14, style="width:560px"), top=True),
 "steps": [
  "Here's the most common Spring bug. Run all calls generate, which is async and transactional.",
  "But the call goes through this, the real object, not the proxy. So generate runs synchronously, on the same thread, without a new transaction. No error, it just silently does nothing extra.",
  "The clean fix is to move generate into a separate bean, so the call crosses a proxy. Injecting your own proxy also works, but is harder to read.",
  "Proxies also can't intercept private or final methods, or calls made while the bean is still being constructed.",
 ]},

{"html": H("@Async and thread ", "pools") + row(
   code("""§0 @EnableAsync
§0 @Async
§0 public CompletableFuture<Report> build(long id) { … }
§2 spring.task.execution.pool:
§2   core-size: 4
§2   max-size: 16
§2   queue-capacity: 100""", 25, style="flex:1"),
   col(box("blue", "@Async", "returns at once · the work runs on an executor thread", 0),
       box("orange", "exceptions", "void methods: lost unless an AsyncUncaughtExceptionHandler · use a future", 1),
       box("red", "pool surprise", "beyond core threads it <b style=\"display:inline\">queues first</b> · grows to max only when the queue is full", 2), gap=14, style="width:600px"), top=True),
 "steps": [
  "Async makes a method return immediately, while its body runs on a thread from an executor. Return a completable future if the caller needs the result.",
  "Exceptions from a void async method go nowhere by default. Return a future, or register an uncaught exception handler.",
  "And a classic surprise in thread pool executor. Beyond the core size, new tasks go into the queue first. Only when the queue is full does the pool grow towards the max. With an unbounded queue, it never grows at all. Size the queue on purpose.",
 ]},

{"html": H("Scheduling and ", "events") + row(
   code("""§0 @Scheduled(fixedRate = 60_000)            // every minute
§0 void refreshRates() { … }
§0 @Scheduled(cron = "0 0 9 * * MON-FRI", zone = "Asia/Kolkata")
§0 void sendReminders() { … }
§2 publisher.publishEvent(new TaskCreated(task.getId()));
§3 @TransactionalEventListener(phase = AFTER_COMMIT)
§3 @Async
§3 void notify(TaskCreated e) { mailer.send(…); }""", 22, style="flex:1"),
   col(box("blue", "@Scheduled", "fixedRate · fixedDelay · cron · single thread by default", 0),
       box("orange", "many instances", "each one runs the job → a lock (ShedLock)", 1),
       box("green", "events", "the publisher doesn't know the listeners", 2),
       box("purple", "AFTER_COMMIT", "only if the transaction committed", 3), gap=14, style="width:520px"), top=True),
 "steps": [
  "Scheduled runs a method on a timer: a fixed rate, a fixed delay after the previous run, or a cron expression with a time zone.",
  "Run three instances of the app, and the job runs three times. For jobs that must run once, take a distributed lock, for example with ShedLock.",
  "Application events decouple code. The task service publishes task created, and doesn't know who listens.",
  "A transactional event listener with after commit runs only if the transaction actually committed, so you never email about a task that was rolled back. Make it async so the request doesn't wait for the email.",
 ]},

{"html": H("", "Caching") + row(
   code("""§0 @EnableCaching
§0 @Cacheable(value = "projects", key = "#id")
§0 public ProjectDto find(long id) { … }       // 2nd call: no query
§1 @CacheEvict(value = "projects", key = "#id")
§1 public void rename(long id, String name) { … }
§2 spring.cache.caffeine.spec: maximumSize=1000,expireAfterWrite=10m""", 22, style="flex:1"),
   col(box("blue", "@Cacheable", "look up first · call the method only on a miss", 0),
       box("orange", "@CacheEvict / @CachePut", "keep the cache honest on writes", 1),
       box("green", "Caffeine", "in-process · very fast · per instance", 2),
       box("purple", "Redis", "shared by all instances · a network hop", 3), gap=14, style="width:520px"), top=True),
 "steps": [
  "Cacheable checks the cache first, keyed by the arguments. On a hit, the method doesn't run at all.",
  "On writes, evict or update the entry, or readers keep seeing stale data.",
  "Caffeine is an in process cache: extremely fast, with size limits and expiry. But each instance has its own copy.",
  "With several instances that must agree, use a shared cache like Redis, at the cost of a network hop. And remember: cacheable is a proxy too, so self calls skip it.",
 ]},

{"html": H("RestClient and rate ", "limiting") + row(
   code("""§0 RestClient client = RestClient.builder()
§0     .baseUrl("https://holidays.example.com")
§0     .requestFactory(factoryWithTimeouts)
§0     .build();
§0 Holiday[] h = client.get().uri("/{year}", 2026)
§0     .retrieve().body(Holiday[].class);
§1 @GetExchange("/{year}") Holiday[] holidays(@PathVariable int year);""", 22, style="flex:1"),
   col(box("blue", "RestClient", "fluent, synchronous · replaces RestTemplate", 0),
       box("orange", "always set timeouts", "the default can wait forever", 0),
       box("green", "HTTP interfaces", "declare an interface · Spring implements it", 1),
       box("purple", "rate limiting", "token bucket per client · over the limit → 429", 2), gap=14, style="width:520px"), top=True),
 "steps": [
  "To call another service, use RestClient: a fluent, synchronous client that replaces rest template. Always configure connect and read timeouts, or one slow dependency can tie up all your threads.",
  "Or declare an HTTP interface with get exchange annotations, and Spring generates the client.",
  "To protect your own API, rate limit it. A token bucket gives each client a number of tokens that refill over time. Each request spends one. When the bucket is empty, reply with status four twenty nine, too many requests.",
 ]},

quiz([
  ("@Async method called via this: what happens?", "it runs <b style=\"display:inline\">synchronously</b>: no proxy", "red",
   "Quiz time. An async method is called from another method of the same bean. What happens?",
   "It runs synchronously, because the call skips the proxy."),
  ("Pool core 4, max 16, queue 100: when does it grow?", "only when the <b style=\"display:inline\">queue is full</b>", "orange",
   "A thread pool has core size four, max sixteen and a queue of a hundred. When does it start more than four threads?",
   "Only once the queue is full."),
  ("Caffeine with 3 instances?", "3 <b style=\"display:inline\">separate</b> caches", "blue",
   "You use a Caffeine cache and run three instances. How many caches are there?",
   "Three separate ones. Use Redis if they must agree."),
]),

recap(["Annotations work through proxies",
       "AOP: aspect · pointcut · @Around advice",
       "Self-invocation skips the proxy",
       "@Async: return a future · pools queue before growing",
       "@Scheduled + ShedLock · AFTER_COMMIT events",
       "Cache: Caffeine vs Redis · RestClient timeouts · 429"],
  "Let's recap. Spring's annotations work through proxies that wrap your bean. AOP lets you write your own, with aspects, pointcuts and around advice. Calls inside the same bean skip the proxy. Async methods should return futures, and thread pools queue before they grow. Scheduled jobs need a lock with many instances, and after commit events fire only for committed work. Caffeine caches per instance, Redis is shared. And RestClient needs timeouts, while rate limits answer with four twenty nine. Now practise with the examples in your notes!"),
]
