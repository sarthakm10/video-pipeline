from conc import *

TAG = "Spring · Testing"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Testing.mp4"

SLIDES = [
title_slide(0, "Testing Spring Boot", "Fast unit tests at the bottom, a few real ones at the top",
  "Welcome to testing Spring Boot applications.",
  "Tests let you change code without fear. But not all tests are equal: some run in milliseconds and test one class, others start the whole app with a real database. By the end you'll know the test pyramid, JUnit five and AssertJ, Mockito, Spring's test slices for the web and JPA layers, full integration tests, Testcontainers, and how to keep the suite fast.",
  pill="SPRING · CONCEPT"),

{"html": H("The test ", "pyramid") + row(
   col(box("green", "unit tests · many", "one class, dependencies mocked · milliseconds", 0),
       box("blue", "slice tests · some", "one layer with real Spring: web or JPA · seconds", 1),
       box("purple", "integration tests · few", "the whole app, a real database · slowest, most realistic", 2), gap=18, style="flex:1"),
   box("orange", "why this shape", "fast tests run on every save · slow ones prove the pieces fit · a failing unit test points at the exact class", 3, "width:600px"), top=True),
 "steps": [
  "Think of tests as a pyramid. At the bottom, many unit tests. Each tests one class, with its dependencies replaced by mocks. They run in milliseconds.",
  "In the middle, slice tests. They start just one layer of Spring, like the web layer or the JPA layer, and take a few seconds.",
  "At the top, a few integration tests. They start the whole application, with a real database. Most realistic, and slowest.",
  "Why that shape? Fast tests can run every time you save. The few slow ones prove the pieces work together. And when a unit test fails, it points straight at the broken class.",
 ]},

{"html": H("JUnit 5 and ", "AssertJ") + code("""§0 class PriceCalculatorTest {
§0   PriceCalculator calc = new PriceCalculator();
§0   @Test
§0   void appliesTenPercentDiscount() {
§1     // given · when · then
§1     var total = calc.total(List.of(100, 50), "SAVE10");
§2     assertThat(total).isEqualTo(135);
§2     assertThatThrownBy(() -> calc.total(List.of(), "NOPE"))
§2         .isInstanceOf(InvalidCouponException.class);
§0   }
§3   @ParameterizedTest @CsvSource({"0,0", "100,90"})
§3   void discounts(int in, int out) { … }
§0 }""", 25) ,
 "steps": [
  "A JUnit five test is a method annotated with at test. Here there's no Spring at all, just a plain object. That's the fastest kind of test.",
  "Structure each test as given, when, then. Set up the input, call the code, check the result. And name the test after the behaviour, like applies ten percent discount.",
  "AssertJ makes the checks read like sentences: assert that total is equal to one thirty five. And assert that thrown by checks that the right exception is thrown.",
  "Parameterized tests run the same test with several inputs, for example from a CSV source. One method, many cases.",
 ]},

{"html": H("Mockito: fake the ", "neighbours") + row(
   code("""§0 @ExtendWith(MockitoExtension.class)
§0 class TaskServiceTest {
§0   @Mock TaskRepository repo;
§0   @InjectMocks TaskService service;
§1   @Test void completesTask() {
§1     when(repo.findById(7L)).thenReturn(Optional.of(task));
§1     service.complete(7L);
§2     verify(repo).save(argThat(t -> t.isDone()));
§1   }
§0 }""", 25, style="flex:1"),
   col(box("blue", "@Mock", "a fake that returns nothing until told otherwise", 0),
       box("green", "when … thenReturn", "<b style=\"display:inline\">stub</b>: decide what a call returns", 1),
       box("purple", "verify", "check a call <b style=\"display:inline\">happened</b>, with the right arguments", 2),
       box("red", "don't mock everything", "mock what you don't own the behaviour of · not value objects", 3), gap=14, style="width:560px"), top=True),
 "steps": [
  "To unit test a service, replace its dependencies with mocks. At mock creates a fake repository, and at inject mocks builds the service with that fake injected. Still no Spring.",
  "Stub the calls the test needs. When find by id seven is called, return this task. Then call the method under test.",
  "Afterwards, verify checks that an interaction happened. Here, that save was called with a task that is now done.",
  "But don't mock everything. Mock boundaries, like repositories and external clients. Simple value objects and records should just be real. Too many mocks make tests that pass while the real code is broken.",
 ]},

{"html": H("Web slice: ", "@WebMvcTest") + row(
   code("""§0 @WebMvcTest(TaskController.class)
§0 class TaskControllerTest {
§0   @Autowired MockMvc mvc;
§0   @MockitoBean TaskService service;
§1   @Test void rejectsBlankTitle() throws Exception {
§1     mvc.perform(post("/api/tasks")
§1           .contentType(APPLICATION_JSON)
§1           .content("{\\"title\\": \\"\\"}"))
§2        .andExpect(status().isBadRequest())
§2        .andExpect(jsonPath("$.errors.title").exists());
§1   }
§0 }""", 23, style="flex:1"),
   col(box("blue", "loads only", "controllers, advice, JSON, validation, security filters", 0),
       box("purple", "@MockitoBean", "puts a mock into the Spring context (was <code>@MockBean</code>)", 0),
       box("green", "MockMvc", "real HTTP handling, no real server", 1),
       box("orange", "tests", "URLs, status codes, JSON shape, validation", 2), gap=14, style="width:560px"), top=True),
 "steps": [
  "Slice tests start only part of Spring. At web MVC test loads the web layer: controllers, controller advice, JSON conversion, validation, and security filters. No services, no repositories, no database. The service is replaced with at mockito bean, which puts a mock into the Spring context. In older versions it was called at mock bean.",
  "Mock MVC sends requests through the real Spring MVC machinery, without starting a server. Here we post a task with a blank title.",
  "And check the answer: status four hundred, and a JSON body with an error for the title. This is where you test URLs, status codes, the JSON shape, and validation.",
 ]},

{"html": H("JPA slice: ", "@DataJpaTest") + row(
   col(box("blue", "loads only", "entities, repositories, the DataSource, Flyway", 0),
       box("green", "rolled back", "each test runs in a transaction that is <b style=\"display:inline\">rolled back</b> → no cleanup", 1),
       box("orange", "real database", "<code>@AutoConfigureTestDatabase(replace = NONE)</code> + Testcontainers, not H2", 2), gap=16, style="flex:1"),
   code("""§0 @DataJpaTest
§0 class TaskRepositoryTest {
§0   @Autowired TaskRepository repo;
§1   @Test void findsOpenTasks() {
§1     repo.save(new Task("a", false));
§1     repo.save(new Task("b", true));
§1     assertThat(repo.findByDoneFalse())
§1         .extracting(Task::getTitle)
§1         .containsExactly("a");
§1   }
§0 }""", 24, style="width:720px"), top=True),
 "steps": [
  "At data JPA test is the slice for the data layer. It loads entities, repositories, the data source, and Flyway migrations. No controllers or services.",
  "Each test runs inside a transaction that's rolled back at the end. So tests don't need cleanup, and don't affect each other. Here we save two tasks, and check that the query returns only the open one.",
  "One warning. By default this slice swaps in an embedded database like H2. But H2 isn't Postgres. Queries that pass on H2 can fail in production. Prefer the real database, which is what Testcontainers is for.",
 ]},

{"html": H("Full app + ", "Testcontainers") + row(
   code("""§0 @SpringBootTest(webEnvironment = RANDOM_PORT)
§1 @Testcontainers
§0 class TaskApiIT {
§1   @Container @ServiceConnection
§1   static PostgreSQLContainer<?> db =
§1       new PostgreSQLContainer<>("postgres:17");
§2   @Autowired TestRestTemplate http;
§2   @Test void createThenFetch() { … }
§0 }""", 24, style="flex:1"),
   col(box("blue", "@SpringBootTest", "the <b style=\"display:inline\">whole</b> application context · a real port", 0),
       box("purple", "Testcontainers", "starts a real Postgres in Docker for the tests, then removes it", 1),
       box("green", "@ServiceConnection", "Boot wires the URL, user and password for you", 1),
       box("orange", "use for", "end-to-end flows: HTTP → service → real database", 2), gap=14, style="width:560px"), top=True),
 "steps": [
  "At the top of the pyramid, at spring boot test starts the whole application, here on a random port, so tests can make real HTTP calls.",
  "And Testcontainers gives it a real database. It starts a Postgres container in Docker before the tests, and throws it away afterwards. At service connection tells Boot to point the data source at that container, with no URLs to configure.",
  "These tests cover whole flows: an HTTP request, through the service, into a real database, and back. Keep them few, because each one is slow.",
 ]},

{"html": H("Keeping the suite ", "fast") + pts([
     ("Spring <b>caches</b> the context between tests with the same configuration", 0),
     ("each different <code>@MockitoBean</code> set or property → a <b>new</b> context", 1),
     ("<code>@DirtiesContext</code> throws the cache away: avoid it", 1),
     ("share one Testcontainers container across test classes", 2),
     ("<code>mvn test</code> runs *Test · <code>mvn verify</code> also runs *IT (Failsafe)", 3)], size=33),
 "steps": [
  "Starting Spring is the slow part, so Spring caches the application context. Test classes with exactly the same configuration reuse it.",
  "But every different combination of mock beans or properties creates a new context, and so does dirties context. Keep test configurations consistent, and avoid dirties context unless you really need it.",
  "Containers are slow to start too. Declare them once, in a shared base class or configuration, so all test classes reuse the same database.",
  "And with Maven, mvn test runs the fast unit tests, named with Test at the end. mvn verify also runs the integration tests, named with IT, through the failsafe plugin.",
 ]},

quiz([
  ("Testing a controller's status codes and JSON?", "<b style=\"display:inline\">@WebMvcTest</b> + MockMvc", "blue",
   "Quiz time. You want to test a controller's status codes and JSON. Which test type?",
   "A web MVC test with mock MVC, and the service mocked."),
  ("Why not H2 for repository tests?", "it isn't your <b style=\"display:inline\">real</b> database", "orange",
   "Why avoid H2 for repository tests, if production runs Postgres?",
   "Because H2 behaves differently. Use Testcontainers to test against real Postgres."),
  ("stub vs verify?", "stub = <b style=\"display:inline\">what it returns</b> · verify = <b style=\"display:inline\">it was called</b>", "purple",
   "In Mockito, what's the difference between stubbing and verifying?",
   "Stubbing decides what a call returns. Verifying checks that a call happened."),
]),

recap(["Pyramid: many unit · some slices · few integration",
       "JUnit 5 + AssertJ: given, when, then",
       "Mockito: @Mock, when…thenReturn, verify",
       "@WebMvcTest: web layer only, service mocked",
       "@DataJpaTest: repositories, rolled back",
       "@SpringBootTest + Testcontainers: real Postgres"],
  "Let's recap. Build a pyramid: many unit tests, some slice tests, and a few integration tests. Write tests as given, when, then, with AssertJ. Mockito fakes dependencies: stub what they return, and verify what was called. Web MVC test covers the web layer with the service mocked. Data JPA test covers repositories, and rolls back after each test. And spring boot test with Testcontainers runs the whole app against a real Postgres. Now practise with the examples in your notes!"),
]
