from conc import *

TAG = "Spring · Deployment"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Deployment.mp4"

SLIDES = [
title_slide(0, "Deployment", "From a jar on your laptop to containers in production",
  "Welcome. Today's concept: deploying a Spring Boot app.",
  "Writing the app is half the job. It also has to start fast, read its configuration and secrets safely, run in a container, and be rolled out without downtime. By the end you'll know the fat jar and its layers, faster startup with CDS, production configuration and secrets, a multi stage Dockerfile, Kubernetes probes and resources, and a CI pipeline.",
  pill="SPRING · CONCEPT"),

{"html": H("The fat jar and its ", "layers") + row(
   code("""§0 ./mvnw package  →  target/app.jar
§0 java -jar target/app.jar
§0 app.jar
§0 ├── BOOT-INF/classes/     your code
§0 ├── BOOT-INF/lib/         every dependency jar
§0 └── org/springframework/boot/loader/
§2 java -Djarmode=tools -jar app.jar extract --layers --launcher
§2 dependencies/  spring-boot-loader/  snapshot-dependencies/  application/""", 22, style="flex:1"),
   col(box("blue", "fat jar", "your code + all libraries + a launcher · runs anywhere with a JRE", 0),
       box("orange", "the problem", "change one line → a new 80 MB image layer", 1),
       box("green", "layers", "rarely-changing first · your code last · Docker reuses the rest", 2), gap=14, style="width:520px"), top=True),
 "steps": [
  "The Spring Boot plugin packages a fat jar: your classes, every dependency jar, and a small launcher. Java dash jar runs it anywhere a JRE exists.",
  "But in a container image, the jar is one big file. Change one line of code, and the whole eighty megabytes becomes a new layer to build, push and pull.",
  "So extract it into layers: dependencies, the loader, snapshot dependencies, and finally your application. Dependencies rarely change, so Docker reuses those layers, and a code change ships only a few kilobytes.",
 ]},

{"html": H("Faster ", "startup") + row(
   box("blue", "CDS", "Class Data Sharing · a training run saves parsed classes → later starts load them", 0, "flex:1"),
   box("green", "AOT cache / Leyden", "Java 24+ goes further · also caches linking and profiling", 1, "flex:1"),
   box("purple", "native image", "GraalVM compiles ahead of time · ms startup, low memory · slow build, reflection limits", 2, "flex:1"), top=True) +
   code("""§0 java -XX:ArchiveClassesAtExit=app.jsa -Dspring.context.exit=onRefresh -jar app.jar
§0 java -XX:SharedArchiveFile=app.jsa -jar app.jar          # e.g. 14.5 s → 8.5 s""", 22, style="margin-top:22px"),
 "steps": [
  "Startup time matters when containers scale up. Class data sharing helps: a training run starts the app, then saves the parsed classes to an archive. Later starts map that archive instead of loading classes one by one. The notes' app went from fourteen and a half seconds to eight and a half.",
  "Newer Java versions extend this with an ahead of time cache that also keeps linking and profiling data.",
  "The extreme option is a GraalVM native image: startup in milliseconds and low memory, but slow builds, and reflection needs extra configuration.",
 ]},

{"html": H("Production ", "configuration") + row(
   code("""§0 java -jar app.jar --spring.profiles.active=prod
§1 SPRING_DATASOURCE_URL=jdbc:postgresql://db/app    # env var
§1   → spring.datasource.url                         (relaxed binding)
§2 @ConfigurationProperties("app.jwt") @Validated
§2 record JwtProperties(@NotBlank String secret,
§2                      @NotNull Duration ttl) { }""", 23, style="flex:1"),
   col(box("blue", "one artifact", "the same jar everywhere · only config changes", 0),
       box("green", "relaxed binding", "env vars map onto properties automatically", 1),
       box("orange", "fail fast", "validated properties stop a bad deploy at startup", 2), gap=14, style="width:540px"), top=True),
 "steps": [
  "Build once, deploy the same artifact everywhere. Only configuration changes, starting with a prod profile.",
  "Relaxed binding maps environment variables onto properties: upper case with underscores becomes the dotted name. That's how containers pass configuration.",
  "Bind settings to a validated configuration properties record. A missing secret or a bad duration then fails at startup, not at three a m when the first user logs in.",
 ]},

{"html": H("", "Secrets") + row(
   box("red", "never", "in the jar, the image, git, or a log line", 0, "flex:1"),
   box("orange", "env vars", "simple · but visible in process listings and crash dumps", 1, "flex:1"),
   box("green", "config trees", "secrets mounted as files · <code>spring.config.import=configtree:/run/secrets/</code>", 2, "flex:1"), top=True) +
   note("Real production: a vault (Vault, AWS Secrets Manager) + rotation", 3),
 "steps": [
  "Secrets, like database passwords and signing keys, must never be in the jar, the image, the git repository, or a log line.",
  "Environment variables are the simple option, but they can leak through process listings, crash reports and child processes.",
  "Better: mount each secret as a file, the way Kubernetes and Docker secrets do. Spring's config tree import turns each file into a property named after it.",
  "In real production, a secrets manager stores them and rotates them regularly.",
 ]},

{"html": H("A multi-stage ", "Dockerfile") + row(
   code("""§0 FROM eclipse-temurin:21-jdk AS build
§0 WORKDIR /src
§0 COPY . .
§0 RUN ./mvnw -q package -DskipTests && \\
§0     java -Djarmode=tools -jar target/app.jar extract --layers --destination out
§1 FROM eclipse-temurin:21-jre
§1 RUN useradd -r app
§1 USER app
§2 COPY --from=build /src/out/dependencies/ ./
§2 COPY --from=build /src/out/application/ ./
§2 ENTRYPOINT ["java", "-jar", "app.jar"]""", 21, style="flex:1"),
   col(box("blue", "stage 1: build", "JDK + Maven · compile and extract layers", 0),
       box("green", "stage 2: run", "JRE only · smaller image, fewer CVEs · not root", 1),
       box("purple", "layer order", "dependencies first → cached between builds", 2), gap=14, style="width:500px"), top=True) +
   note("docker compose: app + PostgreSQL for local runs", 3),
 "steps": [
  "A multi stage Dockerfile builds in one image and runs in another. The first stage has the JDK and Maven, builds the jar, and extracts the layers.",
  "The second stage starts from a small JRE image, so the final image has no compiler, no source, and fewer vulnerabilities. It runs as a normal user, not root.",
  "Layers are copied in order of how often they change, so a code change only rebuilds the last one.",
  "For local development, docker compose starts the app together with PostgreSQL.",
 ]},

{"html": H("Running on ", "Kubernetes") + row(
   code("""§0 replicas: 3
§1 readinessProbe:
§1   httpGet: { path: /actuator/health/readiness, port: 8081 }
§1 livenessProbe:
§1   httpGet: { path: /actuator/health/liveness, port: 8081 }
§2 resources:
§2   requests: { cpu: 500m, memory: 512Mi }
§2   limits:   { memory: 768Mi }
§3 terminationGracePeriodSeconds: 30""", 25, style="flex:1"),
   col(box("blue", "rolling update", "new pods become ready before old ones stop", 0),
       box("green", "probes", "readiness gates traffic · liveness restarts", 1),
       box("orange", "memory", "the JVM sizes its heap from the container limit", 2),
       box("purple", "shutdown", "SIGTERM → graceful shutdown inside the grace period", 3), gap=14, style="width:480px"), top=True),
 "steps": [
  "In Kubernetes, a deployment runs several replicas, and a rolling update brings new pods up before old ones are removed.",
  "Probes tie in with Actuator. Readiness decides when a pod gets traffic. Liveness decides when to restart it.",
  "Requests reserve resources, limits cap them. The JVM reads the container's memory limit and sizes its heap from it, so leave room for non heap memory.",
  "On shutdown, Kubernetes sends a terminate signal. Spring's graceful shutdown finishes in flight requests, as long as the grace period is long enough.",
 ]},

{"html": H("CI/CD with GitHub ", "Actions") + row(
   code("""§0 on: [push, pull_request]
§0 jobs:
§0   build:
§0     runs-on: ubuntu-latest
§0     steps:
§0       - uses: actions/checkout@v4
§0       - uses: actions/setup-java@v4
§0         with: { distribution: temurin, java-version: 21, cache: maven }
§1       - run: ./mvnw -B verify          # tests + Testcontainers
§2       - run: docker build -t ghcr.io/shop/app:${{ github.sha }} .""", 21, style="flex:1"),
   col(box("blue", "CI", "every push: build and run all tests", 0),
       box("green", "real dependencies", "Testcontainers starts PostgreSQL inside the runner", 1),
       box("purple", "CD", "on main: build an image tagged with the commit · deploy it", 2), gap=14, style="width:500px"), top=True) +
   note("Alternative: buildpacks → mvn spring-boot:build-image, no Dockerfile", 3),
 "steps": [
  "Continuous integration runs on every push and pull request. Check out the code, set up Java with a Maven cache.",
  "Then verify: compile and run every test. The runner has Docker, so Testcontainers can start a real PostgreSQL.",
  "Continuous delivery builds an image tagged with the commit hash, pushes it, and deploys it.",
  "Or skip the Dockerfile entirely. Buildpacks build an optimised, layered image with one Maven goal.",
 ]},

quiz([
  ("Why extract the jar into layers?", "dependencies are <b style=\"display:inline\">cached</b>: code changes ship small", "blue",
   "Quiz time. Why split the fat jar into layers?",
   "So the dependency layers are cached, and a code change only ships a small layer."),
  ("Where should a DB password live?", "a mounted <b style=\"display:inline\">secret file</b> / vault, never the image", "red",
   "Where should the database password live?",
   "In a mounted secret file or a vault. Never in the jar, the image or git."),
  ("Why a second Docker stage?", "a <b style=\"display:inline\">JRE-only</b> image: smaller, safer", "green",
   "Why does the Dockerfile have a second stage?",
   "So the final image only has a JRE: smaller, and with fewer vulnerabilities."),
]),

recap(["Fat jar → layers: dependencies cached",
       "CDS / AOT cache for startup · native images",
       "One artifact + prod profile · validated config",
       "Secrets as mounted files, never in the image",
       "Multi-stage Dockerfile · non-root JRE",
       "k8s probes, limits, graceful shutdown · CI on every push"],
  "Let's recap. The fat jar is split into layers so dependencies stay cached. CDS and the AOT cache speed up startup, and native images go further. Ship one artifact, with a prod profile and validated configuration. Mount secrets as files, never bake them into the image. Build with a multi stage Dockerfile and run as a non root user on a JRE. And on Kubernetes, wire probes and limits, shut down gracefully, and let CI test every push. Now practise with the examples in your notes!"),
]
