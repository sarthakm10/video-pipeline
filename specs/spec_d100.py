from conc import *

TAG = "Day 100 · Final Mock Interview Day"
TRACK = "Java Fullstack · Interview Prep"
FILE = "Day 100 Final Mock Interview Day.mp4"

SLIDES = [
title_slide(100, "Final Mock Interview Day", "One hundred days from Hello World: put it all together",
  "Welcome to day one hundred: your final mock interview.",
  "A hundred days ago you printed Hello World. Since then you've learned object oriented Java, collections, streams and threads, data structures and algorithms, Spring Boot with PostgreSQL, security and tests, and how real systems scale with Docker, Kafka and AWS. Today you run a full mock interview: a coding round, a system design round and a Java and Spring deep dive. Then you celebrate.",
  pill="DAY 100 · MOCK"),

{"html": H("Run it like the real ", "thing") + table(["Round", "Time", "From"], [
     (["coding: 2 mediums + 1 hard", "90 min", "Day 99 routine"], 0),
     (["system design: a new problem", "45 min", "Day 92 framework"], 1),
     (["Java / Spring deep-dive + your project", "30 min", "Days 94–98"], 1)], size=28) +
   note("Quiet room · a timer · no notes · a friend as interviewer, or record yourself", 2),
 "steps": [
  "The full mock has three rounds. First, yesterday's coding round: two mediums and a hard in ninety minutes, using the five step routine.",
  "Then a forty five minute system design round on a problem you haven't practised, and a thirty minute deep dive on Java, Spring and your project.",
  "Set it up like the real thing: a quiet room, a timer and no notes. Ask a friend to play the interviewer, or record yourself and watch it back. You'll spot habits you never noticed.",
 ]},

{"html": H("System design: a ride-sharing ", "app") + table(["Step", "Say"], [
     (["requirements", "riders request · drivers accept · live location · ~1M rides/day"], 0),
     (["API", "<code>POST /rides</code> · <code>PUT /drivers/{id}/location</code> · WebSocket for updates"], 1),
     (["high level", "LB → ride service, location service, matching · Kafka between them"], 1),
     (["data", "rides in PostgreSQL · driver locations in Redis (geo index)"], 2),
     (["deep dive", "matching: nearest free drivers by geo cell · lock a driver per ride"], 3),
     (["scale", "location writes every 4 s → shard by city · stateless services"], 3)], size=26),
 "steps": [
  "Here's how the framework handles a problem you've never practised, a ride sharing app. Start with requirements: riders request rides, drivers accept, locations update live, and some numbers, like a million rides a day.",
  "Sketch the API: request a ride, update a driver's location, and a WebSocket for live updates. Then the high level design: a load balancer in front of ride, location and matching services, talking through Kafka.",
  "For data, rides belong in PostgreSQL, while fast changing driver locations go in Redis, with its geo index.",
  "Then deep dive into the hardest part, matching: find the nearest free drivers by map cell, and lock a driver so two rides can't grab them. Location updates every few seconds are the heaviest load, so shard by city and keep services stateless.",
 ]},

{"html": H("The Java and Spring ", "deep-dive") + row(
   box("blue", "HashMap internals", "hash → bucket → equals → tree at 8 → resize at 0.75", 0, "flex:1"),
   box("orange", "N+1 and @Transactional", "lazy loading per row · JOIN FETCH · proxies, self-calls, checked exceptions", 1, "flex:1"),
   box("purple", "auto-config and beans", "conditions on classpath and beans · create → inject → init → destroy", 2, "flex:1"), top=True) +
   box("green", "then: \"tell me about a project you built\"", "your capstone · the 2-minute diagram · decisions with trade-offs · a story with numbers", 3, "margin-top:20px"),
 "steps": [
  "After twenty rapid fire questions come three you should be able to explain in depth. HashMap internals: hashing to a bucket, equals, trees at eight, resizing at three quarters full.",
  "The N plus one problem and transactional pitfalls: lazy loading per row, join fetch, and the proxy that self calls skip.",
  "And how auto configuration decides what to create, plus the bean lifecycle.",
  "Then walk through your capstone as if asked to describe a project: the two minute diagram, your decisions with their trade offs, and a story with numbers.",
 ]},

{"html": H("Before the real ", "interviews") + row(
   col(pts([("✅ progress reviewed, weak list cleared", 0),
            ("✅ resume final · LinkedIn and GitHub updated", 0),
            ("✅ questions to ask · salary range · availability", 1),
            ("✅ cheat sheet read · a good night's sleep", 1)], size=28), style="flex:1"),
   col(box("blue", "they're not looking for", "someone who knows everything", 2),
       box("green", "they're looking for", "strong fundamentals · clear reasoning · keeps learning", 2), gap=14, style="width:560px"), top=True),
 "steps": [
  "Before real interviews, run this checklist. Progress reviewed and your weak list cleared. Resume final, LinkedIn and GitHub up to date.",
  "Logistics ready: your questions for them, your salary expectations, and when you can start. Read your cheat sheet, and get a good night's sleep.",
  "And remember: interviewers aren't looking for someone who knows everything. They want strong fundamentals, clear reasoning, and someone who keeps learning.",
 ]},

{"html": H("What you did in 100 ", "days") + graph(
   {"Java": (100, 140), "DSA": (300, 140), "Spring": (500, 140), "Cloud": (700, 140), "Ready": (900, 140)},
   [("Java", "DSA"), ("DSA", "Spring"), ("Spring", "Cloud"), ("Cloud", "Ready")],
   colors={"Java": ("#dbeafe", "#2563eb"), "DSA": ("#ede9fe", "#7c3aed"), "Spring": ("#dcfce7", "#16a34a"), "Cloud": ("#fef3c7", "#d97706"), "Ready": ("#fee2e2", "#dc2626")},
   w=1000, h=200, directed=True, step=0, r=54) + table(["Stage", "You learned"], [
     (["Java", "OOP · collections · streams · threads"], 0),
     (["DSA", "patterns · trees · graphs · dynamic programming"], 0),
     (["Spring", "REST APIs · JPA · security · tests"], 0),
     (["Cloud", "Docker · Kafka · AWS · system design"], 0)], size=26) +
   note("You learned it from zero, step by step. Walk in and show them.", 1),
 "steps": [
  "Look at the path you've walked. Java from the basics to streams and threads. Data structures and algorithms, from arrays to graphs and dynamic programming. Spring Boot with JPA, security and tests. And the cloud: Docker, Kafka and AWS.",
  "You learned all of it from zero, one day at a time. You've spent a hundred days proving you can learn hard things. Now walk in and show them.",
 ]},

quiz([
  ("System design: first step?", "<b style=\"display:inline\">requirements</b> and numbers", "blue",
   "Quiz time. In a system design round, what comes first?",
   "Requirements, with rough numbers."),
  ("Fast-changing driver locations: store where?", "<b style=\"display:inline\">Redis</b> (geo index)", "red",
   "Where would you keep fast changing driver locations?",
   "In Redis, using its geo index."),
  ("What are interviewers really looking for?", "fundamentals, <b style=\"display:inline\">clear reasoning</b>, learning", "green",
   "What are interviewers really looking for?",
   "Strong fundamentals, clear reasoning, and the ability to keep learning."),
]),

recap(["Mock: coding 90 · design 45 · deep-dive 30",
       "Design: requirements → API → high level → data → deep dive",
       "Deep-dive: HashMap · N+1 + @Transactional · auto-config",
       "Your project: diagram, trade-offs, a story with numbers",
       "Checklist: resume, GitHub, questions, sleep",
       "From Hello World to job-ready 🎉"],
  "Let's recap. The full mock is a ninety minute coding round, a forty five minute design round, and a thirty minute deep dive. For design, go from requirements to API, high level design, data and a deep dive. Be ready to explain HashMap internals, N plus one and transactional pitfalls, and auto configuration, and to walk through your project with its trade offs. Then tick off your checklist and rest. Congratulations: you've gone from Hello World to job ready in a hundred days. Go and get that offer."),
]
