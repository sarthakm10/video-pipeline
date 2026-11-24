from conc import *

TAG = "Java · Design Patterns"
TRACK = "Java Fullstack · Java"
FILE = "Java Design Patterns.mp4"

SLIDES = [
title_slide(0, "Design Patterns", "Named, proven answers to problems that keep coming back",
  "Welcome. Today's concept: design patterns.",
  "A design pattern is a well known solution to a recurring design problem, with a name, so that developers can say builder or strategy and instantly understand each other. You don't memorise code, you learn the problem each pattern solves. By the end you'll know the three families, and the patterns interviews ask about most: singleton, factory, builder, adapter, decorator, proxy, facade, strategy, observer, and a few more.",
  pill="JAVA · CONCEPT"),

{"html": H("Three ", "families") + row(
   box("blue", "creational", "how objects are <b style=\"display:inline\">made</b><br>Singleton · Factory · Abstract Factory · Builder · Prototype", 0, "flex:1"),
   box("purple", "structural", "how objects are <b style=\"display:inline\">composed</b><br>Adapter · Decorator · Proxy · Facade · Composite", 1, "flex:1"),
   box("green", "behavioural", "how objects <b style=\"display:inline\">talk</b><br>Strategy · Observer · Command · Template Method · State · Chain", 2, "flex:1"), top=True) +
   note("Learn the <u>problem</u> each one solves, not the class diagram", 3),
 "steps": [
  "The classic patterns fall into three families. Creational patterns are about how objects get made.",
  "Structural patterns are about how objects are put together, wrapping or combining one another.",
  "Behavioural patterns are about how objects communicate and share responsibilities.",
  "The useful way to learn them is by the problem they solve. If you can describe the problem, you can rebuild the code.",
 ]},

{"html": H("Creational: Singleton, Factory, ", "Builder") + row(
   col(box("blue", "Singleton", "exactly one instance · simplest safe form: an <code>enum</code> · in Spring: just a bean", 0),
       box("purple", "Factory", "callers ask for <b style=\"display:inline\">what</b> they need, not which class: <code>Notifier.of(\"sms\")</code>", 1),
       box("green", "Builder", "many optional fields → readable, immutable construction", 2), gap=16, style="width:500px"),
   code("""§0 enum Config { INSTANCE; String url = "..."; }
§1 static Notifier of(String type) {
§1   return switch (type) {
§1     case "sms"   -> new SmsNotifier();
§1     case "email" -> new EmailNotifier();
§1     default -> throw new IllegalArgumentException(type);
§1   };
§1 }
§2 Pizza p = Pizza.builder().size(12).cheese(true).build();""", 23, style="flex:1"), top=True),
 "steps": [
  "Singleton guarantees one instance. The simplest thread safe version is an enum with one constant. In Spring applications you rarely write one, because beans are singletons by default.",
  "Factory hides which class gets created. Callers say what they need, like an SMS notifier, and the factory picks the class. Adding a new type touches only the factory.",
  "Builder handles objects with many optional fields. Instead of a constructor with ten arguments in a confusing order, you name each value, and build an immutable object at the end. Lombok's at builder generates it.",
 ]},

{"html": H("Structural: wrappers with different ", "jobs") + table(["Pattern", "Wraps an object to…", "Example"], [
     (["<b>Adapter</b>", "change its <b>interface</b> to the one you need", "<code>Arrays.asList</code> · old API → new API"], 0),
     (["<b>Decorator</b>", "<b>add behaviour</b>, same interface, stackable", "<code>new BufferedReader(new FileReader(f))</code>"], 1),
     (["<b>Proxy</b>", "<b>control access</b>: lazy, cache, security, transactions", "Spring's <code>@Transactional</code> proxy"], 2),
     (["<b>Facade</b>", "give a <b>simple front</b> to a complex subsystem", "<code>OrderService.placeOrder()</code>"], 3)], size=28) +
   note("Adapter, Decorator and Proxy all wrap · ask: change the interface, add features, or guard access?", 4),
 "steps": [
  "Four structural patterns are easy to confuse, because they all wrap another object. Adapter changes the interface. Your code expects one shape, a library offers another, and the adapter translates.",
  "Decorator keeps the same interface, and adds behaviour. Decorators stack. Java IO is the textbook example: a buffered reader wrapping a file reader.",
  "Proxy also keeps the interface, but controls access: creating the real object lazily, caching, checking permissions, or opening a transaction. Spring's transactional and security annotations work through proxies.",
  "Facade puts one simple method in front of a complicated subsystem. Place order might reserve stock, charge a card, and send an email behind it.",
  "So when you see a wrapper, ask what it's for: changing the interface, adding features, or guarding access.",
 ]},

{"html": H("Strategy: swap the ", "algorithm") + row(
   code("""§0 interface DiscountStrategy { int apply(int price); }
§1 class NoDiscount  implements DiscountStrategy { … }
§1 class Seasonal    implements DiscountStrategy { … }
§2 class Checkout {
§2   private final DiscountStrategy discount;   // injected
§2   int total(int price) { return discount.apply(price); }
§2 }
§3 Comparator<Task> byDue = Comparator.comparing(Task::due);""", 26, style="flex:1"),
   col(box("blue", "the problem", "a growing <code>if/else</code> over 'which way to do it'", 0),
       box("green", "the fix", "one interface, one class per way, choose at run time", 1),
       box("purple", "you already use it", "a <code>Comparator</code> is a strategy · lambdas make them one-liners", 3), gap=16, style="width:560px"), top=True),
 "steps": [
  "Strategy solves a common smell: a long if else chain choosing between ways of doing the same thing. Define an interface for the varying behaviour.",
  "Write one class per variant. Adding a new discount means adding a class, not editing a chain.",
  "The checkout doesn't know which strategy it has. It's injected, often by Spring, and can be swapped at run time.",
  "You use strategies all the time. A comparator passed to sort is a strategy, and with lambdas, most strategies are one line.",
 ]},

{"html": H("Observer and ", "Command") + row(
   col(box("blue", "Observer", "one subject, many listeners · the subject <b style=\"display:inline\">notifies</b> them, without knowing who they are", 0),
       code("""§0 events.publishEvent(new OrderPlaced(id));
§0 @EventListener void on(OrderPlaced e) { … }""", 24), gap=14, style="flex:1"),
   col(box("purple", "Command", "turn a request into an <b style=\"display:inline\">object</b> · queue it, log it, undo it", 1),
       code("""§1 interface Command { void run(); void undo(); }
§1 Deque<Command> history = new ArrayDeque<>();""", 24), gap=14, style="flex:1"), top=True) +
   note("Observer decouples who acts from who reacts · Command makes actions storable", 2),
 "steps": [
  "Observer: one object changes, and many others want to know. The subject keeps a list of listeners and notifies them, without knowing what they do. Spring's application events work this way: publish an order placed event, and any listener can react, like sending an email.",
  "Command turns an action into an object. Once an action is an object, you can queue it, log it, retry it, or push it on a history stack to support undo.",
  "So observer separates the code that acts from the code that reacts, and command makes actions something you can store and replay.",
 ]},

{"html": H("Template Method, State, ", "Chain") + table(["Pattern", "Idea", "Seen in"], [
     (["<b>Template Method</b>", "the base class fixes the steps · subclasses fill in some", "<code>JdbcTemplate</code> · JUnit lifecycle"], 0),
     (["<b>State</b>", "behaviour changes with state · one class per state, no giant switch", "order: NEW → PAID → SHIPPED"], 1),
     (["<b>Chain of Responsibility</b>", "pass a request along handlers until one handles it", "servlet filters · Spring Security chain"], 2)], size=28),
 "steps": [
  "Three more. Template method: a base class defines the fixed order of steps, and subclasses fill in particular steps. Spring's JDBC template opens the connection, runs your part, and always cleans up.",
  "State: when an object behaves differently depending on its state, give each state its own class, instead of a giant switch repeated in every method. An order that's new, paid, or shipped is the classic example.",
  "Chain of responsibility passes a request along a chain of handlers. Each one handles it, changes it, or passes it on. Servlet filters and the Spring Security filter chain are exactly this.",
 ]},

quiz([
  ("Same interface, extra behaviour, stackable?", "<b style=\"display:inline\">Decorator</b>", "purple",
   "Quiz time. A wrapper with the same interface that adds behaviour, and can be stacked. Which pattern?",
   "Decorator, like a buffered reader around a file reader."),
  ("An if/else chain picking an algorithm?", "<b style=\"display:inline\">Strategy</b>", "blue",
   "A long if else chain picks between several algorithms. Which pattern replaces it?",
   "Strategy. One interface, and one class per algorithm."),
  ("How does @Transactional work?", "a <b style=\"display:inline\">Proxy</b> around your bean", "green",
   "Which pattern does Spring use to make transactional work?",
   "A proxy. It wraps your bean and opens and commits the transaction around each call."),
]),

recap(["Creational · structural · behavioural",
       "Singleton (enum) · Factory · Builder",
       "Adapter changes the interface · Decorator adds · Proxy guards",
       "Facade: one simple front",
       "Strategy replaces if/else · Observer notifies listeners",
       "Spring uses them everywhere: proxies, templates, chains"],
  "Let's recap. Patterns come in three families: creational, structural and behavioural. Singleton, factory and builder control how objects are made. Adapter changes an interface, decorator adds behaviour, proxy guards access, and facade gives a simple front. Strategy replaces if else chains, and observer notifies listeners. And Spring itself is built from patterns: proxies, templates and chains. Now practise with the examples in your notes!"),
]
