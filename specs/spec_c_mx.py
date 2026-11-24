from conc import *

TAG = "DSA · Matrix Traversal"
TRACK = "Java Fullstack · DSA"
FILE = "DSA Matrix Traversal.mp4"


def grid(rows, step=None, size=30, mark=None):
    mark = mark or {}
    return col(*[cells(r, None, None, step, "", size=size, mark={c: mark[(i, c)] for c in range(len(r)) if (i, c) in mark})
                 for i, r in enumerate(rows)], gap=8)


Y = "#fde68a"
G = "#bbf7d0"
B = "#bfdbfe"

SLIDES = [
title_slide(0, "Matrix Traversal", "Walk a grid in any order: spirals, rotations, diagonals, in place",
  "Welcome. Today's concept: matrix traversal.",
  "Lots of interview problems hand you a 2D grid and ask you to walk it in a particular order, or change it in place without extra memory. They feel fiddly, but they reuse a few small ideas. By the end you'll know indexing and direction arrays, the spiral with four boundaries, rotating by transpose and reverse, using the matrix itself as storage, diagonals, Sudoku boxes, and searching a sorted matrix.",
  pill="DSA · CONCEPT"),

{"html": H("Indexing and ", "directions") + row(
   col(box("blue", "rows and columns", "<code>grid[r][c]</code> · rows = <code>grid.length</code> · cols = <code>grid[0].length</code>", 0),
       box("purple", "flatten to 1D", "<code>i = r * cols + c</code> · back: <code>r = i / cols</code>, <code>c = i % cols</code>", 1),
       box("green", "direction arrays", "one loop instead of four copies of the same code", 2), gap=16, style="width:600px"),
   code("""§2 int[][] DIRS = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};  // R D L U
§2 for (int[] d : DIRS) {
§2   int nr = r + d[0], nc = c + d[1];
§3   if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
§2   visit(nr, nc);
§2 }""", 24, style="flex:1"), top=True) +
   note("8 neighbours? add the four diagonals {±1, ±1}", 4),
 "steps": [
  "First the basics. A grid is rows of columns. The number of rows is grid dot length, and the number of columns is grid zero dot length. Mixing those two up is the most common bug.",
  "Sometimes it helps to treat the grid as one long array. Cell r c becomes r times columns plus c. Division and remainder take you back. That's how a sorted matrix can be binary searched, and how union find numbers grid cells.",
  "To visit neighbours, use a direction array instead of four copies of the same code. Each pair is a change in row and a change in column.",
  "And always check bounds before touching the new cell.",
  "For eight neighbours, add the four diagonal pairs.",
 ]},

{"html": H("Spiral: four ", "boundaries") + row(
   grid([[1, 2, 3, 4], [10, 11, 12, 5], [9, 8, 7, 6]], 0, 34,
        {(0, 0): Y, (0, 1): Y, (0, 2): Y, (0, 3): Y, (1, 3): G, (2, 3): G, (2, 2): B, (2, 1): B, (2, 0): B, (1, 0): "#e9d5ff"}),
   code("""§1 int top = 0, bottom = m - 1, left = 0, right = n - 1;
§1 while (top <= bottom && left <= right) {
§1   for (int c = left; c <= right; c++) add(g[top][c]);   top++;
§1   for (int r = top; r <= bottom; r++) add(g[r][right]); right--;
§2   if (top <= bottom)
§2     for (int c = right; c >= left; c--) add(g[bottom][c]); bottom--;
§2   if (left <= right)
§2     for (int r = bottom; r >= top; r--) add(g[r][left]); left++;
§1 }""", 22, style="flex:1"), top=True) +
   note("Numbers = visit order · each colour = one side of one lap", 3),
 "steps": [
  "Reading a matrix in spiral order. The numbers show the order: right along the top, down the right side, back along the bottom, and up the left.",
  "Keep four boundaries: top, bottom, left and right. After walking a side, move that boundary inward, so the next lap is smaller.",
  "The only trap: after the first two sides, the remaining rows or columns may already be used up. Check top less than or equal to bottom, and left less than or equal to right, before walking the last two sides. Otherwise a single row or column is read twice.",
  "The same four boundaries generate a spiral, by writing numbers instead of reading them.",
 ]},

{"html": H("Rotate 90°: transpose, then ", "reverse") + row(
   col(grid([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 0, 34), note("original", 0, "margin-top:10px"), gap=6),
   col(grid([[1, 4, 7], [2, 5, 8], [3, 6, 9]], 1, 34, {(0, 0): Y, (1, 1): Y, (2, 2): Y}), note("transpose", 1, "margin-top:10px"), gap=6),
   col(grid([[7, 4, 1], [8, 5, 2], [9, 6, 3]], 2, 34), note("reverse each row", 2, "margin-top:10px"), gap=6),
   gap=60, style="justify-content:center") +
   code("""§1 for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) swap(m, i, j, j, i);
§2 for (int[] row : m) reverse(row);   // clockwise""", 24, style="margin-top:20px") +
   note("Anticlockwise: transpose, then reverse each <b style=\"display:inline\">column</b>", 3),
 "steps": [
  "Rotating a square image ninety degrees clockwise, in place. Doing it in one move is fiddly. Doing it in two is easy.",
  "First, transpose: swap every cell with its mirror across the main diagonal, so rows become columns. Only loop j from i plus one, or you'd swap everything back.",
  "Then reverse each row. That's the clockwise rotation. Both steps are in place, so the extra memory is constant.",
  "For anticlockwise, transpose, then reverse each column instead.",
 ]},

{"html": H("Use the matrix as its own ", "memory") + row(
   box("blue", "set matrix zeroes", "mark zero rows and columns in the <b style=\"display:inline\">first row and column</b> · two flags for those two themselves", 0, "flex:1"),
   box("green", "game of life", "store old and new state in one int: bit 0 = now, bit 1 = next · then <code>cell &gt;&gt;= 1</code>", 1, "flex:1"), top=True) +
   code("""§1 int live = countLiveNeighbours(r, c);        // reads bit 0 only: g[nr][nc] & 1
§1 if ((g[r][c] & 1) == 1 && (live == 2 || live == 3)) g[r][c] |= 2;
§1 if ((g[r][c] & 1) == 0 && live == 3)               g[r][c] |= 2;
§1 // after the full pass: every cell >>= 1""", 23, style="margin-top:20px") +
   note("Need old values while writing new ones? Encode both, then finish in a second pass", 2),
 "steps": [
  "Some problems update a grid in place, but the update depends on values you're about to overwrite. Set matrix zeroes: if a cell is zero, zero its whole row and column. Instead of extra arrays, use the first row and first column as markers. Two booleans remember whether that row and column themselves had a zero.",
  "Game of life is the same idea with bits. Every cell's next state depends on its neighbours' current states. So keep the current state in bit zero and write the next state into bit one. Neighbours read only bit zero, which hasn't changed. At the end, shift every cell right by one.",
  "The general trick: when you need old values while writing new ones, store both in the same cell, and finish with a second pass.",
 ]},

{"html": H("Diagonals and ", "boxes") + row(
   col(grid([[0, -1, -2], [1, 0, -1], [2, 1, 0]], 0, 30, {(0, 0): Y, (1, 1): Y, (2, 2): Y}), note("r − c", 0, "margin-top:8px"), gap=4),
   col(grid([[0, 1, 2], [1, 2, 3], [2, 3, 4]], 1, 30, {(0, 2): G, (1, 1): G, (2, 0): G}), note("r + c", 1, "margin-top:8px"), gap=4),
   col(box("purple", "Sudoku box", "box index = <code>(r / 3) * 3 + c / 3</code> · one seen-set per row, column and box", 2),
       box("blue", "group by key", "same key → same line · <code>Map&lt;Integer, List&gt;</code>", 3), gap=16, style="flex:1"),
   gap=40, top=True),
 "steps": [
  "Diagonals have a simple key. On every top left to bottom right diagonal, row minus column is constant.",
  "On every anti diagonal, row plus column is constant. Diagonal traverse, the zig zag, just walks these keys from zero up, alternating direction.",
  "Sudoku's three by three boxes have a key too: row divided by three, times three, plus column divided by three. That numbers the nine boxes. Validating a board is then one pass, with a seen set for each row, column and box.",
  "So when cells belong to lines or blocks, find the key, and group by it.",
 ]},

{"html": H("Searching a sorted ", "matrix") + row(
   box("blue", "rows and columns sorted", "start <b style=\"display:inline\">top-right</b>: too big → go left · too small → go down · <b style=\"display:inline\">O(m + n)</b>", 0, "flex:1"),
   box("green", "fully sorted, row after row", "treat it as one array of <code>m · n</code> · binary search · <b style=\"display:inline\">O(log mn)</b>", 1, "flex:1"), top=True) +
   pts([("forgetting <code>grid[0].length</code> for non-square grids", 2),
        ("modifying while reading: copy, or encode both states", 2),
        ("spiral: re-check boundaries before the last two sides", 2)], size=31),
 "steps": [
  "Finally, searching. If every row and every column is sorted, start at the top right corner. If the value there is too big, the whole column below is too big, so go left. If it's too small, go down. Each step removes a row or a column.",
  "If the matrix is sorted as one long sequence, row after row, flatten it in your head and binary search with the index formula from earlier.",
  "And the usual traps: using the row count for columns on non square grids, overwriting values you still need, and forgetting to recheck spiral boundaries.",
 ]},

quiz([
  ("Rotate an n×n image clockwise in place?", "<b style=\"display:inline\">transpose</b>, then reverse each row", "blue",
   "Quiz time. How do you rotate a square image clockwise in place?",
   "Transpose it, then reverse each row."),
  ("Cells on the same anti-diagonal share…?", "the same <b style=\"display:inline\">r + c</b>", "green",
   "What do cells on the same anti diagonal have in common?",
   "The same row plus column."),
  ("Sorted rows and columns: where do you start?", "the <b style=\"display:inline\">top-right</b> corner", "purple",
   "Rows and columns are both sorted. Where do you start searching?",
   "The top right corner, and move left or down."),
]),

recap(["grid.length = rows · grid[0].length = cols",
       "Direction arrays + one bounds check",
       "Spiral: four boundaries, shrink after each side",
       "Rotate: transpose + reverse",
       "In place: encode old and new in one cell",
       "Diagonals: r − c or r + c · boxes: (r/3)*3 + c/3"],
  "Let's recap. Rows are grid dot length, and columns are grid zero dot length. Use direction arrays with one bounds check. For spirals, keep four boundaries and shrink them. Rotate with a transpose and a reverse. To change a grid in place, encode old and new values in the same cell. And diagonals and boxes all have a simple key to group by. Now practise the problems listed in your notes!"),
]
