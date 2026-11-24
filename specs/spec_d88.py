from conc import *

TAG = "Day 88 · AWS Monitoring and Security"
TRACK = "Java Fullstack · Cloud"
FILE = "Day 88 AWS Monitoring and Security.mp4"

SLIDES = [
title_slide(88, "AWS Monitoring & Security", "See what your app is doing, and keep its keys and secrets safe",
  "Welcome to day eighty eight: monitoring and security on AWS.",
  "Once your app runs on AWS, you need to know when it's unhealthy before users tell you, and you need to protect its secrets. By the end you'll know CloudWatch metrics, logs and alarms, tracing with X Ray, encryption keys with KMS, and where to keep secrets: Secrets Manager or Parameter Store.",
  pill="DAY 88 · CLOUD"),

{"html": H("CloudWatch ", "metrics") + row(
   col(box("blue", "built-in", "CPU, network, ALB latency, 5xx count, RDS connections, SQS age", 0),
       box("green", "custom", "your own · e.g. <code>orders.placed</code> via Micrometer", 1),
       box("purple", "namespace + dimensions", "<code>TaskApp</code> · <code>service=api</code>, <code>env=prod</code>", 2), gap=14, style="width:600px"),
   code("""§1 management.cloudwatch.metrics.export:
§1   enabled: true
§1   namespace: TaskApp
§1   step: 1m
§3 resolution: standard 60 s · high-resolution 1 s
§3 percentiles: p50 · p90 · p99 latency""", 25, style="flex:1"), top=True),
 "steps": [
  "CloudWatch collects metrics from every AWS service automatically: CPU, load balancer latency and error counts, database connections, the age of the oldest queue message.",
  "You can publish custom metrics too. With Micrometer's CloudWatch registry, the business numbers from your Spring app appear alongside.",
  "Metrics live in a namespace and are split by dimensions, like service and environment.",
  "Standard resolution is one minute, high resolution goes down to one second. Watch percentiles like p ninety nine, not just averages, because averages hide the slow requests.",
 ]},

{"html": H("Logs and Logs ", "Insights") + row(
   col(box("blue", "log group / stream", "one group per app · one stream per task or instance", 0),
       box("green", "Logs Insights", "query logs with a SQL-like language", 1),
       box("orange", "metric filters", "turn matching log lines into a metric · e.g. count ERROR", 2),
       box("gray", "retention", "set it · the default keeps logs forever, and bills", 3), gap=14, style="width:560px"),
   code("""§1 fields @timestamp, requestId, message
§1 | filter level = "ERROR"
§1 | stats count(*) by bin(5m)
§1 | sort @timestamp desc
§1 | limit 20""", 26, style="flex:1"), top=True),
 "steps": [
  "Container logs flow into CloudWatch Logs: one log group per application, with a stream per task or instance.",
  "Logs Insights queries them with a SQL like language. Because our app writes JSON logs, fields like request id are directly searchable. Here: errors per five minutes.",
  "A metric filter turns matching log lines into a metric, so you can alarm on them.",
  "Set a retention period. By default logs are kept forever, and you pay for every gigabyte.",
 ]},

{"html": H("Alarms and ", "tracing") + row(
   col(box("red", "alarm", "metric crosses a threshold for N periods → SNS → email / Slack / pager", 0),
       box("orange", "smarter alarms", "anomaly detection · composite: \"5xx high AND latency high\"", 1),
       box("blue", "what to alarm on", "error rate · p99 latency · saturation · queue age · symptoms users feel", 2), gap=14, style="flex:1"),
   col(box("purple", "AWS X-Ray", "distributed tracing · a trace map of services · segments per hop", 3),
       box("green", "today", "OpenTelemetry → X-Ray (ADOT) · sampling keeps cost down", 3), gap=14, style="width:560px"), top=True),
 "steps": [
  "An alarm watches a metric. When it crosses a threshold for several periods in a row, it notifies an SNS topic, which emails, messages Slack, or pages someone.",
  "Anomaly detection learns normal patterns. Composite alarms combine conditions, like a high error rate and high latency together, to cut noise.",
  "Alarm on symptoms users feel: error rate, slow responses, saturation, messages waiting too long. Not on every CPU spike.",
  "For tracing across services, X Ray draws a map of how a request flows, with timings per hop. Today you'd usually send OpenTelemetry traces to it, with sampling to control cost.",
 ]},

{"html": H("KMS and envelope ", "encryption") + row(
   code("""§0 KMS key (never leaves KMS)
§0    │ GenerateDataKey
§0    ▼
§1 data key (plaintext) → encrypts the file locally, then forgotten
§1 data key (encrypted) → stored next to the file
§2 to read: KMS Decrypt(encrypted data key) → decrypt the file""", 24, style="flex:1"),
   col(box("blue", "KMS key", "lives in KMS · usage controlled by a key policy · every use logged", 0),
       box("green", "envelope encryption", "big data encrypted locally with a data key", 1),
       box("purple", "used by", "S3 SSE-KMS · RDS · EBS · Secrets Manager", 2), gap=14, style="width:520px"), top=True),
 "steps": [
  "KMS manages encryption keys. A KMS key never leaves the service. Who can use it is set by a key policy, and every use is logged in CloudTrail.",
  "You can't send gigabytes to KMS, so services use envelope encryption. KMS generates a data key. The plaintext copy encrypts the data locally and is thrown away. The encrypted copy is stored next to the data.",
  "To read, ask KMS to decrypt the small data key, then decrypt the data. This is what S3, RDS, disk volumes and Secrets Manager do under the hood.",
 ]},

{"html": H("Where secrets ", "live") + table(["", "Secrets Manager", "Parameter Store"], [
     (["for", "DB passwords, API keys", "config values, some secrets"], 0),
     (["rotation", "<b>built-in</b> (e.g. RDS passwords)", "do it yourself"], 1),
     (["encryption", "always KMS", "<code>SecureString</code> uses KMS"], 1),
     (["cost", "per secret per month", "standard tier free"], 2)], size=28) +
   note("ECS injects them as env vars at start · Spring can import them · never in the image", 3),
 "steps": [
  "Secrets Manager is built for credentials like database passwords and API keys.",
  "Its big feature is automatic rotation, for example changing an RDS password on a schedule. Both services encrypt with KMS. In Parameter Store, choose the secure string type.",
  "Parameter Store's standard tier is free, so it's great for configuration values. Secrets Manager charges per secret.",
  "ECS can inject either into the container as environment variables at startup, and Spring can import them directly. They never belong in the image.",
 ]},

{"html": H("Audit and ", "detection") + row(
   box("blue", "CloudTrail", "every API call: who, what, when, from where · keep it on", 0, "flex:1"),
   box("orange", "GuardDuty", "spots threats · odd logins, crypto-mining, leaked keys in use", 1, "flex:1"),
   box("green", "Security Hub · Config", "checks settings against best practices", 2, "flex:1"), top=True) +
   note("A leaked access key on GitHub is found by bots within minutes: use roles", 3),
 "steps": [
  "CloudTrail records every API call in your account: who did what, when, and from where. Keep it on, it's your audit trail during an incident.",
  "GuardDuty analyses those logs and network traffic for threats, like logins from unusual places, crypto mining, or a leaked key being used.",
  "Security Hub and Config check your settings against best practices, like public buckets or unencrypted databases.",
  "And a reminder of why roles matter: access keys pushed to GitHub are found by bots within minutes.",
 ]},

quiz([
  ("Watch averages or p99 latency?", "<b style=\"display:inline\">p99</b>: averages hide the slow ones", "blue",
   "Quiz time. For latency, should you watch the average or the p ninety nine?",
   "The p ninety nine. Averages hide the slow requests."),
  ("Rotate an RDS password automatically?", "<b style=\"display:inline\">Secrets Manager</b>", "green",
   "Where do you store an RDS password that should rotate automatically?",
   "In Secrets Manager, which has built in rotation."),
  ("Who deleted the bucket?", "<b style=\"display:inline\">CloudTrail</b>", "orange",
   "How do you find out who deleted a bucket?",
   "Look in CloudTrail, which records every API call."),
]),

recap(["CloudWatch metrics: built-in + custom · p99",
       "Logs Insights queries · set retention",
       "Alarms on user-facing symptoms → SNS",
       "X-Ray / OpenTelemetry for traces",
       "KMS + envelope encryption",
       "Secrets Manager (rotation) vs Parameter Store · CloudTrail"],
  "Let's recap. CloudWatch collects built in and custom metrics, and percentiles matter more than averages. Logs Insights queries your logs, and you should set retention. Alarm on symptoms users feel, and notify through SNS. X Ray, fed by OpenTelemetry, traces requests. KMS keys protect data through envelope encryption. Secrets go in Secrets Manager when they need rotation, or Parameter Store for configuration. And CloudTrail records who did what. Tomorrow: Terraform."),
]
