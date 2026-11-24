from conc import *

TAG = "Spring · REST Controllers, Part 1"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring REST Controllers (Part 1).mp4"

SLIDES = [
title_slide(0, "REST Controllers", "Part 1: how a request reaches your method, and how your answer becomes JSON",
  "Welcome to REST controllers, part one.",
  "A REST controller is where HTTP meets your Java code. A request comes in, Spring picks a method, fills its parameters, calls it, and turns the return value into JSON. By the end you'll know the journey of a request through the dispatcher servlet, the mapping annotations, how to read every part of a request, how to choose status codes, why DTOs matter, and how to do CRUD properly.",
  pill="SPRING · CONCEPT · PART 1"),

{"html": H("The journey of a ", "request") + row(
   box("gray", "1 · Tomcat", "receives <code>GET /api/tasks/7</code>", 0, "flex:1"),
   box("blue", "2 · DispatcherServlet", "the <b style=\"display:inline\">front controller</b>: every request goes through it", 1, "flex:1"),
   box("purple", "3 · HandlerMapping", "which method matches this URL and verb?", 2, "flex:1"), top=True) +
   row(box("green", "4 · HandlerAdapter", "fills the parameters, calls your method", 3, "flex:1"),
       box("orange", "5 · message converter", "return value → JSON (Jackson)", 4, "flex:1"),
       box("gray", "6 · response", "status + headers + body", 4, "flex:1"), style="margin-top:22px"),
 "steps": [
  "Let's follow one request. The embedded Tomcat receives GET slash api slash tasks slash seven.",
  "It hands it to the dispatcher servlet. That's Spring MVC's front controller. Every request passes through this one servlet, which then delegates.",
  "First it asks the handler mapping: which controller method is mapped to this path and this HTTP method?",
  "Then a handler adapter prepares that method's arguments, from the path, the query string, headers, or the body, and calls it.",
  "Your method returns an object. A message converter, Jackson for JSON, turns it into the response body, and the status and headers go back to the client. You write only the middle part.",
 ]},

{"html": H("@RestController and the ", "mappings") + code("""§0 @RestController                        // @Controller + @ResponseBody
§0 @RequestMapping("/api/tasks")            // prefix for every method
§0 public class TaskController {
§1   @GetMapping            List<TaskResponse> all()   { … }
§1   @GetMapping("/{id}")   TaskResponse one(...)      { … }
§1   @PostMapping           ResponseEntity<…> create(...) { … }
§1   @PutMapping("/{id}")   …    @PatchMapping("/{id}") …
§1   @DeleteMapping("/{id}") …
§0 }""", 28) + row(
   box("blue", "@Controller", "returns a <b style=\"display:inline\">view name</b> (an HTML template)", 2, "flex:1"),
   box("green", "@RestController", "returns <b style=\"display:inline\">data</b>, written straight into the body", 2, "flex:1"), style="margin-top:22px"),
 "steps": [
  "A REST controller is a class annotated with at rest controller. Request mapping on the class sets a common prefix, here slash api slash tasks.",
  "Each method gets a mapping for one HTTP verb: get mapping, post mapping, put, patch and delete. Combined with the class prefix, that's the full route.",
  "Why rest controller and not controller? A plain controller's return value is treated as a view name, the name of an HTML template to render. Rest controller adds response body to every method, so the return value is the data itself, converted to JSON.",
 ]},

{"html": H("Reading the ", "request") + table(["Part of the request", "Annotation", "Example"], [
     (["path segment", "<code>@PathVariable</code>", "<code>/api/tasks/<b>7</b></code>"], 0),
     (["query parameter", "<code>@RequestParam</code>", "<code>?<b>done=true</b>&amp;page=0</code>"], 1),
     (["header", "<code>@RequestHeader</code>", "<code>X-Request-Id: abc</code>"], 2),
     (["JSON body", "<code>@RequestBody</code>", "<code>{\"title\": \"Write notes\"}</code>"], 3)], size=29) +
   code("""§4 @GetMapping("/{id}")
§4 TaskResponse one(@PathVariable long id,
§4                  @RequestParam(defaultValue = "false") boolean withHistory) { … }""", 26, style="margin-top:20px"),
 "steps": [
  "A request has four places to put data, and each has an annotation. Path variable reads a segment of the URL, like the seven in tasks slash seven. Use it to identify a resource.",
  "Request param reads the query string, after the question mark. Use it for filters, sorting and paging. It's required by default, so give a default value or mark it optional.",
  "Request header reads a header, like a request id or a language.",
  "And request body reads the JSON body and converts it into an object, with Jackson. That's how POST and PUT receive data.",
  "Spring converts types for you. The path text seven becomes a long, and the text false becomes a boolean. A bad value gives a four hundred, not a crash.",
 ]},

{"html": H("Writing the ", "response") + col(
   code("""§0 @PostMapping
§0 ResponseEntity<TaskResponse> create(@RequestBody CreateTask req) {
§0   TaskResponse saved = service.create(req);
§1   return ResponseEntity
§1       .created(URI.create("/api/tasks/" + saved.id()))   // 201 + Location
§1       .body(saved);
§0 }""", 25),
   table(["Code", "When"], [
     (["<b>200</b> OK", "GET · PUT · PATCH success"], 2),
     (["<b>201</b> Created", "POST made something · + <code>Location</code>"], 2),
     (["<b>204</b> No Content", "DELETE success, empty body"], 2),
     (["<b>400</b> / <b>404</b>", "bad input / not found"], 3),
     (["<b>409</b> Conflict", "duplicate, or a version clash"], 3)], size=25), gap=10),
 "steps": [
  "Returning an object gives status two hundred. To control the status and headers, return a response entity.",
  "Creating something should return two oh one, created, with a location header pointing at the new resource. Response entity dot created does both.",
  "The common codes: two hundred for a successful read or update. Two oh one when POST creates something. Two oh four, no content, for a successful delete.",
  "Four hundred when the input is bad, four oh four when the resource doesn't exist, and four oh nine for a conflict, like a duplicate. Choosing the right code is part of a good API. Clients and monitoring rely on it.",
 ]},

{"html": H("DTOs: don't expose your ", "entities") + row(
   col(box("red", "returning the entity", "leaks fields (password hash, internal ids) · ties the API to the DB · lazy-loading errors · endless JSON loops", 0),
       box("green", "a DTO per purpose", "<code>CreateTaskRequest</code> · <code>UpdateTaskRequest</code> · <code>TaskResponse</code>", 1), gap=18, style="flex:1"),
   col(code("""§2 public record TaskResponse(
§2     long id, String title,
§2     boolean done) {}
§3 public record PatchTask(
§3     String title,
§3     Boolean done) {} // null = keep""", 24),
       box("blue", "records", "immutable, short, Jackson-friendly", 2), gap=14, style="width:600px"), top=True),
 "steps": [
  "A big design rule: don't return your database entities from controllers. They can leak fields you never meant to share, like a password hash. They tie your public API to your table layout. And with JPA they can trigger lazy loading errors, or loop forever between two related objects.",
  "Instead, use DTOs, data transfer objects, shaped for each purpose. One for creating, one for updating, one for the response.",
  "Java records are perfect for this. One line, immutable, and Jackson reads and writes them directly.",
  "One detail in the patch DTO: done is a capital B Boolean, not a lowercase boolean. A patch needs three states: true, false, and null, meaning don't change this field.",
 ]},

{"html": H("JSON with ", "Jackson") + row(
   col(box("blue", "serialization", "your object → JSON (response)", 0),
       box("green", "deserialization", "JSON → your object (<code>@RequestBody</code>)", 0),
       box("purple", "Boot 4 uses Jackson 3", "package <code>tools.jackson</code> · configured for you", 1), gap=16, style="flex:1"),
   col(code("""§2 @JsonProperty("task_title") String title
§2 @JsonIgnore String internalNote
§2 @JsonFormat(pattern = "yyyy-MM-dd")
§2 LocalDate due""", 24),
       box("orange", "content negotiation", "the <code>Accept</code> header picks the format: JSON, XML… · none fits → <b style=\"display:inline\">406</b>", 3), gap=16, style="width:660px"), top=True),
 "steps": [
  "Jackson does the JSON conversion both ways. Serialization turns your response object into JSON. Deserialization turns the request body into your object.",
  "Spring Boot four uses Jackson three, which moved to a new package name, tools dot jackson. Older tutorials use com dot fasterxml. Boot configures it for you, so you rarely touch it directly.",
  "A few annotations adjust the output. Json property renames a field, json ignore hides one, and json format controls how dates are written.",
  "And content negotiation: the client's accept header says which format it wants. If the server can't produce any of them, the answer is four oh six, not acceptable.",
 ]},

{"html": H("CRUD done ", "right") + table(["Action", "Request", "Success", "Idempotent?"], [
     (["create", "<code>POST /api/tasks</code>", "201 + Location", "no"], 0),
     (["read one / all", "<code>GET /api/tasks/7</code> · <code>GET /api/tasks</code>", "200", "yes"], 0),
     (["replace", "<code>PUT /api/tasks/7</code> (full object)", "200", "yes"], 1),
     (["partial update", "<code>PATCH /api/tasks/7</code> (only sent fields)", "200", "not necessarily"], 1),
     (["delete", "<code>DELETE /api/tasks/7</code>", "204", "yes"], 2)], size=27) +
   row(box("blue", "idempotent", "sending it twice = sending it once", 3, "flex:1"),
       box("orange", "PUT vs PATCH", "PUT: missing fields become null · PATCH: missing fields <b style=\"display:inline\">stay</b>", 3, "flex:1"), style="margin-top:22px"),
 "steps": [
  "Put together, here's CRUD done properly. POST to the collection creates, and returns two oh one with a location. GET reads one item or the list, and returns two hundred.",
  "PUT replaces the whole resource with what you send. PATCH changes only the fields you send.",
  "And DELETE returns two oh four, with no body.",
  "Two interview favourites. Idempotent means sending the same request twice has the same effect as sending it once. GET, PUT and DELETE are idempotent. POST isn't, because two POSTs create two tasks. And PUT versus PATCH: with PUT, any field you leave out becomes null. With PATCH, fields you leave out stay as they were.",
 ]},

quiz([
  ("@Controller vs @RestController?", "RestController returns <b style=\"display:inline\">data</b>, not a view name", "blue",
   "Quiz time. What's the difference between controller and rest controller?",
   "Rest controller adds response body, so return values are written as data, like JSON, instead of being treated as view names."),
  ("POST created a task. Which status?", "<b style=\"display:inline\">201</b> Created + Location header", "green",
   "A POST successfully created a task. Which status code should you return?",
   "Two oh one, created, with a location header pointing to the new task."),
  ("Filter tasks by done=true: path or query?", "<b style=\"display:inline\">@RequestParam</b> (query)", "purple",
   "You want to filter tasks by done equals true. Path variable or request param?",
   "Request param. Path variables identify a resource, query parameters filter or sort."),
]),

recap(["Every request → DispatcherServlet → your method",
       "@RestController = @Controller + @ResponseBody",
       "@PathVariable identifies · @RequestParam filters · @RequestBody reads JSON",
       "ResponseEntity: 201 + Location · 204 for DELETE",
       "DTOs (records), never entities, in the API",
       "PUT replaces · PATCH changes only sent fields"],
  "Let's recap part one. Every request goes through the dispatcher servlet, which finds your method, fills its parameters, and converts the result. Rest controller means the return value is data. Path variables identify a resource, request params filter, and request body reads JSON. Use response entity for the right status: two oh one with a location for creates, two oh four for deletes. Expose DTOs, never entities. And PUT replaces, while PATCH changes only what you send. In part two: uploads, versioning, filters and interceptors, and the layered architecture!"),
]
