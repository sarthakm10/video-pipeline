from conc import *

TAG = "Day 89 · Terraform: Infrastructure as Code"
TRACK = "Java Fullstack · Cloud"
FILE = "Day 89 Terraform Infrastructure as Code.mp4"

SLIDES = [
title_slide(89, "Terraform", "Infrastructure as code: describe what you want, let the tool make it so",
  "Welcome to day eighty nine: Terraform and infrastructure as code.",
  "Clicking through the AWS console works once. But can you rebuild the same setup for staging, review a change before it happens, or know who opened that port? Infrastructure as code solves this. By the end you'll know HCL, the plan and apply workflow, state and why it must be shared and locked, modules, count versus for each, and lifecycle rules.",
  pill="DAY 89 · CLOUD"),

{"html": H("Why infrastructure as ", "code") + row(
   box("red", "console clicking", "not repeatable · no review · no history · drifts", 0, "flex:1"),
   box("green", "code in git", "reviewed in PRs · same for dev, staging, prod · rebuild anytime", 1, "flex:1"),
   box("blue", "declarative", "you describe the <b style=\"display:inline\">end state</b> · Terraform works out the steps", 2, "flex:1"), top=True) +
   note("Terraform works with AWS, GCP, Azure, GitHub, Datadog… through providers", 3),
 "steps": [
  "Setting things up by clicking in the console isn't repeatable, isn't reviewed, leaves no history, and slowly drifts between environments.",
  "With infrastructure as code, the setup lives in git. Changes go through pull requests, and the same code builds dev, staging and production.",
  "Terraform is declarative. You describe the end state you want, and Terraform works out what to create, change or delete to get there.",
  "It talks to AWS and many other platforms through plugins called providers.",
 ]},

{"html": H("HCL: the ", "language") + code("""§0 provider "aws" { region = "ap-south-1" }
§1 variable "env" { type = string }
§1 locals { name = "task-files-${var.env}" }
§2 resource "aws_s3_bucket" "files" {
§2   bucket = local.name
§2   tags   = { env = var.env }
§2 }
§3 data "aws_caller_identity" "me" {}                  # read, don't create
§4 output "bucket_arn" { value = aws_s3_bucket.files.arn }""", 26),
 "steps": [
  "Terraform files are written in HCL. A provider block configures where resources go, here AWS in Mumbai.",
  "Variables are inputs, set per environment. Locals are computed helper values.",
  "A resource block declares something to manage: its type, a local name, and its settings. Here, an S3 bucket named after the environment.",
  "A data source reads something that already exists, without managing it.",
  "And outputs expose values, like the bucket's ARN, to the user or to other modules. References between blocks also tell Terraform the order to create things in.",
 ]},

{"html": H("The ", "workflow") + code("""§0 terraform init        # download providers and modules, set up the backend
§1 terraform validate    # syntax and types
§2 terraform plan        # + create   ~ update in place   - destroy   -/+ replace
§3 terraform apply       # do exactly what the plan said
§4 terraform destroy     # remove everything this config manages""", 26) + row(
   box("orange", "read the plan", "a <code>-/+</code> on a database means data loss", 2, "flex:1"),
   box("green", "in CI", "plan on every PR · apply after merge", 3, "flex:1"), top=True, style="margin-top:22px"),
 "steps": [
  "Init downloads the providers and modules, and connects to the state backend.",
  "Validate checks syntax and types.",
  "Plan compares your code with reality and shows what would change: plus to create, tilde to update in place, minus to destroy, and minus plus to replace. Always read it. A replace on a database means losing its data.",
  "Apply makes exactly those changes. In a team, CI runs plan on every pull request, and apply after merging.",
  "Destroy removes everything this configuration manages, handy for short lived test environments.",
 ]},

{"html": H("", "State") + row(
   col(box("blue", "what it is", "a JSON map: code address ↔ real resource id", 0),
       box("red", "local state", "on one laptop · lost or out of sync · contains secrets", 1),
       box("green", "remote state", "S3 bucket (versioned, encrypted) + a lock", 2),
       box("purple", "workspaces", "one state per env from the same code", 3), gap=14, style="width:600px"),
   code("""§2 terraform {
§2   backend "s3" {
§2     bucket       = "acme-tf-state"
§2     key          = "task-app/prod.tfstate"
§2     region       = "ap-south-1"
§2     encrypt      = true
§2     use_lockfile = true    # or a DynamoDB lock table
§2   }
§2 }""", 24, style="flex:1"), top=True),
 "steps": [
  "Terraform remembers what it created in a state file: a map from each address in your code to the real resource id in AWS.",
  "By default it's a local file. That breaks in a team: it can be lost, two people get different versions, and it can contain secrets in plain text.",
  "So store state remotely, in a versioned, encrypted S3 bucket, with a lock so two applies can't run at once. Newer versions lock with a file in S3, older setups use a DynamoDB table.",
  "Workspaces, or separate state keys, give each environment its own state from the same code.",
 ]},

{"html": H("Modules and ", "for_each") + row(
   code("""§0 module "files_bucket" {
§0   source = "./modules/secure-bucket"
§0   name   = "task-files-${var.env}"
§0 }
§1 resource "aws_sqs_queue" "q" {
§1   for_each = toset(["email", "stock", "analytics"])
§1   name     = "orders-${each.key}"
§1 }
§2 # count = 3 → q[0], q[1], q[2]: remove the first → the rest shift""", 23, style="flex:1"),
   col(box("blue", "module", "a reusable folder of resources · registry, git, or local", 0),
       box("green", "for_each", "one per key · stable addresses <code>q[\"email\"]</code>", 1),
       box("orange", "count", "by index · removing one renumbers the rest", 2), gap=14, style="width:520px"), top=True),
 "steps": [
  "A module is a reusable folder of Terraform code. A secure bucket module, with encryption, versioning and public access blocked, can be used everywhere with one block.",
  "To create several similar resources, use for each over a set or map. Each gets a stable address by key, like the email queue.",
  "Count creates them by index. Remove the first item, and every other index shifts, so Terraform wants to destroy and recreate them. Prefer for each.",
 ]},

{"html": H("Lifecycle and ", "import") + table(["Tool", "Does"], [
     (["<code>create_before_destroy</code>", "make the replacement first · no gap"], 0),
     (["<code>prevent_destroy</code>", "plan fails if it would delete this · for databases"], 0),
     (["<code>ignore_changes</code>", "don't fight changes made elsewhere · e.g. ASG size"], 1),
     (["<code>terraform import</code> / <code>import</code> block", "adopt a resource made by hand"], 2),
     (["drift", "someone changed it in the console → plan shows it"], 3)], size=27),
 "steps": [
  "Lifecycle rules tune behaviour. Create before destroy builds the replacement first, so there's no gap. Prevent destroy makes any plan that would delete the resource fail, which is a good guard on databases.",
  "Ignore changes tells Terraform not to undo changes made elsewhere, like an auto scaling group's current size.",
  "Import adopts resources that were created by hand, so Terraform manages them from now on.",
  "And if someone changes something in the console, the next plan shows that drift, and offers to put it back.",
 ]},

quiz([
  ("What does terraform plan show?", "the <b style=\"display:inline\">changes</b> apply would make", "blue",
   "Quiz time. What does terraform plan show?",
   "The exact changes apply would make, without making them."),
  ("Why remote state with a lock?", "shared by the team · no <b style=\"display:inline\">two applies</b> at once", "green",
   "Why keep state remotely, with a lock?",
   "So the team shares one state, and two applies can't run at the same time."),
  ("count or for_each for named queues?", "<b style=\"display:inline\">for_each</b>: stable addresses", "orange",
   "Count or for each, for a set of named queues?",
   "For each, so each queue keeps a stable address."),
]),

recap(["IaC: reviewed, repeatable, declarative",
       "HCL: provider · variable · resource · data · output",
       "init → validate → plan → apply",
       "Remote state in S3 + locking · per-env state",
       "Modules · prefer for_each to count",
       "prevent_destroy · import · drift"],
  "Let's recap. Infrastructure as code makes setups reviewed, repeatable and declarative. HCL has providers, variables, resources, data sources and outputs. The workflow is init, validate, plan and apply, and you always read the plan. Keep state remotely in S3, locked, one per environment. Reuse modules, and prefer for each over count. And protect important resources, import hand made ones, and watch for drift. Tomorrow: Terraform practice and a cloud review."),
]
