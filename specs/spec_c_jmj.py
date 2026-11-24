from conc import *

TAG = "Java · JUnit, Maven, Gradle and JDBC"
TRACK = "Java Fullstack · Java"
FILE = "Java JUnit Maven Gradle and JDBC.mp4"

SLIDES = [
title_slide(0, "JUnit, Build Tools & JDBC", "Test it, build it, talk to a database: the three tools around every Java project",
  "Welcome. Today's concepts: unit testing with JUnit, build tools, and JDBC.",
  "Real Java code doesn't live alone. It's tested, built with a tool that fetches libraries, and usually talks to a database. By the end you'll know how to write JUnit five tests, mock dependencies with Mockito, how Maven and Gradle manage dependencies and builds, and how JDBC runs SQL safely, with prepared statements, transactions and connection pools.",
  pill="JAVA · CONCEPT"),

{"html": H("A JUnit 5 ", "test") + row(
   code("""§0 class CalculatorTest {
§0   Calculator calc = new Calculator();
§0   @Test
§0   void addsTwoNumbers() {
§1     assertEquals(5, calc.add(2, 3));       // expected, actual
§1     assertTrue(calc.isEven(4));
§2     assertThrows(ArithmeticException.class,
§2         () -> calc.divide(1, 0));
§0   }
§0 }""", 25, style="flex:1"),
   col(box("blue", "@Test", "a method JUnit finds and runs · no main needed", 0),
       box("green", "assertions", "<code>assertEquals</code> · <code>assertTrue</code> · <code>assertNull</code> · first failure stops the test", 1),
       box("orange", "exceptions", "<code>assertThrows</code> takes a lambda and returns the exception", 2), gap=14, style="width:600px"), top=True) +
   note("Arrange → Act → Assert · one behaviour per test · a name that says what it checks", 3),
 "steps": [
  "A unit test checks one small piece of code in isolation. In JUnit five, any method marked with the test annotation is found and run by the framework. There's no main method.",
  "Assertions state what should be true. Assert equals takes the expected value first, then the actual one. The first failing assertion stops that test and reports it.",
  "To check that code throws, assert throws takes the exception type and a lambda. It returns the exception, so you can check its message too.",
  "A good test has three parts: arrange, act, assert. Test one behaviour, and give it a name that says what it checks.",
 ]},

{"html": H("Lifecycle and parameterised ", "tests") + row(
   code("""§0 @BeforeAll static void startOnce() { … }   // once per class
§0 @BeforeEach void setUp() { list = new ArrayList<>(); }
§0 @AfterEach  void tearDown() { … }
§1 @ParameterizedTest
§1 @CsvSource({ "2, 3, 5", "-1, 1, 0", "0, 0, 0" })
§1 void adds(int a, int b, int sum) {
§1   assertEquals(sum, calc.add(a, b));
§1 }
§2 @DisplayName("rejects a negative amount")
§2 @Disabled("flaky, see ticket 42")""", 24, style="flex:1"),
   col(box("blue", "fresh each time", "a new test-class instance per test · <code>@BeforeEach</code> resets state", 0),
       box("green", "one test, many inputs", "<code>@ValueSource</code> · <code>@CsvSource</code> · <code>@MethodSource</code>", 1),
       box("gray", "readability", "<code>@DisplayName</code> · <code>@Disabled</code> · <code>@Nested</code>", 2), gap=14, style="width:560px"), top=True),
 "steps": [
  "JUnit creates a new instance of the test class for every test, so tests can't leak state into each other. Before each and after each run around every test. Before all and after all run once, for expensive setup like starting a server.",
  "A parameterised test runs the same check with many inputs. CSV source gives each row as arguments. Value source and method source are the other common providers. Three rows, three test runs.",
  "Display name gives a readable title, disabled skips a test with a reason, and nested groups related tests.",
 ]},

{"html": H("Mocking with ", "Mockito") + row(
   code("""§0 @ExtendWith(MockitoExtension.class)
§0 class OrderServiceTest {
§0   @Mock PaymentGateway gateway;          // a fake
§0   @InjectMocks OrderService service;     // gets the fake
§1   @Test void chargesTheCard() {
§1     when(gateway.charge(100)).thenReturn(true);
§1     assertTrue(service.placeOrder(100));
§2     verify(gateway).charge(100);
§2     verify(gateway, never()).refund(anyInt());
§1   }
§0 }""", 24, style="flex:1"),
   col(box("blue", "why mock", "test the service without a real payment API, database or network", 0),
       box("green", "stub", "<code>when(…).thenReturn(…)</code> · <code>thenThrow</code> for failures", 1),
       box("purple", "verify", "was it called? how often? with what?", 2), gap=14, style="width:560px"), top=True) +
   note("Mock what you don't own and what's slow · don't mock the class you're testing", 3),
 "steps": [
  "Most classes depend on others. To test an order service without a real payment provider, replace the gateway with a mock: a fake object that records calls and returns whatever you tell it. Inject mocks puts the fakes into the class under test.",
  "Stubbing says what the mock returns. When charge is called with a hundred, return true. Then throw lets you test the failure path too.",
  "Verify checks the interaction: charge was called with a hundred, and refund was never called.",
  "Mock slow or external things, like networks and databases. Don't mock the class you're testing, or plain values.",
 ]},

{"html": H("Test-driven ", "development") + row(
   box("red", "1 · red", "write a test for behaviour that doesn't exist yet · watch it fail", 0, "flex:1"),
   box("green", "2 · green", "write the <b style=\"display:inline\">simplest</b> code that makes it pass", 1, "flex:1"),
   box("blue", "3 · refactor", "clean up the code, tests still green", 2, "flex:1"), top=True) +
   pts([("Tests become a spec of the behaviour, written before the code", 3),
        ("Small steps: one failing test at a time", 3),
        ("The test pyramid: many unit tests, fewer integration, few end-to-end", 4)], size=30),
 "steps": [
  "Test driven development turns the order around. First, write a test for behaviour that doesn't exist yet, and watch it fail. That proves the test can fail.",
  "Then write the simplest code that makes it pass. Nothing more.",
  "Then refactor: improve names and structure while the tests stay green. Repeat.",
  "The tests become a specification written before the code, and every step is small.",
  "Overall, aim for a pyramid: lots of fast unit tests, fewer integration tests, and a handful of slow end to end tests.",
 ]},

{"html": H("Build tools: Maven and ", "Gradle") + table(["", "Maven", "Gradle"], [
     (["config", "<code>pom.xml</code> · XML, declarative", "<code>build.gradle(.kts)</code> · Groovy / Kotlin code"], 0),
     (["a dependency", "groupId · artifactId · version", "<code>implementation(\"g:a:v\")</code>"], 0),
     (["build", "<code>mvn clean package</code>", "<code>./gradlew build</code>"], 1),
     (["model", "fixed lifecycle of phases", "a graph of tasks · incremental, build cache"], 1),
     (["layout", "<code>src/main/java</code> · <code>src/test/java</code>", "the same"], 2)], size=27) +
   note("Both download libraries from Maven Central, with all their transitive dependencies", 3),
 "steps": [
  "A build tool compiles code, runs tests, packages a jar, and, most importantly, downloads libraries. Maven is configured with an XML file, the pom. Gradle uses a script in Groovy or Kotlin. Both identify a library by group, artifact and version.",
  "Maven runs a fixed lifecycle: clean package compiles, tests and packages. Gradle builds a graph of tasks, and skips work whose inputs didn't change, so large builds are faster.",
  "Both use the same folder layout, main code and test code side by side.",
  "And both pull libraries from Maven Central, including the libraries those libraries need, called transitive dependencies.",
 ]},

{"html": H("Dependency ", "scopes") + col(table(["Maven", "Gradle", "Available"], [
     (["<code>compile</code>", "<code>implementation</code>", "compile + run · the default"], 0),
     (["<code>provided</code>", "<code>compileOnly</code>", "compile only · the server supplies it"], 1),
     (["<code>runtime</code>", "<code>runtimeOnly</code>", "run only · e.g. a JDBC driver"], 1),
     (["<code>test</code>", "<code>testImplementation</code>", "tests only · JUnit, Mockito"], 2)], size=28), style="width:1100px") +
   note("Gradle's <code>api</code> vs <code>implementation</code>: leak a dependency to consumers, or keep it private", 3),
 "steps": [
  "A scope says where a dependency is visible. Compile, or implementation in Gradle, is the default: available when compiling and running.",
  "Provided means you compile against it, but the runtime supplies it. Runtime is the opposite: not needed to compile, only to run, like a database driver you only reach through interfaces.",
  "Test scope keeps JUnit and Mockito out of the shipped application.",
  "Gradle adds one more distinction: api exposes a dependency to projects that use yours, while implementation keeps it private, which makes builds faster.",
 ]},

{"html": H("JDBC: talking to a ", "database") + row(
   code("""§0 String url = "jdbc:postgresql://localhost:5432/shop";
§0 try (Connection con = DriverManager.getConnection(url, user, pw);
§1      PreparedStatement ps = con.prepareStatement(
§1        "SELECT id, name FROM users WHERE age > ?")) {
§1   ps.setInt(1, 18);                       // parameters are 1-based
§2   try (ResultSet rs = ps.executeQuery()) {
§2     while (rs.next())
§2       print(rs.getLong("id") + " " + rs.getString("name"));
§2   }
§0 }""", 23, style="flex:1"),
   col(box("blue", "Connection", "one session with the database · always close it", 0),
       box("green", "PreparedStatement", "SQL with <code>?</code> placeholders · values set separately", 1),
       box("purple", "ResultSet", "a cursor · <code>next()</code> moves to the next row", 2), gap=14, style="width:520px"), top=True) +
   note("executeQuery → rows · executeUpdate → number of rows changed", 3),
 "steps": [
  "JDBC is Java's standard API for SQL databases. A connection is one session with the database, opened from a URL. Use try with resources, so it's always closed.",
  "A prepared statement holds SQL with question mark placeholders. You set the values separately, by position, starting at one.",
  "Execute query returns a result set, a cursor over the rows. Next moves to the following row and returns false at the end. Read columns by name or index.",
  "For inserts, updates and deletes, execute update returns the number of rows changed.",
 ]},

{"html": H("SQL injection and ", "transactions") + row(
   col(box("red", "string concatenation", "<code>\"… WHERE name = '\" + input + \"'\"</code> · input <code>' OR '1'='1</code> → every row", 0),
       box("green", "PreparedStatement", "values are sent as <b style=\"display:inline\">data</b>, never parsed as SQL", 1), gap=14, style="width:640px"),
   code("""§2 con.setAutoCommit(false);
§2 try {
§2   debit.executeUpdate();
§2   credit.executeUpdate();
§2   con.commit();                // both or neither
§2 } catch (SQLException e) {
§2   con.rollback();
§2 }
§3 ps.addBatch(); … ps.executeBatch();""", 24, style="flex:1"), top=True) +
   note("Production: a connection pool (HikariCP) + a DAO class per table", 4),
 "steps": [
  "Never build SQL by gluing in user input. If someone types a quote followed by OR one equals one, the condition becomes always true and returns every row. That's SQL injection.",
  "Prepared statements fix it. The SQL is parsed first, and the values are sent separately as data, so they can never change the query.",
  "By default every statement commits on its own. To move money, turn auto commit off, run the debit and the credit, then commit. If anything fails, roll back, so it's both or neither.",
  "For many inserts, add them to a batch and send them in one round trip.",
  "Opening connections is slow, so real apps borrow them from a pool like Hikari. And they hide the SQL behind a data access object, one class per table.",
 ]},

quiz([
  ("Order of arguments in assertEquals?", "<b style=\"display:inline\">expected</b>, then actual", "blue",
   "Quiz time. In assert equals, which argument comes first?",
   "The expected value, then the actual one."),
  ("Scope for a JDBC driver?", "<b style=\"display:inline\">runtime</b> (runtimeOnly)", "green",
   "Which scope suits a JDBC driver you only use through interfaces?",
   "Runtime. It's needed to run, not to compile."),
  ("How do you prevent SQL injection?", "<b style=\"display:inline\">PreparedStatement</b> with <code>?</code>", "red",
   "How do you prevent SQL injection in JDBC?",
   "Use a prepared statement with placeholders, so input is always data."),
]),

recap(["JUnit 5: @Test · assertEquals(expected, actual)",
       "@BeforeEach · @ParameterizedTest + @CsvSource",
       "Mockito: when…thenReturn · verify",
       "TDD: red → green → refactor",
       "Maven pom / Gradle tasks · scopes",
       "JDBC: PreparedStatement · commit / rollback · pool"],
  "Let's recap. JUnit five finds methods marked test, and assertions check expected against actual. Lifecycle methods reset state, and parameterised tests run one check over many inputs. Mockito replaces dependencies with fakes you stub and verify. Test driven development goes red, green, refactor. Maven and Gradle download dependencies and build, with scopes controlling where each library is visible. And JDBC runs SQL through prepared statements, with transactions and a connection pool. Now practise with the examples in your notes!"),
]
