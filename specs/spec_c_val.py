from conc import *

TAG = "Spring · Validation and Error Handling"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Validation and Error Handling.mp4"

SLIDES = [
title_slide(0, "Validation & Errors", "Reject bad input at the door, and answer every failure the same clean way",
  "Welcome to validation and error handling.",
  "Every API receives bad input sooner or later: a missing title, a negative price, an email that isn't one. And things go wrong inside too: a task that doesn't exist, a duplicate name. By the end you'll know where validation belongs, Bean Validation's annotations, at valid, custom constraints, how Spring MVC turns exceptions into responses, controller advice, and the standard error format, Problem Details.",
  pill="SPRING · CONCEPT"),

{"html": H("Where validation ", "belongs") + row(
   box("blue", "1 · shape", "at the edge, on the DTO: required, length, format · <b style=\"display:inline\">Bean Validation</b>", 0, "flex:1"),
   box("purple", "2 · business rules", "in the service: \"due date after start\", \"title unique for this user\"", 1, "flex:1"),
   box("green", "3 · the database", "NOT NULL · UNIQUE · foreign keys: the last safety net", 2, "flex:1"), top=True) +
   note("Fail fast at the edge · never trust the client, even your own frontend", 3),
 "steps": [
  "Validation happens in layers. The first is shape, checked at the edge on the request DTO. Is the title there? Is it too long? Is this a valid email? That's Bean Validation.",
  "The second is business rules, which need context or the database. Is the due date after the start date? Is the title unique for this user? Those belong in the service.",
  "The third is the database itself. Not null, unique, and foreign key constraints are the last safety net, even if a bug slips past the code.",
  "The principle: fail fast at the edge, and never trust input from a client. Not even from your own frontend, because anyone can call your API directly.",
 ]},

{"html": H("Bean ", "Validation") + row(
   code("""§0 public record CreateTask(
§0   @NotBlank @Size(max = 200) String title,
§0   @Email String ownerEmail,
§0   @Min(1) @Max(5) int priority,
§0   @FutureOrPresent LocalDate due) {}
§1 @PostMapping
§1 TaskResponse create(@Valid @RequestBody CreateTask req) { … }""", 26, style="flex:1"),
   col(box("blue", "spring-boot-starter-validation", "Hibernate Validator · <code>jakarta.validation</code>", 0),
       box("green", "@Valid", "without it, the annotations are <b style=\"display:inline\">ignored</b>", 1),
       box("red", "invalid?", "<code>MethodArgumentNotValidException</code> → 400, your method never runs", 2), gap=16, style="width:600px"), top=True) +
   note("@NotNull: not null · @NotEmpty: + not empty · @NotBlank: + not just spaces", 3),
 "steps": [
  "Bean Validation puts the rules on the DTO itself, as annotations. Not blank, a maximum size, a valid email, a range for priority, a date that's today or later. The starter is spring boot starter validation, and the implementation is Hibernate Validator.",
  "Then mark the parameter with at valid. This part is easy to forget. Without at valid, the annotations are just decoration, and nothing is checked.",
  "If any rule fails, Spring throws method argument not valid exception before your method runs, and the client gets a four hundred.",
  "A classic interview question: not null, not empty, not blank. Not null only rejects null. Not empty also rejects an empty string or collection. Not blank also rejects a string of only spaces. For text fields, you usually want not blank.",
 ]},

{"html": H("Beyond the request ", "body") + row(
   box("blue", "path and query parameters", "constraints on the parameters · maybe <code>@Validated</code> on the class", 0, "flex:1"),
   box("purple", "nested objects", "<code>@Valid</code> on the field, or its rules are skipped", 1, "flex:1"),
   box("green", "custom constraint", "an annotation + a <code>ConstraintValidator</code>", 2, "flex:1"), top=True) +
   code("""§0 @GetMapping("/{id}")
§0 TaskResponse one(@PathVariable @Positive long id)
§2 @Constraint(validatedBy = SlugValidator.class)
§2 @interface Slug { String message() default "bad slug"; … }
§2 class SlugValidator implements ConstraintValidator<Slug, String> {
§2   public boolean isValid(String v, ConstraintValidatorContext c) {
§2     return v == null || v.matches("[a-z0-9-]+");
§2   }
§2 }""", 25, style="margin-top:20px"),
 "steps": [
  "You can validate path variables and query parameters too. Put constraints like positive on the parameters. Depending on your Spring version, you may need at validated on the controller class for this to kick in.",
  "For a DTO that contains another object, put at valid on that field as well. Otherwise the nested object's rules are skipped.",
  "And when no built in rule fits, write a custom constraint. It's an annotation pointing to a validator class, whose is valid method returns true or false. Return true for null, and let not null decide whether null is allowed. That keeps each rule doing one job.",
 ]},

{"html": H("How exceptions become ", "responses") + row(
   box("gray", "1 · thrown", "anywhere: controller, service, repository", 0, "flex:1"),
   box("blue", "2 · DispatcherServlet", "catches it, asks the <b style=\"display:inline\">exception resolvers</b>", 1, "flex:1"),
   box("green", "3 · resolved", "an <code>@ExceptionHandler</code> · <code>@ResponseStatus</code> · Spring's defaults", 2, "flex:1"), top=True) +
   table(["Exception", "Default status"], [
     (["<code>MethodArgumentNotValidException</code>", "400"], 3),
     (["<code>HttpMessageNotReadableException</code> (broken JSON)", "400"], 3),
     (["<code>NoResourceFoundException</code>", "404"], 3),
     (["anything you didn't handle", "<b>500</b>"], 3)], size=28),
 "steps": [
  "What happens when an exception escapes? It could come from the controller, the service, or the repository.",
  "It travels back up to the dispatcher servlet, which asks a chain of exception resolvers: does anyone know how to turn this into a response?",
  "Your own at exception handler methods are asked first. Then at response status annotations on exception classes. Then Spring's defaults.",
  "Spring already maps many of its own exceptions. A failed validation is four hundred. Broken JSON is also four hundred, and it fails before validation even starts. An unknown path is four oh four. And anything nobody handles becomes a five hundred.",
 ]},

{"html": H("One place for errors: ", "@RestControllerAdvice") + code("""§0 @RestControllerAdvice
§0 public class ApiErrors {
§1   @ExceptionHandler(TaskNotFoundException.class)
§1   ProblemDetail notFound(TaskNotFoundException e) {
§1     return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, e.getMessage());
§1   }
§2   @ExceptionHandler(Exception.class)
§2   ProblemDetail unexpected(Exception e) {
§2     log.error("unexpected", e);                      // full detail in the log
§2     return ProblemDetail.forStatus(HttpStatus.INTERNAL_SERVER_ERROR);  // none to the client
§2   }
§0 }""", 25) + note("Services throw meaningful exceptions · the advice decides the HTTP answer", 3),
 "steps": [
  "Rather than catching exceptions in every controller, put the handling in one class, annotated rest controller advice. It applies to all controllers.",
  "Each at exception handler method handles one type of exception. Here, task not found becomes a four oh four, with the message as the detail.",
  "Add a catch all for unexpected exceptions. Log the full stack trace on the server, but send the client a plain five hundred, without internals. Stack traces in responses leak information to attackers.",
  "This keeps responsibilities clean. Services throw exceptions that describe what went wrong in business terms. The advice alone decides how that maps to HTTP.",
 ]},

{"html": H("Problem ", "Details") + row(
   code("""§0 HTTP/1.1 404 Not Found
§0 Content-Type: application/problem+json
§0
§0 {
§0   "type": "about:blank",
§0   "title": "Not Found",
§0   "status": 404,
§0   "detail": "Task 7 not found",
§0   "instance": "/api/tasks/7",
§1   "errors": { "title": "must not be blank" }
§0 }""", 25, style="flex:1"),
   col(box("blue", "RFC 9457", "one standard JSON shape for every error", 0),
       box("purple", "extend it", "<code>setProperty(\"errors\", …)</code> for field errors", 1),
       box("green", "Spring's own errors too", "<code>spring.mvc.problemdetails.enabled</code> or extend <code>ResponseEntityExceptionHandler</code>", 2), gap=16, style="width:700px"), top=True),
 "steps": [
  "What should an error response look like? There's a standard: Problem Details, RFC nine four five seven. A content type of application slash problem plus json, and fields for the type, a title, the status, a human readable detail, and which request failed. Spring's problem detail class builds it.",
  "You can add your own properties. For validation failures, add a map from each field to its message, so a frontend can show the error next to the right input.",
  "To make Spring's built in errors use the same format, turn on the problem details property, or extend response entity exception handler in your advice. Then every error from your API has one consistent shape.",
 ]},

{"html": H("Status codes and good ", "habits") + table(["Situation", "Status"], [
     (["malformed JSON · failed validation", "400 Bad Request"], 0),
     (["not logged in · logged in but not allowed", "401 · 403"], 0),
     (["the resource doesn't exist", "404 Not Found"], 1),
     (["duplicate · version conflict", "409 Conflict"], 1),
     (["valid shape, but breaks a business rule", "422 Unprocessable Content"], 1),
     (["a bug or an outage", "500 · 503"], 2)], size=29) +
   note("Never leak stack traces · log once, where it's handled · same shape everywhere", 3),
 "steps": [
  "Choosing the status is part of the design. Bad JSON or failed validation is four hundred. Not logged in is four oh one, logged in but not allowed is four oh three.",
  "A missing resource is four oh four. A duplicate or a version conflict is four oh nine. And some teams use four twenty two when the input is well formed, but breaks a business rule.",
  "Five hundreds are for bugs and outages, the server's fault, not the client's.",
  "And three habits. Never send stack traces to clients. Log an exception once, where it's handled, not at every layer it passes through. And keep one error shape across the whole API.",
 ]},

quiz([
  ("Annotations on the DTO, but nothing is checked. Why?", "<b style=\"display:inline\">@Valid</b> is missing", "red",
   "Quiz time. Your DTO has validation annotations, but invalid requests still get through. What's missing?",
   "At valid on the request body parameter. Without it, nothing is validated."),
  ("@NotNull vs @NotBlank for a title?", "<b style=\"display:inline\">@NotBlank</b>: rejects \"\" and \"   \"", "blue",
   "For a title field, not null or not blank?",
   "Not blank. It also rejects empty strings and strings of only spaces."),
  ("Where do you map exceptions to HTTP?", "one <b style=\"display:inline\">@RestControllerAdvice</b>", "green",
   "Where should exceptions be turned into HTTP responses?",
   "In one rest controller advice class, with an exception handler per exception type."),
]),

recap(["Shape at the edge · rules in the service · DB as safety net",
       "Annotate the DTO, and add @Valid",
       "@NotBlank for text · custom constraints for the rest",
       "Unhandled exception → 500",
       "@RestControllerAdvice: one place for errors",
       "ProblemDetail: one standard error shape"],
  "Let's recap. Check the shape of input at the edge, business rules in the service, and keep database constraints as a safety net. Annotate the DTO and remember at valid. Use not blank for text, and write custom constraints when nothing built in fits. Any exception you don't handle becomes a five hundred. Handle them in one rest controller advice. And answer with Problem Details, so every error has the same shape. Now practise with the examples in your notes!"),
]
