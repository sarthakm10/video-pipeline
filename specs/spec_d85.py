from conc import *

TAG = "Day 85 · AWS Compute: EC2, ECS and Lambda"
TRACK = "Java Fullstack · Cloud"
FILE = "Day 85 AWS Compute EC2 ECS and Lambda.mp4"

SLIDES = [
title_slide(85, "AWS Compute: EC2, ECS & Lambda", "Three ways to run your code, from a whole machine to a single function",
  "Welcome to day eighty five: compute on AWS.",
  "There are three main ways to run code on AWS. Rent a virtual machine with EC2, run containers with ECS, or run single functions with Lambda. Each trades control for convenience. By the end you'll know instance types and pricing, auto scaling, load balancers, ECS tasks, services and their two roles, Lambda cold starts and concurrency, and how to choose between them.",
  pill="DAY 85 · CLOUD"),

{"html": H("Three ways to run ", "code") + row(
   box("blue", "EC2", "a virtual machine · you manage the OS, Java, patches · most control", 0, "flex:1"),
   box("green", "ECS (+ Fargate)", "run containers · AWS places them · Fargate: no servers to manage", 1, "flex:1"),
   box("purple", "Lambda", "a function per event · pay per call · scales to zero", 2, "flex:1"), top=True) +
   note("Less control → less to operate · a Spring Boot API usually fits ECS Fargate", 3),
 "steps": [
  "EC2 gives you a virtual machine. You choose the OS, install Java, and apply patches. Maximum control, and maximum work.",
  "ECS runs containers for you. You hand it a Docker image, and it keeps the right number running. With Fargate, there aren't even servers to manage.",
  "Lambda runs a single function in response to an event, like an upload or an HTTP call. You pay per invocation, and it scales to zero when idle.",
  "The less control you need, the less you operate. A typical Spring Boot API fits ECS on Fargate nicely.",
 ]},

{"html": H("EC2: types and ", "pricing") + row(
   table(["Family", "Optimised for"], [
     (["<code>t3</code> / <code>m6</code>", "general purpose · t3 bursts"], 0),
     (["<code>c6</code>", "compute · CPU-heavy work"], 0),
     (["<code>r6</code>", "memory · caches, big heaps"], 0),
     (["<code>i3</code>", "fast local storage"], 0)], size=27),
   table(["Pricing", "Fits"], [
     (["On-Demand", "pay per second · no commitment"], 1),
     (["Reserved / Savings Plans", "commit 1–3 years · up to ~70% off"], 1),
     (["Spot", "spare capacity · up to 90% off · can be <b>taken back</b>"], 2)], size=27), top=True),
 "steps": [
  "Instance types come in families. T and M are general purpose, and T instances can burst above their baseline. C is for compute heavy work, R for lots of memory, and I for fast local storage. The number after the letter is the generation.",
  "You pay on demand, by the second, with no commitment. If you know you'll run for one to three years, reserved instances or savings plans cut the price a lot.",
  "Spot instances use spare capacity at up to ninety percent off, but AWS can take them back with two minutes' notice. Great for batch jobs, risky for your only API server.",
 ]},

{"html": H("Auto Scaling and load ", "balancers") + graph(
   {"users": (90, 170), "ALB": (330, 170), "app 1": (600, 60), "app 2": (600, 170), "app 3": (600, 280)},
   [("users", "ALB"), ("ALB", "app 1"), ("ALB", "app 2"), ("ALB", "app 3")],
   colors={"ALB": ("#ede9fe", "#7c3aed"), "app 3": ("#dcfce7", "#16a34a")},
   labels={"app 3": "added under load"}, w=700, h=370, directed=True, step=0, r=56) + col(
   box("blue", "Auto Scaling Group", "keeps N healthy instances · target tracking: \"CPU at 50%\"", 1),
   box("purple", "ALB vs NLB", "ALB: HTTP, routes by path / host · NLB: TCP, ultra-low latency", 2), gap=14, style="margin-top:20px"),
 "steps": [
  "Users don't talk to instances directly. A load balancer spreads requests across healthy targets, and stops sending to any that fail health checks.",
  "An auto scaling group keeps the right number of instances running. Target tracking says, for example, keep average CPU at fifty percent. It adds instances under load, removes them when it's quiet, and replaces unhealthy ones. Launch templates describe what to start.",
  "An application load balancer works at the HTTP level and can route by path or host name. A network load balancer works at the TCP level, for very low latency.",
 ]},

{"html": H("ECS: tasks, services, ", "roles") + row(
   col(box("blue", "task definition", "the recipe · image, CPU, memory, ports, env, secrets", 0),
       box("green", "service", "keeps N tasks running · rolling deploys · behind an ALB", 1),
       box("gray", "cluster", "where tasks run · Fargate or your EC2 capacity", 1), gap=14, style="width:560px"),
   col(box("orange", "execution role", "for ECS itself: pull the image · write logs · read secrets", 2),
       box("purple", "task role", "for <b style=\"display:inline\">your app</b>: read S3, send to SQS", 2), gap=14, style="flex:1"), top=True) +
   note("AccessDenied pulling the image → execution role · AccessDenied in your code → task role", 3),
 "steps": [
  "In ECS, a task definition is the recipe for your container: the image, CPU and memory, ports, environment variables and secrets.",
  "A service keeps a number of tasks running, replaces failed ones, does rolling deployments, and registers them with the load balancer. Tasks run in a cluster, on Fargate or on your own EC2 capacity.",
  "Two roles cause endless confusion. The execution role is for ECS itself: pulling the image, writing logs, reading secrets at startup. The task role is for your application code, like reading from S3.",
  "So if the task can't start because the image pull is denied, fix the execution role. If your code gets access denied, fix the task role.",
 ]},

{"html": H("", "Lambda") + row(
   col(box("blue", "event → function", "API Gateway, S3 upload, SQS message, a schedule", 0),
       box("orange", "cold start", "a new environment boots the runtime · Java + Spring: seconds", 1),
       box("green", "fixes", "SnapStart · provisioned concurrency · small frameworks", 2),
       box("purple", "concurrency", "one request per environment · account limit · reserved per function", 3), gap=14, style="width:620px"),
   code("""§0 public class Resize implements RequestHandler<S3Event, String> {
§0   public String handleRequest(S3Event e, Context c) {
§0     // make a thumbnail of the uploaded image
§0     return "ok";
§0   }
§0 }
§0 max 15 minutes · pay per ms of run time""", 23, style="flex:1"), top=True),
 "steps": [
  "Lambda runs a function when an event happens: an HTTP call through API Gateway, a file uploaded to S3, a message on a queue, or a schedule. It can run for at most fifteen minutes.",
  "The first call to a new environment is a cold start: it boots the runtime and your code. For Java with Spring, that can take seconds. Warm environments are reused and fast.",
  "SnapStart restores a snapshot of an initialised environment, provisioned concurrency keeps some warm, and lighter frameworks start faster.",
  "Each environment handles one request at a time, so a hundred parallel requests mean a hundred environments, up to your account limit. Reserved concurrency caps or guarantees a function's share.",
 ]},

{"html": H("Choosing ", "compute") + table(["Need", "Pick"], [
     (["full OS control · special software · long-lived", "<b>EC2</b> (+ Auto Scaling)"], 0),
     (["a containerised API, steady traffic", "<b>ECS on Fargate</b> behind an ALB"], 1),
     (["spiky, event-driven, short jobs", "<b>Lambda</b>"], 2),
     (["many teams, Kubernetes skills", "<b>EKS</b>"], 3)], size=29),
 "steps": [
  "Choose EC2 when you need full control of the operating system, special software, or long running processes.",
  "For a containerised API with steady traffic, like our Spring Boot app, ECS on Fargate behind a load balancer is the sweet spot.",
  "For spiky, event driven, short tasks, like resizing an uploaded image, Lambda is cheaper and simpler.",
  "And if your organisation already runs Kubernetes, EKS is the managed version.",
 ]},

quiz([
  ("Spot instance for your only API server?", "<b style=\"display:inline\">no</b>: it can be taken back", "red",
   "Quiz time. Is a spot instance a good idea for your only API server?",
   "No. AWS can take it back at two minutes' notice."),
  ("Your code gets AccessDenied on S3 in ECS: fix which role?", "the <b style=\"display:inline\">task role</b>", "purple",
   "In ECS, your code gets access denied on S3. Which role do you fix?",
   "The task role, which belongs to your application."),
  ("Why is the first Lambda call slow?", "a <b style=\"display:inline\">cold start</b>", "blue",
   "Why is the first call to a Lambda function slow?",
   "A cold start: a new environment boots the runtime and your code."),
]),

recap(["EC2 VMs · ECS containers · Lambda functions",
       "Families t / m / c / r · On-Demand, Savings, Spot",
       "ALB spreads load · Auto Scaling keeps N healthy",
       "ECS: task definition, service · execution vs task role",
       "Lambda: events, cold starts, concurrency",
       "Spring Boot API → ECS Fargate behind an ALB"],
  "Let's recap. EC2 gives virtual machines, ECS runs containers, Lambda runs functions. Instance families match workloads, and pricing ranges from on demand to savings plans and spot. Load balancers spread traffic while auto scaling keeps enough healthy instances. ECS uses task definitions and services, with an execution role for ECS and a task role for your code. Lambda reacts to events, with cold starts and concurrency limits. And a Spring Boot API usually belongs on ECS Fargate. Tomorrow: storage with S3."),
]
