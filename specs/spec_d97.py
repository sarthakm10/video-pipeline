from conc import *

TAG = "Day 97 · Behavioral Interviews"
TRACK = "Java Fullstack · Interview Prep"
FILE = "Day 97 Behavioral Interviews and Final Weak Areas.mp4"

SLIDES = [
title_slide(97, "Behavioral Interviews", "How you talk about your work is what gets you hired",
  "Welcome to day ninety seven: behavioral interviews and your last weak areas.",
  "Technical skill gets you shortlisted, but every interview also asks about you: how you work, solve problems and learn. These questions are the easiest to prepare for, because you can write your answers in advance. By the end you'll know the STAR method, a sixty second answer to tell me about yourself, and stories for the questions that come up most.",
  pill="DAY 97 · INTERVIEW PREP"),

{"html": H("The STAR ", "method") + graph(
   {"S": (110, 110), "T": (360, 110), "A": (610, 110), "R": (860, 110)},
   [("S", "T"), ("T", "A"), ("A", "R")],
   colors={"S": ("#dbeafe", "#2563eb"), "T": ("#ede9fe", "#7c3aed"), "A": ("#fef3c7", "#d97706"), "R": ("#dcfce7", "#16a34a")},
   labels={"S": "Situation", "T": "Task", "A": "Action", "R": "Result"}, w=980, h=230, directed=True, step=0, r=56) + row(
   box("blue", "Situation + Task", "brief · the context and what <b style=\"display:inline\">you</b> had to do", 0, "flex:1"),
   box("orange", "Action", "the longest part · say <b style=\"display:inline\">I</b>, not we · the steps you took", 1, "flex:1"),
   box("green", "Result", "what changed · numbers if you can · what you learned", 2, "flex:1"), top=True, style="margin-top:6px") +
   note("About two minutes per story · projects, college work and internships all count", 3),
 "steps": [
  "STAR gives every story a clear shape. Situation: the context, in a sentence or two. Task: what you specifically had to achieve.",
  "Action is the longest part: the steps you took. Say I, not we. The interviewer is hiring you, not your team.",
  "Result: what changed, with numbers if possible, and what you learned.",
  "Keep each story to about two minutes. As a fresher, your stories can come from projects, including this course's capstone, from college work, internships, or anything you organised.",
 ]},

{"html": H("\"Tell me about ", "yourself\"") + row(
   code("""§0 [0–15 s]  who you are now
§0            "I'm a Java backend developer…"
§1 [15–40 s] what you've built
§1            "…a Spring Boot API with JWT, PostgreSQL,
§1             tests and CI, deployed with Docker…"
§2 [40–60 s] why this role
§2            "…and I'd like to grow on a team that…"
""", 22, style="flex:1"),
   col(box("blue", "about 60 seconds", "it's almost always the first question", 0),
       box("green", "a trailer, not the film", "mention things they'll want to ask about", 1),
       box("red", "avoid", "your life story · reading your CV · \"I'm a hard worker\"", 2), gap=14, style="width:480px"), top=True),
 "steps": [
  "Tell me about yourself is almost always first, so prepare a sixty second answer. Start with who you are now, for example a Java backend developer.",
  "Then what you've built, with the stack. Think of it as a trailer: mention things like JWT or the N plus one fix that you'd be happy to be asked about.",
  "Finish with why you want this role. Avoid your life story, reading your CV aloud, or claims with no evidence. Practise until it sounds natural, not recited.",
 ]},

{"html": H("Two stories to ", "prepare") + row(
   col(box("orange", "made it faster", "", 0),
       pts([("<b>S</b> the projects list took 2 s", 0),
            ("<b>T</b> find out why", 0),
            ("<b>A</b> enabled SQL logging → 101 queries → <code>JOIN FETCH</code>", 0),
            ("<b>R</b> 2 queries, 2 s → 80 ms · added a test", 0)], size=25), gap=10, style="flex:1"),
   col(box("purple", "a hard bug", "", 1),
       pts([("<b>S</b> some users saw others' tasks", 1),
            ("<b>T</b> find and fix it, fast", 1),
            ("<b>A</b> reproduced it in a failing test → missing owner check", 1),
            ("<b>R</b> fixed · the test stops it coming back", 1)], size=25), gap=10, style="flex:1"), top=True) +
   note("Always say how you measured it, and how you stopped it happening again", 2),
 "steps": [
  "Prepare a story about making something faster. For example: the projects list took two seconds. With SQL logging on, you found a hundred and one queries, the N plus one problem. A join fetch cut it to two queries and eighty milliseconds.",
  "And a debugging story. Some users could see other people's tasks. You reproduced it with a failing test, found a missing ownership check, fixed it, and the test now stops it coming back.",
  "Both stories work because they have numbers and a clear ending. Always say how you measured, and how you made sure it can't happen again.",
 ]},

{"html": H("The other common ", "questions") + table(["Question", "What they want to hear"], [
     (["Conflicting priorities?", "clarify what matters most · say early if something won't fit"], 0),
     (["Learned something quickly?", "how you learned: a plan, daily practice, building projects"], 1),
     (["A disagreement?", "you listened, used data, and committed to the decision"], 2),
     (["A failure?", "a real one · what you changed afterwards"], 2),
     (["Why this company?", "something specific you found out about them"], 3)], size=27),
 "steps": [
  "For conflicting priorities, they want to hear that you ask what matters most, and say early when something won't fit, instead of silently dropping work.",
  "For learning something quickly, you have a great answer: you went from no Java to a secured, tested Spring Boot API with Kafka and AWS in a hundred days. Describe how: a plan, daily practice, and building projects.",
  "For a disagreement, show you listened, used facts, and then committed to the team's decision. For a failure, pick a real one, and focus on what you changed afterwards.",
  "And for why this company, mention something specific you found out about them. A generic answer shows you didn't look.",
 ]},

{"html": H("Close your last ", "gaps") + row(
   box("blue", "Backlog &amp; Stats", "one last pass over missed notes and unchecked topics", 0, "flex:1"),
   box("green", "explain out loud", "your five hardest concepts · to a friend, a mirror or a recording", 1, "flex:1"),
   box("purple", "three problems", "from your weakest DSA areas · no timer · understand fully", 2, "flex:1"), top=True) +
   box("orange", "a 1-minute pitch per project", "what it does · the stack · the hardest problem · what you'd improve", 3, "margin-top:20px"),
 "steps": [
  "Use the rest of today to close gaps. Take one last pass through Backlog and Stats.",
  "Pick the five concepts you find hardest to explain, and explain each out loud. Fluent explanation is exactly what interviews test.",
  "Solve three problems from your weakest DSA areas with no timer, aiming for full understanding rather than speed.",
  "And prepare a one minute pitch for each project on your CV: what it does, the stack, the hardest problem you solved, and what you'd improve.",
 ]},

quiz([
  ("Which STAR part should be longest?", "<b style=\"display:inline\">Action</b>", "orange",
   "Quiz time. Which part of a STAR answer should be the longest?",
   "Action: what you did."),
  ("\"We\" or \"I\" in your stories?", "<b style=\"display:inline\">I</b>: what you did", "blue",
   "Should you say we or I in your stories?",
   "I. They're hiring you, so say what you personally did."),
  ("What makes a performance story strong?", "<b style=\"display:inline\">numbers</b> before and after", "green",
   "What makes a performance story strong?",
   "Numbers: what you measured before and after."),
]),

recap(["STAR: Situation, Task, Action, Result",
       "Action longest · say I · about 2 minutes",
       "Tell me about yourself: 60 s, now → built → why",
       "Speed story with numbers · bug story with a test",
       "Priorities: clarify and say it early",
       "Explain your hard five out loud · pitch each project"],
  "Let's recap. Shape every story with STAR: situation, task, action and result. Make the action the longest part, say I, and keep it to about two minutes. Tell me about yourself is sixty seconds: who you are, what you've built, and why this role. Prepare a performance story with numbers and a debugging story that ends with a test. For conflicting priorities, clarify and say it early. Then explain your five hardest concepts aloud, and prepare a pitch for each project. Tomorrow: your resume, LinkedIn and project story."),
]
