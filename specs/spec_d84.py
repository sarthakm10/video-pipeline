from conc import *

TAG = "Day 84 · AWS: Accounts, IAM and Networking"
TRACK = "Java Fullstack · Cloud"
FILE = "Day 84 AWS Accounts IAM and Networking.mp4"

SLIDES = [
title_slide(84, "AWS: Accounts, IAM & Networking", "Rent computers safely: who may do what, and how the network is fenced",
  "Welcome to day eighty four: getting started with AWS.",
  "Your Spring Boot app is containerised. Now it needs somewhere to run. The cloud lets you rent computers by the hour, but first you need three foundations: an account that can't run up a surprise bill, identities with only the permissions they need, and a private network around your servers. By the end you'll know regions and availability zones, how to set up an account safely, IAM users, roles and policies, and how a VPC is laid out.",
  pill="DAY 84 · CLOUD"),

{"html": H("The cloud, in simple ", "words") + row(
   col(box("blue", "renting computers", "servers, storage and databases by the hour · no hardware to buy", 0),
       box("green", "a region", "a geographic area · e.g. <code>ap-south-1</code> (Mumbai)", 1),
       box("purple", "availability zones", "2–6 separate data centres per region · own power and network", 2), gap=14, style="width:640px"),
   graph({"AZ-a": (140, 100), "AZ-b": (420, 100), "AZ-c": (280, 320)},
         [("AZ-a", "AZ-b"), ("AZ-b", "AZ-c"), ("AZ-c", "AZ-a")],
         colors={"AZ-a": ("#dbeafe", "#2563eb"), "AZ-b": ("#dbeafe", "#2563eb"), "AZ-c": ("#dbeafe", "#2563eb")},
         labels={"AZ-c": "one region · low-latency links"}, w=560, h=420, step=2, r=62), top=True) +
   note("Run at least 2 AZs: one data centre can fail, your app keeps running", 3),
 "steps": [
  "The cloud, in simple words, is renting computers. Instead of buying servers, you rent compute, storage and databases by the hour, and give them back when you're done.",
  "AWS is split into regions, geographic areas like Mumbai or Frankfurt. Pick one close to your users, and where your data is allowed to live.",
  "Each region has several availability zones: separate data centres with their own power and network, joined by fast links.",
  "So run your app in at least two zones. If one data centre fails, the other keeps serving.",
 ]},

{"html": H("Open an account ", "safely") + row(
   box("red", "the root user", "can do <b style=\"display:inline\">anything</b>, even close the account · MFA on it, then lock it away", 0, "flex:1"),
   box("orange", "a billing alarm", "a budget + alert at e.g. $5 · free tier has limits", 1, "flex:1"),
   box("green", "an admin user", "your daily login · via IAM Identity Center · MFA too", 2, "flex:1"), top=True) +
   note("Forgotten resources keep billing: stop or delete what you don't use", 3),
 "steps": [
  "A new account comes with a root user that can do everything, including closing the account. Turn on multi factor authentication for it, and then stop using it.",
  "Next, set a budget with an alert, say five dollars. The free tier is generous but limited, and the alert catches mistakes early.",
  "For daily work, create an administrator identity, ideally through IAM Identity Center, also with MFA.",
  "And remember: resources bill until you delete them. A forgotten database or NAT gateway is the classic surprise bill.",
 ]},

{"html": H("IAM: who can do ", "what") + row(
   col(box("blue", "users and groups", "people · put permissions on groups, not individuals", 0),
       box("green", "roles", "temporary credentials for apps and services · no stored keys", 1),
       box("purple", "policies", "JSON: Effect · Action · Resource · Condition", 2), gap=14, style="width:560px"),
   code("""§2 {
§2   "Effect": "Allow",
§2   "Action": ["s3:GetObject", "s3:PutObject"],
§2   "Resource": "arn:aws:s3:::task-files/*"
§2 }
§3 // default: DENY · an explicit Deny always wins""", 26, style="flex:1"), top=True) +
   note("Least privilege: only the actions and resources the job needs", 4),
 "steps": [
  "Identity and Access Management decides who can do what. Users represent people. Put them in groups, and attach permissions to the groups.",
  "Roles are for software. An EC2 instance or an ECS task assumes a role and gets short lived credentials automatically, so no access keys are stored in your app.",
  "Permissions are written as policies: JSON saying which actions are allowed on which resources. This one lets the app read and write files in one bucket, nothing else.",
  "Everything starts denied. An allow opens a door, and an explicit deny beats any allow.",
  "The guiding rule is least privilege: grant only what the job needs.",
 ]},

{"html": H("Identity vs resource ", "policies") + row(
   box("blue", "identity-based", "attached to a user, group or role · \"what can <i>I</i> do?\"", 0, "flex:1"),
   box("green", "resource-based", "attached to the thing · e.g. an S3 bucket policy · \"who can touch <i>me</i>?\"", 1, "flex:1"),
   box("purple", "cross-account", "a role in account B trusts account A · STS hands out temporary keys", 2, "flex:1"), top=True) +
   pts([("No root use · MFA everywhere · no long-lived access keys", 3),
        ("Rotate what must exist · review unused permissions", 3)], size=30),
 "steps": [
  "Policies can live in two places. Identity based policies attach to a user, group or role, and say what that identity may do.",
  "Resource based policies attach to the resource itself, like a bucket policy, and say who may access it. A request is allowed when the policies together allow it and nothing denies it.",
  "To work across accounts, a role in one account trusts another account, and the Security Token Service hands out temporary credentials.",
  "Best practices: don't use root, use MFA everywhere, avoid long lived access keys, rotate what must exist, and remove permissions nobody uses.",
 ]},

{"html": H("A ", "VPC") + row(
   code("""§0 VPC 10.0.0.0/16
§1 ├── public subnet  10.0.1.0/24   (AZ a)   ALB, NAT gateway
§1 │     route 0.0.0.0/0 → Internet Gateway
§2 ├── private subnet 10.0.2.0/24   (AZ a)   app, database
§2 │     route 0.0.0.0/0 → NAT gateway (outbound only)
§3 └── the same pair again in AZ b""", 24, style="flex:1"),
   col(box("blue", "VPC", "your private network · an IP range", 0),
       box("green", "public subnet", "a route to the internet gateway", 1),
       box("orange", "private subnet", "no inbound from the internet · outbound through NAT", 2), gap=14, style="width:500px"), top=True),
 "steps": [
  "A virtual private cloud is your own private network inside AWS, with an IP range like ten dot zero dot zero dot zero slash sixteen.",
  "You split it into subnets. A public subnet has a route to the internet gateway. Put only the load balancer and NAT gateway there.",
  "A private subnet has no route in from the internet. Your app and database live here. A NAT gateway lets them reach out, to download updates or call an API, without being reachable.",
  "And repeat the pair in a second availability zone for resilience.",
 ]},

{"html": H("Security groups vs ", "NACLs") + table(["", "Security group", "Network ACL"], [
     (["attached to", "an instance / ENI", "a subnet"], 0),
     (["rules", "allow only", "allow and deny"], 0),
     (["state", "<b>stateful</b>: replies allowed automatically", "stateless: allow both directions"], 1),
     (["typical use", "app SG allows 8080 only from the ALB SG", "block a bad IP range"], 2)], size=28) +
   note("Reference security groups, not IPs: \"DB accepts 5432 from the app SG\"", 3),
 "steps": [
  "Two firewalls guard a VPC. A security group is attached to an instance, and only has allow rules. A network ACL is attached to a subnet, and can allow and deny.",
  "Security groups are stateful: if a request is allowed in, its reply is allowed out automatically. NACLs are stateless, so you must allow both directions.",
  "Typically, the app's security group allows port eight zero eight zero only from the load balancer's security group. NACLs are a coarse extra layer, like blocking an IP range.",
  "Reference other security groups instead of IP addresses. The database accepts five four three two from the app group, however many app instances there are.",
 ]},

quiz([
  ("What should you do with the root user?", "add <b style=\"display:inline\">MFA</b>, then stop using it", "red",
   "Quiz time. What should you do with the root user?",
   "Turn on MFA, then stop using it for daily work."),
  ("App on EC2 needs S3: access keys or…?", "an IAM <b style=\"display:inline\">role</b>", "green",
   "An app on EC2 needs to read from S3. Store access keys, or what?",
   "Give it an IAM role. Its credentials are temporary and rotated automatically."),
  ("Where does the database go?", "a <b style=\"display:inline\">private</b> subnet", "blue",
   "Which subnet does the database go in?",
   "A private subnet, with no route in from the internet."),
]),

recap(["Regions contain AZs · use at least 2",
       "Root: MFA, then lock away · set a billing alarm",
       "IAM: groups for people, roles for apps",
       "Policies: default deny · explicit deny wins",
       "VPC: public subnet for ALB, private for app + DB",
       "Stateful security groups reference each other"],
  "Let's recap. A region contains availability zones, and you should use at least two. Protect the root user with MFA, then stop using it, and set a billing alarm. In IAM, people go in groups and applications use roles. Everything is denied by default, and an explicit deny always wins. In a VPC, the load balancer sits in public subnets, and the app and database in private ones. And stateful security groups reference each other. Tomorrow: compute, with EC2, ECS and Lambda."),
]
