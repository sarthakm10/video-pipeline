from conc import *

TAG = "DSA · Trie"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Trie.mp4"

E = ("#dcfce7", "#16a34a")   # end of word
P = ("#fde68a", "#d97706")   # on the path

SLIDES = [
title_slide(0, "Trie", "A tree of characters: words that share a prefix share a path",
  "Welcome. Today's concept: the trie, or prefix tree.",
  "A hash set can tell you whether a word exists. But it can't tell you which words start with c a, or suggest completions as someone types. A trie stores words character by character, so shared prefixes share a path. By the end you'll know the node structure, insert, search and starts with, their cost, wildcard search, autocomplete, word search two, and the binary trie trick for maximum XOR.",
  pill="DSA · CONCEPT"),

{"html": H("Words as ", "paths") + sub("cat · car · cart · dog") + row(
   graph({"·": (330, 40), "c": (200, 130), "d": (460, 130), "a": (200, 220), "o": (460, 220),
          "t": (110, 320), "r": (290, 320), "g": (460, 320), "t ": (290, 410)},
         [("·", "c"), ("·", "d"), ("c", "a"), ("d", "o"), ("a", "t"), ("a", "r"), ("o", "g"), ("r", "t ")],
         w=640, h=460, r=32, step=0, colors={"t": E, "r": E, "g": E, "t ": E}),
   col(box("blue", "each edge = one character", "the root is empty", 0),
       box("purple", "shared prefix → shared path", "<b style=\"display:inline\">ca</b> is stored once for cat, car and cart", 1),
       box("green", "isEnd marks a word", "car is a word, and also a prefix of cart", 2), gap=16, style="flex:1"), top=True),
 "steps": [
  "Here are four words: cat, car, cart and dog. Each edge in the trie is one character, starting from an empty root.",
  "Words that share a prefix share a path. C, a is stored once, and branches into t and r.",
  "A green node marks the end of a word. R is green because car is a word, even though the path continues to cart. That flag is what tells a word apart from a mere prefix.",
 ]},

{"html": H("The node and the ", "operations") + code("""§0 class Node {
§0   Node[] next = new Node[26];   // or Map<Character, Node>
§0   boolean isEnd;
§0 }
§1 void insert(String w) {
§1   Node cur = root;
§1   for (char ch : w.toCharArray()) {
§1     int i = ch - 'a';
§1     if (cur.next[i] == null) cur.next[i] = new Node();
§1     cur = cur.next[i];
§1   }
§1   cur.isEnd = true;
§1 }
§2 boolean search(String w)     { Node n = walk(w); return n != null && n.isEnd; }
§2 boolean startsWith(String p) { return walk(p) != null; }""", 26),
 "steps": [
  "A node holds an array of twenty six children, one per lowercase letter, and the end flag. For larger alphabets, use a hash map of children instead.",
  "Insert walks the word letter by letter, creating missing children on the way, then marks the last node as an end.",
  "Search and starts with both walk down the path. Starts with only needs the path to exist. Search also needs the final node to be marked as an end. That's the whole difference.",
 ]},

{"html": H("Cost and ", "memory") + table(["Operation", "Trie", "HashSet"], [
     (["insert / search a word of length L", "O(L)", "O(L) to hash"], 0),
     (["all words starting with a prefix", "<b>O(P + output)</b>", "scan every word"], 1),
     (["memory", "26 pointers per node: heavy", "light"], 2),
     (["sorted order", "DFS in letter order", "no"], 2)], size=30) +
   note("A trie pays memory to make <u>prefix</u> questions cheap", 3),
 "steps": [
  "Inserting or searching a word costs its length, L. A hash set is also order L, since hashing reads every character.",
  "The difference is prefixes. To list every word starting with a prefix, the trie walks P steps and then visits only matching words. A hash set would have to check every word it holds.",
  "The price is memory. An array of twenty six pointers per node adds up fast. And a depth first walk in letter order gives the words in sorted order for free.",
  "So use a trie when the questions are about prefixes. For plain membership, a hash set is simpler.",
 ]},

{"html": H("Wildcards and ", "autocomplete") + row(
   col(box("purple", "wildcard search", "<code>c.t</code>: at a <code>.</code>, try <b style=\"display:inline\">every</b> child (DFS)", 0),
       code("""§0 boolean dfs(Node n, String w, int i) {
§0   if (n == null) return false;
§0   if (i == w.length()) return n.isEnd;
§0   char ch = w.charAt(i);
§0   if (ch == '.') {
§0     for (Node c : n.next) if (dfs(c, w, i + 1)) return true;
§0     return false;
§0   }
§0   return dfs(n.next[ch - 'a'], w, i + 1);
§0 }""", 23), gap=14, style="flex:1"),
   col(box("green", "autocomplete", "walk to the prefix node, then DFS in letter order, stop after 3 words", 1),
       box("blue", "faster suggestions", "store the top 3 words <b style=\"display:inline\">in each node</b> while inserting", 2),
       box("orange", "replace words", "walk each word: the first <code>isEnd</code> on the path is its shortest root", 3), gap=16, style="width:560px"), top=True),
 "steps": [
  "Tries handle patterns well. In a wildcard search, a dot matches any letter. At a dot, try every child with depth first search. Normal letters just follow one edge.",
  "Autocomplete: walk down to the prefix node, then depth first search below it in letter order, and stop after three words. They come out sorted.",
  "If suggestions are requested on every keystroke, store the best three words directly in each node while inserting. Then each lookup is just a walk.",
  "And replace words: for each word in a sentence, walk the trie. The first end marker you pass is the shortest root that word starts with.",
 ]},

{"html": H("Word Search II: trie + ", "backtracking") + row(
   col(box("red", "naive", "one grid search <b style=\"display:inline\">per word</b> · thousands of words → too slow", 0),
       box("green", "with a trie", "one grid DFS · follow trie edges as you move · stop when no child matches", 1),
       box("blue", "tricks", "store the word in its end node · remove it once found · prune empty nodes", 2), gap=16, style="flex:1"),
   col(cells(["o", "a", "a", "n"], None, None, 0, "", size=36),
       cells(["e", "t", "a", "e"], None, None, 0, "", size=36),
       cells(["i", "h", "k", "r"], None, None, 0, "", size=36),
       cells(["i", "f", "l", "v"], None, None, 0, "", size=36), gap=10), top=True) +
   note("The trie searches for <u>all</u> words at once", 3),
 "steps": [
  "Word search two gives you a grid of letters and a list of words. Find every word that can be traced in the grid. Searching the grid once per word repeats a lot of work.",
  "Instead, put all words in a trie, and run one backtracking search over the grid. As you step from cell to cell, step down the trie too. The moment the trie has no child for the next letter, abandon that path. No word starts that way.",
  "A few tricks make it fast. Store the full word in its end node, so you don't rebuild strings. Clear it once found, to avoid duplicates. And remove trie nodes that have no children left.",
  "The key idea: the trie lets one search look for every word at the same time.",
 ]},

{"html": H("Binary trie: maximum ", "XOR") + row(
   col(box("purple", "store numbers as bits", "from the highest bit down · two children: 0 and 1", 0),
       box("green", "greedy per bit", "for x, prefer the child with the <b style=\"display:inline\">opposite</b> bit: that bit of the XOR becomes 1", 1),
       box("blue", "cost", "O(32) per number → O(32·n) for the best pair", 2), gap=16, style="width:440px"),
   code("""§1 int best(int x) {
§1   Node cur = root; int res = 0;
§1   for (int b = 31; b >= 0; b--) {
§1     int bit = (x >> b) & 1, want = bit ^ 1;
§1     if (cur.next[want] != null) {
§1       res |= 1 << b; cur = cur.next[want];
§1     }
§1     else cur = cur.next[bit];
§1   }
§1   return res;
§1 }""", 24, style="flex:1"), top=True),
 "steps": [
  "A trie doesn't have to hold letters. To find the largest XOR of any two numbers, store each number's bits in a trie, from the highest bit down. Each node has just two children, zero and one.",
  "For each number, walk down greedily. At each bit, prefer the child with the opposite bit, because that makes this bit of the XOR equal to one. A high bit set to one beats all lower bits combined, so the greedy choice is always right.",
  "Each number takes thirty two steps, so the best pair is found in linear time.",
 ]},

quiz([
  ("search vs startsWith?", "search also needs <b style=\"display:inline\">isEnd</b>", "blue",
   "Quiz time. What's the difference between search and starts with?",
   "Both walk the path, but search also requires the last node to be marked as the end of a word."),
  ("Only “is this word in the set?” Trie?", "a <b style=\"display:inline\">HashSet</b> is simpler", "orange",
   "You only ever ask whether a word is in the set. Do you need a trie?",
   "No. A hash set is simpler and lighter. Tries pay off for prefix questions."),
  ("Max XOR: which child do you prefer?", "the <b style=\"display:inline\">opposite</b> bit", "purple",
   "In the binary trie for maximum XOR, which child do you try first?",
   "The one with the opposite bit, so that bit of the XOR becomes one."),
]),

recap(["Shared prefixes share a path",
       "Node = children[26] + isEnd",
       "search needs isEnd · startsWith doesn't",
       "O(L) per word · prefix queries are the point",
       "Word Search II: one DFS, guided by the trie",
       "Binary trie: greedy opposite bit → max XOR"],
  "Let's recap. In a trie, words with a shared prefix share a path. Each node has children and an end flag. Search needs the end flag, starts with doesn't. Every operation costs the length of the word, and prefix questions are where tries beat hash sets. In word search two, one grid search guided by the trie finds every word. And a binary trie finds the maximum XOR by greedily taking the opposite bit. Now practise the problems listed in your notes!"),
]
