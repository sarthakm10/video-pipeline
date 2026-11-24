from conc import *

TAG = "Day 99 · DSA Mock: A Timed Coding Round"
TRACK = "Java Fullstack · Interview Prep"
FILE = "Day 99 DSA Mock A Timed Coding Round.mp4"

SLIDES = [
title_slide(99, "DSA Mock: A Timed Coding Round", "Two mediums and a hard in 90 minutes, out loud",
  "Welcome to day ninety nine: a timed coding round, run like the real thing.",
  "Today you rehearse the first round of tomorrow's full mock. The problems matter less than the routine: interviewers grade how you think as much as whether your code works. By the end you'll have a five step routine for any coding question, a checklist of edge cases, a plan for the ninety minutes, and what to do when you're stuck.",
  pill="DAY 99 · MOCK"),

{"html": H("The five-step ", "routine") + graph(
   {"1": (100, 120), "2": (310, 120), "3": (520, 120), "4": (730, 120), "5": (940, 120)},
   [("1", "2"), ("2", "3"), ("3", "4"), ("4", "5")],
   colors={"1": ("#dbeafe", "#2563eb"), "2": ("#ede9fe", "#7c3aed"), "3": ("#fef3c7", "#d97706"), "4": ("#dcfce7", "#16a34a"), "5": ("#fee2e2", "#dc2626")},
   labels={"1": "clarify", "2": "approach + Big-O", "3": "code", "4": "test", "5": "final Big-O"},
   w=1040, h=240, directed=True, step=0, r=48) + row(
   box("blue", "talk the whole time", "silence looks like being stuck", 1, "flex:1"),
   box("purple", "approach before code", "get a nod before you type", 2, "flex:1"),
   box("green", "they grade the reasoning", "a clean plan beats a rushed answer", 3, "flex:1"), top=True, style="margin-top:6px"),
 "steps": [
  "Use the same five steps for every problem. Clarify the question. Explain your approach and its complexity. Write the code. Test it by walking through an example. And state the final time and space complexity.",
  "Think out loud throughout. Silence looks like being stuck, even when you're not.",
  "Always explain your approach before coding, and get a nod from the interviewer. It catches a wrong idea before you spend twenty minutes on it.",
  "Interviewers grade your reasoning and communication, not just the final answer. A clear plan, well explained, beats a rushed answer.",
 ]},

{"html": H("Step 1: ", "clarify") + row(
   col(box("blue", "a toy question", "\"Does this list contain a duplicate?\"", 0),
       pts([("Can the list be empty? → return false", 1),
            ("Numbers only? Negatives? → yes, any int", 1),
            ("How big? → up to a million", 2),
            ("Can I change the input? → no", 2)], size=27), gap=14, style="flex:1"),
   col(box("green", "why ask", "edge cases and limits decide the approach", 1),
       box("orange", "size → target", "a million items → aim for O(n log n) or better", 2), gap=14, style="width:520px"), top=True),
 "steps": [
  "Take a toy question: does this list contain a duplicate? Before writing anything, ask questions.",
  "Can it be empty? What values can appear? Each answer becomes an edge case you'll test later.",
  "Ask how big the input can be, and whether you may change it. A million items rules out a quadratic solution, so you're aiming for n log n or better. These answers decide your approach.",
 ]},

{"html": H("Step 2: from brute force to ", "better") + table(["Idea", "Time", "Space", "Say"], [
     (["compare every pair", "O(n²)", "O(1)", "correct, too slow for a million"], 0),
     (["sort, then check neighbours", "O(n log n)", "O(1)*", "but it changes the input"], 1),
     (["remember what you've seen in a HashSet", "O(n)", "O(n)", "trade memory for time ✓"], 2)], size=27) +
   note("Start with brute force out loud, then improve: it shows how you think", 3),
 "steps": [
  "Start by saying the brute force: compare every pair. It's correct, but quadratic, too slow for a million items.",
  "Then improve. Sorting puts duplicates next to each other, so n log n. But we were told not to change the input.",
  "Remembering seen values in a hash set gives linear time, using extra memory. That trade, memory for time, is the most common improvement in interviews.",
  "Saying the brute force first isn't wasted time: it proves you understand the problem, and shows how you think your way to something better.",
 ]},

{"html": H("Steps 3–5: code, test, ", "complexity") + row(
   code("""§0 boolean hasDuplicate(int[] nums) {
§0   Set<Integer> seen = new HashSet<>();
§0   for (int n : nums) {
§0     if (!seen.add(n)) return true;   // add → false if present
§0   }
§0   return false;
§0 }""", 23, style="flex:1"),
   col(table(["Edge case", "Expect"], [
     (["empty array", "false"], 1),
     (["one element", "false"], 1),
     (["duplicate at the end", "true"], 1),
     (["negatives, MIN/MAX", "works"], 1)], size=25),
       box("purple", "say it", "O(n) time · O(n) space", 2), gap=14, style="width:480px"), top=True),
 "steps": [
  "Write clean code with clear names. Small helpers and Java's own tools, like the fact that a set's add returns false when the value is already there, keep it short.",
  "Then test before saying you're done. Walk through a small example, then the edge cases from step one: empty, one element, the duplicate right at the end, and extreme values.",
  "Finish by stating the complexity: linear time and linear space.",
 ]},

{"html": H("The 90 minutes, and when ", "stuck") + row(
   col(table(["Problem", "Budget"], [
     (["medium 1", "25 min"], 0),
     (["medium 2", "25 min"], 0),
     (["hard", "35 min"], 0),
     (["review", "5 min"], 0)], size=27), style="width:420px"),
   col(box("orange", "stuck?", "say what you've tried · try a smaller example · think of a pattern", 1),
       box("blue", "patterns to try", "two pointers · sliding window · hash map · heap · BFS/DFS · DP", 1),
       box("green", "afterwards", "write down what slowed you · that's tomorrow's focus", 2), gap=14, style="flex:1"), top=True),
 "steps": [
  "Budget your ninety minutes: about twenty five minutes per medium, thirty five for the hard one, and five to review. If a medium overruns, move on and come back.",
  "When you're stuck, say what you've tried. Work a smaller example by hand, and run through the patterns you know: two pointers, sliding window, a hash map, a heap, BFS or DFS, dynamic programming. Interviewers often give a hint when you reason out loud.",
  "Afterwards, write down what slowed you down. That's exactly what to review before the real interviews.",
 ]},

quiz([
  ("When do you explain your approach?", "<b style=\"display:inline\">before</b> writing code", "blue",
   "Quiz time. When should you explain your approach?",
   "Before writing any code."),
  ("A million items: is O(n²) OK?", "<b style=\"display:inline\">no</b>: aim for O(n log n) or better", "orange",
   "The input has a million items. Is a quadratic solution acceptable?",
   "No. Aim for n log n or better."),
  ("Code done: what next?", "<b style=\"display:inline\">test</b> with an example and edge cases", "green",
   "You've finished the code. What do you do next?",
   "Test it: walk through an example and the edge cases."),
]),

recap(["Clarify → approach → code → test → Big-O",
       "Think out loud · approach before code",
       "Input size tells you the target complexity",
       "Brute force first, then improve",
       "Test edge cases: empty, one, ends, extremes",
       "Budget time · when stuck, try patterns"],
  "Let's recap. Every coding question follows the same routine: clarify, explain the approach with its complexity, code, test, and state the final complexity. Think out loud, and agree the approach before typing. The input size tells you what complexity to aim for. Say the brute force, then improve it. Test with an example and the edge cases. And budget your time, trying known patterns when you're stuck. Tomorrow: the final mock interview."),
]
