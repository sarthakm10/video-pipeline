from conc import *

TAG = "Spring · Core: IoC, DI and Beans"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Core IoC, Dependency Injection and Beans.mp4"

SLIDES = [
title_slide(0, "Spring Core", "IoC, dependency injection, beans, scopes, lifecycle and proxies",
  "Welcome to Spring Core: inversion of control, dependency injection, and beans.",
  "Everything else in Spring is built on this. Controllers, repositories, transactions, and security are all just beans the container wires together. If you understand this video, the rest of Spring stops feeling like magic.",
  pill="SPRING · CONCEPT"),

{"html": H("The problem: tight ", "coupling") + row(
   code("""§0 class TaskService {
§0   private final TaskRepository repo =
§0       new PostgresTaskRepository();   // hard-wired
§0 }""", 28, style="flex:1"),
   col(box("red", "to swap the database", "edit TaskService itself", 1),
       box("red", "to unit test", "you need a real PostgreSQL", 1), gap=16, style="width:520px"), top=True) +
   code("""§2 class TaskService {
§2   private final TaskRepository repo;
§2   TaskService(TaskRepository repo) { this.repo = repo; }   // given from outside
§2 }""", 28, style="margin-top:24px"),
 "steps": [
  "Start with the problem. This task service creates its own repository with new. It's hard-wired to PostgreSQL.",
  "So to switch databases, you must edit the service. And to unit test it, you need a real PostgreSQL running. The class is tightly coupled to one implementation.",
  "The fix is simple. Don't create the dependency. Ask for it in the constructor, as an interface. Now whoever creates the service decides which repository it gets. A real one in production, a fake one in tests.",
 ]},

{"html": H("IoC and ", "DI") + table(["Term", "Meaning"], [
     (["<b>Inversion of Control</b>", "a framework creates objects and calls your code · \"don't call us, we'll call you\""], 0),
     (["<b>Dependency Injection</b>", "an object <b>receives</b> its dependencies instead of creating them"], 0),
     (["<b>IoC container</b>", "the <code>ApplicationContext</code>: creates, wires and manages objects"], 1),
     (["<b>bean</b>", "any object the container manages · <code>new</code> yourself → <b>not</b> a bean"], 1)], size=29) +
   row(box("blue", "loose coupling", "depend on interfaces", 2, "flex:1"), box("green", "easy tests", "pass a mock", 2, "flex:1"),
       box("purple", "one place to configure", "swap H2 ↔ PostgreSQL", 2, "flex:1"), style="margin-top:24px"),
 "steps": [
  "That idea has names. Inversion of control means your code no longer creates objects and drives the flow. A framework does, and calls your code. Don't call us, we'll call you. Dependency injection is one way to do it. An object receives its dependencies, instead of creating them.",
  "In Spring, the IoC container is the application context. It creates objects, wires their dependencies, and manages their lifecycle. And each object it manages is a bean. An object you create yourself with new is not a bean.",
  "The payoff: loose coupling, because classes depend on interfaces. Easy testing, because you can pass in a mock. And one place to configure what's used where. This is the D in SOLID, dependency inversion.",
 ]},

{"html": H("Registering ", "beans") + row(
   col(box("blue", "component scanning", "annotate your own classes", 0),
       code("""§0 @Service
§0 class TaskService { … }
§0 @Repository
§0 class JpaTaskRepository … { … }""", 27), gap=16, style="flex:1"),
   col(box("green", "<code>@Configuration</code> + <code>@Bean</code>", "for classes you can't annotate", 1),
       code("""§1 @Configuration
§1 class AppConfig {
§1   @Bean Clock clock() {
§1     return Clock.systemUTC(); } }""", 27), gap=16, style="flex:1"), top=True) +
   note("<code>@Component</code> · <code>@Service</code> · <code>@Repository</code> · <code>@Controller</code>: same mechanism, different <u>meaning</u>", 2),
 "steps": [
  "How does the container know what to create? Two ways. Component scanning: put an annotation on your own class, like service or repository, and Spring finds it at startup and makes it a bean.",
  "And for classes you can't annotate, like library classes, write a configuration class with bean methods. Each method returns an object, and Spring registers it.",
  "The stereotype annotations, component, service, repository, and controller, all work the same way. They differ in meaning. Repository also translates database exceptions, and controller marks web endpoints.",
 ]},

{"html": H("Three ways to ", "inject") + table(["Style", "Looks like", "Verdict"], [
     (["<b>constructor</b>", "<code>TaskService(TaskRepository repo)</code>", "✅ <b>use this</b>"], 0),
     (["setter", "<code>@Autowired void setRepo(…)</code>", "optional dependencies only"], 1),
     (["field", "<code>@Autowired private TaskRepository repo;</code>", "❌ avoid"], 1)], size=29) +
   row(box("green", "why constructor wins", "<code>final</code> fields · never half-built · dependencies visible · tests just call <code>new</code>", 2, "flex:1"),
       box("blue", "one constructor?", "no <code>@Autowired</code> needed", 3, "width:440px"), style="margin-top:24px"),
 "steps": [
  "Spring can inject a dependency three ways. Through the constructor, which is the one to use.",
  "Through a setter, which is only for optional dependencies. Or straight into a field, which you'll see in old tutorials, but should avoid.",
  "Why does constructor injection win? The fields can be final. The object is never half built. Its dependencies are visible in one place. And a test just calls new, passing fakes, with no Spring needed.",
  "And if a class has exactly one constructor, Spring uses it automatically. You don't even need the autowired annotation.",
 ]},

{"html": H("Two beans, one ", "type") + row(
   box("red", "the error", "two <code>NotificationSender</code> beans → <code>NoUniqueBeanDefinitionException</code>", 0, "flex:1"),
   col(box("blue", "<code>@Primary</code>", "the default choice", 1),
       box("purple", "<code>@Qualifier(\"sms\")</code>", "pick one by name at the injection point", 1),
       box("green", "<code>List&lt;NotificationSender&gt;</code>", "inject them <b style=\"display:inline\">all</b>", 2), gap=16, style="width:640px"), top=True),
 "steps": [
  "What if two beans have the same type? Say, an email sender and an SMS sender. Asking for a notification sender is now ambiguous, and startup fails with a no unique bean definition exception.",
  "Two fixes. Mark one primary, as the default. Or use qualifier at the injection point to pick one by name.",
  "And sometimes you want them all. Ask for a list of notification senders, and Spring injects every matching bean. Handy for plugins, or sending through every channel.",
 ]},

{"html": H("Bean ", "scopes") + table(["Scope", "Instances", "Notes"], [
     (["<b>singleton</b> (default)", "one per container", "shared → must be <b>thread-safe</b>"], 0),
     (["prototype", "a new one each time it's requested", "no <code>@PreDestroy</code>"], 1),
     (["request · session", "one per HTTP request · session", "web apps"], 1)], size=29) +
   row(box("orange", "not the GoF Singleton", "one per container, not a private constructor", 2, "flex:1"),
       box("red", "the trap", "a prototype inside a singleton is injected <b style=\"display:inline\">once</b> → use <code>ObjectProvider</code>", 3, "flex:1"), style="margin-top:24px"),
 "steps": [
  "A scope decides how many instances of a bean exist. The default is singleton: one per container, shared by everyone. So it must be thread safe. Never keep per-request data in a singleton's fields.",
  "Prototype creates a new instance every time it's requested, and Spring then forgets about it. Request and session scopes give one per HTTP request or session, in web apps.",
  "Careful: Spring's singleton isn't the design pattern with a private constructor. It just means one per container.",
  "And a classic trap. Inject a prototype into a singleton, and you get one instance forever, because the singleton is only built once. To get a fresh one each time, ask an object provider.",
 ]},

{"html": H("The bean ", "lifecycle") + row(
   box("gray", "1 · create", "constructor", 0, "flex:1"), '<div class="arrow" style="min-width:50px"></div>',
   box("blue", "2 · inject", "dependencies", 0, "flex:1"), '<div class="arrow" style="min-width:50px"></div>',
   box("green", "3 · init", "<code>@PostConstruct</code>", 1, "flex:1"), '<div class="arrow" style="min-width:50px"></div>',
   box("purple", "4 · post-process", "may wrap in a <b style=\"display:inline\">proxy</b>", 2, "flex:1"), gap=10) +
   row(box("orange", "5 · in use", "", 3, "flex:1"), '<div class="arrow" style="min-width:50px"></div>',
       box("red", "6 · destroy", "<code>@PreDestroy</code> on shutdown", 3, "flex:1"), gap=10, style="margin-top:26px") +
   note("Startup work goes in <code>@PostConstruct</code>, not the constructor: dependencies are ready", 4),
 "steps": [
  "Every singleton goes through the same steps. First the constructor runs. Then dependencies are injected.",
  "Then initialisation. A method marked post construct runs, once everything is wired.",
  "Then post processors run, and this is where Spring may wrap your bean in a proxy. Hold that thought.",
  "Then the bean is in use, until the container shuts down, when a method marked pre destroy runs, to release resources.",
  "So startup work, like warming a cache, belongs in post construct. By then, every dependency is ready.",
 ]},

{"html": H("Profiles, cycles and ", "@Lazy") + row(
   col(box("blue", "<code>@Value</code> + profiles", "read config values · <code>@Profile(\"dev\")</code> beans only exist in dev", 0),
       box("green", "spring.profiles.active=prod", "switch the whole setup without code changes", 0), gap=16, style="flex:1"),
   col(box("red", "circular dependency", "A needs B, B needs A, both via constructors → <b style=\"display:inline\">startup fails</b>", 1),
       box("orange", "the real fix", "redesign: extract the shared part into a third bean", 2),
       box("gray", "<code>@Lazy</code>", "a quick escape: inject a lazy proxy", 2), gap=16, style="flex:1"), top=True),
 "steps": [
  "Two practical topics. Configuration values come in with the value annotation. And profiles let a bean exist only in some environments. Set spring profiles active to prod, and the whole setup switches without code changes.",
  "Circular dependencies. If A needs B, and B needs A, both through constructors, neither can be built first, and startup fails.",
  "The real fix is a redesign. Usually the shared logic belongs in a third bean that both use. Lazy is a quick escape. It injects a proxy that creates the real bean later. But a cycle is usually a design smell.",
 ]},

{"html": H("Proxies: how Spring adds ", "behaviour") + row(
   box("blue", "caller", "injects TaskService", 0, "flex:1"), '<div class="arrow" style="min-width:60px"></div>',
   box("purple", "proxy", "begin transaction → call → commit", 0, "flex:1.3"), '<div class="arrow" style="min-width:60px"></div>',
   box("green", "your bean", "the real method", 0, "flex:1"), gap=10) +
   table(["Rule", "Why"], [
     (["<code>this.other()</code> skips <code>@Transactional</code>", "<code>this</code> is the real object, not the proxy"], 1),
     (["methods public, not <code>final</code>", "the proxy subclass must override them"], 2),
     (["only beans get it", "an object made with <code>new</code> was never wrapped"], 2)], size=29),
 "steps": [
  "Finally, the magic. How does adding transactional to a method make it run in a transaction? In the post processing step, Spring hands out a proxy instead of your bean. Everyone who injects your service actually gets the proxy, which begins a transaction, calls your real method, and commits. Caching, async, and method security all work this way.",
  "That explains some confusing rules. If a method calls another method of the same class through this, it skips the proxy, so that method's transactional annotation is ignored.",
  "Proxied methods must be public and not final, because the proxy is a generated subclass that overrides them. And only beans get any of this. An object you create with new was never wrapped.",
 ]},

quiz([
  ("Which injection style should you use?", "<b style=\"display:inline\">constructor</b> injection", "blue",
   "Quiz time. Which injection style should you use by default?",
   "Constructor injection. Final fields, visible dependencies, and easy tests."),
  ("Default bean scope?", "<b style=\"display:inline\">singleton</b>: one per container", "green",
   "What's the default bean scope, and what does that mean for its fields?",
   "Singleton. One shared instance, so it must be thread safe."),
  ("Why does <code>this.save()</code> skip <code>@Transactional</code>?", "it bypasses the <b style=\"display:inline\">proxy</b>", "purple",
   "Why does calling this dot save inside the same class skip the transactional annotation?",
   "Because this is the real object. The call never goes through the proxy."),
]),

recap(["IoC: the container creates and wires objects",
       "DI: receive dependencies · constructor injection",
       "Beans: @Component family or @Bean methods",
       "Two of a type: @Primary, @Qualifier, List",
       "Singleton by default → thread-safe · lifecycle hooks",
       "Proxies add transactions, caching, security"],
  "Let's recap. Inversion of control means the container creates and wires your objects. Dependency injection means classes receive their dependencies, and constructor injection is the way to do it. Register beans with the component annotations, or bean methods. Resolve two beans of one type with primary, qualifier, or a list. Beans are singletons by default, so keep them thread safe, and use the lifecycle hooks. And proxies are how Spring adds transactions, caching, and security. Now try the examples in your notes!"),
]
