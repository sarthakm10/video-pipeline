from lib import *

TAG = "Frontend 26 · Frontend System Design"
FILE = "Frontend 26 Frontend System Design.mp4"

SLIDES = [
title_slide(26, "Frontend System Design", "Design a UI product: components, state, data flow, API, trade-offs",
  "Welcome to module twenty six: frontend system design.",
  "Frontend system design rounds ask you to design a UI product, not a backend. Components, state, data flow, the API between client and server, performance and accessibility. There's no single right answer. Interviewers grade your structure and your trade-offs. This module gives you a framework, and two worked designs."),

{"html": H("The ", "RADIO", " framework") + table(["Step", "Time", "What you do"], [
   (["<b>R</b>equirements", "5–8 min", "functional + non-functional · agree what's <b>out of scope</b>"], 0),
   (["<b>A</b>rchitecture", "5–10 min", "views, components, client store, API layer, server"], 0),
   (["<b>D</b>ata model", "5 min", "entities, fields, which store, what's derived"], 0),
   (["<b>I</b>nterface", "5–10 min", "endpoints, request/response shapes, pagination"], 0),
   (["<b>O</b>ptimisations", "15–20 min", "performance, UX states, a11y, security, edge cases"], 0)], size=28) +
   row(box("blue", "ask before assuming", "mobile? how many items? real-time? offline?", 1, "flex:1"),
       box("green", "name trade-offs", "and cover every UX state", 1, "flex:1"),
       box("purple", "unprompted", "accessibility + performance", 1, "flex:1"), style="margin-top:24px"),
 "steps": [
  "A forty five to sixty minute round, in five steps. Some candidates remember them as RADIO. Requirements: what users can do, plus devices, scale, offline, and accessibility, and what's out of scope. Architecture: a box diagram of views, components, the client store, and the API layer. Data model. Interface, meaning the API. And optimisations, the deep dives. Say each step out loud as you start it.",
  "Good habits. Ask before assuming. Mobile or desktop? How many items? Real-time? Name your trade-offs. Cover the UX states: loading, empty, error, slow network, offline. And mention accessibility and performance unprompted. That's what separates frontend specialists.",
 ]},

{"html": H("Example: a Kanban ", "board") + row(code("""§0 BoardPage          board query, filters (URL)
§0 ├─ BoardHeader
§0 ├─ Column × n
§0 │  ├─ CardList     virtualized if long
§0 │  │  └─ Card × n  draggable
§0 │  └─ AddCardForm  local draft text
§0 └─ CardModal       lazy, /card/:cardId""", 26, style="flex:1"),
   code("""§1 type Column = { id: string;
§1   title: string; cardIds: string[] };
§1 type Card = { id: string; title: string;
§1   labels: string[]; version: number };
§1 // cards: Record<id, Card>""", 26, style="flex:1"), top=True) +
   code("""§2 GET   /api/boards/:id          → { board, columns, cards }
§2 PATCH /api/cards/:id           { title?, version } → Card
§2 POST  /api/cards/:id/move      { toColumnId, toIndex }
§2 WS    /ws/boards/:id           card.created · card.moved""", 26, style="margin-top:20px") +
   note("Optimistic moves · version conflicts · WebSocket vs polling · keyboard \"Move to…\"", 3),
 "steps": [
  "Take a Kanban board as an example. First, components. Break the screen into a tree, and decide who owns which state. The page owns the board query and the filters, which live in the URL. The add card form owns its draft text. And the card modal is lazy loaded, with its own route.",
  "Data model. Normalise server data, so each card lives in one place, in a record by I D. The order lives in each column's list of card I Ds. And a version number on each card handles conflicts.",
  "The API. One request for the whole board on the first paint. Patch to edit a card, with its version. A move endpoint. And a WebSocket that pushes changes from other users.",
  "Then discuss the key decisions. Optimistic moves, that roll back if the server rejects them. Conflicts between two users. WebSocket versus polling. And accessible drag and drop, with a keyboard move to menu.",
 ]},

{"html": H("Design an ", "autocomplete") + row(
   col(box("blue", "1 · debounce", "250 ms, not a request per keystroke", 0),
       box("orange", "2 · ignore stale", "AbortController, or drop old queries", 0),
       box("green", "3 · cache per query", "backspace is instant · <code>queryKey: [\"users\", q]</code>", 0),
       box("gray", "4 · min length + states", "idle · loading · results · none · error", 0), gap=12, style="width:560px"),
   code("""§1 <input role="combobox"
§1   aria-expanded="true"
§1   aria-controls="user-list"
§1   aria-activedescendant="opt-2">
§1 <ul id="user-list" role="listbox">
§1   <li id="opt-1" role="option">Asha</li>
§1   <li id="opt-2" role="option"
§1       aria-selected="true">Ashok</li>
§1 </ul>""", 26, style="flex:1"), top=True) +
   note("↓ ↑ Enter Escape · focus <u>stays in the input</u> · highlight with &lt;mark&gt;, never innerHTML", 2),
 "steps": [
  "Design an autocomplete. Design it as a reusable component, with props like fetch suggestions, render item, and on select. How it works. One: debounce the input, so you don't send a request on every keystroke. Two: ignore stale responses, by aborting the previous request. Three: cache results per query, so backspacing is instant. And four: a minimum length, and every state. Idle, loading, results, no results, and error.",
  "For accessibility, follow the WAI ARIA combobox pattern. The input has role combobox, and points at a listbox of options. Aria active descendant marks the highlighted option.",
  "Arrow keys move the highlight, enter selects, and escape closes. Focus stays in the input the whole time. Highlight matching text with a mark element, by splitting strings, never inner HTML. And on the server, a prefix index or a search engine returns the top results.",
 ]},

{"html": H("Design a news ", "feed") + code("""§0 GET /api/feed?limit=20                → { items, nextCursor: "p_8812" }
§0 GET /api/feed?limit=20&cursor=p_8812  → { items, nextCursor: "p_8790" }
§1 const observer = new IntersectionObserver(([entry]) => {
§1   if (entry.isIntersecting && hasNextPage) fetchNextPage();
§1 }, { rootMargin: "600px" });           // start before the end
§1 observer.observe(sentinelRef.current);""", 26) +
   row(box("purple", "many posts", "virtualize · stable heights", 2, "flex:1"),
       box("blue", "new posts", "\"5 new posts\" pill, no jump", 2, "flex:1"),
       box("green", "likes", "optimistic + rollback", 2, "flex:1"),
       box("orange", "a11y", "a \"Load more\" button", 2, "flex:1"), style="margin-top:22px"),
 "steps": [
  "Design a news feed with infinite scroll. Use cursor pagination, not offset. With page three, new posts arriving at the top shift everything, so users see duplicates, or miss posts. A cursor means: give me the items after this one.",
  "Load more with an intersection observer on a sentinel element near the bottom, not a scroll listener. A root margin of six hundred pixels starts loading before the user reaches the end. TanStack Query's use infinite query keeps the pages.",
  "Then the deep dives. Many posts in the DOM? Virtualize, and keep heights stable to avoid layout shift. New posts? Show a five new posts pill, instead of jumping the list. Likes? Optimistic, with rollback. Restore the scroll position when the user comes back. And infinite scroll traps keyboard users above the footer, so add a load more button.",
 ]},

{"html": H("Data and real-time ", "strategies") + row(
   col(table(["Pattern", "When"], [
     (["prefetch on hover", "likely next clicks"], 0),
     (["parallel requests", "independent data"], 0),
     (["<b>BFF</b> endpoint", "one screen, many calls"], 0),
     (["optimistic update", "likes, toggles · not payments"], 1)], size=27), style="flex:1"),
   col(table(["", "Use for"], [
     (["Polling", "dashboards every minute"], 2),
     (["SSE", "notifications, live scores"], 2),
     (["WebSocket", "chat, collaboration, games"], 2)], size=27),
       box("gray", "offline", "service worker shell · IndexedDB queue syncs later", 3), style="width:620px;flex-shrink:0"), top=True),
 "steps": [
  "Decisions that come up in almost every design. Prefetch on hover for links users will likely click. Parallel requests for independent data. And a BFF, a backend for frontend, when one screen would otherwise make many calls. The server aggregates them into one.",
  "Optimistic updates change the UI first, and roll back if the request fails. Great for likes, toggles, and reordering. Risky for payments.",
  "For real-time, polling asks every few seconds. Simplest, fine for dashboards. Server sent events push one way, over plain HTTP, for notifications and live scores. And WebSockets go both ways, for chat, collaborative editing, and games.",
  "And offline. A service worker caches the app shell, and IndexedDB stores data plus a queue of pending changes, that sync when the connection returns.",
 ]},

{"html": H("Cross-cutting ", "concerns") + fill(
   row(box("blue", "performance", "code splitting · images · virtualization · Web Vitals", 0, "flex:1"),
       box("green", "accessibility", "keyboard for everything · focus · ARIA patterns", 0, "flex:1"),
       box("purple", "i18n", "<code>Intl</code> · plurals · text grows 30–40% · RTL", 0, "flex:1")),
   row(box("red", "security", "escape · sanitise · token storage · CSP", 0, "flex:1"),
       box("orange", "reliability", "error boundaries · retries with backoff", 0, "flex:1"),
       box("gray", "observability + testing", "Sentry · web-vitals · flags · E2E", 0, "flex:1")),
   note("Mention all in a sentence · go <u>deep on the two</u> that matter most for this product", 1)),
 "steps": [
  "Close every design by walking through these. Performance. Accessibility. Internationalisation, with the Intl APIs for dates and numbers, plural rules, longer text, and right-to-left layouts. Security. Reliability, with error boundaries and retries. And observability and testing, with error reporting, real user metrics, and feature flags.",
  "You won't have time to go deep on all of them. Mention each in a sentence, then go deep on the two that matter most for the product. Performance and accessibility for a feed. Security and reliability for payments.",
 ]},

quiz([
  ("Autocomplete: three must-haves?", "<b style=\"display:inline\">debounce</b> · cancel stale · cache", "blue",
   "Quiz time. What are three must-haves for an autocomplete?",
   "Debounce the input, cancel stale requests, and cache results."),
  ("Feed pagination?", "<b style=\"display:inline\">cursor</b>-based, not offset", "green",
   "How should a feed paginate?",
   "With a cursor, not an offset."),
  ("What is a BFF?", "a backend-for-frontend that aggregates for one screen", "purple",
   "And what's a BFF?",
   "A backend for frontend endpoint, that aggregates data for one screen."),
]),

recap(["RADIO: Requirements, Architecture, Data, Interface, Optimisations",
       "Clarify scope first · name trade-offs · every UX state",
       "Normalise client data · state in the right home",
       "Autocomplete: debounce, abort, cache · combobox ARIA",
       "Feed: cursor pagination · IntersectionObserver",
       "Polling vs SSE vs WebSocket · cross-cutting concerns"],
  "Let's recap. Use RADIO: requirements, architecture, data model, interface, and optimisations. Clarify the scope first, name your trade-offs, and cover every UX state. Normalise client data, and put each kind of state in its right home. An autocomplete needs debouncing, aborting, caching, and the combobox pattern. A feed uses cursor pagination and an intersection observer. And know polling, server sent events, and WebSockets, plus the cross-cutting concerns. Next time: the machine coding round!"),
]
