from conc import *

TAG = "Day 98 · Resume, LinkedIn and Your Project Story"
TRACK = "Java Fullstack · Interview Prep"
FILE = "Day 98 Resume LinkedIn and Your Project Story.mp4"

SLIDES = [
title_slide(98, "Resume, LinkedIn & Your Project", "Be easy to find, and ready to go deep on what you built",
  "Welcome to day ninety eight: your resume, LinkedIn, GitHub and project story.",
  "Interviewers will pick one project and go deep, so today you'll prepare to walk through your capstone: its architecture, its trade offs and its stories. Then we'll polish your resume, LinkedIn and GitHub, and cover the Git workflow teams expect you to know on day one: branches, pull requests, merge versus rebase, and conflicts.",
  pill="DAY 98 · INTERVIEW PREP"),

{"html": H("Your project on a ", "whiteboard") + code("§0 client → JWT filter → controller → service → repository → PostgreSQL", 26) + row(
   col(table(["Layer", "Its job"], [
     (["security filter", "check the JWT · who is calling?"], 0),
     (["controller", "HTTP in/out · validate the input"], 0),
     (["service", "business rules · <code>@Transactional</code>"], 0),
     (["repository + DB", "Spring Data JPA · PostgreSQL · Flyway"], 0)], size=25), style="flex:1"),
   col(box("blue", "draw it in 2 minutes", "request path first · then tests, CI, Docker", 0),
       box("purple", "expect \"why?\"", "every box is a decision they can question", 1), gap=14, style="width:500px"), top=True, style="margin-top:16px"),
 "steps": [
  "Practise drawing your capstone in two minutes. Follow one request: the client sends it, the security filter checks the JWT, the controller validates input, the service applies the rules in a transaction, and the repository talks to PostgreSQL, whose schema Flyway manages. Then mention tests, CI and Docker.",
  "Expect the interviewer to point at any box and ask why. So prepare your design decisions next.",
 ]},

{"html": H("Decisions and their ", "trade-offs") + table(["Decision", "Why", "Downside"], [
     (["Flyway, not <code>ddl-auto</code>", "versioned, reviewed schema changes", "you write every migration"], 0),
     (["other users' tasks → 404, not 403", "doesn't reveal what exists", "harder to debug"], 1),
     (["page size capped at 100", "no huge responses", "clients must page"], 1),
     (["JWT, not sessions", "stateless · any server can answer", "can't easily revoke a token"], 2)], size=26) +
   note("Every decision has a downside · naming it is what shows understanding", 3),
 "steps": [
  "Pick three or four decisions and know why you made them. Flyway instead of letting Hibernate create tables: schema changes are versioned and reviewed, at the cost of writing each migration.",
  "Returning not found for another user's task hides what exists, but makes debugging harder. Capping page size protects the server, but clients must page.",
  "And JWT instead of sessions keeps servers stateless, but you can't easily revoke a token before it expires.",
  "Notice that each row has a downside. Naming it, without being asked, is exactly what shows real understanding.",
 ]},

{"html": H("Resume bullets that show ", "impact") + table(["Weak", "Strong"], [
     (["Worked on a REST API", "Built a Spring Boot REST API with JWT auth and 40 tests"], 0),
     (["Improved performance", "Fixed an N+1 issue: 101 queries → 2, 2 s → 80 ms"], 1),
     (["Used Docker and CI", "Automated build, tests and Docker image on every push"], 1),
     (["Knows Java, Spring, Kafka, AWS, K8s, React…", "only what you can discuss for 10 minutes"], 2)], size=27),
 "steps": [
  "A strong bullet starts with a verb, says what you built, and shows impact. Not worked on a REST API, but built a Spring Boot API with JWT authentication and forty tests.",
  "Numbers make it real: a hundred and one queries down to two, two seconds down to eighty milliseconds. Automated, built, reduced, designed: strong verbs.",
  "And list only technologies you can talk about for ten minutes. Every word on your resume is a possible interview question.",
 ]},

{"html": H("Git: the team ", "workflow") + row(
   graph({"main": (80, 120), "branch": (290, 120), "PR": (500, 120), "merged": (710, 120)},
         [("main", "branch"), ("branch", "PR"), ("PR", "merged")],
         colors={"PR": ("#ede9fe", "#7c3aed"), "merged": ("#dcfce7", "#16a34a")},
         labels={"branch": "feature/filter", "PR": "review + CI"},
         w=790, h=230, directed=True, step=0, r=52),
   col(box("blue", "one branch per change", "small · short-lived · named for the work", 0),
       box("purple", "pull request", "a teammate reviews · CI runs the tests", 1),
       box("green", "good commits", "\"Fix N+1 in task list\" · not \"stuff\"", 2), gap=14, style="flex:1"), top=True),
 "steps": [
  "On a team, nobody commits straight to main. You create a short lived branch for one change, named for the work, like feature slash filter.",
  "When it's ready, you open a pull request. A teammate reviews the code, CI runs the tests, and only then is it merged into main. Most teams use this trunk based flow rather than long lived release branches.",
  "Write commit messages that say what changed and why, like fix N plus one in the task list. A history full of messages like stuff or wip is a red flag on your GitHub too.",
 ]},

{"html": H("Merge vs rebase, and ", "conflicts") + row(
   code("""§0 git switch -c feature/x        # new branch
§0 git commit -m "Add task filter"
§1 git merge main                 # keeps history · adds a merge commit
§2 git rebase main                # replays your commits on top · linear
§3 <<<<<<< HEAD
§3 int limit = 50;
§3 =======
§3 int limit = 100;
§3 >>>>>>> feature/x               # choose, edit, git add, continue""", 22, style="flex:1"),
   col(box("blue", "merge", "safe · true history · extra merge commits", 1),
       box("green", "rebase", "clean, linear history · rewrites your commits", 2),
       box("red", "golden rule", "never rebase a branch others have pulled", 2),
       box("orange", "conflict", "both sides changed the same lines · you decide", 3), gap=14, style="width:500px"), top=True),
 "steps": [
  "Your branch falls behind main while you work. There are two ways to catch up.",
  "Merge brings main's changes in with a merge commit. It's safe and keeps the true history, but adds extra commits.",
  "Rebase replays your commits on top of the latest main, giving a clean, straight history. But it rewrites your commits, so never rebase a branch someone else has already pulled.",
  "Either way, if both sides changed the same lines, Git stops with a conflict and shows both versions between markers. You choose the right code, remove the markers, stage the file, and continue. Run the tests before pushing.",
 ]},

{"html": H("LinkedIn, GitHub and your ", "questions") + row(
   box("blue", "LinkedIn", "headline: Java Backend Developer · Spring Boot · SQL · AWS · about = your 60-s pitch", 0, "flex:1"),
   box("green", "GitHub", "pin 2–3 repos, capstone first · good READMEs · tidy history", 1, "flex:1"),
   box("purple", "ask them", "how code reaches production · how new joiners learn · success in 6 months", 2, "flex:1"), top=True) +
   note("Make a one-page cheat sheet of your 20 key topics and read it before each interview", 3),
 "steps": [
  "On LinkedIn, use a clear headline, like Java backend developer, Spring Boot, SQL, AWS. Your about section is a written version of yesterday's sixty second pitch.",
  "GitHub is your portfolio, and recruiters do look. Pin two or three repositories, your capstone first, each with a good README and a tidy history.",
  "Prepare three or four questions for your interviewers: how code reaches production, how new joiners learn, and what success looks like in six months. Good questions show real interest.",
  "Finally, write a one page cheat sheet of the twenty topics you most want to remember, and read it before each interview.",
 ]},

quiz([
  ("Answering \"why Flyway?\": what else should you mention?", "its <b style=\"display:inline\">downside</b>", "orange",
   "Quiz time. You're asked why you chose Flyway. What should your answer include besides the benefits?",
   "The downside. Every decision has one."),
  ("Rebase a branch your teammate already pulled?", "<b style=\"display:inline\">no</b>: merge instead", "red",
   "Should you rebase a branch your teammate has already pulled?",
   "No. Rebasing rewrites commits they depend on. Merge instead."),
  ("Strong resume bullet needs…?", "a verb, what you built, and a <b style=\"display:inline\">number</b>", "green",
   "What does a strong resume bullet need?",
   "A strong verb, what you built, and a measurable result."),
]),

recap(["Draw your project in 2 minutes",
       "Know each decision's trade-off",
       "Bullets: verb + what + number",
       "Branch → PR → review + CI → main",
       "Merge = safe · rebase = linear, never on shared branches",
       "LinkedIn headline · pinned repos · your questions"],
  "Let's recap. Practise drawing your project in two minutes, and know the downside of every decision. Write resume bullets with a strong verb, what you built and a number, and list only what you can discuss. On a team, work in a branch, open a pull request, and merge after review and CI pass. Merge is safe, rebase is linear but never for shared branches, and conflicts mean you choose the right lines. Then polish LinkedIn and GitHub, and prepare questions to ask. Tomorrow: a timed coding mock."),
]
