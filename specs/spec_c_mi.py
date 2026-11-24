from conc import *

TAG = "DSA · Merge Intervals"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Merge Intervals.mp4"


def bars(items, step, label="", w=900, scale=50):
    """Intervals drawn on a number line. items: (start, end, colour). Labels sit right of each bar."""
    h = 40 + 50 * len(items)
    parts = []
    for i, (s, e, c) in enumerate(items):
        y = 14 + 50 * i
        parts.append(f'<rect x="{20 + s * scale}" y="{y}" width="{(e - s) * scale}" height="38" rx="9" fill="{c}" stroke="#334155" stroke-width="2.5"/>'
                     f'<text x="{20 + e * scale + 10}" y="{y + 27}" font-size="24" font-weight="700" font-family="Cascadia Code, monospace" fill="#1f2937">[{s},{e}]</text>')
    ticks = "".join(f'<line x1="{20 + t * scale}" y1="{h - 14}" x2="{20 + t * scale}" y2="{h - 6}" stroke="#94a3b8" stroke-width="2"/>'
                    f'<text x="{20 + t * scale}" y="{h + 14}" font-size="18" text-anchor="middle" fill="#64748b">{t}</text>' for t in range(0, (w - 120) // scale + 1, 2))
    svg = (f'<svg width="{w}" height="{h + 20}" viewBox="0 0 {w} {h + 20}" style="flex-shrink:0">{"".join(parts)}'
           f'<line x1="20" y1="{h - 10}" x2="{w - 100}" y2="{h - 10}" stroke="#94a3b8" stroke-width="2"/>{ticks}</svg>')
    lab = f'<div style="font-size:26px;color:#475569;margin-top:2px">{label}</div>' if label else ""
    return f'<div data-step="{step}">{svg}{lab}</div>'


BLUE, GREEN, RED, PURPLE = "#bfdbfe", "#bbf7d0", "#fecaca", "#e9d5ff"

SLIDES = [
title_slide(0, "Merge Intervals", "Sort by start, then each interval either joins the last group or starts a new one",
  "Welcome. Today's concept: intervals.",
  "Meetings, bookings, time ranges, segments on a line. Interval questions look different on the surface, but almost all of them start the same way: sort, then sweep from left to right making one local decision. By the end you'll know the overlap test, merging, inserting, the greedy end-time rule, counting meeting rooms with a sweep line, and which sort order each question needs.",
  pill="DSA · CONCEPT"),

{"html": H("The overlap ", "test") + row(
   col(bars([(1, 6, BLUE), (4, 9, GREEN)], 0, "overlap", scale=60),
       bars([(1, 4, BLUE), (6, 9, GREEN)], 1, "no overlap", scale=60), gap=18),
   col(box("purple", "two intervals overlap when", "<code>a.start &lt;= b.end &amp;&amp; b.start &lt;= a.end</code>", 2),
       box("orange", "touching ends", "<code>[1,4]</code> and <code>[4,7]</code>: overlap or not? <b style=\"display:inline\">read the question</b> (≤ vs &lt;)", 3), gap=18, style="flex:1"), top=True),
 "steps": [
  "Everything starts with one test. Do two intervals overlap? Here, one to six and four to nine share the stretch from four to six.",
  "Here, one to four ends before six to nine starts. No overlap.",
  "The rule: they overlap when each one starts before the other ends. It's easier to think about the opposite. They don't overlap when one ends before the other starts.",
  "One detail to check in every question: do intervals that only touch, like one to four and four to seven, count as overlapping? For merging, usually yes. For meetings, usually no, since one ends as the next begins. That decides less than or equal versus less than.",
 ]},

{"html": H("Merge: sort by ", "start") + row(
   col(bars([(1, 3, BLUE), (2, 6, BLUE), (8, 10, GREEN), (9, 12, GREEN), (15, 17, PURPLE)], 0, "sorted by start", w=900, scale=44),
       bars([(1, 6, BLUE), (8, 12, GREEN), (15, 17, PURPLE)], 1, "merged", w=900, scale=44), gap=12),
   code("""§0 Arrays.sort(iv, (a, b) -> a[0] - b[0]);
§1 List<int[]> out = new ArrayList<>();
§1 for (int[] x : iv) {
§1   int[] last = out.isEmpty() ? null
§1                : out.get(out.size()-1);
§1   if (last == null || x[0] > last[1])
§1     out.add(x);                  // new group
§2   else last[1] = Math.max(last[1], x[1]);
§1 }""", 23, style="flex:1"), top=True) +
   note("After sorting, only the <u>last</u> merged interval can overlap the next one", 3),
 "steps": [
  "To merge overlapping intervals, first sort them by start. Now overlapping intervals sit next to each other.",
  "Walk through them. If the next interval starts after the last merged one ends, it begins a new group.",
  "Otherwise it overlaps, so stretch the last group's end. Take the maximum, because the new interval might be completely inside the old one.",
  "Why does this work? After sorting, every later interval starts at or after the current one. So only the most recent group can possibly overlap it. One comparison per interval, and the sort dominates: n log n.",
 ]},

{"html": H("Insert into a sorted ", "list") + row(
   box("gray", "1 · before", "intervals that end before the new one starts: copy them", 0, "flex:1"),
   box("blue", "2 · overlapping", "absorb them: <code>start = min</code>, <code>end = max</code>", 1, "flex:1"),
   box("green", "3 · after", "add the merged one, then copy the rest", 2, "flex:1"), top=True) +
   bars([(1, 2, "#e5e7eb"), (3, 5, BLUE), (6, 7, BLUE), (8, 10, BLUE), (12, 16, "#e5e7eb")], 0, "existing (sorted)", w=1400, scale=70) +
   bars([(4, 8, RED)], 1, "new: [4,8] → absorbs [3,5], [6,7], [8,10] → [3,10]", w=1400, scale=70),
 "steps": [
  "Inserting a new interval into a list that's already sorted and merged doesn't even need a sort. It's three phases. First, copy every interval that ends before the new one starts.",
  "Second, every interval that overlaps the new one gets absorbed into it. The start becomes the smallest start, and the end the largest end. Here, four to eight swallows three to five, six to seven, and eight to ten, becoming three to ten.",
  "Third, add the merged interval, and copy everything after it. One linear pass.",
 ]},

{"html": H("Greedy: sort by ", "end") + row(
   col(box("purple", "remove the fewest to make them non-overlapping", "= keep the <b style=\"display:inline\">most</b> non-overlapping intervals", 0),
       box("green", "the rule", "always keep the interval that <b style=\"display:inline\">ends first</b>: it leaves the most room", 1),
       box("blue", "same idea", "fewest arrows to burst balloons · activity selection", 2), gap=18, style="width:640px"),
   code("""§1 Arrays.sort(iv, (a, b) -> Integer.compare(a[1], b[1]));
§1 int kept = 0, end = Integer.MIN_VALUE;
§1 for (int[] x : iv)
§1   if (x[0] >= end) { kept++; end = x[1]; }
§1 return iv.length - kept;""", 24, style="flex:1"), top=True),
 "steps": [
  "A different family. Remove the fewest intervals so that the rest don't overlap. Flip it around: keep as many non-overlapping intervals as possible.",
  "The greedy rule: sort by end time, and always keep the interval that finishes first. It leaves the most room for everything after it. Any other choice ends later, and can only block more.",
  "The same rule solves the fewest arrows to burst balloons, and the classic activity selection problem. Sort by end, and count how many times you have to start a new group. Note the comparator: Integer dot compare, because subtracting two large ints can overflow.",
 ]},

{"html": H("Meeting rooms: the sweep ", "line") + row(
   bars([(0, 30, BLUE), (5, 10, GREEN), (15, 20, PURPLE)], 0, "how many rooms?", w=820, scale=22),
   col(box("blue", "events", "start → +1 · end → −1 · sort by time", 1),
       box("green", "sweep", "running total = meetings happening now · answer = the <b style=\"display:inline\">peak</b>", 2),
       box("orange", "same time?", "process the end (−1) <b style=\"display:inline\">before</b> the start (+1)", 3), gap=16, style="flex:1"), top=True) +
   note("Or: sort starts, keep a min-heap of end times · heap size = rooms in use", 4),
 "steps": [
  "Now count the rooms needed for a set of meetings. One long meeting from zero to thirty, and two short ones inside it.",
  "Turn every meeting into two events: plus one when it starts, minus one when it ends. Sort all events by time.",
  "Sweep through them, keeping a running total. That total is how many meetings are happening right now, and the answer is its highest value. Here it peaks at two.",
  "Ties matter. If one meeting ends at ten and another starts at ten, they can share a room. So process the end before the start.",
  "The other common solution sorts by start, and keeps a min heap of end times. Before each meeting, free the rooms whose meetings have ended. The heap's size is the number of rooms in use.",
 ]},

{"html": H("Which sort ", "order?") + table(["Question", "Sort by", "Then"], [
     (["merge / insert overlapping", "start", "extend the last group"], 0),
     (["keep the most / remove the fewest", "<b>end</b>", "greedy: keep what ends first"], 1),
     (["rooms / max overlap at once", "events by time", "sweep, track the peak"], 2),
     (["remove covered intervals", "start ↑, then end ↓", "track the farthest end"], 3)], size=30) +
   note("Two sorted lists (intersections)? No sort, two pointers: advance whichever ends first", 3),
 "steps": [
  "The biggest decision in an interval question is the sort order. For merging or inserting, sort by start.",
  "To keep the most intervals, or remove the fewest, sort by end, and keep whatever finishes first.",
  "To count rooms or the most overlap at any moment, split into events, sort by time, and sweep.",
  "And to remove intervals covered by another, sort by start, and for equal starts put the longer one first, so it covers the shorter. If you're given two lists that are already sorted, like for intersections, don't sort at all. Use two pointers, and advance whichever interval ends first.",
 ]},

quiz([
  ("Merge intervals: sort by?", "<b style=\"display:inline\">start</b>", "blue",
   "Quiz time. To merge overlapping intervals, what do you sort by?",
   "By start. Then only the last merged interval can overlap the next one."),
  ("Fewest removals to stop all overlaps: sort by?", "<b style=\"display:inline\">end</b>, keep what ends first", "green",
   "Fewest intervals to remove so the rest don't overlap. What do you sort by?",
   "By end time. Greedily keep the interval that ends first."),
  ("Meeting ends at 10, another starts at 10. Same room?", "<b style=\"display:inline\">yes</b>: process the end first", "orange",
   "One meeting ends at ten, and another starts at ten. Can they share a room?",
   "Yes. In the sweep, process the end event before the start event."),
]),

recap(["Overlap: each starts before the other ends",
       "Merge: sort by start, extend or start a new group",
       "Insert: before · absorb overlaps · after",
       "Keep the most: sort by end, greedy",
       "Rooms: +1 / −1 events, the peak is the answer",
       "Touching ends: check ≤ vs <"],
  "Let's recap. Two intervals overlap when each starts before the other ends. To merge, sort by start and either extend the last group or start a new one. To insert, copy what's before, absorb the overlaps, then copy the rest. To keep the most intervals, sort by end and keep whatever finishes first. For meeting rooms, turn intervals into plus one and minus one events, and the peak is the answer. And always check whether touching ends count. Now practise the problems listed in your notes!"),
]
