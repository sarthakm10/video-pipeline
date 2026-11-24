from lib import *

TAG = "Frontend 23 · Testing Frontend Code"
FILE = "Frontend 23 Testing Frontend Code.mp4"

SLIDES = [
title_slide(23, "Testing Frontend Code", "Test what the user sees and does, not how the code is written",
  "Welcome to module twenty three: testing frontend code.",
  "You tested Spring Boot with JUnit, Mockito, and Testcontainers. Frontend testing has the same ideas, with different tools. Vitest instead of JUnit. React Testing Library for components. MSW instead of mocking your HTTP client. And Playwright for the full browser. The guiding rule: test what the user sees and does, not how the code is written."),

{"html": H("The testing ", "pyramid") + table(["Level", "Tests", "Speed", "Confidence"], [
   (["<b>End-to-end</b> · Playwright", "the real app, a real browser", "seconds", "highest"], 0),
   (["<b>Component</b> · RTL", "render, click, type, check the screen", "fast", "good"], 0),
   (["<b>Unit</b> · Vitest", "functions, reducers, hooks", "ms", "narrow"], 0),
   (["<b>Static</b>", "TypeScript, ESLint", "free", "a whole class of bugs"], 1)], size=29) +
   row(box("green", "most tests here", "component / integration level", 1, "flex:1"),
       box("blue", "test first", "critical flows · tricky logic · anything that broke before", 2, "flex:1"), style="margin-top:26px"),
 "steps": [
  "Frontend tests come in three levels. Unit tests check a function, a reducer, or a hook, in milliseconds. Component tests use a component the way a user would. Render it, click, type, and check the screen. And end-to-end tests drive the real app in a real browser. Slowest, but the highest confidence.",
  "Many frontend teams use the testing trophy. Most tests at the component level, because that's where you get the most confidence per test. And static checks at the base. TypeScript and ESLint catch a whole class of bugs for free.",
  "What to test first? Critical user flows, like login and creating a task. Tricky logic, like dates and permissions. And anything that broke before. Write the test that would have caught it.",
 ]},

{"html": H("", "Vitest") + row(code("""§0 import { describe, it, expect } from "vitest";
§0 describe("progress", () => {
§0   it("is 0 for no tasks", () => {
§0     expect(progress([])).toBe(0);
§0   });
§0   it("rounds to a whole percentage", () => {
§0     expect(progress([{ done: true }, { done: false },
§0       { done: false }])).toBe(33);
§0   });
§0 });""", 27, style="flex:1"),
   col(table(["Vitest", "JUnit 5"], [
     (["<code>describe</code>", "a test class"], 1),
     (["<code>it</code> / <code>test</code>", "<code>@Test</code>"], 1),
     (["<code>expect(x).toBe(y)</code>", "<code>assertEquals</code>"], 1),
     (["<code>it.each</code>", "<code>@ParameterizedTest</code>"], 1)], size=26),
       box("purple", "mocks", "<code>vi.fn()</code> · <code>vi.mock(\"./api\")</code> · <code>vi.useFakeTimers()</code>", 2), style="width:500px;flex-shrink:0"), top=True),
 "steps": [
  "Vitest is Vite's test runner, with a Jest compatible API. Npm test runs in watch mode, re-running affected tests on save. Describe groups tests, it is a test, and expect checks a result.",
  "It's the same mental model as JUnit five. Describe is like a test class. It is at test. Expect to be is assert equals. And it dot each is a parameterized test. Remember, to be checks identity, and to equal checks deep equality, for objects and arrays.",
  "For mocks, v i dot f n makes a spy function, v i dot mock replaces a module, and fake timers control set timeout. Perfect for testing a debounce.",
 ]},

{"html": H("React Testing ", "Library") + code("""it("adds a task and clears the input", async () => {
  const user = userEvent.setup();
  const onAdd = vi.fn();
§0   render(<AddTaskForm onAdd={onAdd} />);
§1   const input = screen.getByRole("textbox", { name: /new task/i });
§2   await user.type(input, "Write tests");
§2   await user.click(screen.getByRole("button", { name: /add/i }));
§2   expect(onAdd).toHaveBeenCalledWith("Write tests");
§2   expect(input).toHaveValue("");
});""", 28) + note("Query priority: <u>getByRole</u> → getByLabelText / getByText → getByTestId (last resort)", 1),
 "steps": [
  "React Testing Library renders a component into a simulated DOM, called j s dom.",
  "Then you find things the way a user would. By role, label, and text. Get by role with a name is the first choice. It's what assistive technology sees, so it tests accessibility too. A test I D is the last resort.",
  "User event types and clicks like a real user. Then check what happened. On add was called with the text, and the input was cleared.",
 ]},

{"html": H("getBy, queryBy, ", "findBy") + table(["Prefix", "Nothing matches", "Use for"], [
   (["<code>getBy…</code>", "throws", "things that must be there now"], 0),
   (["<code>queryBy…</code>", "returns null", "asserting something is <b>not</b> there"], 0),
   (["<code>findBy…</code>", "waits, then throws", "things that appear after loading"], 0)], size=32) +
   row(box("red", "✗ implementation", "state variables · which hook ran", 1, "flex:1"),
       box("green", "✓ behaviour", "refactor without changing the UI → tests still pass", 1, "flex:1"), style="margin-top:30px"),
 "steps": [
  "Three query prefixes. Get by throws if nothing matches, for things that must be there now. Query by returns null, so you can assert something is not there. And find by waits, asynchronously. Use it for things that appear after loading.",
  "And test behaviour, not implementation. Don't check state variables, or which hook was called. If you can refactor a component without changing what the user sees, its tests shouldn't break.",
 ]},

{"html": H("Mocking the API with ", "MSW") + code("""§0 export const server = setupServer(
§0   http.get("*/api/tasks", () =>
§0     HttpResponse.json([{ id: 1, title: "Learn MSW", done: false }])),
§0 );
§0 beforeAll(() => server.listen()); afterEach(() => server.resetHandlers());

§1 render(<TaskList />, { wrapper: Providers });
§1 expect(await screen.findByText("Learn MSW")).toBeInTheDocument();

§2 server.use(http.get("*/api/tasks", () => new HttpResponse(null, { status: 500 })));
§2 expect(await screen.findByRole("alert")).toHaveTextContent(/couldn't load/i);""", 26),
 "steps": [
  "Mock service worker intercepts requests at the network level. Your components and API client run their real code. Only the server is fake. It's like WireMock for the frontend. Define handlers for each endpoint, and start the server before the tests.",
  "Now render the task list, and find the task that came from the fake API.",
  "To test errors, override a handler for one test. Return a five hundred, and check the alert appears. And the same handlers can run in the browser during development, so you can build the UI before the Spring endpoint even exists.",
 ]},

{"html": H("End-to-end with ", "Playwright") + row(code("""test("log in and add a task", async ({ page }) => {
§0   await page.goto("/login");
§0   await page.getByLabel("Email").fill("asha@example.com");
§0   await page.getByLabel("Password").fill("…");
§0   await page.getByRole("button", { name: "Log in" }).click();
§0   await expect(page).toHaveURL(/\\/tasks/);
§0   await page.getByRole("textbox", { name: "New task" }).fill("Ship it");
§0   await page.getByRole("button", { name: "Add" }).click();
§0   await expect(page.getByText("Ship it")).toBeVisible();
});""", 28, style="flex:1")) +
   row(box("blue", "auto-waits", "Chromium, Firefox, WebKit · <code>codegen</code> records clicks", 1, "flex:1"),
       box("orange", "slow, can be flaky", "keep for <b style=\"display:inline\">critical journeys</b> · run in CI", 2, "flex:1"), style="margin-top:22px"),
 "steps": [
  "End-to-end tests drive a real browser, through your real app. This Playwright test logs in, checks it landed on the tasks page, adds a task, and checks it's visible.",
  "Playwright auto-waits for elements to be ready, runs in Chromium, Firefox, and WebKit, and its locators look like Testing Library's queries. Codegen even records your clicks into a test. Cypress is the other popular choice.",
  "But E2E tests are slow, and can be flaky. So keep them for the critical journeys. Sign up, log in, the core create and edit flow, and checkout. And run them in CI, against a test environment.",
 ]},

quiz([
  ("<code>toBe</code> vs <code>toEqual</code>?", "identity · deep equality", "blue",
   "Quiz time. To be versus to equal?",
   "To be checks identity. To equal checks deep equality."),
  ("Which query to prefer?", "<code>getByRole</code> with an accessible name", "green",
   "Which Testing Library query should you prefer?",
   "Get by role, with an accessible name."),
  ("What does MSW mock?", "the <b style=\"display:inline\">network</b> · real client code runs", "purple",
   "And what does MSW mock?",
   "The network. Your real client code runs, against a fake server."),
]),

recap(["Unit · component · end-to-end · static checks",
       "Most tests at the component level",
       "Vitest: describe, it, expect · vi.fn, fake timers",
       "RTL: getByRole first · test behaviour",
       "getBy · queryBy · findBy",
       "MSW fakes the network · Playwright for critical journeys"],
  "Let's recap. Frontend tests are unit, component, and end-to-end, on top of static checks. Put most of them at the component level. Vitest gives you describe, it, and expect, plus mocks and fake timers. With Testing Library, prefer get by role, and test behaviour, not implementation. Get by throws, query by returns null, and find by waits. MSW fakes the network, and Playwright covers the critical journeys. Next time: web performance and accessibility!"),
]
