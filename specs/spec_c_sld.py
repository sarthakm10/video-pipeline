from conc import *

TAG = "Java · SOLID and Low Level Design"
TRACK = "Java Fullstack · Java"
FILE = "Java SOLID and Low Level Design.mp4"

SLIDES = [
title_slide(0, "SOLID & LLD", "Five principles for code that's easy to change, and how to use them in a design interview",
  "Welcome. Today's concept: SOLID, and low level design.",
  "Code is read and changed far more often than it's written. SOLID is five principles that keep classes small, focused, and safe to change. Low level design interviews ask you to apply them live: design a parking lot, design a library. By the end you'll know cohesion and coupling, each SOLID principle with a tiny example, composition over inheritance, and a step by step approach for LLD interviews.",
  pill="JAVA · CONCEPT"),

{"html": H("Cohesion and ", "coupling") + row(
   box("green", "high cohesion ✓", "everything in a class serves <b style=\"display:inline\">one</b> purpose", 0, "flex:1"),
   box("red", "low coupling ✓", "classes know little about each other · change one, the others don't break", 1, "flex:1"), top=True) +
   note("SOLID is five concrete ways to get high cohesion and low coupling", 2),
 "steps": [
  "Two ideas sit under all of this. Cohesion: how strongly the parts of a class belong together. High cohesion means a class does one job well.",
  "Coupling: how much classes depend on each other's details. Low coupling means you can change one class without breaking others.",
  "SOLID is five concrete rules for getting high cohesion and low coupling.",
 ]},

{"html": H("S: Single ", "Responsibility") + col(
   code("""§0 class Invoice {
§0   int total() { … }
§0   void saveToDb() { … }       // persistence
§0   String toPdf() { … }        // formatting
§0   void email(String to) { … } // delivery
§0 }""", 24),
   code("""§1 class Invoice { int total() { … } }
§1 class InvoiceRepository { void save(Invoice i) { … } }
§1 class InvoicePdf        { byte[] render(Invoice i) { … } }
§1 class InvoiceMailer     { void send(Invoice i, String to) { … } }""", 24), gap=14) +
   box("blue", "one reason to change", "the DB changes, the PDF layout changes, the mail provider changes: three <b style=\"display:inline\">different</b> people, three classes", 2, "margin-top:24px"),
 "steps": [
  "S is the single responsibility principle. This invoice calculates totals, saves itself, renders a PDF, and sends email. It has four reasons to change.",
  "Split it. Invoice keeps the business logic. A repository saves it. A PDF class renders it. A mailer sends it.",
  "The test is: a class should have one reason to change. A new database, a new PDF layout, a new mail provider each affect exactly one class, often owned by different people.",
 ]},

{"html": H("O: Open/", "Closed") + col(
   code("""§0 double area(Shape s) {
§0   if (s instanceof Circle c) return Math.PI * c.r() * c.r();
§0   if (s instanceof Square q) return q.side() * q.side();
§0   // add Triangle → edit this method again
§0 }""", 25),
   code("""§1 interface Shape { double area(); }
§1 record Circle(double r)    implements Shape { … }
§1 record Square(double side) implements Shape { … }
§1 record Triangle(…)         implements Shape { … } // new file""", 25), gap=14) +
   box("green", "open for extension, closed for modification", "add behaviour by adding code, not by editing working code · polymorphism, Strategy", 2, "margin-top:24px"),
 "steps": [
  "O is the open closed principle. This area method checks the type of each shape. Every new shape means editing it again, and risking what already works.",
  "Instead, make area part of the shape interface. Each shape computes its own area. Adding a triangle is a new class, and existing code doesn't change.",
  "Open for extension, closed for modification. Add features by adding code. Polymorphism and the strategy pattern are the usual tools.",
 ]},

{"html": H("L: Liskov ", "Substitution") + row(
   col(box("red", "Square extends Rectangle?", "<code>setWidth(5)</code> on a Square also changes the height · code expecting a Rectangle breaks", 0),
       box("orange", "the rule", "a subclass must work <b style=\"display:inline\">anywhere</b> its parent is expected, with no surprises", 1),
       box("green", "warning signs", "overrides that throw <code>UnsupportedOperationException</code> · empty overrides · <code>instanceof</code> checks", 2), gap=16, style="width:820px"),
   code("""§0 void stretch(Rectangle r) {
§0   r.setWidth(5); r.setHeight(4);
§0   assert r.area() == 20;   // fails for Square!
§0 }""", 26, style="flex:1"), top=True),
 "steps": [
  "L is the Liskov substitution principle. Is a square a rectangle? Mathematically, yes. But if square extends rectangle, setting its width also changes its height. Code written for rectangles, like this stretch method, suddenly fails.",
  "The rule: a subclass must work anywhere its parent is expected, without surprising the caller. If it can't keep the parent's promises, it shouldn't be a subclass.",
  "Watch for the warning signs: overrides that throw unsupported operation, overrides that do nothing, and callers checking instance of to handle one subclass specially.",
 ]},

{"html": H("I and D: small interfaces, depend on ", "abstractions") + row(
   col(box("purple", "I: Interface Segregation", "don't force classes to implement methods they don't use", 0),
       code("""§0 interface Printer { void print(Doc d); }
§0 interface Scanner { void scan(Doc d); }
§0 class SimplePrinter implements Printer { … }""", 24), gap=14, style="flex:1"),
   col(box("blue", "D: Dependency Inversion", "high-level code depends on an <b style=\"display:inline\">interface</b>, not a concrete class", 1),
       code("""§1 class OrderService {
§1   private final PaymentGateway pay;   // interface
§1   OrderService(PaymentGateway pay) { this.pay = pay; }
§1 }""", 24), gap=14, style="flex:1"), top=True) +
   note("Dependency Inversion + constructor injection = what Spring does for you", 2),
 "steps": [
  "I is interface segregation. A fat multifunction machine interface forces a simple printer to implement scan and fax with empty methods. Split it into small interfaces, and classes implement only what they support.",
  "D is dependency inversion. The order service shouldn't create a Stripe client itself. It depends on a payment gateway interface, and the real implementation is passed in. Now it's easy to swap providers, or use a fake in tests.",
  "That's exactly what Spring's constructor injection does. Dependency inversion is the principle, and dependency injection is the mechanism.",
 ]},

{"html": H("Composition over ", "inheritance") + row(
   col(box("red", "inheritance", "<b style=\"display:inline\">is-a</b> · fixed at compile time · subclass sees parent internals · deep trees get fragile", 0),
       box("green", "composition", "<b style=\"display:inline\">has-a</b> · hold a field of an interface type · swap behaviour at run time", 1), gap=16, style="flex:1"),
   col(box("blue", "also", "DRY: don't repeat knowledge · KISS: keep it simple · YAGNI: don't build it until needed", 2),
       box("purple", "Law of Demeter", "talk to friends only · <code>a.getB().getC().doIt()</code> is a smell", 2), gap=16, style="flex:1"), top=True),
 "steps": [
  "A related rule: prefer composition over inheritance. Inheritance is an is a relationship, fixed when you compile. Subclasses depend on parent internals, and deep hierarchies break in surprising ways.",
  "Composition is a has a relationship. A class holds a field of an interface type, and delegates to it. You can swap the behaviour at run time. Strategy and decorator are both composition.",
  "And a few short principles. DRY, don't repeat yourself: keep each piece of knowledge in one place. KISS: keep it simple. YAGNI: you aren't going to need it, so don't build for imagined futures. And the law of Demeter: don't reach through chains of objects.",
 ]},

{"html": H("An LLD interview, step by ", "step") + row(
   box("blue", "1 · clarify", "requirements · what's in and out of scope", 0, "flex:1"),
   box("purple", "2 · entities", "nouns → classes: <code>ParkingLot</code>, <code>Level</code>, <code>Spot</code>, <code>Vehicle</code>, <code>Ticket</code>", 1, "flex:1"),
   box("green", "3 · relationships", "has-a / is-a · enums for types: <code>SpotSize</code>", 2, "flex:1"), top=True) +
   row(box("orange", "4 · behaviour", "verbs → methods: <code>park()</code>, <code>unpark()</code>, <code>fee()</code>", 3, "flex:1"),
       box("gray", "5 · patterns", "Strategy for pricing · Factory for vehicles · Singleton only if asked", 4, "flex:1"),
       box("red", "6 · edge cases", "lot full · lost ticket · concurrency on spots", 5, "flex:1"), style="margin-top:22px"),
 "steps": [
  "In a low level design interview, don't start coding. First, clarify requirements and scope. For a parking lot: how many levels, which vehicle types, how is pricing done?",
  "Then find the entities. Nouns in the requirements become classes: parking lot, level, spot, vehicle, ticket.",
  "Decide relationships. A lot has levels, a level has spots. A car is a vehicle. Use enums for fixed types like spot size.",
  "Then behaviour. Verbs become methods: park, unpark, calculate the fee.",
  "Apply patterns where they fit. A pricing strategy, so hourly and flat pricing can be swapped. A factory for vehicles. Don't force patterns in.",
  "And finish with edge cases: the lot is full, a ticket is lost, two cars race for the same spot. Talking about those shows real design maturity.",
 ]},

quiz([
  ("Invoice saves, prints and emails itself. Which principle?", "<b style=\"display:inline\">S</b>: single responsibility", "blue",
   "Quiz time. An invoice class saves itself, renders a PDF, and sends email. Which principle does it break?",
   "Single responsibility. It has several reasons to change."),
  ("Override throws UnsupportedOperationException?", "breaks <b style=\"display:inline\">L</b>iskov", "red",
   "A subclass overrides a method just to throw unsupported operation exception. Which principle is broken?",
   "Liskov substitution. The subclass can't be used everywhere its parent can."),
  ("Spring constructor injection implements?", "<b style=\"display:inline\">D</b>ependency Inversion", "purple",
   "Which SOLID principle does Spring's constructor injection support?",
   "Dependency inversion. Classes depend on interfaces, and implementations are passed in."),
]),

recap(["High cohesion, low coupling",
       "S: one reason to change",
       "O: extend by adding code, not editing it",
       "L: subclasses keep the parent's promises",
       "I: small interfaces · D: depend on abstractions",
       "LLD: clarify → entities → relations → behaviour → edge cases"],
  "Let's recap. Aim for high cohesion and low coupling. Single responsibility: one reason to change. Open closed: extend by adding code, not editing it. Liskov: subclasses must keep their parent's promises. Interface segregation: small, focused interfaces. Dependency inversion: depend on abstractions, which is what Spring's injection gives you. Prefer composition over inheritance. And in LLD interviews, clarify, find entities and relationships, add behaviour, and finish with edge cases. Now practise with the examples in your notes!"),
]
