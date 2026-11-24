from conc import *

TAG = "Spring · Maven in Depth"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Maven in Depth.mp4"

SLIDES = [
title_slide(0, "Maven in Depth", "Coordinates, dependency resolution, lifecycles and multi-module builds",
  "Welcome. Today's concept: Maven, in depth.",
  "Every Spring Boot project you create starts with a pom file, and most build problems, like a missing class at runtime or two versions of the same library, are really Maven problems. By the end you'll know the project layout and the wrapper, coordinates and snapshots, how transitive dependencies are resolved, scopes, exclusions and BOMs, lifecycles, phases and goals, plugins, multi module builds, and profiles.",
  pill="SPRING · CONCEPT"),

{"html": H("Layout, wrapper and ", "coordinates") + row(
   code("""§0 my-app/
§0 ├── mvnw, mvnw.cmd, .mvn/     ← the wrapper
§0 ├── pom.xml
§0 └── src/main/java · src/main/resources
§0     src/test/java · src/test/resources
§1 <groupId>com.shop</groupId>
§1 <artifactId>orders</artifactId>
§1 <version>1.4.0-SNAPSHOT</version>""", 25, style="flex:1"),
   col(box("blue", "the wrapper", "<code>./mvnw</code> downloads the right Maven version · same build everywhere", 0),
       box("green", "GAV", "group · artifact · version = a unique address in a repository", 1),
       box("orange", "SNAPSHOT", "work in progress · may change · releases never change", 2), gap=14, style="width:600px"), top=True),
 "steps": [
  "A Maven project has a standard layout: main code, main resources, and their test twins. Next to the pom sits the wrapper. Running m v n w downloads the exact Maven version the project expects, so every laptop and CI server builds the same way.",
  "Every artifact has coordinates: a group id, an artifact id and a version. Together they're its unique address in a repository like Maven Central.",
  "A version ending in snapshot means work in progress. Maven may fetch a newer build of it. A release version is fixed forever, which is what reproducible builds need.",
 ]},

{"html": H("Transitive ", "dependencies") + graph(
   {"app": (450, 60), "web": (230, 190), "jpa": (670, 190), "2.17": (110, 320), "log": (350, 320), "hib": (670, 320), "2.15": (670, 450)},
   [("app", "web"), ("app", "jpa"), ("web", "2.17"), ("web", "log"), ("jpa", "hib"), ("hib", "2.15")],
   colors={"2.17": ("#bbf7d0", "#16a34a"), "2.15": ("#fecaca", "#dc2626")},
   labels={"2.17": "jackson · depth 2 ✓", "2.15": "jackson · depth 3 ✗", "hib": "", "log": ""},
   w=900, h=540, directed=True, step=0, r=46) +
   note("Two versions of one library → Maven keeps the <b>nearest</b> · a tie → the first declared", 1),
 "steps": [
  "You declare only your direct dependencies. Each of them brings its own, and those bring more. That's the transitive dependency tree, and m v n dependency colon tree prints it.",
  "Often two paths ask for different versions of the same library. Maven keeps only one: the nearest to your project in the tree. If they're equally near, the one declared first wins. Note that it doesn't pick the highest version, which is how surprise downgrades happen.",
 ]},

{"html": H("Scopes, exclusions and ", "BOMs") + row(
   col(box("blue", "scopes", "<code>compile</code> · <code>provided</code> · <code>runtime</code> · <code>test</code> · <code>import</code>", 0),
       box("orange", "exclusions", "cut one transitive dependency out of the tree", 1),
       box("green", "dependencyManagement", "sets versions · adds nothing by itself", 2),
       box("purple", "a BOM", "a pom of agreed versions · the Spring Boot parent is one", 3), gap=14, style="width:560px"),
   code("""§1 <dependency>
§1   <groupId>org.springframework.boot</groupId>
§1   <artifactId>spring-boot-starter-web</artifactId>
§1   <exclusions><exclusion>
§1     <artifactId>spring-boot-starter-tomcat</artifactId>
§1   </exclusion></exclusions>
§1 </dependency>
§3 <dependency>  <!-- in dependencyManagement -->
§3   <artifactId>spring-cloud-dependencies</artifactId>
§3   <type>pom</type> <scope>import</scope>
§3 </dependency>""", 22, style="flex:1"), top=True),
 "steps": [
  "Scopes decide where a dependency is visible: compile is the default, provided and runtime split compiling from running, and test stays out of the shipped app.",
  "An exclusion removes one transitive dependency, for example swapping Tomcat for another web server.",
  "Dependency management fixes versions without adding anything. When a module later declares that library without a version, it gets the managed one.",
  "A bill of materials, or BOM, is a pom full of versions known to work together. Import it, and every Spring or Spring Cloud library lines up. Spring Boot's parent pom does exactly this, which is why your starters have no versions.",
 ]},

{"html": H("Lifecycles, phases and ", "goals") + code("§0 validate → compile → test → package → verify → install → deploy", 30) + row(
   box("blue", "a phase", "a step in a lifecycle · running one runs <b style=\"display:inline\">all before it</b>", 1, "flex:1"),
   box("green", "a goal", "a plugin's task · <code>compiler:compile</code> · bound to a phase", 2, "flex:1"),
   box("purple", "3 lifecycles", "<code>clean</code> · <code>default</code> · <code>site</code>", 3, "flex:1"), top=True, style="margin-top:24px") +
   note("mvn clean package → clean, then every phase up to package", 4),
 "steps": [
  "Maven's default lifecycle is a fixed list of phases: validate, compile, test, package, verify, install and deploy.",
  "Running a phase runs every phase before it. So m v n package compiles and tests before building the jar. Install also copies it into your local repository, and deploy uploads it to a shared one.",
  "Phases don't do work by themselves. Plugin goals do, like the compiler plugin's compile goal, and each goal is bound to a phase.",
  "There are three lifecycles: clean, default, and site for documentation.",
  "So m v n clean package runs the clean lifecycle, then the default one up to package.",
 ]},

{"html": H("Plugins and the ", "enforcer") + table(["Plugin", "Does"], [
     (["<code>maven-compiler-plugin</code>", "compiles · sets the Java release"], 0),
     (["<code>maven-surefire-plugin</code>", "runs unit tests in <code>test</code>"], 0),
     (["<code>maven-failsafe-plugin</code>", "runs integration tests in <code>verify</code>"], 1),
     (["<code>spring-boot-maven-plugin</code>", "repackages into an executable fat jar"], 1),
     (["<code>maven-enforcer-plugin</code>", "fails the build on rule breaks · e.g. version conflicts"], 2)], size=28) +
   note("Configure a plugin's goals under &lt;build&gt;&lt;plugins&gt; · pin plugin versions too", 3),
 "steps": [
  "Everything Maven does comes from plugins. The compiler plugin compiles, and surefire runs unit tests during the test phase.",
  "Failsafe runs integration tests in verify, and doesn't stop the build until cleanup has run. The Spring Boot plugin repackages the jar so it can run on its own with java dash jar.",
  "The enforcer plugin fails the build when a rule breaks, such as two versions of one library converging badly, or the wrong Java version.",
  "Plugins are configured in the build section. Pin their versions too, so builds stay reproducible.",
 ]},

{"html": H("Multi-module ", "builds") + row(
   code("""§0 shop/                      <packaging>pom</packaging>
§0 ├── pom.xml                <modules> common, orders, api </modules>
§0 ├── common/pom.xml
§0 ├── orders/pom.xml         depends on common
§0 └── api/pom.xml            depends on orders""", 24, style="flex:1"),
   col(box("blue", "the parent", "shared versions, plugins and properties", 0),
       box("green", "the reactor", "sorts modules by dependency · builds common → orders → api", 1),
       box("orange", "handy flags", "<code>-pl api -am</code> build api and what it needs", 2), gap=14, style="width:560px"), top=True),
 "steps": [
  "Big projects split into modules. A parent pom with packaging pom lists the modules, and holds shared versions, plugins and properties.",
  "When you build the parent, the reactor works out the order from their dependencies. Common first, then orders, then the API.",
  "And you can build part of it. Dash p l picks a module, and dash a m also builds the modules it needs.",
 ]},

{"html": H("Profiles and ", "settings.xml") + row(
   code("""§0 <profiles>
§0   <profile>
§0     <id>ci</id>
§0     <properties><skipITs>false</skipITs></properties>
§0   </profile>
§0 </profiles>
§0 mvn verify -Pci
§2 ~/.m2/settings.xml   mirrors · server passwords · proxy
§2 ~/.m2/repository     the local cache""", 25, style="flex:1"),
   col(box("blue", "profiles", "switch properties, plugins or modules · <code>-P</code> or auto-activation", 0),
       box("orange", "keep them few", "the same artifact should run everywhere", 1),
       box("gray", "settings.xml", "per machine · never commit credentials to the pom", 2), gap=14, style="width:560px"), top=True),
 "steps": [
  "A profile changes the build when activated, with dash capital P, or automatically on a JDK version, operating system, or property. Here a CI profile enables integration tests.",
  "Use them sparingly. For Spring apps, environment differences belong in runtime configuration, not in different builds.",
  "Machine level settings live in settings dot xml in your home folder: repository mirrors, passwords for servers, proxies. The local repository caches every downloaded artifact.",
 ]},

quiz([
  ("Two versions of a library in the tree: which wins?", "the <b style=\"display:inline\">nearest</b> one", "orange",
   "Quiz time. Two versions of the same library appear in the dependency tree. Which does Maven keep?",
   "The nearest to your project. Not the highest."),
  ("mvn package also runs…?", "every phase before it: compile, <b style=\"display:inline\">test</b>…", "blue",
   "What else runs when you type m v n package?",
   "Every earlier phase, including compile and test."),
  ("What does a BOM do?", "fixes <b style=\"display:inline\">versions</b> that work together", "purple",
   "What does importing a BOM do?",
   "It fixes versions of a family of libraries, so they work together."),
]),

recap(["mvnw pins the Maven version · GAV coordinates",
       "SNAPSHOT changes · releases never do",
       "Conflicts: nearest wins · check dependency:tree",
       "dependencyManagement + BOMs fix versions",
       "Phase runs all earlier phases · goals do the work",
       "Multi-module reactor · profiles · settings.xml"],
  "Let's recap. The wrapper pins Maven's version, and coordinates give every artifact an address. Snapshots can change, releases can't. In version conflicts the nearest declaration wins, so inspect the dependency tree. Dependency management and BOMs fix versions in one place. Running a phase runs every phase before it, while plugin goals do the actual work. And multi module builds use the reactor, with profiles and settings dot xml for the rest. Now practise with the examples in your notes!"),
]
