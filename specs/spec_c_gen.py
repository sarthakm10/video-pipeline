from conc import *

TAG = "Java · Generics in Depth"
TRACK = "Java Fullstack · Java"
FILE = "Java Generics in Depth.mp4"

SLIDES = [
title_slide(0, "Generics in Depth", "Type safety at compile time, and why the types vanish at run time",
  "Welcome. Today's concept: generics, in depth.",
  "You use generics every day: list of string, map of string to integer. But a few rules surprise almost everyone. Why isn't a list of integer a list of number? What do question mark extends and question mark super really mean? And why can't you write new T? By the end you'll know generic classes and methods, bounds, invariance, wildcards and the PECS rule, and type erasure with the limits it causes.",
  pill="JAVA · CONCEPT"),

{"html": H("Why ", "generics") + row(
   code("""§0 List list = new ArrayList();      // before Java 5
§0 list.add("hi");
§0 list.add(42);                      // allowed!
§0 String s = (String) list.get(1);  // ClassCastException""", 26, style="flex:1"),
   code("""§1 List<String> list = new ArrayList<>();
§1 list.add("hi");
§1 list.add(42);           // compile error ✓
§1 String s = list.get(0); // no cast""", 26, style="flex:1"), top=True) +
   row(box("green", "type safety", "mistakes caught by the <b style=\"display:inline\">compiler</b>, not in production", 2, "flex:1"),
       box("blue", "no casts", "the compiler inserts them for you", 2, "flex:1"),
       box("purple", "reuse", "one <code>Box&lt;T&gt;</code> works for every type", 2, "flex:1"), style="margin-top:24px"),
 "steps": [
  "Before Java five, collections held plain objects. You could put a string and an integer in the same list, and you had to cast when reading. A wrong cast crashed at run time, with a class cast exception.",
  "With generics, the list says what it holds. Adding an integer to a list of string is a compile error, and reading needs no cast.",
  "So generics give three things. Type safety, with mistakes caught by the compiler. No casts in your code. And reuse: one class works with any type.",
 ]},

{"html": H("Generic classes and ", "methods") + row(
   code("""§0 class Box<T> {
§0   private T value;
§0   T get() { return value; }
§0   void set(T v) { value = v; }
§0 }
§0 Box<String> b = new Box<>();   // diamond
§1 static <T> T first(List<T> list) {
§1   return list.get(0);
§1 }
§1 String s = first(List.of("a", "b"));""", 26, style="flex:1"),
   col(box("blue", "type parameter", "<code>T</code> is a placeholder, filled in at use", 0),
       box("purple", "generic method", "declares its own <code>&lt;T&gt;</code> <b style=\"display:inline\">before</b> the return type", 1),
       box("green", "inference", "the compiler works out <code>T</code> from the arguments", 1),
       box("gray", "naming", "T type · E element · K, V key/value · R result", 2), gap=14, style="width:560px"), top=True),
 "steps": [
  "A generic class declares a type parameter, here T, in angle brackets. Inside, T is used like any type. When you use the class, you fill it in. Box of string. The diamond on the right lets the compiler copy the type from the left.",
  "Methods can be generic on their own, even in a non generic class. The type parameter goes before the return type. Here first takes a list of any T, and returns a T. You rarely write the type when calling it. The compiler infers it from the arguments.",
  "By convention, type parameters are single capital letters. T for type, E for element, K and V for key and value, R for result.",
 ]},

{"html": H("Bounded type ", "parameters") + code("""§0 static <T extends Comparable<T>> T max(List<T> list) {
§0   T best = list.get(0);
§0   for (T x : list) if (x.compareTo(best) > 0) best = x;
§0   return best;
§0 }
§1 <T extends Number & Comparable<T>>   // a class first, then interfaces""", 27) + row(
   box("blue", "upper bound", "<code>T extends X</code>: T must be X or a subtype · <b style=\"display:inline\">extends</b> also means implements", 0, "flex:1"),
   box("purple", "what you gain", "you can call X's methods on T, like <code>compareTo</code>", 2, "flex:1"), style="margin-top:22px"),
 "steps": [
  "Sometimes T can't be just anything. To find a maximum, we need to compare elements. So we bound T: T extends comparable of T. Now only comparable types are allowed, and inside the method we can call compare to.",
  "You can list several bounds with an ampersand. A class comes first, then any interfaces.",
  "Note that in a bound, extends is used for both classes and interfaces. It just means T must be that type, or a subtype of it. That's what lets the compiler accept the method calls.",
 ]},

{"html": H("Invariance: the big ", "surprise") + row(
   col(box("green", "arrays are covariant", "<code>Integer[]</code> is a <code>Number[]</code>", 0),
       box("red", "…and fail at run time", "storing a Double → <code>ArrayStoreException</code>", 0),
       box("orange", "generics are invariant", "<code>List&lt;Integer&gt;</code> is <b style=\"display:inline\">not</b> a <code>List&lt;Number&gt;</code>", 1), gap=16, style="flex:1"),
   code("""§0 Number[] nums = new Integer[3];
§0 nums[0] = 1.5;   // ArrayStoreException
§1 List<Integer> ints = new ArrayList<>();
§1 List<Number> nums = ints;  // compile error
§2 nums.add(1.5);   // ...because this would
§2                  // put a Double in ints""", 25, style="width:720px"), top=True),
 "steps": [
  "Here's the rule that surprises everyone. An integer is a number. And an integer array is a number array. Arrays are covariant. But that's unsafe. Store a double into it, and Java can only stop you at run time, with an array store exception.",
  "Generics learned from that mistake. A list of integer is not a list of number, even though integer is a number. Generics are invariant. Assigning one to the other is a compile error.",
  "Why? If it were allowed, you could add a double through the list of number, and it would end up inside the list of integer. Invariance stops that before the code ever runs. But it also makes methods less flexible. That's what wildcards fix.",
 ]},

{"html": H("Wildcards and ", "PECS") + table(["Wildcard", "Accepts", "You can", "Think"], [
     (["<code>List&lt;? extends Number&gt;</code>", "List of Integer, Double, …", "<b>read</b> as Number · not add", "producer"], 0),
     (["<code>List&lt;? super Integer&gt;</code>", "List of Integer, Number, Object", "<b>add</b> Integers · read as Object", "consumer"], 1),
     (["<code>List&lt;?&gt;</code>", "any list", "read as Object only", "don't care"], 2)], size=28) +
   code("""§3 static <T> void copy(List<? super T> dst, List<? extends T> src) {
§3   for (T x : src) dst.add(x);   // src produces, dst consumes
§3 }""", 27, style="margin-top:20px") +
   note("<b>PECS</b>: Producer Extends, Consumer Super", 3),
 "steps": [
  "Wildcards restore flexibility. Question mark extends number accepts a list of integer, a list of double, any list of a subtype. You can read from it, and everything you get is a number. But you can't add, because the compiler doesn't know which subtype the list really holds.",
  "Question mark super integer is the opposite. It accepts a list of integer, number, or object. You can safely add integers, since all of those can hold one. But reading only gives you object.",
  "A plain question mark means any list, when you don't care about the type at all.",
  "The rule to remember is PECS: producer extends, consumer super. If a parameter gives you values, use extends. If it takes values from you, use super. Collections dot copy is the textbook example. The source produces, the destination consumes.",
 ]},

{"html": H("Type ", "erasure") + row(
   code("""§0 // what you write
§0 List<String> names = new ArrayList<>();
§0 String first = names.get(0);
§1 // what the bytecode holds
§1 List names = new ArrayList();
§1 String first = (String) names.get(0);""", 26, style="flex:1"),
   col(box("blue", "compile time only", "generic types are checked, then <b style=\"display:inline\">erased</b>", 0),
       box("purple", "T → its bound", "unbounded T becomes <code>Object</code> · casts are inserted", 1),
       box("green", "why", "old pre-generics code kept working", 2), gap=16, style="width:560px"), top=True),
 "steps": [
  "Generics exist only at compile time. The compiler checks your types, and then erases them. This is type erasure.",
  "In the bytecode, list of string is just list, T becomes object, or its bound if it has one, and the compiler quietly inserts the casts you used to write by hand.",
  "Why design it this way? Backward compatibility. When generics arrived in Java five, every existing library and class file kept working, without being recompiled.",
 ]},

{"html": H("What erasure ", "forbids") + table(["You can't…", "Because at run time…"], [
     (["<code>new T()</code> or <code>new T[10]</code>", "there is no T to create"], 0),
     (["<code>x instanceof List&lt;String&gt;</code>", "every List is just List"], 1),
     (["overload <code>f(List&lt;String&gt;)</code> and <code>f(List&lt;Integer&gt;)</code>", "both erase to <code>f(List)</code>"], 2),
     (["<code>List&lt;int&gt;</code>", "T erases to Object · use <code>Integer</code>"], 3)], size=29) +
   note("Need the type at run time? Pass a <code>Class&lt;T&gt;</code>: <code>create(Class&lt;T&gt; type)</code>", 4),
 "steps": [
  "Erasure explains a set of rules that otherwise seem random. You can't write new T, or create a T array, because at run time there's no T to create.",
  "You can't check instance of list of string. At run time, every list is just a list.",
  "You can't overload a method on list of string and list of integer. After erasure, both have the same signature.",
  "And you can't use primitives as type arguments. T becomes object, and int isn't an object, so you use integer, with autoboxing.",
  "When you really need the type at run time, pass a class object in explicitly. That's why libraries ask for things like task dot class.",
 ]},

quiz([
  ("Is List&lt;Integer&gt; a List&lt;Number&gt;?", "<b style=\"display:inline\">no</b>: generics are invariant", "red",
   "Quiz time. Is a list of integer a list of number?",
   "No. Generics are invariant, otherwise you could add a double to a list of integers."),
  ("A method only reads Numbers from a list. Which type?", "<code>List&lt;? extends Number&gt;</code>", "blue",
   "A method only reads numbers out of a list. What should the parameter type be?",
   "List of question mark extends number. It's a producer, so extends."),
  ("Why can't you write new T()?", "type <b style=\"display:inline\">erasure</b>: no T at run time", "purple",
   "Why can't you write new T inside a generic class?",
   "Because of type erasure. At run time the type T doesn't exist any more."),
]),

recap(["Generics: compile-time safety, no casts",
       "Generic method: &lt;T&gt; before the return type",
       "T extends X: a bound, so you can call X's methods",
       "Invariant: List&lt;Integer&gt; is not List&lt;Number&gt;",
       "PECS: producer extends, consumer super",
       "Erasure: no new T, no instanceof List&lt;String&gt;"],
  "Let's recap. Generics give compile time type safety, and remove casts. A generic method declares its type parameter before the return type. A bound like T extends comparable lets you call that type's methods. Generics are invariant, so a list of integer is not a list of number. Wildcards fix that, following PECS: producer extends, consumer super. And type erasure removes generic types at run time, which is why you can't create a T or check instance of with a type argument. Now practise with the examples in your notes!"),
]
