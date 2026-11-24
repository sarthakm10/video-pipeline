from lib import *

TAG = "Frontend 11 · Modules, npm and Tooling"
FILE = "Frontend 11 Modules, npm and Tooling.mp4"

SLIDES = [
title_slide(11, "Modules, npm & Tooling", "Maven and the JDK, frontend edition",
  "Welcome to module eleven: modules, npm, and tooling.",
  "Real frontend projects aren't one script tag. They're hundreds of files, split into modules, with packages from npm, and a build tool that bundles it all for the browser. Think of this as Maven and the JDK, frontend edition. You set it up once per project, and then React sits on top."),

{"html": H("import and ", "export") + row(
   code("""// math.js
§0 export const PI = 3.14159;
§0 export function area(r) {
§0   return PI * r * r;
§0 }
§1 export default function format(n) {
§1   return n.toFixed(2);
§1 }""", 30, style="flex:1"),
   code("""// app.js
§2 import format, { area, PI } from "./math.js";
§3 import { area as circleArea } from "./math.js";
§3 import * as math from "./math.js";

format(area(2));   // "12.57" """, 30, style="flex:1.4"), top=True) +
   table(["", "Named", "Default"], [
     (["Per file", "as many as you like", "at most one"], 2),
     (["Import with", "exact name, in braces", "any name, no braces"], 2),
     (["Good for", "utilities, constants", "the file's main thing (a component)"], 2)], size=29),
 "steps": [
  "A module is a file with its own scope. Nothing leaks out unless you export it. Here, math dot j s has two named exports: PI, and the area function.",
  "It can also have one default export. Usually the file's main thing.",
  "To import, the default comes first, with any name you like and no braces. Then named exports, with their exact names, in curly braces.",
  "You can rename a named import with as, or import everything as one object. And you'll still see the older require style in Node code, but new frontend code uses import and export.",
 ]},

{"html": H("Node.js and ", "npm") + row(
   code("""§0 node --version
§1 npm init -y             # creates package.json
§1 npm install axios       # runtime dependency
§1 npm install -D vitest   # dev dependency
§1 npm run dev             # a script from package.json
§1 npx some-tool           # run without installing""", 30, style="flex:1"),
   col(box("green", "Node.js", "runs JavaScript outside the browser: needed for the tools", 0),
       box("blue", "npm", "Maven Central + the <code>mvn</code> command", 1), style="width:520px"), top=True),
 "steps": [
  "Node dot j s runs JavaScript outside the browser. Even though your app runs in the browser, you need Node for the tools. Install the L T S version.",
  "It comes with npm, the package manager. Think Maven Central, plus the m v n command. N p m init creates a package dot json. Install adds a dependency. Dash capital D makes it a dev dependency, for tools and tests. N p m run runs a script. And n p x runs a package's command without installing it globally.",
 ]},

{"html": H("package.json and the ", "lock file") + row(
   code("""{
  "name": "task-ui",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": { "react": "^19.0.0" },
  "devDependencies": { "vite": "^6.0.0" }
}""", 28, style="flex:1"),
   table(["File", "Commit?"], [
     (["<code>package.json</code>", "✓ yes"], 0),
     (["<code>package-lock.json</code><br><small style=\"font-size:24px\">exact versions</small>", "✓ yes"], 1),
     (["<code>node_modules/</code>", "✗ .gitignore"], 1)], size=30), top=True) +
   note("<code>^1.7.0</code> → any 1.x from 1.7.0 · <code>~1.7.0</code> → only 1.7.x · <code>npm ci</code> installs exactly the lock file", 2),
 "steps": [
  "Package dot json is the project file, like your p o m dot x m l. It lists your scripts, your dependencies, and your dev dependencies, with version ranges.",
  "Package lock dot json records the exact versions that were installed, so every machine gets the same. Commit both. But never commit node modules. It's the downloaded packages, and it's often huge. Add it to git ignore.",
  "A caret allows any newer minor version, so no breaking changes. A tilde allows only patches. After cloning a project, run n p m install. And on CI servers, n p m c i installs exactly what's in the lock file.",
 ]},

{"html": H("What ", "Vite", " does") + code("""npm create vite@latest task-ui -- --template react-ts
npm run dev       # http://localhost:5173 · instant hot reload
npm run build     # production build in dist/""", 30) +
   row(box("blue", "dev: npm run dev", "serves files as they are · starts in milliseconds · hot reload keeps page state", 1, "flex:1"),
       box("green", "prod: npm run build", "<b style=\"display:inline\">bundles</b> · <b style=\"display:inline\">minifies</b> · <b style=\"display:inline\">tree-shakes</b> · hashed filenames <code>index-a1b2c3.js</code>", 2, "flex:1"), style="margin-top:26px") +
   note("<code>dist/</code> = plain static files: Vercel, Netlify, S3, or Spring Boot's <code>static/</code>", 3),
 "steps": [
  "A real project needs more than the browser gives you. Importing npm packages by name, turning JSX and TypeScript into JavaScript, and a small, fast production build. Vite is the standard tool for new projects. One command creates a React plus TypeScript starter.",
  "In development, Vite serves your files as they are, transforming each one on request. So it starts in milliseconds. And hot module replacement shows your edits instantly, without losing the page's state.",
  "For production, it bundles everything into a few files, minifies them, and tree shakes, which means dropping code you never use. And it adds a content hash to each filename, so browsers can cache them for a long time.",
  "The result is a dist folder of plain static files. You can deploy it anywhere. Even inside Spring Boot's static folder. And Create React App is deprecated, so don't start new projects with it.",
 ]},

{"html": H("ESLint and ", "Prettier") + table(["Tool", "Job", "Example catch"], [
   (["<b>ESLint</b>", "finds likely bugs and bad patterns", "unused variable · <code>==</code> · missing hook dependency"], 0),
   (["<b>Prettier</b>", "formats code the same for everyone", "quotes · semicolons · line breaks"], 1)], size=31) +
   code("""§2 npx eslint .            # report problems
§2 npx prettier --write .  # reformat every file""", 30, style="margin-top:24px") +
   note("Format on save in VS Code · pre-commit hook (husky + lint-staged) · like Checkstyle and SpotBugs", 2),
 "steps": [
  "Two tools almost every team runs. ESLint finds likely bugs and bad patterns. An unused variable, double equals instead of triple, or a missing hook dependency.",
  "Prettier just formats code, the same way for everyone. Quotes, semicolons, line breaks. No more style arguments in code review.",
  "Set up VS Code to format on save and show ESLint warnings inline, and many mistakes never reach the browser. Teams often add a pre-commit hook too. It's the same idea as Checkstyle and SpotBugs in Java.",
 ]},

{"html": H("Environment ", "variables") + row(
   code("""§0 # .env.development
§0 VITE_API_URL=http://localhost:8080/api
§0 # .env.production
§0 VITE_API_URL=https://api.mytasks.com/api

§0 const API = import.meta.env.VITE_API_URL;""", 29, style="flex:1"),
   col(box("green", "✓ fine", "API URLs · public analytics IDs · feature flags", 2),
       box("red", "✗ never", "DB passwords · secret API keys · JWT secrets", 2), style="width:500px"), top=True) +
   note("Everything in a frontend build is <u>public</u> · secrets live on the backend", 1),
 "steps": [
  "Your API address is different on your laptop and in production. Vite reads dot env files. Only variables starting with VITE underscore are exposed to your code. And they're inlined into the JavaScript at build time.",
  "And that's the big rule. Everything in a frontend build is public. Anyone can open dev tools and read your JavaScript, including every environment variable in it.",
  "So API URLs and feature flags are fine. But database passwords, secret API keys, and JWT secrets? Never. Secrets belong on your backend. If the frontend needs a paid third party API, it calls your backend, which adds the secret and forwards the request.",
 ]},

quiz([
  ("Named vs default export?", "named: many, in braces · default: one, any name", "blue",
   "Quiz time. Named versus default exports?",
   "Named exports: as many as you like, imported in braces. Default: one per file, imported with any name."),
  ("Commit <code>node_modules</code>?", "<b style=\"display:inline\">No</b> · commit package.json + the lock file", "red",
   "Should you commit node modules?",
   "No. Commit package dot json and the lock file."),
  ("A secret API key in <code>VITE_KEY</code>: safe?", "<b style=\"display:inline\">No</b> · it's inlined into public JS", "orange",
   "And is a secret API key safe in a VITE environment variable?",
   "No! It's inlined into the JavaScript, which anyone can read."),
]),

recap(["Modules: named (braces) and default (any name) exports",
       "npm installs packages · <code>-D</code> for dev tools",
       "Commit package.json + lock · never node_modules",
       "Vite: instant dev server, optimised build in <code>dist/</code>",
       "Build: bundle, minify, tree-shake, hash",
       "ESLint finds bugs · Prettier formats · secrets stay on the backend"],
  "Let's recap. Modules share only what they export, with named exports in braces, and one default. N p m installs packages, with dash D for dev tools. Commit package dot json and the lock file, never node modules. Vite gives you an instant dev server, and an optimised build. A production build bundles, minifies, tree shakes, and hashes filenames. ESLint finds bugs, Prettier formats, and secrets always stay on the backend. Next time: the JavaScript interview deep dive!"),
]
