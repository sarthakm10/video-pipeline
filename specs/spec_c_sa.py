from conc import *

TAG = "DSA · String Algorithms"
TRACK = "Java Fullstack · DSA"
FILE = "DSA String Algorithms.mp4"

SLIDES = [
title_slide(0, "String Algorithms", "KMP, Z and Manacher: never re-read what you've already matched",
  "Welcome. Today's concept: string matching algorithms.",
  "Finding a pattern inside a text sounds trivial, and for everyday code index of is fine. But the naive approach can re-read the same characters again and again. A few classic algorithms remember what they've already matched, and run in linear time. By the end you'll know the prefix function, KMP search and its tricks, the Z algorithm, Manacher for palindromes, and when to use rolling hashes instead.",
  pill="DSA · CONCEPT"),

{"html": H("Why naive matching is ", "slow") + col(
   cells(list("aaaaaaab"), 0, 3, 0, "text", size=36),
   cells(list("aaab"), None, None, 0, "pattern", size=36, mark={3: "#fecaca"}),
   cells(list("aaaaaaab"), 1, 4, 1, "next try", size=36), gap=14) +
   note("Naive: O(n · m) · the fix: on a mismatch, reuse what already matched", 2),
 "steps": [
  "The naive way tries the pattern at every position. Here the pattern a a a b matches three characters, then fails on the fourth.",
  "Then it shifts by one and starts over, re-reading characters it has already seen. On inputs like this, that's n times m work.",
  "But after matching a a a, we already know what the text looks like there. The smart algorithms use that knowledge, so the text pointer never moves backwards.",
 ]},

{"html": H("The prefix function (", "LPS)") + sub("lps[i] = longest proper prefix of p[0..i] that is also a suffix") + row(
   col(cells(list("aabaab"), None, None, 0, "pattern", size=40),
       cells([0, 1, 0, 1, 2, 3], None, None, 1, "lps", size=40, mark={5: "#bbf7d0"}), gap=14),
   code("""§2 int[] lps = new int[m];
§2 for (int i = 1, len = 0; i < m; ) {
§2   if (p.charAt(i) == p.charAt(len)) lps[i++] = ++len;
§3   else if (len > 0) len = lps[len - 1];   // fall back
§2   else lps[i++] = 0;
§2 }""", 22, style="flex:1"), gap=28, top=True) +
   note("Last value 3: \"aab\" is both a prefix and a suffix of \"aabaab\"", 1),
 "steps": [
  "Everything starts with one array, the prefix function, also called LPS. For each position, it stores the length of the longest proper prefix of the pattern that also ends at that position.",
  "For a a b a a b: the last value is three, because a a b is both how the pattern starts and how it ends.",
  "It's built in linear time. Keep a length, the current matched prefix. If the next characters match, extend it.",
  "If they don't, don't restart from zero. Fall back to the next shorter prefix that's also a suffix, which the array already knows: lps of length minus one. That fallback is the whole trick.",
 ]},

{"html": H("KMP ", "search") + row(
   col(box("blue", "on a match", "advance both pointers", 0),
       box("red", "on a mismatch", "<code>j = lps[j − 1]</code> · the text pointer <b style=\"display:inline\">never</b> goes back", 1),
       box("green", "the shortcut", "compute LPS of <code>pattern + \"#\" + text</code> · a value equal to <code>m</code> = a match", 2), gap=16, style="width:700px"),
   code("""§0 for (int i = 0, j = 0; i < n; i++) {
§1   while (j > 0 && t.charAt(i) != p.charAt(j)) j = lps[j - 1];
§0   if (t.charAt(i) == p.charAt(j)) j++;
§0   if (j == m) { found(i - m + 1); j = lps[j - 1]; }
§0 }""", 25, style="flex:1"), top=True) +
   note("O(n + m) time · O(m) extra space", 3),
 "steps": [
  "KMP search walks the text once, with j counting how much of the pattern currently matches. On a match, both advance.",
  "On a mismatch, j falls back using the LPS array, to the longest prefix that still matches the text we've read. The text pointer never goes backwards.",
  "A neat shortcut: build the LPS array of the pattern, a separator, and the text. Wherever the value equals the pattern length, the pattern ends there.",
  "So search is linear in the text plus the pattern.",
 ]},

{"html": H("LPS ", "tricks") + table(["Problem", "Idea"], [
     (["repeated substring pattern", "<code>p = n − lps[n−1]</code> · repeats if <code>lps[n−1] &gt; 0</code> and <code>n % p == 0</code>"], 0),
     (["longest happy prefix", "it's just <code>s.substring(0, lps[n−1])</code>"], 1),
     (["shortest palindrome (add in front)", "LPS of <code>s + \"#\" + reverse(s)</code> → longest palindromic prefix"], 2)], size=29) +
   note("\"abcabc\": lps ends with 3 → period 3 → \"abc\" × 2", 0),
 "steps": [
  "The LPS array answers more than search. Does a string consist of a repeated block? The smallest period is the length minus the last LPS value. If that period divides the length, the string repeats.",
  "The longest prefix that's also a suffix is literally the last LPS value.",
  "And to make a string a palindrome by adding characters in front, find its longest palindromic prefix. Compute LPS of the string, a separator, and its reverse. The last value is that prefix's length.",
 ]},

{"html": H("The Z-", "algorithm") + sub("z[i] = length of the longest substring starting at i that matches a prefix") + row(
   col(cells(list("aabxaab"), None, None, 0, "s", size=40),
       cells(["–", 1, 0, 0, 3, 1, 0], None, None, 0, "z", size=40, mark={4: "#bbf7d0"}), gap=14),
   col(box("blue", "the Z-box [l, r]", "the rightmost match found so far · inside it, copy from <code>z[i − l]</code>, then extend", 1),
       box("green", "search", "<code>pattern + \"$\" + text</code> · <code>z[i] == m</code> → match", 2), gap=16, style="flex:1"), gap=40, top=True),
 "steps": [
  "The Z algorithm builds a different array. At each position, how long does the string from here match the start of the string? At position four of a a b x a a b, three characters match.",
  "It's linear thanks to the Z box: the rightmost window known to match the prefix. A position inside it already has a mirror position near the start, so copy that value, capped at the box edge, and only extend beyond what's known.",
  "For search, compute Z of the pattern, a separator, and the text. Any value equal to the pattern length is a match. Same power as KMP, and many people find it easier to remember.",
 ]},

{"html": H("Manacher and choosing an ", "algorithm") + row(
   col(box("purple", "Manacher", "longest palindromic substring in <b style=\"display:inline\">O(n)</b> · insert <code>#</code> between chars, reuse the mirror's radius", 0),
       box("orange", "in an interview", "expand around each centre: O(n²), much simpler, usually enough", 1), gap=16, style="width:760px"),
   table(["Need", "Use"], [
     (["one pattern in a text", "<b>KMP</b> or <b>Z</b>"], 2),
     (["many patterns / substring equality", "<b>rolling hash</b> (Rabin-Karp)"], 2),
     (["longest palindrome", "expand around centre · Manacher"], 2),
     (["everyday code", "<code>indexOf</code> / <code>contains</code>"], 2)], size=27), top=True),
 "steps": [
  "Manacher does for palindromes what KMP does for matching. Put a separator between characters so even and odd palindromes look the same. Then each centre reuses the radius of its mirror inside the current rightmost palindrome. Linear time.",
  "But in interviews, expanding around each centre is quadratic, far simpler, and usually accepted. Mention Manacher as the follow up.",
  "To choose: one pattern, use KMP or Z. Many patterns, or comparing lots of substrings, use a rolling hash. Palindromes, expand around centres. And in everyday code, the built in index of is fine.",
 ]},

quiz([
  ("lps[i] means…?", "longest proper prefix that's also a <b style=\"display:inline\">suffix</b> of p[0..i]", "blue",
   "Quiz time. What does the LPS value at position i mean?",
   "The length of the longest proper prefix of the pattern, up to i, that is also a suffix there."),
  ("KMP mismatch: what moves?", "only <b style=\"display:inline\">j</b>: <code>j = lps[j−1]</code>", "red",
   "In KMP, on a mismatch, what moves?",
   "Only the pattern pointer, which falls back to lps of j minus one. The text pointer never goes back."),
  ("Time for KMP?", "<b style=\"display:inline\">O(n + m)</b>", "green",
   "What's the time complexity of KMP search?",
   "Linear: the text length plus the pattern length."),
]),

recap(["Naive matching re-reads: O(n · m)",
       "LPS: longest prefix that's also a suffix",
       "KMP: fall back with lps · text never rewinds",
       "pattern + # + text → matches where value = m",
       "Z-array: match length with the prefix",
       "Palindromes: expand around centre · Manacher O(n)"],
  "Let's recap. Naive matching re-reads characters, costing n times m. The LPS array stores the longest prefix that's also a suffix. KMP uses it to fall back without ever rewinding the text, in linear time. Joining the pattern, a separator, and the text turns search into one array. The Z array measures matches with the prefix. And for palindromes, expand around centres, or use Manacher for linear time. Now practise the problems listed in your notes!"),
]
