from conc import *

TAG = "Java · Modern Java Features"
TRACK = "Java Fullstack · Java"
FILE = "Java Modern Java Features.mp4"

SLIDES = [
title_slide(0, "Modern Java", "Java 9 to 21 and beyond: less boilerplate, safer types, cheap threads",
  "Welcome. Today's concept: modern Java features.",
  "A lot of Java code you'll read was written for Java eight. Since then, the language has changed more than in the ten years before. Records, sealed types, pattern matching and virtual threads change how you model data and write services. By the end you'll know the release timeline, the everyday conveniences, records, sealed types, pattern matching for switch, sequenced collections and virtual threads.",
  pill="JAVA · CONCEPT"),

{"html": H("The release ", "timeline") + table(["Version", "Year", "Headline features"], [
     (["8 (LTS)", "2014", "lambdas · streams · Optional"], 0),
     (["11 (LTS)", "2018", "<code>var</code> · <code>List.of</code> · new String methods · HTTP client"], 1),
     (["17 (LTS)", "2021", "records · sealed classes · text blocks · switch expressions"], 1),
     (["21 (LTS)", "2023", "pattern matching for switch · record patterns · virtual threads"], 2),
     (["25 (LTS)", "2025", "the current long-term release · Spring Boot 4 runs on 17+"], 3)], size=29) +
   note("A new version every 6 months · a long-term support release every 2 years", 4),
 "steps": [
  "Java eight, in twenty fourteen, brought lambdas and streams. A lot of code still looks like that.",
  "Java eleven and seventeen, both long term support releases, added var, collection factories, records, sealed classes, text blocks and switch expressions.",
  "Java twenty one completed pattern matching, and added virtual threads.",
  "Java twenty five is the current long term release. Spring Boot four needs at least Java seventeen.",
  "Java now ships every six months, with a long term support release every two years. Companies mostly stay on those.",
 ]},

{"html": H("Everyday ", "conveniences") + code("""§0 var list = new ArrayList<String>();          // type inferred, still static
§1 List<String> names = List.of("Asha", "Ravi");  // immutable · no nulls
§1 Map<String, Integer> ages = Map.of("Asha", 25);
§2 "  hi  ".strip();  " ".isBlank();  "ab".repeat(3);  text.lines()
§3 String json = \"\"\"
§3     { "name": "Asha", "age": 25 }
§3     \"\"\";
§4 String size = switch (n) {
§4   case 0 -> "none";
§4   case 1, 2 -> "few";
§4   default -> { log(n); yield "many"; }
§4 };""", 26),
 "steps": [
  "Var lets the compiler infer a local variable's type. It's still statically typed, just less repetition. Use it when the type is obvious from the right hand side.",
  "List of, set of and map of create small immutable collections. Adding to them throws, and they reject nulls.",
  "Strings gained strip, which understands Unicode spaces, is blank, repeat, and lines.",
  "Text blocks, with three quotes, write multi line strings like JSON or SQL without escaping every quote and newline.",
  "And switch became an expression. Arrow cases don't fall through, several labels can share a case, and yield returns a value from a block.",
 ]},

{"html": H("", "Records") + row(
   code("""§0 record Point(int x, int y) { }
§1 record Range(int lo, int hi) {
§1   Range {                                  // compact constructor
§1     if (lo > hi) throw new IllegalArgumentException();
§1   }
§2   int length() { return hi - lo; }
§2   static Range of(int a, int b) { return new Range(a, b); }
§1 }""", 26, style="flex:1"),
   col(box("blue", "you get", "private final fields · constructor · <code>x()</code> accessors · <code>equals</code> · <code>hashCode</code> · <code>toString</code>", 0),
       box("green", "validate", "a compact constructor runs before the fields are set", 1),
       box("orange", "can't", "extend a class · add instance fields · be mutable", 3), gap=16, style="width:620px"), top=True) +
   note("Use for DTOs, map keys, return values · not for JPA entities", 3),
 "steps": [
  "A record is a class for plain data. One line gives you private final fields, a constructor, accessor methods named like the fields, and correct equals, hash code and to string.",
  "To validate, write a compact constructor. It has no parameter list, and runs before the fields are assigned.",
  "You can still add methods and static factories.",
  "But records are final, can't extend another class, and can't add instance fields or setters. They're perfect for DTOs, map keys and return values. They're not suited to JPA entities, which need to be mutable.",
 ]},

{"html": H("Sealed types and pattern ", "matching") + row(
   code("""§0 sealed interface Shape permits Circle, Square, Rect { }
§0 record Circle(double r) implements Shape { }
§0 record Square(double side) implements Shape { }
§0 record Rect(double w, double h) implements Shape { }
§1 if (obj instanceof String s && !s.isBlank()) use(s);
§2 double area(Shape s) {
§2   return switch (s) {
§2     case Circle c       -> Math.PI * c.r() * c.r();
§2     case Square q       -> q.side() * q.side();
§3     case Rect(var w, var h) -> w * h;      // record pattern
§2   };                                      // no default needed
§2 }""", 24, style="flex:1"),
   col(box("purple", "sealed", "only the listed classes may implement it", 0),
       box("blue", "instanceof pattern", "test and cast in one step", 1),
       box("green", "exhaustive switch", "the compiler knows every case · add a new shape → compile error", 2),
       box("orange", "record patterns", "take a record apart right in the case", 3), gap=14, style="width:560px"), top=True),
 "steps": [
  "A sealed interface lists exactly which classes may implement it. Here, a shape is a circle, a square or a rectangle, and nothing else.",
  "Pattern matching for instance of tests the type and binds a variable in one step. No more separate cast.",
  "Switch can now match on types. Because shape is sealed, the compiler knows all the cases, so no default is needed. Add a new shape later, and every switch that forgot it becomes a compile error. That's the big win.",
  "Record patterns go further, and unpack the record's components right in the case label.",
 ]},

{"html": H("Sequenced collections and ", "more") + row(
   box("blue", "SequencedCollection (21)", "<code>getFirst()</code> · <code>getLast()</code> · <code>addFirst()</code> · <code>reversed()</code> on lists, deques, linked sets and maps", 0, "flex:1"),
   box("green", "smaller wins", "helpful NullPointerException messages · <code>Stream.toList()</code> · <code>Objects.requireNonNullElse</code>", 1, "flex:1"),
   box("purple", "newer still", "unnamed variables <code>_</code> · String templates were withdrawn · stream gatherers", 2, "flex:1"), top=True) +
   code("""§0 list.getLast();          // was list.get(list.size() - 1)
§1 // NPE: Cannot invoke "String.length()" because "user.name" is null""", 25, style="margin-top:22px"),
 "steps": [
  "Java twenty one added sequenced collections. Lists, deques, linked hash sets and linked hash maps now share get first, get last, add first and reversed. No more size minus one.",
  "Smaller improvements add up. Null pointer exceptions now say exactly which reference was null. Streams have a direct to list.",
  "Newer releases keep going: an underscore for unused variables, and stream gatherers. Some previews, like string templates, were withdrawn, so check before relying on preview features.",
 ]},

{"html": H("Virtual ", "threads") + row(
   col(box("red", "platform threads", "one per OS thread · ~1 MB stack · a few thousand at most", 0),
       box("green", "virtual threads", "managed by the JVM · tiny · <b style=\"display:inline\">millions</b> · parked while they wait on I/O", 1),
       box("blue", "good for", "blocking I/O: HTTP calls, database queries · simple blocking code, async-level scale", 2),
       box("orange", "not for", "CPU-heavy work · don't pool them · watch <code>ThreadLocal</code> use", 3), gap=14, style="width:640px"),
   code("""§1 try (var ex = Executors
§1          .newVirtualThreadPerTaskExecutor()) {
§1   for (var url : urls) ex.submit(() -> fetch(url));
§1 }
§4 spring.threads.virtual.enabled=true""", 24, style="flex:1"), top=True),
 "steps": [
  "Classic Java threads map one to one onto operating system threads. Each one is heavy, so a server can only run a few thousand.",
  "Virtual threads are scheduled by the JVM. They're tiny, so you can have millions. When one blocks on I O, the JVM parks it and runs another on the same OS thread.",
  "So simple, blocking code, like calling a database, scales almost like asynchronous code. That's their purpose: lots of waiting.",
  "They don't make CPU heavy work faster. Create one per task instead of pooling them, and be careful with thread locals, since you may have millions.",
  "In Spring Boot, one property switches the web server to virtual threads.",
 ]},

quiz([
  ("Free with a record?", "constructor · accessors · <b style=\"display:inline\">equals/hashCode/toString</b>", "blue",
   "Quiz time. What do you get for free with a record?",
   "The constructor, accessors, and equals, hash code and to string."),
  ("Switch over a sealed type: why no default?", "the compiler knows <b style=\"display:inline\">every</b> subtype", "purple",
   "Why doesn't a switch over a sealed interface need a default?",
   "The compiler knows every permitted subtype, so it can check the switch is exhaustive."),
  ("Virtual threads help with…?", "<b style=\"display:inline\">blocking I/O</b>, not CPU work", "green",
   "What kind of work do virtual threads help with?",
   "Blocking I O, lots of waiting. Not CPU heavy work."),
]),

recap(["LTS: 8 · 11 · 17 · 21 · 25",
       "var · List.of · text blocks · switch expressions",
       "Records: immutable data, validated in a compact constructor",
       "Sealed + switch patterns → exhaustive, compiler-checked",
       "getFirst / getLast / reversed (21)",
       "Virtual threads: millions, for blocking I/O"],
  "Let's recap. The long term releases are eight, eleven, seventeen, twenty one and twenty five. Everyday code gets var, immutable collection factories, text blocks and switch expressions. Records give immutable data classes in one line. Sealed types with pattern matching switch make the compiler check every case. Sequenced collections add get first and get last. And virtual threads let blocking code scale to millions of tasks. Now practise with the examples in your notes!"),
]
