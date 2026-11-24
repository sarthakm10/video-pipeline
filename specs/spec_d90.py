from conc import *

TAG = "Day 90 · Terraform Practice and Cloud Review"
TRACK = "Java Fullstack · Cloud"
FILE = "Day 90 Terraform Practice and Cloud Review.mp4"

SLIDES = [
title_slide(90, "Terraform Practice & Cloud Review", "Write real infrastructure, then pull the whole AWS week together",
  "Welcome to day ninety: Terraform practice and a cloud review.",
  "Today you apply what you learned. We'll write Terraform for a secure S3 bucket, and for a server with its security group and role. Then we review the whole cloud week with decision rules you can use in interviews, and finish by drawing a production architecture for the Spring Boot app.",
  pill="DAY 90 · CLOUD"),

{"html": H("Practice 1: a secure ", "bucket") + code("""§0 resource "aws_s3_bucket" "files" { bucket = "task-files-${var.env}" }
§1 resource "aws_s3_bucket_versioning" "v" {
§1   bucket = aws_s3_bucket.files.id
§1   versioning_configuration { status = "Enabled" }
§1 }
§2 resource "aws_s3_bucket_server_side_encryption_configuration" "e" {
§2   bucket = aws_s3_bucket.files.id
§2   rule {
§2     apply_server_side_encryption_by_default { sse_algorithm = "aws:kms" }
§2   }
§2 }
§3 resource "aws_s3_bucket_lifecycle_configuration" "l" {
§3   bucket = aws_s3_bucket.files.id
§3   rule {
§3     id     = "archive"
§3     status = "Enabled"
§3     transition {
§3       days          = 90
§3       storage_class = "GLACIER"
§3     }
§3   }
§3 }""", 19),
 "steps": [
  "First practice: a secure bucket. In the current AWS provider, the bucket itself is one resource, and each feature is a separate resource pointing at it.",
  "Turn on versioning, so overwrites and deletes can be undone.",
  "Set default encryption with KMS.",
  "And add a lifecycle rule moving objects to Glacier after ninety days. Public access blocking is a fourth resource. Together, that's a good candidate for a module.",
 ]},

{"html": H("Practice 2: server, firewall, ", "role") + row(
   code("""§0 resource "aws_security_group" "app" {
§0   vpc_id = var.vpc_id
§0   ingress {
§0     from_port       = 8080
§0     to_port         = 8080
§0     protocol        = "tcp"
§0     security_groups = [aws_security_group.alb.id]
§0   }
§0 }
§1 resource "aws_iam_role" "app" {
§1   assume_role_policy = data.aws_iam_policy_document.ec2_trust.json
§1 }
§2 resource "aws_instance" "app" {
§2   ami                    = data.aws_ami.al2023.id
§2   instance_type          = "t3.small"
§2   subnet_id              = var.private_subnet_id
§2   vpc_security_group_ids = [aws_security_group.app.id]
§2   iam_instance_profile   = aws_iam_instance_profile.app.name
§2 }""", 21, style="flex:1"),
   col(box("blue", "security group", "8080 only from the ALB's group", 0),
       box("green", "role", "trust: EC2 may assume it · then attach least-privilege policies", 1),
       box("purple", "instance", "private subnet · gets the role via an instance profile", 2), gap=14, style="width:480px"), top=True),
 "steps": [
  "Second practice: a server. The security group allows port eight zero eight zero only from the load balancer's security group. An egress rule, not shown, lets traffic out.",
  "The IAM role has a trust policy saying EC2 may assume it. Then you attach least privilege permissions, like reading that bucket.",
  "The instance goes in a private subnet, with the security group, and receives the role through an instance profile. No access keys anywhere.",
 ]},

{"html": H("Review: compute and ", "storage") + table(["Question", "Rule of thumb"], [
     (["EC2, ECS or Lambda?", "OS control → EC2 · containers → ECS Fargate · short events → Lambda"], 0),
     (["Which EC2 pricing?", "steady → Savings Plans · flexible → On-Demand · batch → Spot"], 0),
     (["Which S3 class?", "hot → Standard · unknown → Intelligent-Tiering · archive → Glacier"], 1),
     (["Browser upload?", "presigned URL · never AWS keys in the client"], 1),
     (["Which encryption?", "default SSE-S3 · audit or key control → SSE-KMS"], 1)], size=27),
 "steps": [
  "Let's review with rules of thumb. For compute: need the operating system, EC2. Containers, ECS on Fargate. Short event driven tasks, Lambda. For pricing: steady load on savings plans, flexible on demand, and interruptible batch on spot.",
  "For storage: hot data in standard, unknown patterns in intelligent tiering, archives in Glacier. Browser uploads use presigned URLs. And use KMS encryption when you need an audit trail or control over the key.",
 ]},

{"html": H("Review: network, IAM, ", "secrets") + table(["Question", "Rule of thumb"], [
     (["Where does the DB go?", "a private subnet · SG allows 5432 from the app SG only"], 0),
     (["Security group or NACL?", "SGs (stateful) for almost everything · NACLs for coarse blocks"], 0),
     (["App needs AWS access?", "an IAM <b>role</b> · never access keys"], 1),
     (["KMS or Secrets Manager?", "KMS holds keys · Secrets Manager holds passwords (rotation)"], 1),
     (["Production health?", "CloudWatch alarms on errors and p99 · logs with request ids"], 2)], size=27),
 "steps": [
  "For networking: databases in private subnets, accepting traffic only from the app's security group. Security groups do almost all the work. NACLs are for coarse blocks.",
  "Applications get IAM roles, never access keys. KMS holds encryption keys, while Secrets Manager holds passwords and rotates them.",
  "And production health means CloudWatch alarms on error rate and p ninety nine latency, plus searchable logs with request ids.",
 ]},

{"html": H("Draw it: a production ", "architecture") + graph(
   {"users": (90, 225), "ALB": (330, 225), "ECS": (570, 225), "RDS": (880, 55), "Redis": (880, 168), "S3": (880, 281), "CW": (880, 394)},
   [("users", "ALB"), ("ALB", "ECS"), ("ECS", "RDS"), ("ECS", "Redis"), ("ECS", "S3"), ("ECS", "CW")],
   colors={"ALB": ("#ede9fe", "#7c3aed"), "ECS": ("#dbeafe", "#2563eb"), "RDS": ("#dcfce7", "#16a34a"), "Redis": ("#fee2e2", "#dc2626"), "S3": ("#fef3c7", "#d97706")},
   labels={"ALB": "public subnets", "ECS": "private · 2 AZs"},
   w=1000, h=450, directed=True, step=0, r=50) +
   note("Everything in Terraform · secrets from Secrets Manager · deploys from CI", 1),
 "steps": [
  "Here's the picture to draw in an interview. Users hit a load balancer in public subnets. It forwards to the Spring Boot app on ECS Fargate, in private subnets across two zones. The app uses PostgreSQL on RDS with Multi AZ, Redis on ElastiCache for caching and rate limits, S3 for files, and CloudWatch for logs, metrics and alarms.",
  "All of it is described in Terraform, secrets come from Secrets Manager, and CI builds the image and deploys it. If you can draw this and explain each arrow, you're ready for most cloud questions.",
 ]},

quiz([
  ("Bucket features in the current AWS provider?", "<b style=\"display:inline\">separate</b> resources per feature", "blue",
   "Quiz time. How are bucket features like versioning written in the current AWS provider?",
   "As separate resources that point at the bucket."),
  ("Steady 24/7 load: which pricing?", "<b style=\"display:inline\">Savings Plans</b> / Reserved", "green",
   "Steady, around the clock load. Which EC2 pricing?",
   "Savings plans or reserved instances."),
  ("App → DB traffic: allow by IP or by…?", "the app's <b style=\"display:inline\">security group</b>", "purple",
   "Should the database allow the app by IP address, or by what?",
   "By the app's security group, so it works however many instances run."),
]),

recap(["A secure bucket = bucket + versioning + KMS + lifecycle",
       "SG from the ALB · IAM role via instance profile",
       "Compute & pricing rules of thumb",
       "Storage classes · presigned URLs · KMS",
       "Private DB · roles not keys · alarms on symptoms",
       "ALB → ECS → RDS + Redis + S3 + CloudWatch"],
  "Let's recap. A secure bucket in Terraform combines the bucket with versioning, KMS encryption and lifecycle rules. A server gets a security group that only trusts the load balancer, and a role through an instance profile. We reviewed rules of thumb for compute, pricing, storage and encryption, and for networking, roles, secrets and monitoring. And the architecture to draw: load balancer, ECS, RDS, Redis, S3 and CloudWatch. Tomorrow we start system design."),
]
