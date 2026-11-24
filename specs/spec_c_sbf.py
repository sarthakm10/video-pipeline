from conc import *

TAG = "Spring · Boot Fundamentals"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Boot Fundamentals.mp4"

SLIDES = [
title_slide(0, "Spring Boot", "Starters, auto-configuration, externalized config, profiles and the runnable jar",
  "Welcome to Spring Boot fundamentals.",
  "In the Spring Core video, we saw the container that creates and wires beans. Spring Boot sits on top of it and removes the setup work. Pick dependencies, write your code, run one jar. By the end you'll know what starters are, what happens at startup, how auto-configuration decides what to create, how configuration is layered, and how profiles and the executable jar work.",
  pill="SPRING · CONCEPT"),

{"html": H("Spring vs Spring ", "Boot") + row(
   box("blue", "Spring Framework", "the engine: IoC container, MVC, data access, transactions…", 0, "flex:1"),
   box("green", "Spring Boot", "an <b style=\"display:inline\">opinionated layer</b> on top: sensible defaults so it just runs", 1, "flex:1"), top=True) +
   table(["Boot gives you", "Instead of"], [
     (["<b>starters</b>: one dependency per purpose", "hand-picking compatible library versions"], 2),
     (["<b>auto-configuration</b>", "declaring DataSource, ObjectMapper, DispatcherServlet… yourself"], 2),
     (["an <b>embedded server</b>", "deploying a WAR to an external Tomcat"], 3),
     (["<b>externalized configuration</b>", "rebuilding to change a port or a password"], 3)], size=28),
 "steps": [
  "First, the difference. The Spring framework is the engine: the container, web MVC, data access, transactions. It's powerful, but you used to configure all of it yourself.",
  "Spring Boot is an opinionated layer on top. It uses Spring, it doesn't replace it. It makes sensible choices for you, so a new app runs with almost no setup.",
  "It gives you four things. Starters, so one dependency brings a whole compatible set of libraries. And auto-configuration, so the common beans are created for you.",
  "An embedded server, so your app is a plain jar you run with java dash jar, not a WAR deployed somewhere. And externalized configuration, so you change settings without rebuilding.",
 ]},

{"html": H("Starters and the ", "parent POM") + row(
   code("""§0 <parent>
§0   <groupId>org.springframework.boot</groupId>
§0   <artifactId>spring-boot-starter-parent</artifactId>
§0 </parent>
§1 <dependency>
§1   <artifactId>spring-boot-starter-webmvc</artifactId>
§1 </dependency>                     <!-- no <version>! -->""", 25, style="flex:1"),
   col(box("blue", "the parent", "manages <b style=\"display:inline\">versions</b> of hundreds of libraries that are tested together", 0),
       box("green", "a starter", "a dependency that brings everything for one job: Spring MVC + Jackson + embedded Tomcat", 1),
       box("purple", "the plugin", "<code>spring-boot-maven-plugin</code> builds the runnable jar", 2), gap=16, style="width:620px"), top=True),
 "steps": [
  "Start with the build file. The starter parent manages the versions of hundreds of libraries that are known to work together. That's why your dependencies have no version numbers.",
  "A starter is a dependency that brings everything needed for one job. The web MVC starter brings Spring MVC, the Jackson JSON library and an embedded Tomcat. There are starters for data JPA, security, validation, testing, and so on.",
  "And the Boot Maven plugin packages everything into one runnable jar. We'll see what's inside it at the end.",
 ]},

{"html": H("@SpringBootApplication and ", "startup") + row(
   code("""§0 @SpringBootApplication
§0 public class TaskApp {
§0   public static void main(String[] args) {
§2     SpringApplication.run(TaskApp.class, args);
§0   }
§0 }""", 28, style="flex:1"),
   col(box("blue", "@SpringBootConfiguration", "this class is a configuration class", 1),
       box("green", "@EnableAutoConfiguration", "turn on Boot's automatic beans", 1),
       box("purple", "@ComponentScan", "find <code>@Component</code>s in <b style=\"display:inline\">this package and below</b>", 1), gap=14, style="width:600px"), top=True) +
   pts([("<code>run()</code>: read config → create the context → scan → auto-configure → start the server → call runners", 2),
        ("Put the main class in the <u>root</u> package, or scanning misses your beans", 3)], size=30, style="margin-top:20px"),
 "steps": [
  "A Boot app starts with one annotated class and a main method.",
  "At Spring Boot Application is three annotations in one. Spring Boot Configuration marks the class as configuration. Enable Auto Configuration turns on Boot's automatic beans. And Component Scan finds your components, in this class's package and every package below it.",
  "Spring application dot run does the startup work. It reads the configuration, creates the application context, scans for your beans, applies auto-configuration, starts the embedded server, and finally calls any runners.",
  "One classic mistake: put the main class in a sub-package, and component scan never sees controllers that sit beside it or above it. Keep it in the root package.",
 ]},

{"html": H("Auto-configuration: how the ", "magic", " works") + row(
   code("""§0 @AutoConfiguration
§1 @ConditionalOnClass(DataSource.class)  // library?
§2 class DataSourceAutoConfiguration {
§2   @Bean
§2   @ConditionalOnMissingBean            // none of yours?
§2   DataSource dataSource(…) { … }
§2 }""", 25, style="flex:1"),
   col(box("gray", "candidates", "listed in <code>META-INF/spring/…AutoConfiguration.imports</code>", 0),
       box("blue", "@ConditionalOnClass", "only if the library is on the classpath", 1),
       box("green", "@ConditionalOnMissingBean", "only if <b style=\"display:inline\">you</b> haven't made one → Boot <b style=\"display:inline\">backs off</b>", 2),
       box("orange", "@ConditionalOnProperty", "only if a setting says so", 3), gap=14, style="width:660px"), top=True),
 "steps": [
  "Auto-configuration isn't magic. It's ordinary configuration classes with conditions. Boot lists its candidate classes in an imports file inside its jars.",
  "Each one is guarded by conditions. Conditional on class means: only if this library is on the classpath. Add the JDBC driver, and the data source configuration becomes active.",
  "Conditional on missing bean means: only if you haven't defined this bean yourself. And auto-configuration runs after your own configuration. So if you declare your own data source, Boot simply backs off. Your bean always wins.",
  "And conditional on property switches things on or off from a setting. That's the whole mechanism: your classpath and your beans decide what Boot creates.",
 ]},

{"html": H("Overriding and ", "debugging") + table(["To change Boot's choice", "Do this"], [
     (["tweak a setting", "set a property: <code>spring.datasource.url=…</code>"], 0),
     (["replace a bean", "declare your own <code>@Bean</code>: Boot backs off"], 1),
     (["turn one off", "<code>@SpringBootApplication(exclude = …)</code> or <code>spring.autoconfigure.exclude</code>"], 2)], size=29) +
   row(box("blue", "--debug", "prints the <b style=\"display:inline\">conditions report</b>: what matched, what didn't, and why", 3, "flex:1"),
       box("green", "/actuator/conditions", "the same report from a running app", 3, "flex:1"), style="margin-top:24px"),
 "steps": [
  "So how do you change what Boot does? In order of preference. Most of the time, just set a property, like the database URL.",
  "If a property isn't enough, define your own bean of that type. Because of conditional on missing bean, Boot steps aside.",
  "And to turn an auto-configuration off completely, exclude it, in the annotation or with a property.",
  "When something is configured and you don't know why, run with dash dash debug. Boot prints a conditions report, listing every auto-configuration, whether it matched, and the reason. Actuator shows the same report from a running app.",
 ]},

{"html": H("Externalized ", "configuration") + row(
   col(code("""§0 # application.yml
§0 server:
§0   port: 8080
§0 tasks:
§0   max-open-tasks: 5""", 26),
       box("gray", "properties or YAML", "same features · YAML is hierarchical · pick one", 0), gap=16, style="width:600px"),
   table(["Priority (high → low)", "Example"], [
     (["command-line args", "<code>--server.port=9090</code>"], 1),
     (["Java system properties", "<code>-Dserver.port=9090</code>"], 1),
     (["environment variables", "<code>SERVER_PORT=9090</code>"], 1),
     (["files outside the jar", "<code>./config/application.yml</code>"], 2),
     (["files inside the jar", "<code>src/main/resources/</code>"], 2),
     (["defaults", "in code"], 2)], size=26), top=True) +
   note("Relaxed binding: <code>max-open-tasks</code> = <code>maxOpenTasks</code> = <code>TASKS_MAXOPENTASKS</code>", 3),
 "steps": [
  "Settings live outside your code, in application dot properties or application dot yml. Same features. YAML is just hierarchical. Pick one and stay consistent.",
  "The same setting can come from many places, and there's a fixed priority. Command-line arguments beat system properties, which beat environment variables.",
  "Those beat files outside the jar, which beat files packaged inside it, and finally defaults. That's how the same jar runs everywhere. The jar holds safe defaults, and each server overrides them with environment variables or arguments. Secrets never get baked into the build.",
  "And relaxed binding means the same property can be written in different styles. Kebab case in files, camel case, or upper case with underscores as an environment variable. They all bind to the same setting.",
 ]},

{"html": H("Type-safe config and ", "profiles") + row(
   col(code("""§0 @ConfigurationProperties("tasks")
§0 @Validated
§0 record TaskProps(@Min(1) int maxOpenTasks,
§0                  Duration timeout) {}""", 25),
       box("green", "vs @Value(\"${…}\")", "one value, no grouping, no validation · prefer <code>@ConfigurationProperties</code>", 1), gap=16, style="flex:1"),
   col(box("blue", "profiles", "<code>application-dev.yml</code> · <code>application-prod.yml</code> override the base file", 2),
       box("purple", "activate", "<code>--spring.profiles.active=prod</code> or <code>SPRING_PROFILES_ACTIVE=prod</code>", 2),
       box("orange", "beans too", "<code>@Profile(\"dev\")</code> → only created in dev", 3), gap=14, style="width:620px"), top=True),
 "steps": [
  "To read settings in code, bind a whole group into a record with configuration properties. You get types, like durations, nesting, and validation that fails at startup if a value is wrong.",
  "At value reads one value at a time, with no grouping and no validation. It's fine for a single setting, but configuration properties is the better default.",
  "Profiles handle different environments. Application dash dev dot yml and application dash prod dot yml hold the differences, and they override the base file. Activate one with a command-line argument or an environment variable.",
  "Profiles work on beans too. A bean marked with profile dev is only created when dev is active, like a fake email sender for local testing.",
 ]},

{"html": H("Runners and the executable ", "jar") + row(
   col(box("blue", "CommandLineRunner", "<code>run(String... args)</code> once after startup", 0),
       box("green", "ApplicationRunner", "the same, with parsed <code>ApplicationArguments</code>", 0),
       box("red", "startup failures", "port in use · missing bean · bad config → clear <b style=\"display:inline\">failure analysis</b> message", 1), gap=16, style="flex:1"),
   col(box("gray", "java -jar app.jar", "", 2),
       box("purple", "BOOT-INF/classes", "your code", 2),
       box("purple", "BOOT-INF/lib/*.jar", "every dependency, nested", 2),
       box("orange", "JarLauncher", "Boot's Main-Class: sets up a class loader, then calls your main", 3), gap=12, style="width:620px"), top=True),
 "steps": [
  "To run code once the app has started, like loading sample data, implement a command line runner or an application runner. The second one gets the arguments already parsed.",
  "And when startup fails, Boot prints a failure analysis: the port is already in use, a bean is missing, a setting is invalid. Read the bottom of the log first.",
  "Finally, the executable jar. You run the whole app with java dash jar. Inside, your classes are in boot info classes, and every dependency sits as a nested jar in boot info lib.",
  "Plain Java can't load nested jars, so the jar's main class is actually Boot's jar launcher. It sets up a class loader that can read them, then calls your main method. And it runs an embedded Tomcat inside, so no external server is needed.",
 ]},

quiz([
  ("You define your own DataSource bean. What does Boot do?", "<b style=\"display:inline\">backs off</b>: @ConditionalOnMissingBean", "green",
   "Quiz time. You define your own data source bean. What does Boot's auto-configuration do?",
   "It backs off, because its data source is conditional on a missing bean."),
  ("Port in the jar's yml vs SERVER_PORT env var?", "the <b style=\"display:inline\">env var</b> wins", "blue",
   "The jar's YAML says port 8080, and the environment variable SERVER_PORT says 9090. Which wins?",
   "The environment variable. It has higher priority than files inside the jar."),
  ("Controllers aren't found at startup. Likely cause?", "main class not in the <b style=\"display:inline\">root package</b>", "orange",
   "Your controllers aren't being found. What's a likely cause?",
   "The main class isn't in the root package, so component scan doesn't reach them."),
]),

recap(["Boot = opinionated defaults on top of Spring",
       "Starters + parent POM = compatible versions",
       "@SpringBootApplication = config + auto-config + scan",
       "Auto-config: conditions · your bean wins",
       "Config: args > env vars > files outside > inside",
       "Profiles per environment · java -jar via JarLauncher"],
  "Let's recap. Spring Boot is an opinionated layer of defaults on top of Spring. Starters and the parent POM give you compatible versions. At Spring Boot Application combines configuration, auto-configuration and component scanning, so keep it in the root package. Auto-configuration is conditional, and your own bean always wins. Configuration is layered, with command-line arguments and environment variables beating files. And profiles handle environments, while java dash jar runs everything through Boot's launcher. Now practise with the exercises in your notes!"),
]
