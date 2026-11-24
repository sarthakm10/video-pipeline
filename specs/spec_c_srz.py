from conc import *

TAG = "Java · Serialization, Reflection, Regex and Time"
TRACK = "Java Fullstack · Java"
FILE = "Java Serialization Reflection Regex and Time.mp4"

SLIDES = [
title_slide(0, "Serialization, Reflection, Regex & Time", "Four built-in toolkits that frameworks use constantly, and that hide classic traps",
  "Welcome. Today's concepts: serialization, reflection, regular expressions, and java dot time.",
  "These four don't have much in common, except that you rarely write them by hand, yet frameworks like Spring and Jackson use them all the time, and interviewers ask about their traps. By the end you'll know how Java serialization works and why it's avoided, how reflection and dynamic proxies power frameworks, regex in Java without the classic bugs, and the modern date and time classes.",
  pill="JAVA · CONCEPT"),

{"html": H("Java ", "serialization") + row(
   code("""§0 class User implements Serializable {
§1   private static final long serialVersionUID = 1L;
§0   private String name;
§2   private transient String password;          // not written
§0 }
§0 try (var out = new ObjectOutputStream(new FileOutputStream("u.bin"))) {
§0   out.writeObject(user);                       // the whole object graph
§0 }""", 24, style="flex:1"),
   col(box("blue", "Serializable", "a marker interface · every reachable field must be serializable too", 0),
       box("orange", "serialVersionUID", "the class version · mismatch → <code>InvalidClassException</code> · declare it yourself", 1),
       box("green", "transient", "skip a field · it comes back as null / 0", 2), gap=14, style="width:620px"), top=True),
 "steps": [
  "Java serialization turns an object into bytes and back. Implement serializable, a marker interface with no methods, and an object output stream writes the object and everything it references.",
  "Every serializable class has a version number. If you don't declare one, Java computes it from the class's shape, so almost any change breaks reading old data, with an invalid class exception. Declare it yourself.",
  "Mark a field transient to leave it out, like a password or a cache. After reading, it holds its default, null or zero. For full control, a class can define private write object and read object methods.",
 ]},

{"html": H("Why it's ", "avoided") + row(
   box("red", "security", "reading untrusted bytes can run attacker-chosen code (gadget chains) · a long CVE history", 0, "flex:1"),
   box("orange", "brittle", "tied to class internals · Java-only · bypasses constructors", 1, "flex:1"),
   box("green", "use instead", "JSON with Jackson · Protobuf / Avro for services · records with a real constructor", 2, "flex:1"), top=True) +
   note("Never deserialize data you don't trust · if you must, use an ObjectInputFilter", 3),
 "steps": [
  "Built in serialization is largely avoided today. The biggest reason is security. Reading bytes from an untrusted source can trigger chains of existing classes that end up running code the attacker chose. It has caused many serious vulnerabilities.",
  "It's also brittle. The format depends on private fields, only Java can read it, and objects are created without running their constructors, so validation is skipped.",
  "Use JSON with Jackson, or Protobuf and Avro between services. Records help too: when they're deserialized, their canonical constructor runs, so validation still happens.",
  "The rule: never deserialize data you don't trust. If you must, restrict the allowed classes with an object input filter.",
 ]},

{"html": H("", "Reflection") + row(
   code("""§0 Class<?> c = user.getClass();             // or User.class, Class.forName(…)
§0 for (Field f : c.getDeclaredFields()) print(f.getName());
§1 Method m = c.getMethod("greet", String.class);
§1 Object out = m.invoke(user, "hi");         // call by name
§2 if (m.isAnnotationPresent(Transactional.class)) { … }
§3 Field f = c.getDeclaredField("password");
§3 f.setAccessible(true);                     // break encapsulation""", 24, style="flex:1"),
   col(box("blue", "inspect", "fields, methods, constructors, annotations at runtime", 0),
       box("green", "act", "create objects · call methods · read and write fields", 1),
       box("purple", "who uses it", "Spring (DI, <code>@Autowired</code>), JPA, Jackson, JUnit", 2),
       box("red", "costs", "slower · no compile-time checks · blocked across modules", 3), gap=14, style="width:600px"), top=True),
 "steps": [
  "Reflection lets code inspect classes at runtime. From a class object you can list fields, methods, constructors and annotations.",
  "And act on them: create instances, and call methods by name, with invoke.",
  "Frameworks are built on this. Spring scans annotations and injects dependencies, JPA reads entity fields, Jackson maps JSON to properties, JUnit finds test methods.",
  "Set accessible even reaches private fields. The costs: it's slower, errors only show at runtime, and the module system blocks access to packages that aren't opened. Use it in frameworks and tools, not everyday business code.",
 ]},

{"html": H("Dynamic ", "proxies") + row(
   code("""§0 PaymentService proxy = (PaymentService) Proxy.newProxyInstance(
§0     loader, new Class<?>[]{PaymentService.class},
§1     (p, method, args) -> {
§1       long t = System.nanoTime();
§1       Object result = method.invoke(realService, args);
§1       log(method.getName() + " took " + (System.nanoTime() - t));
§1       return result;
§1     });""", 24, style="flex:1"),
   col(box("blue", "a proxy", "a class generated at runtime that implements your interface", 0),
       box("green", "every call", "goes to one handler: before, call the real object, after", 1),
       box("purple", "that's Spring AOP", "<code>@Transactional</code>, <code>@Cacheable</code>, <code>@Async</code> wrap your bean in a proxy", 2), gap=14, style="width:600px"), top=True) +
   note("Self-invocation skips the proxy → @Transactional on an internal call does nothing", 3),
 "steps": [
  "Reflection can also create classes. A dynamic proxy is an object generated at runtime that implements the interfaces you list.",
  "Every method call on it goes to one handler. The handler can do something before, call the real object, and do something after. Here it times every call.",
  "This is exactly how Spring implements transactional, cacheable and async. Your bean is wrapped in a proxy, which starts the transaction, calls your method, and commits. For classes without an interface, Spring generates a subclass instead.",
  "And that explains a famous bug. When a method calls another method on the same object, the call doesn't go through the proxy, so the annotation on the inner method does nothing.",
 ]},

{"html": H("Regex in ", "Java") + row(
   col(table(["Pattern", "Means"], [
     (["<code>\\d \\w \\s</code>", "digit · word char · whitespace"], 0),
     (["<code>[a-z] [^0-9]</code>", "one of · none of"], 0),
     (["<code>* + ? {2,4}</code>", "0+ · 1+ · 0-1 · 2 to 4"], 0),
     (["<code>^ $ ( ) |</code>", "start · end · group · or"], 0)], size=27), style="width:760px"),
   code("""§1 private static final Pattern EMAIL =
§1     Pattern.compile("(\\\\w+)@(\\\\w+\\\\.com)");   // compile once
§2 Matcher m = EMAIL.matcher(text);
§2 while (m.find()) print(m.group(1));       // find: anywhere
§2 EMAIL.matcher(s).matches();               // matches: the WHOLE string
§3 "a.b.c".split("\\\\.");                      // split takes a regex!""", 22, style="flex:1"), top=True),
 "steps": [
  "A quick syntax refresher: character classes like digit, word and whitespace, sets in square brackets, quantifiers like star, plus and question mark, anchors, groups and alternatives.",
  "In Java, backslashes must be doubled inside string literals. Compile a pattern once, into a static final field, because compiling is the expensive part.",
  "Find looks for the next match anywhere in the text, while matches requires the whole string to match. Groups give you the captured parts.",
  "And watch out: split, replace all and string dot matches all take a regex. Splitting on a dot without escaping it splits on every character.",
 ]},

{"html": H("Regex ", "traps") + row(
   box("orange", "greedy vs lazy", "<code>&lt;.*&gt;</code> on <code>&lt;a&gt;&lt;b&gt;</code> matches both · <code>&lt;.*?&gt;</code> stops at the first <code>&gt;</code>", 0, "flex:1"),
   box("red", "catastrophic backtracking", "<code>(a+)+b</code> on \"aaaa…ac\" → exponential time · a ReDoS risk", 1, "flex:1"),
   box("blue", "hidden recompiles", "<code>String.matches</code> / <code>replaceAll</code> in a loop compile every time", 2, "flex:1"), top=True) +
   note("Prefer simple patterns · test them · never run user-supplied regex unbounded", 3),
 "steps": [
  "Quantifiers are greedy: they grab as much as possible, then back off. Dot star between angle brackets matches from the first bracket to the last. Add a question mark to make it lazy, and it stops at the first closing bracket.",
  "Nested quantifiers can explode. A pattern like a plus, grouped and repeated, on a long run of a's that doesn't match, tries exponentially many ways to split them. An attacker can use that to freeze a server.",
  "And convenience methods on string compile the pattern every time they're called. In a loop, use a precompiled pattern.",
  "Keep patterns simple, test them, and never run a regex supplied by users without limits.",
 ]},

{"html": H("java.", "time") + table(["Class", "Holds", "Example"], [
     (["<code>LocalDate</code>", "a date, no time, no zone", "a birthday"], 0),
     (["<code>LocalDateTime</code>", "date + time, no zone", "a meeting on a calendar"], 0),
     (["<code>ZonedDateTime</code>", "date + time + zone (rules, DST)", "10:00 in Asia/Kolkata"], 1),
     (["<code>Instant</code>", "a point on the UTC timeline", "<b>store this</b> · timestamps"], 1),
     (["<code>Duration</code> · <code>Period</code>", "seconds/nanos · years/months/days", "timeout · age"], 2)], size=27) +
   note("Immutable, thread-safe · replaces Date, Calendar and the non-thread-safe SimpleDateFormat", 3),
 "steps": [
  "Java eight's java dot time package replaced the old date classes. Local date is a date without a time or zone, like a birthday. Local date time adds a time, still without a zone.",
  "Zoned date time knows the zone's rules, including daylight saving. Instant is a point on the UTC timeline, the right thing to store in databases and logs. Convert to a zone only for display.",
  "Duration measures time in seconds and nanoseconds, for timeouts. Period measures in years, months and days, for things like age.",
  "All of them are immutable and thread safe. The old date and calendar were mutable, and simple date format isn't thread safe, a classic bug when shared as a static field. Use date time formatter instead.",
 ]},

quiz([
  ("transient field after deserializing?", "its default: <b style=\"display:inline\">null</b> / 0", "blue",
   "Quiz time. What value does a transient field have after deserializing?",
   "Its default value: null, zero, or false."),
  ("@Transactional method called from the same class?", "<b style=\"display:inline\">no transaction</b>: the proxy is skipped", "red",
   "A transactional method is called from another method in the same class. What happens?",
   "No transaction starts, because the call doesn't go through the proxy."),
  ("Store a timestamp in the DB as…?", "an <b style=\"display:inline\">Instant</b> (UTC)", "green",
   "Which java dot time class should you use to store a timestamp?",
   "An instant, in UTC. Convert to a zone only for display."),
]),

recap(["Serializable + serialVersionUID · transient skips",
       "Don't deserialize untrusted data · prefer JSON",
       "Reflection: inspect and call at runtime · frameworks",
       "Dynamic proxies = Spring AOP · self-calls skip them",
       "Regex: compile once · matches vs find · lazy .*?",
       "java.time: Instant to store · immutable, thread-safe"],
  "Let's recap. Java serialization writes object graphs, needs a declared version, and skips transient fields. But never deserialize untrusted data, and prefer JSON. Reflection inspects and calls code at runtime, and frameworks rely on it. Dynamic proxies are how Spring adds transactions, which is why self calls skip them. For regex, compile once, know matches from find, and beware greedy patterns. And with java dot time, store instants, and enjoy immutable, thread safe classes. Now practise with the examples in your notes!"),
]
