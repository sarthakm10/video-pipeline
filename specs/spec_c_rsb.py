from conc import *

TAG = "Spring · REST Controllers, Part 2"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring REST Controllers (Part 2).mp4"

SLIDES = [
title_slide(0, "REST Controllers", "Part 2: uploads, versioning, filters and interceptors, and the layered architecture",
  "Welcome to REST controllers, part two.",
  "In part one, a request reached your method and came back as JSON. Real APIs need more. Accepting files. Changing the API without breaking old clients. Running code around every request, for logging or timing. And organising the code into layers that each have one job. By the end you'll know multipart uploads, Spring's API versioning, filters versus interceptors, custom annotations, HATEOAS, and the layered architecture.",
  pill="SPRING · CONCEPT · PART 2"),

{"html": H("File ", "uploads") + row(
   code("""§0 @PostMapping(path = "/{id}/attachments",
§0               consumes = MediaType.MULTIPART_FORM_DATA_VALUE)
§0 AttachmentInfo upload(@PathVariable long id,
§0                       @RequestPart("file") MultipartFile file)
§0     throws IOException {
§1   String name = file.getOriginalFilename();
§1   long size = file.getSize();
§1   storage.save(id, file.getInputStream());
§0 }""", 24, style="flex:1"),
   col(box("blue", "multipart/form-data", "the body is split into parts: files + fields", 0),
       box("green", "MultipartFile", "name · size · content type · <code>getInputStream()</code>", 1),
       box("orange", "limits", "<code>spring.servlet.multipart.max-file-size</code> (default 1MB) · over it → error", 2),
       box("red", "never trust it", "check type and size · never use the client's filename as a path", 3), gap=14, style="width:560px"), top=True),
 "steps": [
  "Files arrive as multipart form data. The body is split into parts, which can be files or ordinary form fields. Read a file part with request part, as a multipart file.",
  "A multipart file gives you the original name, the size, the content type, and an input stream to read or store it.",
  "Spring Boot limits upload sizes, one megabyte per file by default. Change it with the max file size property. Larger uploads are rejected before your code runs.",
  "And treat uploads as hostile. Check the type and size yourself, and never use the client's file name as a path on disk, or someone could write outside your folder.",
 ]},

{"html": H("API ", "versioning") + row(
   code("""§0 # application.yml
§0 spring.mvc.apiversion:
§0   use.header: API-Version
§0   default: "1"
§1 @GetMapping(path = "/{id}", version = "1")
§1 TaskV1 oneV1(@PathVariable long id) { … }
§1 @GetMapping(path = "/{id}", version = "2")
§1 TaskV2 oneV2(@PathVariable long id) { … }""", 25, style="flex:1"),
   col(box("blue", "why", "a breaking change must not break <b style=\"display:inline\">old</b> clients", 0),
       box("green", "Spring 7 · Boot 4", "first-class versioning: header, path, query or media type", 1),
       box("orange", "unknown version", "<code>API-Version: 9</code> → 400 · no header → the default", 2), gap=16, style="width:560px"), top=True),
 "steps": [
  "When a response must change in a way old clients can't handle, you version the API. Spring Framework seven, in Boot four, supports this directly. Here it reads the version from a header called API version, with version one as the default.",
  "Then the same path can have one method per version. Old clients keep getting version one, new clients ask for two. The version can also come from the path, a query parameter, or the media type.",
  "An unsupported version gets a four hundred, and a request without the header gets the default. Before Spring seven, people built this by hand, usually with slash v one in the path.",
 ]},

{"html": H("Filters vs ", "interceptors") + row(
   box("gray", "client", "", 0, "width:175px"),
   box("blue", "Filter", "servlet level · sees <b style=\"display:inline\">every</b> request, even static files · security, CORS, logging", 0, "flex:1"),
   box("gray", "Dispatcher­Servlet", "", 0, "width:250px"),
   box("purple", "Interceptor", "Spring MVC level · knows the <b style=\"display:inline\">handler method</b> · <code>preHandle</code> / <code>postHandle</code> / <code>afterCompletion</code>", 1, "flex:1"),
   box("gray", "controller", "", 0, "width:255px"), top=True) +
   table(["Need", "Use"], [
     (["auth, CORS, request IDs, raw body access", "<b>Filter</b> (Spring Security is one)"], 2),
     (["timing per endpoint, reading the method's annotations", "<b>Interceptor</b>"], 2)], size=29) +
   note("Custom <code>@RateLimited</code> → an interceptor reads it from <code>HandlerMethod</code>", 3),
 "steps": [
  "Two ways to run code around every request. A filter sits in front of the dispatcher servlet, at the servlet level. It sees every request, even for static files, and can change the raw request and response. A request goes through all filters before Spring MVC sees it.",
  "An interceptor runs inside Spring MVC, after the handler method is chosen. So it knows which controller method will run. It has pre handle, post handle, and after completion hooks.",
  "So: authentication, CORS, and request IDs belong in filters. Spring Security is in fact a chain of filters. Timing per endpoint, or anything that needs the controller method, belongs in an interceptor.",
  "That's how custom annotations work. Put at rate limited on a controller method, and an interceptor reads it from the handler method in pre handle, and decides whether to continue.",
 ]},

{"html": H("HATEOAS: responses with ", "links") + row(
   code("""§0 {
§0   "id": 7, "title": "Write notes", "done": false,
§0   "_links": {
§0     "self":     { "href": "/api/tasks/7" },
§0     "complete": { "href": "/api/tasks/7/complete" },
§0     "owner":    { "href": "/api/users/3" }
§0   }
§0 }""", 26, style="flex:1"),
   col(box("blue", "the idea", "the response tells the client what it can do <b style=\"display:inline\">next</b>", 0),
       box("purple", "spring-boot-starter-hateoas", "<code>EntityModel</code> · <code>linkTo(methodOn(…))</code>", 1),
       box("gray", "in practice", "rare in internal APIs · good to <b style=\"display:inline\">know</b> for interviews", 2), gap=16, style="width:560px"), top=True),
 "steps": [
  "HATEOAS is the strictest form of REST. Each response includes links to related actions. This task links to itself, to completing it, and to its owner. A finished task simply wouldn't include the complete link.",
  "Spring HATEOAS builds these with entity model, and link to method on, which generates URLs from your controller methods so they never go out of date.",
  "In practice, most internal APIs skip it, since the frontend already knows the URLs. But it's a common interview question about REST maturity.",
 ]},

{"html": H("The layered ", "architecture") + row(
   box("blue", "controller", "HTTP only: parse, validate, call the service, map to a DTO", 0, "flex:1"),
   box("green", "service", "business rules · <code>@Transactional</code> · no HTTP types", 1, "flex:1"),
   box("purple", "repository", "data access only · Spring Data JPA", 2, "flex:1"), top=True) +
   row(box("orange", "dependencies point down", "controller → service → repository · never upwards", 3, "flex:1"),
       box("red", "smells", "<code>HttpServletRequest</code> in a service · SQL in a controller · entities in responses", 3, "flex:1"), style="margin-top:22px"),
 "steps": [
  "Finally, how the code is organised. The controller layer only deals with HTTP. It reads the request, validates it, calls a service, and maps the result to a DTO.",
  "The service layer holds the business rules and the transactions. It knows nothing about HTTP, so it could be called from a scheduled job or a message listener just as well.",
  "The repository layer only talks to the database.",
  "Dependencies point downward only. Watch for the smells: HTTP request objects inside a service, SQL inside a controller, or entities returned straight to clients. Each one mixes two layers' jobs.",
 ]},

quiz([
  ("Auth check for every request, even static files?", "a <b style=\"display:inline\">Filter</b>", "blue",
   "Quiz time. You need an authentication check on every request, including static files. Filter or interceptor?",
   "A filter. It runs before Spring MVC, for every request."),
  ("Read a custom annotation on the controller method?", "an <b style=\"display:inline\">Interceptor</b> (HandlerMethod)", "purple",
   "You want to read a custom annotation on the controller method being called. Filter or interceptor?",
   "An interceptor. It knows the handler method, so it can read its annotations."),
  ("Where does @Transactional belong?", "the <b style=\"display:inline\">service</b> layer", "green",
   "In the layered architecture, where does transactional belong?",
   "On service methods, where the business actions are."),
]),

recap(["Uploads: multipart, MultipartFile, size limits",
       "Never trust filenames or types from the client",
       "Spring 7 versioning: version = \"2\" on the mapping",
       "Filter: every request, before Spring MVC",
       "Interceptor: knows the handler method",
       "Controller → service → repository, one job each"],
  "Let's recap part two. Files arrive as multipart parts, read as a multipart file, with size limits. Never trust the client's file name or type. Spring seven adds API versioning, with a version attribute on the mapping. Filters run for every request before Spring MVC, and interceptors know the handler method. And the layered architecture keeps HTTP in controllers, business rules in services, and data access in repositories. Now practise with the examples in your notes!"),
]
