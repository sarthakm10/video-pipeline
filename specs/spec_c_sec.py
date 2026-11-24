from conc import *

TAG = "Spring · Security"
TRACK = "Java Fullstack · Spring Boot"
FILE = "Spring Security.mp4"

SLIDES = [
title_slide(0, "Spring Security", "Who are you, what may you do, and how a filter chain enforces it",
  "Welcome to Spring Security.",
  "Security questions come up in almost every backend interview. Who is this user? What are they allowed to do? How does a stateless API know who's calling? By the end you'll know authentication versus authorization, the attacks every app must handle, the filter chain at the heart of Spring Security, password hashing, sessions versus tokens, JWT, OAuth2, and how to protect URLs and methods.",
  pill="SPRING · CONCEPT"),

{"html": H("Authentication vs ", "authorization") + row(
   box("blue", "authentication", "<b style=\"display:inline\">who</b> are you? · login, token, certificate", 0, "flex:1"),
   box("green", "authorization", "what may you <b style=\"display:inline\">do</b>? · roles, permissions", 1, "flex:1"), top=True) +
   row(box("orange", "401 Unauthorized", "really means <b style=\"display:inline\">unauthenticated</b>: we don't know who you are", 2, "flex:1"),
       box("red", "403 Forbidden", "we know who you are, and the answer is <b style=\"display:inline\">no</b>", 2, "flex:1"), style="margin-top:24px"),
 "steps": [
  "Two words that sound alike. Authentication answers: who are you? You prove it with a password, a token, or a certificate.",
  "Authorization answers: what are you allowed to do? It happens after authentication, using roles or permissions.",
  "And the status codes follow that split, with a confusing name. Four oh one, unauthorized, actually means unauthenticated. We don't know who you are, so log in. Four oh three, forbidden, means we know exactly who you are, and you're not allowed.",
 ]},

{"html": H("The attacks to ", "know") + table(["Attack", "What happens", "Defence"], [
     (["<b>CSRF</b>", "another site makes your browser send a request <b>with your cookie</b>", "CSRF token · SameSite cookies · on by default"], 0),
     (["<b>XSS</b>", "injected script runs in your page, steals data", "escape output · Content-Security-Policy"], 1),
     (["<b>SQL injection</b>", "input changes the meaning of a query", "bind parameters, always"], 2),
     (["<b>CORS</b> (not an attack)", "browser blocks cross-origin calls unless the server allows them", "allow only your front-end's origin"], 3)], size=27),
 "steps": [
  "Four terms you must know. CSRF, cross site request forgery: a malicious site makes your browser send a request to your bank, and the browser attaches your session cookie automatically. The defence is a CSRF token, or same site cookies. Spring Security turns CSRF protection on by default.",
  "XSS, cross site scripting: an attacker's script gets into your page and runs as if it were yours. Escape everything you output, and add a content security policy.",
  "SQL injection: user input changes the meaning of a query. Bind parameters prevent it completely.",
  "And CORS isn't an attack, it's a browser rule. By default a page can't call an API on another origin. The server must explicitly allow your front end's origin. And that's it, not star, when cookies or credentials are involved.",
 ]},

{"html": H("The filter ", "chain") + row(
   box("gray", "request", "", 0, "width:170px"),
   box("blue", "DelegatingFilterProxy", "a servlet filter that hands off to Spring", 0, "flex:1"),
   box("purple", "SecurityFilterChain", "CORS · CSRF · authentication filters · exception handling · authorization", 1, "flex:1"),
   box("green", "Dispatcher­Servlet", "your controller", 1, "width:280px"), top=True) +
   row(col(box("orange", "SecurityContextHolder", "who is logged in, for <b style=\"display:inline\">this</b> request (thread-local)", 2),
           box("blue", "AuthenticationManager", "checks credentials with a <code>UserDetailsService</code> + <code>PasswordEncoder</code>", 2), gap=16, style="flex:1"),
       box("red", "it all happens before your code", "an unauthenticated request never reaches the controller", 3, "flex:1"), style="margin-top:26px", top=True),
 "steps": [
  "Spring Security is a chain of servlet filters that runs before the dispatcher servlet. A delegating filter proxy plugs it into Tomcat, and hands each request to Spring's security filter chain.",
  "That chain is a list of filters in order. CORS, CSRF checks, filters that read credentials, an exception filter that turns failures into four oh one or four oh three, and finally the authorization check. Only then does the request reach your controller.",
  "When a filter authenticates the user, the result goes into the security context holder. It's thread local, so any code handling this request can ask who is logged in. The checking itself is done by the authentication manager, which loads the user with a user details service and compares passwords with a password encoder.",
  "The key point: all of this happens before your code. A request that fails security never reaches your controller.",
 ]},

{"html": H("Configuring ", "security") + code("""§0 @Bean
§0 SecurityFilterChain api(HttpSecurity http) throws Exception {
§0   return http
§1     .authorizeHttpRequests(auth -> auth
§1         .requestMatchers("/api/public/**").permitAll()
§1         .requestMatchers(HttpMethod.DELETE, "/api/**").hasRole("ADMIN")
§1         .anyRequest().authenticated())
§2     .httpBasic(Customizer.withDefaults())
§2     .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
§0     .build();
§0 }""", 27) + note("Rules are checked <u>top to bottom</u>: specific first, <code>anyRequest()</code> last", 3),
 "steps": [
  "You configure security by declaring a security filter chain bean, using the http security builder. This lambda style replaced the old configurer classes.",
  "Authorize HTTP requests lists the URL rules. Public endpoints are permitted for everyone. Deletes need the admin role. And any other request needs an authenticated user.",
  "Then choose how users authenticate, here HTTP basic, and for an API, make it stateless, so no session is created.",
  "One rule to remember: the matchers are checked from top to bottom, and the first match wins. Put specific rules first, and any request last. Get the order wrong, and a broad rule can hide a stricter one.",
 ]},

{"html": H("Users and ", "passwords") + row(
   col(box("blue", "UserDetailsService", "<code>loadUserByUsername(name)</code> → username, hash, roles (from your DB)", 0),
       box("red", "never store passwords", "not plain, not encrypted, not MD5/SHA-256", 1),
       box("green", "BCrypt", "slow on purpose · random <b style=\"display:inline\">salt</b> per password · tunable cost", 1), gap=16, style="flex:1"),
   col(code("""§2 @Bean PasswordEncoder encoder() {
§2   return PasswordEncoderFactories
§2       .createDelegatingPasswordEncoder();
§2 }
§2 // stored: {bcrypt}$2a$10$N9qo…""", 22),
       box("purple", "login", "hash the attempt the same way and <b style=\"display:inline\">compare</b> · you can't decrypt", 3), gap=16, style="width:680px"), top=True),
 "steps": [
  "Where do users come from? You implement user details service. Given a username, it loads the user from your database: the username, the password hash, and the roles.",
  "Never store passwords as plain text. Not encrypted either, because encryption can be reversed. And not with a fast hash like MD5 or SHA two fifty six, which can be guessed billions of times a second.",
  "Use BCrypt. It's deliberately slow, it adds a random salt to each password so identical passwords get different hashes, and its cost can be raised as computers get faster.",
  "The delegating encoder stores the algorithm name in front of the hash, so you can upgrade algorithms later. At login, the attempt is hashed the same way, and the hashes are compared. Nobody, not even you, can decrypt a stored password.",
 ]},

{"html": H("Sessions vs ", "tokens") + row(
   box("blue", "stateful: form login + session", "server stores the session · browser sends a <code>JSESSIONID</code> cookie · needs CSRF protection · logout is easy", 0, "flex:1"),
   box("green", "stateless: a token on every request", "<code>Authorization: Bearer …</code> · nothing stored on the server · scales across instances · no cookie → CSRF off", 1, "flex:1"), top=True) +
   table(["", "Session", "Token (JWT)"], [
     (["server state", "yes", "no"], 2),
     (["revoke / log out", "delete the session", "hard: wait for expiry or keep a denylist"], 2),
     (["typical client", "server-rendered web app", "SPA · mobile · service to service"], 2)], size=28),
 "steps": [
  "There are two ways to remember a logged in user. Stateful: after form login, the server keeps a session, and the browser sends a session cookie with every request. Because the browser sends that cookie automatically, you need CSRF protection. Logging out is easy, just delete the session.",
  "Stateless: the client sends a token with every request, in the authorization header. The server stores nothing, so any instance can handle any request, which scales well. And since no cookie is involved, CSRF protection can be turned off.",
  "The trade off: sessions are easy to revoke but need server state. Tokens need no state, but you can't easily cancel one before it expires. Sessions suit server rendered apps. Tokens suit single page apps, mobile apps, and services calling each other.",
 ]},

{"html": H("", "JWT") + row(
   col(box("gray", "header.payload.signature", "three Base64URL parts", 0),
       box("blue", "payload (claims)", "<code>sub</code>: user · <code>roles</code> · <code>exp</code>: expiry", 0),
       box("orange", "signed, not encrypted", "anyone can <b style=\"display:inline\">read</b> it · nobody can <b style=\"display:inline\">change</b> it without the key", 1), gap=16, style="flex:1"),
   col(box("green", "validating", "check the signature · check <code>exp</code> · then trust the claims", 2),
       box("purple", "Spring", "<code>oauth2ResourceServer(o -&gt; o.jwt(…))</code> does it for you", 2),
       box("red", "rules", "short expiry + refresh token · no secrets in the payload · HTTPS only", 3), gap=16, style="flex:1"), top=True),
 "steps": [
  "A JSON web token has three parts separated by dots: a header, a payload, and a signature. The payload holds claims, like the user's id, their roles, and an expiry time.",
  "The most misunderstood point: a JWT is signed, not encrypted. Anyone who has it can decode and read the payload. But nobody can change it, because the signature would no longer match without the server's key.",
  "So validating a token means checking the signature and the expiry. If both pass, trust the claims, with no database lookup. In Spring, configure the app as an OAuth2 resource server with JWT, and the filter does this for you.",
  "And three rules. Keep access tokens short lived, and use refresh tokens to get new ones. Never put secrets in the payload. And only send tokens over HTTPS.",
 ]},

{"html": H("OAuth2 and method ", "security") + row(
   col(box("blue", "OAuth2", "<b style=\"display:inline\">authorization</b>: let an app act for you without your password", 0),
       box("green", "OpenID Connect", "OAuth2 + an ID token → <b style=\"display:inline\">login</b> (\"Sign in with Google\")", 0),
       box("gray", "roles", "client app · authorization server (issues tokens) · resource server (your API)", 1), gap=16, style="flex:1"),
   col(code("""§2 @EnableMethodSecurity
§2 @PreAuthorize("hasRole('ADMIN')")
§2 void deleteUser(long id) { … }
§3 @PreAuthorize("#id == authentication.name")
§3 Account load(String id) { … }""", 22),
       box("orange", "hasRole('ADMIN')", "checks the authority <code>ROLE_ADMIN</code>", 3), gap=16, style="width:700px"), top=True),
 "steps": [
  "OAuth2 is about authorization. It lets one app act on your behalf, without ever seeing your password. OpenID Connect adds an ID token on top, which turns it into a login protocol. That's sign in with Google.",
  "There are three roles. The client app, the authorization server that issues tokens, and the resource server, your API, which validates those tokens.",
  "URL rules aren't always enough, so you can also secure methods. Enable method security, then put pre authorize on a service method, like delete user only for admins.",
  "Expressions can use arguments too, like letting users load only their own account. One detail: has role admin actually checks for an authority named role underscore admin. Spring adds that prefix for you.",
 ]},

quiz([
  ("Logged in, but no permission. 401 or 403?", "<b style=\"display:inline\">403</b> Forbidden", "red",
   "Quiz time. A user is logged in, but doesn't have permission. Four oh one or four oh three?",
   "Four oh three. Four oh one means we don't know who you are."),
  ("Is a JWT's payload secret?", "<b style=\"display:inline\">no</b>: signed, not encrypted", "orange",
   "Is the payload of a JWT secret?",
   "No. It's signed, not encrypted, so anyone can read it. They just can't change it."),
  ("Why is CSRF off for a token API?", "no <b style=\"display:inline\">cookie</b> is sent automatically", "blue",
   "Why can CSRF protection be disabled for a stateless token API?",
   "Because CSRF abuses cookies the browser sends automatically, and a token in a header isn't sent automatically."),
]),

recap(["Authentication = who · authorization = what · 401 vs 403",
       "CSRF · XSS · SQL injection · CORS",
       "A filter chain runs before your controller",
       "Rules top to bottom · BCrypt, never plain passwords",
       "Session (stateful, CSRF) vs token (stateless)",
       "JWT: signed not encrypted · @PreAuthorize for methods"],
  "Let's recap. Authentication is who you are, authorization is what you may do, and that's four oh one versus four oh three. Know CSRF, XSS, SQL injection, and how CORS works. Spring Security is a filter chain that runs before your controller. URL rules are checked top to bottom, and passwords are hashed with BCrypt. Sessions are stateful and need CSRF protection, tokens are stateless. A JWT is signed, not encrypted. And pre authorize secures individual methods. Now practise with the exercises in your notes!"),
]
