from conc import *

TAG = "DSA · Maths Extras"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Maths Extras.mp4"

SLIDES = [
title_slide(0, "Maths Extras", "Fast power, modular inverses, nCr and counting: the maths behind \"return it modulo 10⁹ + 7\"",
  "Welcome. Today's concept: the maths extras.",
  "Some problems ask for huge counts, then say: return the answer modulo ten to the nine plus seven. Behind that line sits a small toolkit. By the end you'll know safe modular arithmetic, fast power, pow with negative exponents, modular inverses, three ways to compute n choose r, the counting formulas that keep appearing, Catalan numbers, inclusion exclusion, and matrix exponentiation.",
  pill="DSA · CONCEPT"),

{"html": H("Modular arithmetic, ", "safely") + row(
   col(box("blue", "why 10⁹ + 7", "prime · fits in an int · the product of two fits in a <code>long</code>", 0),
       box("green", "+, −, ×", "reduce after every step · cast to <code>long</code> before multiplying", 1),
       box("red", "÷ doesn't work", "<code>(a / b) % m ≠ (a % m) / (b % m)</code> → multiply by an <b style=\"display:inline\">inverse</b>", 3), gap=16, style="width:720px"),
   code("""§1 static final int MOD = 1_000_000_007;
§1 long add = (a + b) % MOD;
§1 long mul = (long) a * b % MOD;          // cast FIRST
§2 long sub = ((a - b) % MOD + MOD) % MOD;  // Java's % can be negative""", 25, style="flex:1"), top=True),
 "steps": [
  "Why ten to the nine plus seven? It's prime, it fits in an int, and the product of two such numbers still fits in a long.",
  "Addition and multiplication can be reduced after every step. Cast to long before multiplying, or the int product overflows before the modulo ever runs.",
  "Subtraction has a Java trap: the remainder operator can return a negative number. Add the modulus and reduce again.",
  "And division doesn't survive the modulo at all. Instead, you multiply by a modular inverse, coming up shortly.",
 ]},

{"html": H("Fast power: ", "squaring") + row(
   col(box("blue", "the idea", "3<sup>13</sup>: 13 = 1101₂ → 3<sup>8</sup> · 3<sup>4</sup> · 3<sup>1</sup>", 0),
       box("green", "the loop", "square the base each step · multiply it in when the bit is 1", 1),
       box("purple", "cost", "<b style=\"display:inline\">O(log n)</b> instead of O(n)", 2), gap=16, style="width:640px"),
   code("""§1 long power(long a, long n, long mod) {
§1   long result = 1; a %= mod;
§1   while (n > 0) {
§1     if ((n & 1) == 1) result = result * a % mod;
§1     a = a * a % mod;
§1     n >>= 1;
§1   }
§1   return result;
§1 }""", 26, style="flex:1"), top=True) +
   note("Pow(x, n) with doubles: use a <code>long</code> for n · <code>Integer.MIN_VALUE</code> can't be negated", 3),
 "steps": [
  "Computing a to the power n by multiplying n times is far too slow when n is a billion. Write n in binary instead. Thirteen is one one zero one, so three to the thirteen is three to the eight, times three to the four, times three to the one.",
  "The loop squares the base at every step, giving a, a squared, a to the four, and so on. Whenever the current bit of n is one, multiply that power into the result.",
  "That's log n multiplications.",
  "The same idea solves pow of x and n with doubles. For a negative exponent, compute one over x to the minus n. But copy n into a long first, because the smallest int has no positive counterpart.",
 ]},

{"html": H("Modular ", "inverse") + row(
   col(box("blue", "what it is", "<code>b⁻¹</code> with <code>b · b⁻¹ ≡ 1 (mod m)</code> · then <code>a / b ≡ a · b⁻¹</code>", 0),
       box("green", "Fermat (m prime)", "<code>b⁻¹ = b<sup>m−2</sup> mod m</code> · one fast power", 1),
       box("orange", "m not prime", "extended Euclid · exists only if <code>gcd(b, m) = 1</code>", 2), gap=16, style="width:640px"),
   code("""§1 long inv(long b) {
§1   return power(b, MOD - 2, MOD);
§1 }
§1 long divide(long a, long b) {
§1   return a % MOD * inv(b) % MOD;
§1 }""", 26, style="flex:1"), top=True),
 "steps": [
  "A modular inverse of b is the number that multiplies with b to give one, modulo m. Dividing by b then becomes multiplying by its inverse.",
  "When the modulus is prime, Fermat's little theorem gives it directly: b to the power m minus two. That's one call to fast power.",
  "If the modulus isn't prime, use the extended Euclidean algorithm. Either way, an inverse exists only when b and m share no factor.",
 ]},

{"html": H("n choose r, three ", "ways") + table(["Way", "How", "When"], [
     (["Pascal's triangle", "<code>C[n][r] = C[n−1][r−1] + C[n−1][r]</code>", "n ≤ ~1000 · any modulus"], 0),
     (["factorials + inverses", "<code>n! · inv(r!) · inv((n−r)!)</code> · precompute O(n)", "many queries · prime mod"], 1),
     (["multiplicative loop", "<code>c = c * (n − i) / (i + 1)</code>", "one value · no mod · small"], 2)], size=28) +
   note("Precompute <code>fact[]</code> and <code>invFact[]</code> once → each nCr is O(1)", 3),
 "steps": [
  "There are three ways to compute n choose r. Pascal's triangle builds each value from the two above it. It's quadratic, but works with any modulus.",
  "For many queries with a prime modulus, precompute factorials and inverse factorials once. Then each n choose r is three multiplications.",
  "For a single value without a modulus, multiply and divide in a loop. Each intermediate result is itself a binomial coefficient, so the division is always exact. Use a long.",
  "In contest style problems, the factorial table is the usual choice.",
 ]},

{"html": H("Counting patterns and ", "Catalan") + row(
   table(["Count", "Formula"], [
     (["orderings of n distinct items", "n!"], 0),
     (["orderings with repeats (a, b alike)", "n! / (a! · b!)"], 0),
     (["grid paths, m right + n down", "C(m + n, n)"], 1),
     (["n identical items into k boxes", "C(n + k − 1, k − 1)"], 1)], size=27),
   col(box("purple", "Catalan numbers", "1, 1, 2, 5, 14, 42 … · <code>C(2n, n) / (n + 1)</code>", 2),
       box("blue", "they count", "balanced parentheses · BST shapes · polygon triangulations", 2), gap=16, style="width:600px"), top=True),
 "steps": [
  "A few formulas cover most counting questions. N distinct items can be ordered in n factorial ways. If some items are identical, divide by the factorials of each group.",
  "A path through a grid with m moves right and n moves down is a choice of which moves go down: m plus n choose n. And putting n identical items into k boxes is stars and bars: n plus k minus one, choose k minus one.",
  "Then the Catalan numbers: one, one, two, five, fourteen. They count balanced parentheses, the shapes of binary search trees, and triangulations of a polygon. When small answers come out as one, two, five, fourteen, think Catalan.",
 ]},

{"html": H("Inclusion–exclusion and matrix ", "power") + row(
   col(box("blue", "inclusion–exclusion", "<code>|A ∪ B| = |A| + |B| − |A ∩ B|</code>", 0),
       box("green", "example", "1..100 divisible by 2 or 3: 50 + 33 − 16 = <b style=\"display:inline\">67</b>", 0), gap=16, style="flex:1"),
   col(box("purple", "matrix exponentiation", "a linear recurrence = a matrix power · fast power on matrices", 1),
       code("""§1 [F(n+1)  F(n)  ]   [1 1]^n
§1 [F(n)    F(n−1)] = [1 0]""", 26),
       box("orange", "cost", "O(k³ · log n) for a k×k matrix · n can be 10¹⁸", 2), gap=16, style="flex:1"), top=True),
 "steps": [
  "Inclusion exclusion counts a union without double counting. Add the sizes of the sets, subtract each overlap, add back triple overlaps, and so on. Numbers up to a hundred divisible by two or three: fifty plus thirty three, minus the sixteen divisible by six. Sixty seven.",
  "Matrix exponentiation handles huge n in linear recurrences. Fibonacci can be written as a two by two matrix raised to the power n. Use the same fast power loop, with matrix multiplication instead of number multiplication.",
  "A k by k matrix costs k cubed per multiply, times log n. So even the ten to the eighteenth Fibonacci number, modulo a prime, is instant.",
 ]},

quiz([
  ("<code>a * b % MOD</code> with ints: the bug?", "overflow: cast to <b style=\"display:inline\">long</b> first", "red",
   "Quiz time. What's wrong with a times b, modulo MOD, when a and b are ints?",
   "The product overflows before the modulo. Cast to long first."),
  ("Inverse of b, modulo a prime m?", "<code>b<sup>m−2</sup> mod m</code> (Fermat)", "blue",
   "How do you compute the inverse of b modulo a prime?",
   "Raise b to the power m minus two, with fast power."),
  ("1, 1, 2, 5, 14…?", "<b style=\"display:inline\">Catalan</b> numbers", "purple",
   "Your small answers come out as one, one, two, five, fourteen. What are they?",
   "The Catalan numbers."),
]),

recap(["Cast to long before multiplying · fix negative %",
       "Fast power: square the base, use the bits of n",
       "Division → multiply by an inverse (Fermat: b^(m−2))",
       "nCr: Pascal · factorial tables · loop",
       "Catalan: 1, 1, 2, 5, 14 · inclusion–exclusion",
       "Linear recurrence + huge n → matrix power"],
  "Let's recap. Cast to long before multiplying, and fix negative remainders. Fast power squares the base and uses the bits of the exponent, in log n. Division becomes multiplication by an inverse, which Fermat gives for prime moduli. Compute n choose r with Pascal's triangle, factorial tables, or a loop. Recognise Catalan numbers, and use inclusion exclusion for unions. And for a linear recurrence with huge n, raise a matrix to a power. Now practise the problems listed in your notes!"),
]
