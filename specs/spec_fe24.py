from lib import *

TAG = "Frontend 24 · Web Performance and Accessibility"
FILE = "Frontend 24 Web Performance and Accessibility.mp4"

SLIDES = [
title_slide(24, "Web Performance & Accessibility", "A fast page that everyone can use is part of the job",
  "Welcome to module twenty four: web performance and accessibility.",
  "A fast page that everyone can use is part of the job, not an extra. Google ranks pages partly on speed, slow pages lose users, and accessibility is a legal requirement in many countries. This module covers how speed is measured, the fixes that matter most, and accessibility beyond the basics."),

{"html": H("Core Web ", "Vitals") + table(["Metric", "Measures", "Good", "Usual causes"], [
   (["<b>LCP</b>", "main content appears", "≤ 2.5 s", "slow server, big images, blocking CSS/JS"], 0),
   (["<b>INP</b>", "response to clicks, typing", "≤ 200 ms", "long JS tasks, heavy re-renders"], 1),
   (["<b>CLS</b>", "content jumping around", "≤ 0.1", "images without size, late banners"], 2)], size=28) +
   row(box("blue", "Lighthouse", "lab test · production build · incognito · mobile throttling", 3, "flex:1"),
       box("green", "PageSpeed Insights", "plus real-user field data", 3, "flex:1"),
       box("purple", "Performance tab", "long tasks marked in red", 3, "flex:1"), style="margin-top:26px"),
 "steps": [
  "Google's core web vitals measure what users feel. Largest contentful paint is when the main content appears, like the hero image or headline. Good is two and a half seconds or less.",
  "Interaction to next paint is how quickly the page responds to clicks and typing. Under two hundred milliseconds. Long JavaScript tasks are the usual cause when it's bad.",
  "And cumulative layout shift is how much content jumps around while loading. Images without a width and height, or banners inserted above the content.",
  "To measure, run Lighthouse in dev tools, on a production build, in an incognito window, with mobile throttling. PageSpeed Insights adds real user data, which is what Google actually ranks on. And the performance tab shows long tasks in red.",
 ]},

{"html": H("Loading ", "faster") + code("""§0 <img src="hero-800.webp"
§0      srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1600.webp 1600w"
§0      sizes="(max-width: 600px) 100vw, 800px"
§0      width="800" height="450" alt="Dashboard" fetchpriority="high">
§0 <img src="avatar.webp" loading="lazy" width="48" height="48" alt="">""", 26) +
   row(box("orange", "less JS", "split routes · drop huge deps · defer 3rd-party", 1, "flex:1"),
       box("blue", "cache", "hashed files: a year, <code>immutable</code> · <code>index.html</code>: no-cache", 2, "flex:1"),
       box("green", "CDN + Brotli", "files near the user", 3, "flex:1"),
       box("purple", "preconnect", "open the API connection early", 3, "flex:1"), style="margin-top:24px"),
 "steps": [
  "The biggest wins, roughly in order. First, images, which are often most of a page's bytes. Use modern formats like WebP. Serve the right size with source set. Always set width and height, so nothing shifts. Give the hero image high fetch priority, and lazy load only images below the fold. Never the hero.",
  "Second, less JavaScript. Split by route, check your bundle for huge dependencies, and defer third party scripts, like chat widgets.",
  "Third, caching. Build tools give files a content hash in their names, so they can be cached for a year, as immutable. But index dot HTML uses no cache, so users always get the new version.",
  "And serve static files from a CDN near the user, with Brotli compression. Preconnect to your API early. And for API data, show cached data instantly, fetch in parallel, and render a skeleton instead of a blank page.",
 ]},

{"html": H("The critical rendering ", "path") + table(["Tag", "Downloads", "Runs", "Order"], [
   (["<code>&lt;script src&gt;</code>", "<b>blocks</b> parsing", "immediately", "kept"], 0),
   (["<code>defer</code>", "in parallel", "after parsing", "kept"], 1),
   (["<code>async</code>", "in parallel", "when downloaded", "<b>not</b> kept"], 1),
   (["<code>type=\"module\"</code>", "in parallel", "deferred", "kept"], 1)], size=30) +
   row(box("green", "app scripts", "<code>defer</code> or modules", 2, "flex:1"), box("blue", "analytics", "<code>async</code>", 2, "flex:1"),
       box("orange", "CSS", "render-blocking by design · keep it small", 3, "flex:1"), box("purple", "fonts", "<code>font-display: swap</code>", 3, "flex:1"), style="margin-top:26px"),
 "steps": [
  "The browser can't paint until it has the HTML, all the CSS, and has run any blocking scripts. That's the critical rendering path. A plain script tag blocks HTML parsing while it downloads and runs.",
  "Defer downloads in parallel, and runs after parsing, in order. Async downloads in parallel, but runs as soon as it arrives, in any order. And modules are deferred by default.",
  "So use defer, or modules, for your app scripts. Vite already does. And async for independent third party scripts, like analytics.",
  "CSS is render-blocking by design, otherwise you'd see unstyled content flash. So keep it small. And for fonts, font display swap shows fallback text right away, instead of invisible text.",
 ]},

{"html": H("Accessibility in ", "practice") + fill(
   row(box("blue", "keyboard", "real <code>button</code>, <code>a</code>, <code>input</code> · never remove focus without <code>:focus-visible</code> · skip link", 0, "flex:1"),
       box("purple", "focus management", "modal: move in, trap Tab, Escape, return focus · route change: focus the heading", 1, "flex:1")),
   row(box("green", "visual", "contrast <b style=\"display:inline\">4.5:1</b> · not colour alone · zoom to 200% · reduced motion", 2, "flex:1"),
       box("orange", "screen readers + tools", "NVDA, VoiceOver · Lighthouse · axe · jsx-a11y · RTL roles", 3, "flex:1"))),
 "steps": [
  "The standard is WCAG, and most companies aim for level double A. First, the keyboard. Every action must work without a mouse. Use real buttons, links, and inputs. Never remove the focus outline without replacing it. And a skip to main content link helps keyboard users jump past the navigation.",
  "Single page apps need focus management. When a modal opens, move focus into it, trap tab inside, close it on escape, and return focus to the button that opened it. The native dialog element does most of this. And after a route change, move focus to the new page's heading.",
  "Visually, text needs a contrast of at least four and a half to one. Don't rely on colour alone. An error says error, and has an icon. Text must zoom to two hundred percent without breaking. And respect reduced motion.",
  "Screen readers read the accessibility tree, built from your HTML. Try NVDA or VoiceOver on your own app for ten minutes. It's eye-opening. And use tools. Lighthouse, the axe extension, the jsx a11y lint rules, and Testing Library's role queries.",
 ]},

{"html": H("", "ARIA", ": when you need it") + row(code("""§1 <button aria-label="Delete task">🗑️</button>
§1 <input aria-describedby="pw-help">
§1 <button aria-expanded="false" aria-controls="filters">
§2 <div aria-live="polite">3 results found</div>
§2 <p role="alert">Couldn't save the task.</p>
§1 <input aria-invalid="true">
§1 <span aria-hidden="true">★</span>""", 27, style="flex:1"),
   col(box("red", "rule 1", "don't use ARIA if a <b style=\"display:inline\">native element</b> does the job", 0),
       box("blue", "complex widgets", "tabs, combobox, menu → WAI-ARIA patterns · Radix, React Aria", 3),
       box("orange", "bad ARIA &gt; none", "<code>role=\"button\"</code> without keyboard support", 3), style="width:520px"), top=True),
 "steps": [
  "ARIA attributes add roles, names, and states to the accessibility tree, when HTML alone can't. The first rule of ARIA: don't use it if a native element does the job. A button already has the role, focus, and keyboard handling. A div with role button only has the role.",
  "When you do need it. Aria label names an icon-only button. Aria described by links a field to its help or error text. Aria expanded tells whether a menu is open. Aria invalid marks a bad field. And aria hidden hides decoration.",
  "To announce changes that happen without focus moving, like search results or a toast, use an aria live region. Or role alert for urgent ones, which are announced immediately.",
  "Complex widgets, like tabs and comboboxes, need specific roles and keyboard behaviour. Follow the WAI ARIA patterns, or use a library like Radix or React Aria. Because bad ARIA is worse than none.",
 ]},

quiz([
  ("The three Core Web Vitals?", "<b style=\"display:inline\">LCP</b> · <b style=\"display:inline\">INP</b> · <b style=\"display:inline\">CLS</b>", "blue",
   "Quiz time. What are the three core web vitals?",
   "LCP for loading, INP for responsiveness, and CLS for visual stability."),
  ("<code>defer</code> vs <code>async</code>?", "after parsing, in order · whenever downloaded", "green",
   "Defer versus async?",
   "Defer runs in order after parsing. Async runs whenever it's downloaded."),
  ("First rule of ARIA?", "use a <b style=\"display:inline\">native element</b> if one does the job", "red",
   "And what's the first rule of ARIA?",
   "Use a native HTML element if one does the job."),
]),

recap(["LCP ≤ 2.5 s · INP ≤ 200 ms · CLS ≤ 0.1",
       "Images: WebP, srcset, width + height, lazy below the fold",
       "Hashed files cached a year · index.html no-cache",
       "defer app scripts · async analytics · small CSS",
       "Keyboard, focus management, contrast 4.5:1",
       "Native elements first · ARIA when needed · aria-live"],
  "Let's recap. Aim for LCP under two and a half seconds, INP under two hundred milliseconds, and CLS under zero point one. Use modern, right-sized images with a width and height, and lazy load only below the fold. Cache hashed files for a year, and index dot HTML with no cache. Defer app scripts, load analytics async, and keep CSS small. Make everything work by keyboard, manage focus, and keep contrast at four and a half to one. And use native elements first, ARIA only when needed, and live regions for updates. Next time: web security and browser APIs!"),
]
