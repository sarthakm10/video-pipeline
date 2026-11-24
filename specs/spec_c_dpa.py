from conc import *

TAG = "DSA · Dynamic Programming, Part 1"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Dynamic Programming (Part 1).mp4"


def node(t, bg="#fff", border="#9ca3af"):
    return (f'<div style="padding:10px 18px;border:4px solid {border};border-radius:14px;background:{bg};'
            f'font:700 32px Cascadia Code,Consolas,monospace">{t}</div>')


RED, GREY = ("#fee2e2", "#dc2626"), ("#f1f5f9", "#64748b")
TREE = col(
  row(node("fib(5)", "#ffedd5", "#ea580c"), gap=0, style="justify-content:center"),
  row(node("fib(4)"), node("fib(3)", *RED), gap=200, style="justify-content:center"),
  row(node("fib(3)", *RED), node("fib(2)", *GREY), node("fib(2)", *GREY), node("fib(1)"), gap=40, style="justify-content:center"),
  row(node("fib(2)", *GREY), node("fib(1)"), gap=40, style="justify-content:center;margin-right:420px"), gap=22)

SLIDES = [
title_slide(0, "Dynamic Programming", "Part 1 · what DP is, memo vs tabulation, the five-step method, knapsack",
  "Welcome to dynamic programming, part one.",
  "DP has a scary reputation, but it's one idea. Solve each smaller problem once, remember the answer, and build up. In this part: when DP applies, the four ways to write it, a five-step method that works for every DP problem, and the two most important families. Take or skip, and knapsack.",
  pill="DSA · CONCEPT"),

{"html": H("When does DP ", "apply", "?") + row(
   col(box("blue", "optimal substructure", "the best answer is built from the best answers to smaller subproblems", 0),
       box("red", "overlapping subproblems", "the same subproblems are needed again and again", 1), gap=18, style="width:620px"),
   col(TREE, note("~2ⁿ calls, only <u>n distinct</u> subproblems", 2), style="flex:1"), top=True),
 "steps": [
  "DP works when a problem has two properties. First, optimal substructure. The best answer is built from the best answers to smaller problems. A shortest path from A to C through B is the shortest A to B, plus the shortest B to C.",
  "Second, overlapping subproblems. The same smaller problems come up again and again. Look at fib of five. Fib of three is computed twice, and fib of two three times.",
  "The tree has about two to the n calls, but only n different subproblems. DP computes each different one once, and reuses it. If subproblems don't overlap, like the two halves in merge sort, caching wouldn't help. That's plain divide and conquer.",
 ]},

{"html": H("DP vs greedy vs divide and ", "conquer") + table(["", "Greedy", "Divide &amp; conquer", "DP"], [
     (["decision", "best local choice, never reconsider", "split into <b>independent</b> parts", "try <b>all</b> choices, reuse results"], 0),
     (["overlap?", "—", "no", "<b>yes</b>"], 0),
     (["example", "activity selection", "merge sort", "coin change, LCS"], 0)], size=29) +
   row(box("orange", "coins {1, 3, 4}, amount 6", "greedy: 4 + 1 + 1 = <b style=\"display:inline\">3 coins</b> · best: 3 + 3 = <b style=\"display:inline\">2 coins</b>", 1, "flex:1"),
       style="margin-top:26px") + note("Greedy can be wrong → you need DP to try every choice", 2),
 "steps": [
  "How is DP different from greedy, or divide and conquer? Greedy takes the locally best choice, and never looks back. Divide and conquer splits into independent parts. DP tries every choice, but reuses the shared results, so trying everything stays cheap.",
  "Here's how to tell greedy from DP. Look for a counter-example. Coins one, three, and four, making six. Greedy grabs the biggest coin first. Four, then one, then one. Three coins. But three plus three is just two.",
  "Once greedy can be wrong, you need to try every choice. And trying every choice efficiently is exactly what DP does.",
 ]},

{"html": H("Fibonacci, four ", "ways") + row(
   col(code("""§0 // 1. recursion: O(2ⁿ)
§0 int fib(int n) {
§0   if (n <= 1) return n;
§0   return fib(n-1) + fib(n-2);
§0 }
§1 // 2. memo (top-down): O(n)
§1 if (memo[n] != null) return memo[n];
§1 return memo[n] = fib(n-1) + fib(n-2);""", 26), style="flex:1"),
   col(code("""§2 // 3. tabulation (bottom-up): O(n)
§2 dp[0] = 0; dp[1] = 1;
§2 for (int i = 2; i <= n; i++)
§2   dp[i] = dp[i-1] + dp[i-2];
§3 // 4. two variables: O(1) space
§3 int a = 0, b = 1;
§3 for (int i = 2; i <= n; i++) {
§3   int c = a + b; a = b; b = c; }""", 26), style="flex:1"), top=True),
 "steps": [
  "Every DP solution can be written four ways. Start with plain recursion. It's correct, but exponential, because it recomputes the same calls.",
  "Two, memoisation. Same recursion, but before computing, check a cache. After computing, store it. Now each n is solved once. That's top-down DP.",
  "Three, tabulation. Drop the recursion, and fill an array from the smallest case up. Each entry uses entries already filled. That's bottom-up DP.",
  "And four, if each step only needs the last few values, keep just those in variables. Same time, constant space.",
 ]},

{"html": H("Top-down or ", "bottom-up", "?") + table(["", "Memoisation (top-down)", "Tabulation (bottom-up)"], [
     (["how", "recursion + a cache", "loops filling a table"], 0),
     (["computes", "only the states it needs", "every state"], 0),
     (["easiest when", "the order is tricky", "the order is obvious"], 0),
     (["risk", "deep recursion → StackOverflowError", "must get the fill order right"], 1),
     (["space trick", "hard", "keep only the rows you need"], 1)], size=30) +
   note("Interview path: <u>recursion → memo → table → less space</u>", 2),
 "steps": [
  "So which should you use? Memoisation is recursion plus a cache. It only computes the states it actually needs, and it's easiest when the fill order isn't obvious. Tabulation uses loops, and computes every state.",
  "Memoisation's risk is deep recursion. A few thousand levels can overflow the stack in Java. Tabulation avoids that, and makes it easy to cut space by keeping only the rows you need.",
  "In an interview, a great path is: write the recursion, add memo, then convert to a table, and then reduce space if asked. Each step is a small, safe change.",
 ]},

{"html": H("The five-step ", "method") + table(["Step", "Question", "Climbing stairs (1 or 2 steps)"], [
     (["1 · state", "what does <code>dp[i]</code> <b>mean</b>, in words?", "ways to reach step i"], 0),
     (["2 · transition", "how is it built from smaller states? (the <b>last choice</b>)", "<code>dp[i-1] + dp[i-2]</code>"], 1),
     (["3 · base cases", "what's known without the transition?", "<code>dp[0] = 1, dp[1] = 1</code>"], 2),
     (["4 · order", "fill so dependencies come first", "i increasing"], 2),
     (["5 · answer", "which state is the final answer?", "<code>dp[n]</code>"], 2)], size=29) +
   note("Write these five down <u>before</u> coding", 3),
 "steps": [
  "Here's a method that works for every DP problem. Five questions. One, the state. What does d p of i mean, in plain words? For climbing stairs, the number of ways to reach step i.",
  "Two, the transition. How is a state built from smaller ones? Think about the last choice. The last move was either one step or two, so the ways to reach i are the ways to reach i minus one, plus the ways to reach i minus two.",
  "Three, base cases: the states you know directly. Four, the order: fill so every dependency is ready first. Here, i increasing. And five, the answer: which state answers the question. D p of n.",
  "Write these five down before you write any code. If you can answer all five, the code is almost mechanical.",
 ]},

{"html": H("Finding the ", "state") + row(
   box("purple", "ask yourself", "\"If I were halfway through solving this <b style=\"display:inline\">by hand</b>, what would I need to remember to finish?\"", 0, "flex:1"),
   box("blue", "that's the state", "\"which item I'm at, and capacity left\" → <code>dp[i][cap]</code>", 1, "flex:1")) +
   note("<span class=\"big\" style=\"font-size:50px;color:#16a34a\">time = number of states × work per state</span><br>LCS: m·n states × O(1) → O(m·n)", 2, "text-align:center;transform:none;margin-top:40px"),
 "steps": [
  "The state is the hardest part. Here's a question that finds it. If you were halfway through solving this by hand, what would you need to remember to finish?",
  "Whatever that is, is your state. If the answer is which item I'm at, and how much capacity is left, then the state is d p of i and capacity.",
  "And once you have the state, the complexity follows. Time is the number of states, times the work for each one. For longest common subsequence, there are m times n states, each constant work, so it's m times n.",
 ]},

{"html": H("Family 1: take or ", "skip") + sub("No two adjacent houses · best loot") +
   col(cells([2, 7, 9, 3, 1], label="houses", size=40),
       cells([2, 7, 11, 11, 12], 0, 4, 1, "best up to i", size=40), gap=18) +
   code("""§2 dp[i] = Math.max(dp[i-1],            // skip house i
§2                  a[i] + dp[i-2]);    // take it, so skip i-1""", 30, style="margin-top:28px") +
   note("At each item: <u>take it or skip it</u>, keep the better", 3),
 "steps": [
  "Now the most common DP family. Take or skip. Houses in a row, each with money, and you can't take two neighbours. What's the most you can take?",
  "Let d p of i be the best total using houses up to i. Here it grows two, seven, eleven, eleven, twelve.",
  "At each house, you have two choices. Skip it, and keep the best up to the previous house. Or take it, adding its money to the best from two houses back, since its neighbour is now off limits. Keep the larger.",
  "That take or skip choice appears everywhere. Knapsack, subset sum, partitions, and many more. Spot the choice at each item, and the transition writes itself.",
 ]},

{"html": H("Family 2: ", "knapsack") + row(
   col(box("blue", "0/1 knapsack", "each item <b style=\"display:inline\">at most once</b> · maximise value within capacity W", 0),
       code("""§1 dp[i][w] = max(
§1   dp[i-1][w],                    // skip
§1   val[i] + dp[i-1][w - wt[i]]);  // take""", 26), gap=18, style="flex:1"),
   col(box("green", "unbounded", "each item <b style=\"display:inline\">any number</b> of times · e.g. coin change", 2),
       table(["Type", "1D capacity loop"], [
         (["0/1", "<b>downwards</b>"], 2), (["unbounded", "<b>upwards</b>"], 2)], size=28), gap=18, style="width:560px"), top=True) +
   note("Downwards keeps the <u>previous row's</u> values, so no item is used twice", 3),
 "steps": [
  "The second family is knapsack. Items with weights and values, and a bag with capacity W. In zero one knapsack, each item can be taken at most once.",
  "The state is which items you've considered, and the capacity left. The transition is take or skip again. Skip item i, or take it, adding its value to the best answer with its weight removed from the capacity.",
  "In unbounded knapsack, each item can be used any number of times. Coin change is the classic. In a one dimensional table, the whole difference is the direction of one loop. Zero one goes downwards. Unbounded goes upwards.",
  "Why? Going downwards, the smaller capacities still hold the previous item's row, so the current item can't be added twice. Going upwards, they may already include it, which is exactly what unbounded allows.",
 ]},

{"html": H("Counting: loop order ", "matters") + row(
   code("""§0 // combinations: {1,2} = {2,1}
§0 for (int c : coins)               // coins OUTSIDE
§0   for (int a = c; a <= amt; a++)
§0     dp[a] += dp[a - c];""", 25, style="flex:1"),
   code("""§1 // permutations: {1,2} ≠ {2,1}
§1 for (int a = 1; a <= amt; a++)    // amount OUTSIDE
§1   for (int c : coins)
§1     if (c <= a) dp[a] += dp[a - c];""", 25, style="flex:1"), top=True) +
   note("<code>dp[0] = 1</code>: one way to make zero · swapping two loops changes the <u>question</u>", 2),
 "steps": [
  "One more trap, when counting the ways to make an amount. With coins in the outer loop, coins are added in a fixed order. All ones, then all twos. So one plus two, and two plus one, are counted once. That counts combinations.",
  "Swap the loops, putting the amount outside. Now at each amount, any coin can be the last one, so every ordering is counted separately. That counts permutations.",
  "Both start with d p of zero equal to one. There's exactly one way to make zero: use nothing. The code is nearly identical, but swapping two loops changes which question you're answering.",
 ]},

quiz([
  ("Two properties DP needs?", "<b style=\"display:inline\">optimal substructure</b> + overlapping subproblems", "blue",
   "Quiz time. What two properties does a problem need for DP?",
   "Optimal substructure, and overlapping subproblems."),
  ("Memo vs tabulation risk?", "memo: <b style=\"display:inline\">deep recursion</b> overflows the stack", "green",
   "What's the main risk of memoisation in Java?",
   "Deep recursion can overflow the stack. Tabulation avoids it."),
  ("0/1 knapsack in 1D: loop direction?", "capacity <b style=\"display:inline\">downwards</b>", "purple",
   "In a one dimensional zero one knapsack, which way does the capacity loop go?",
   "Downwards, so each item is used at most once."),
]),

recap(["DP = optimal substructure + overlapping subproblems",
       "Recursion → memo → table → less space",
       "Five steps: state, transition, base, order, answer",
       "Time = states × work per state",
       "Take or skip · 0/1 (down) vs unbounded (up)",
       "Coins outside = combinations · amount outside = permutations"],
  "Let's recap part one. DP needs optimal substructure and overlapping subproblems. Write it as recursion, then memo, then a table, then save space. Use the five steps: state, transition, base cases, order, and answer. Time is the number of states times the work per state. And the two big families: take or skip, and knapsack, where the loop direction decides zero one or unbounded. Next time, part two: grid DP, subsequences, strings, intervals, trees, and stock problems!"),
]
