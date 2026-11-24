from conc import *

TAG = "Java · Functional Interfaces and Optional"
TRACK = "Java Fullstack · Java"
FILE = "Java Functional Interfaces and Optional.mp4"

SLIDES = [
title_slide(0, "Functional Interfaces & Optional", "Behaviour as a value, and absence as a type",
  "Welcome. Today's concept: functional interfaces, and Optional.",
  "Lambdas let you pass behaviour around like data. But a lambda always needs a target: a functional interface. And Optional is Java's answer to the question, what if there's no value? By the end you'll know what makes an interface functional, the big four from java dot util dot function, method references, composing functions, and how to use Optional well, including the mistakes to avoid.",
  pill="JAVA · CONCEPT"),

{"html": H("What makes an interface ", "functional") + row(
   code("""§0 @FunctionalInterface
§0 interface Validator {
§0   boolean check(String s);          // exactly ONE abstract method
§1   default Validator and(Validator o) { … }  // defaults are fine
§0 }
§2 Validator notBlank = s -> !s.isBlank();
§2 notBlank.check("hi");                // true""", 26, style="flex:1"),
   col(box("blue", "one abstract method", "the lambda <b style=\"display:inline\">is</b> that method's body", 0),
       box("gray", "defaults and statics", "don't count · <code>@FunctionalInterface</code> makes the compiler check", 1),
       box("green", "already everywhere", "<code>Runnable</code> · <code>Comparator</code> · <code>Callable</code>", 2), gap=16, style="width:560px"), top=True),
 "steps": [
  "A functional interface has exactly one abstract method. That's all. A lambda is simply an implementation of that one method.",
  "It can still have default and static methods, because those already have bodies. The at functional interface annotation is optional, but it makes the compiler complain if someone adds a second abstract method.",
  "So the lambda s arrow not s dot is blank becomes a validator. And you've been using functional interfaces all along: runnable, comparator, callable.",
 ]},

{"html": H("Lambdas and effectively ", "final") + row(
   code("""§0 int limit = 10;
§0 Predicate<Integer> small = x -> x < limit;   // captures limit
§1 limit = 20;            // compile error: limit must not change
§2 int[] count = {0};     // workaround people use…
§2 list.forEach(x -> count[0]++);   // …but prefer streams' count()""", 25, style="flex:1"),
   col(box("purple", "capture", "a lambda can read local variables from around it", 0),
       box("red", "effectively final", "never reassigned after its first value", 1),
       box("blue", "this", "in a lambda: the <b style=\"display:inline\">enclosing</b> object · in an anonymous class: the class itself", 3), gap=16, style="width:600px"), top=True),
 "steps": [
  "A lambda can use local variables from the code around it. Here, small captures limit.",
  "But a captured variable must be effectively final, meaning never reassigned. If you change limit later, it's a compile error. The lambda might run later, or on another thread, so Java copies the value, and doesn't let it drift.",
  "People work around it with a one element array, but that's a smell. Usually a stream operation, like count or sum, is the cleaner answer.",
  "One more difference from anonymous classes. Inside a lambda, this means the enclosing object. Inside an anonymous class, this is the anonymous object itself.",
 ]},

{"html": H("The big ", "four") + table(["Interface", "Method", "Shape", "Used for"], [
     (["<code>Function&lt;T, R&gt;</code>", "<code>apply</code>", "T → R", "<code>map</code>"], 0),
     (["<code>Predicate&lt;T&gt;</code>", "<code>test</code>", "T → boolean", "<code>filter</code>"], 1),
     (["<code>Consumer&lt;T&gt;</code>", "<code>accept</code>", "T → nothing", "<code>forEach</code>"], 2),
     (["<code>Supplier&lt;T&gt;</code>", "<code>get</code>", "nothing → T", "<code>orElseGet</code>, lazy values"], 3)], size=30) +
   note("Two inputs: <code>BiFunction</code> · same type in and out: <code>UnaryOperator</code>, <code>BinaryOperator</code> · primitives: <code>IntPredicate</code>…", 4),
 "steps": [
  "Java ships ready made functional interfaces in java dot util dot function. Four matter most. A function takes a T and returns an R. Stream's map takes one.",
  "A predicate takes a T and returns a boolean. Filter takes one.",
  "A consumer takes a T and returns nothing. It does something, like printing. For each takes one.",
  "And a supplier takes nothing and returns a T. It's how you make something lazy: the value is only produced when get is called.",
  "There are variants. Bi function takes two inputs. Unary operator and binary operator keep the same type in and out. And primitive versions, like int predicate, avoid boxing every number.",
 ]},

{"html": H("Method ", "references") + table(["Kind", "Method reference", "Same as"], [
     (["static method", "<code>Integer::parseInt</code>", "<code>s -> Integer.parseInt(s)</code>"], 0),
     (["method of a given object", "<code>System.out::println</code>", "<code>x -> System.out.println(x)</code>"], 1),
     (["method of the argument", "<code>String::toUpperCase</code>", "<code>s -> s.toUpperCase()</code>"], 2),
     (["constructor", "<code>ArrayList::new</code>", "<code>() -> new ArrayList&lt;&gt;()</code>"], 3)], size=29) +
   note("Use them when the lambda only passes its arguments along", 3),
 "steps": [
  "When a lambda only calls one existing method, a method reference says it shorter. Integer colon colon parse int is the same as a lambda that parses its argument.",
  "System dot out colon colon print line calls a method on one specific object.",
  "String colon colon to upper case calls the method on the argument itself. The argument becomes the object.",
  "And array list colon colon new refers to a constructor. Use method references when the lambda just passes its arguments straight through. If it does more, a lambda is clearer.",
 ]},

{"html": H("Composing ", "functions") + code("""§0 Predicate<String> notBlank = s -> !s.isBlank();
§0 Predicate<String> shortOne = s -> s.length() < 10;
§0 Predicate<String> ok = notBlank.and(shortOne).or(String::isEmpty);
§1 Function<Integer, Integer> plus1 = x -> x + 1, twice = x -> x * 2;
§1 plus1.andThen(twice).apply(3);   // (3 + 1) * 2 = 8
§1 plus1.compose(twice).apply(3);   // 3 * 2 + 1 = 7
§2 Comparator.comparing(Task::priority).thenComparing(Task::title)""", 27) +
   note("Small named pieces, combined: easier to read and test", 3),
 "steps": [
  "Functional interfaces come with default methods for combining them. Predicates combine with and, or, and negate. Here two small rules become one.",
  "Functions chain. plus one and then twice means add one first, then double. Three becomes eight. Compose runs the other one first. Three doubled is six, plus one is seven.",
  "And comparators chain with then comparing. You saw that in the comparator video.",
  "The benefit is building logic from small, named pieces, which are each easy to read and to test.",
 ]},

{"html": H("Optional: why it ", "exists") + row(
   col(box("red", "null as 'no value'", "invisible in the signature · forget a check → <code>NullPointerException</code>", 0),
       box("green", "Optional&lt;T&gt;", "the return type <b style=\"display:inline\">says</b> it may be empty · the caller must decide", 1),
       box("blue", "creating", "<code>Optional.of(x)</code> · <code>ofNullable(x)</code> · <code>empty()</code>", 2), gap=16, style="width:640px"),
   code("""§1 Optional<User> findByEmail(String email);
§2 Optional.of(null);         // NPE!
§2 Optional.ofNullable(null); // empty""", 27, style="flex:1"), top=True),
 "steps": [
  "Returning null to mean no value has a problem. Nothing in the method signature warns you. Forget one null check, and you get a null pointer exception, often far away from the cause.",
  "Optional makes absence visible. A method that returns optional of user tells every caller: this might be empty, decide what to do.",
  "You create one with of, for a value that's definitely there, of nullable, for a value that might be null, or empty. Careful: of with null throws immediately. Use of nullable when you're not sure.",
 ]},

{"html": H("Using Optional ", "well") + code("""§0 String name = repo.findByEmail(email)
§1     .filter(User::active)
§1     .map(User::name)                       // Optional<String>
§2     .orElse("guest");                      // default value
§3 repo.findById(id).orElseThrow(() -> new NotFoundException(id));
§3 repo.findById(id).ifPresent(u -> mailer.welcome(u));""", 27) + row(
   box("orange", "orElse vs orElseGet", "<code>orElse(x)</code> always builds x · <code>orElseGet(() -> x)</code> only when empty", 2, "flex:1"),
   box("purple", "map vs flatMap", "the function already returns an Optional → <code>flatMap</code>", 1, "flex:1"), style="margin-top:22px"),
 "steps": [
  "Here's Optional used well. Look up a user. The result might be empty.",
  "Filter keeps the value only if it passes a test. Map transforms the value if one is there, and does nothing if it's empty. If your function itself returns an optional, use flat map, so you don't get an optional inside an optional.",
  "At the end, decide what empty means. Or else gives a default. But note: or else always evaluates its argument, even when there's a value. If the default is expensive, use or else get, which takes a supplier and only runs when needed.",
  "Or else throw turns empty into an exception, which is perfect for a not found error. And if present runs some code only when there's a value.",
 ]},

{"html": H("Optional ", "anti-patterns") + table(["Don't", "Instead"], [
     (["<code>if (opt.isPresent()) opt.get()</code>", "<code>map</code> · <code>orElse</code> · <code>ifPresent</code>"], 0),
     (["<code>opt.get()</code> with no check", "<code>orElseThrow()</code>: the intent is clear"], 0),
     (["Optional fields and parameters", "return types only"], 1),
     (["<code>Optional&lt;List&lt;T&gt;&gt;</code>", "return an <b>empty list</b>"], 2),
     (["returning <code>null</code> from an Optional method", "<code>Optional.empty()</code>"], 2)], size=29),
 "steps": [
  "A few anti patterns. Checking is present and then calling get is just a null check with extra steps. Use map, or else, or if present. And calling get without checking is no safer than null. If you mean that it must exist, say or else throw.",
  "Optional was designed for return values. Don't use it for fields or method parameters. It isn't serializable, and it adds noise.",
  "Don't wrap a collection in an optional. An empty list already means nothing found. And never return null from a method declared to return optional. That defeats the whole point.",
 ]},

quiz([
  ("filter takes which functional interface?", "<code>Predicate&lt;T&gt;</code>", "blue",
   "Quiz time. Stream's filter takes which functional interface?",
   "A predicate. It takes an element and returns a boolean."),
  ("Expensive default: orElse or orElseGet?", "<b style=\"display:inline\">orElseGet</b>: runs only if empty", "orange",
   "The default value is expensive to build. Or else, or or else get?",
   "Or else get. It takes a supplier, so the default is only built when the optional is empty."),
  ("Optional.of(null)?", "throws <b style=\"display:inline\">NullPointerException</b>", "red",
   "What happens with optional dot of null?",
   "It throws a null pointer exception. Use of nullable when the value might be null."),
]),

recap(["Functional interface = one abstract method",
       "Captured locals must be effectively final",
       "Function · Predicate · Consumer · Supplier",
       "Method references when a lambda just forwards",
       "Optional for return types: map, filter, orElse…",
       "orElseGet for expensive defaults · no get() without a check"],
  "Let's recap. A functional interface has one abstract method, and a lambda implements it. Captured local variables must be effectively final. The big four are function, predicate, consumer and supplier. Method references replace lambdas that just forward their arguments. Optional is for return types, used with map, filter, and or else. Use or else get for expensive defaults, and never call get without a check. Now practise with the examples in your notes!"),
]
