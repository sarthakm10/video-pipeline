from conc import *

TAG = "Day 86 · AWS Storage with S3"
TRACK = "Java Fullstack · Cloud"
FILE = "Day 86 AWS Storage with S3.mp4"

SLIDES = [
title_slide(86, "AWS Storage with S3", "Store any number of files, cheaply, durably and securely",
  "Welcome to day eighty six: storage with Amazon S3.",
  "Almost every app stores files: avatars, uploaded documents, reports, backups. S3 stores them as objects, practically without limit. By the end you'll know buckets and objects, who can access them, storage classes and lifecycle rules, versioning and encryption, presigned URLs for direct uploads, and event notifications.",
  pill="DAY 86 · CLOUD"),

{"html": H("Buckets and ", "objects") + row(
   code("""§0 s3://task-files/projects/7/report-2026-11.pdf
§0      └─bucket─┘ └──────────── key ──────────────┘
§1 s3.putObject(PutObjectRequest.builder()
§1         .bucket("task-files").key(key)
§1         .contentType("application/pdf").build(),
§1     RequestBody.fromFile(path));
§2 s3.getObject(r -> r.bucket("task-files").key(key));""", 23, style="flex:1"),
   col(box("blue", "a bucket", "a globally unique name · in one region", 0),
       box("green", "an object", "bytes + metadata · up to 5 TB · addressed by key", 0),
       box("purple", "flat namespace", "\"folders\" are just key prefixes", 1),
       box("orange", "durability", "11 nines · copies across AZs", 2), gap=14, style="width:520px"), top=True),
 "steps": [
  "S3 stores objects in buckets. A bucket has a globally unique name and lives in one region. An object is the file's bytes plus metadata, up to five terabytes, addressed by a key.",
  "There are no real folders. Slashes in the key are just a naming convention that the console displays as folders. From Java, the AWS SDK puts and gets objects by bucket and key.",
  "S3 is designed for eleven nines of durability, keeping copies across availability zones. You will practically never lose an object to hardware failure.",
 ]},

{"html": H("Who can ", "access") + row(
   box("blue", "IAM policy", "on the role: \"my app may read task-files/*\"", 0, "flex:1"),
   box("green", "bucket policy", "on the bucket: who may touch it · e.g. only via HTTPS, only this role", 1, "flex:1"),
   box("gray", "ACLs", "legacy · disabled by default · leave them off", 2, "flex:1"), top=True) +
   note("Block Public Access: on by default · keep it on unless you're hosting a public site", 3),
 "steps": [
  "Access is controlled in two places. The IAM policy on your app's role says what the app may do.",
  "The bucket policy, on the bucket itself, says who may touch it at all. For example, deny anything that isn't HTTPS, or allow another account to read.",
  "Access control lists are a legacy mechanism, disabled by default on new buckets. Leave them off.",
  "Block public access is on by default too. Keep it on, unless the bucket really hosts a public website. Leaked public buckets are a classic data breach.",
 ]},

{"html": H("Storage classes and ", "lifecycle") + row(
   col(table(["Class", "For"], [
     (["Standard", "hot data · ms access"], 0),
     (["Intelligent-Tiering", "unknown patterns · moves itself"], 0),
     (["Standard-IA", "monthly reads · cheaper storage, pay per read"], 1),
     (["Glacier Instant / Flexible", "archives · ms / minutes–hours"], 1),
     (["Glacier Deep Archive", "compliance · ~12 h to restore"], 1)], size=26), style="width:820px"),
   code("""§2 Rules:
§2   transition → STANDARD_IA   after 30 days
§2   transition → GLACIER       after 90 days
§2   expire                     after 365 days""", 24, style="flex:1"), top=True),
 "steps": [
  "Every object has a storage class. Standard is for data you read often. Intelligent tiering watches access and moves objects between tiers for you.",
  "Infrequent access is cheaper to store but charges per read, good for monthly reports. The Glacier classes are for archives, from instant retrieval to deep archive, which takes hours to restore but costs almost nothing.",
  "Lifecycle rules automate it: move reports to infrequent access after thirty days, to Glacier after ninety, and delete them after a year.",
 ]},

{"html": H("Versioning and ", "encryption") + row(
   col(box("blue", "versioning", "every overwrite keeps the old version · a delete adds a marker", 0),
       box("purple", "Object Lock", "write once, read many · nobody can delete until the date", 1), gap=14, style="flex:1"),
   col(box("green", "SSE-S3", "default · AWS manages the keys", 2),
       box("orange", "SSE-KMS", "your KMS key · every use is logged · permissions on the key", 2),
       box("gray", "SSE-C", "you send the key with each request", 2), gap=14, style="flex:1"), top=True) +
   note("All new objects are encrypted at rest by default", 3),
 "steps": [
  "With versioning on, overwriting an object keeps the old version, and deleting adds a delete marker instead of destroying data. It saves you from accidental deletes.",
  "Object lock goes further: write once, read many. Nobody, not even an admin, can delete it before the retention date. That's what regulators ask for.",
  "Encryption at rest has three flavours. SSE S3, where AWS manages the keys. SSE KMS, using your own KMS key, with every use logged and access controlled by key permissions. And SSE C, where you supply the key yourself on each request.",
  "Today, every new object is encrypted at rest by default.",
 ]},

{"html": H("Presigned ", "URLs") + code("§0 browser → API: may I upload?  ·  API → browser: presigned URL  ·  browser → PUT → S3", 26) + row(
   code("""§1 PresignedPutObjectRequest p = presigner.presignPutObject(r -> r
§1     .signatureDuration(Duration.ofMinutes(10))
§1     .putObjectRequest(o -> o.bucket("task-files").key(key)));
§1 return p.url();      // the browser PUTs the file straight to S3""", 23, style="flex:1"),
   col(box("green", "why", "big files skip your server · no AWS keys in the browser", 2),
       box("orange", "limits", "time-limited (≤ 7 days) · one bucket + key", 2), gap=14, style="width:480px"), top=True, style="margin-top:20px"),
 "steps": [
  "How does a browser upload a large file? Not through your API. The browser asks your API for permission.",
  "Your API checks the user, then creates a presigned URL: a link signed with your app's credentials, valid for one key and a few minutes. The browser uploads directly to S3 with it.",
  "Large files never pass through your server, and no AWS credentials ever reach the browser. The URL expires, at most after seven days, and only works for that one object.",
 ]},

{"html": H("Events and big ", "files") + row(
   box("blue", "event notifications", "object created / deleted → Lambda, SQS or SNS · e.g. make a thumbnail", 0, "flex:1"),
   box("green", "multipart upload", "split files over ~100 MB into parts · parallel, resumable", 1, "flex:1"),
   box("purple", "replication", "copy to another region for disaster recovery", 2, "flex:1"), top=True) +
   note("Lambda writing back to the same bucket prefix can trigger itself forever", 3),
 "steps": [
  "S3 can emit an event when an object is created or deleted, and deliver it to Lambda, an SQS queue or an SNS topic. Upload a photo, and a function makes the thumbnail.",
  "For files over about a hundred megabytes, multipart upload splits them into parts that upload in parallel and can be retried individually.",
  "Cross region replication copies objects to a bucket in another region, for disaster recovery.",
  "One trap: if a Lambda writes its output into the same prefix that triggers it, it triggers itself in an endless loop. Write to a different prefix or bucket.",
 ]},

quiz([
  ("Are S3 \"folders\" real?", "<b style=\"display:inline\">no</b>: just key prefixes", "blue",
   "Quiz time. Are folders in S3 real?",
   "No. They're just prefixes in the object key."),
  ("Let a browser upload directly, safely?", "a <b style=\"display:inline\">presigned URL</b>", "green",
   "How do you let a browser upload straight to S3, safely?",
   "Give it a presigned URL, valid for one key and a short time."),
  ("Archive reports after 90 days automatically?", "a <b style=\"display:inline\">lifecycle rule</b>", "purple",
   "How do you move reports to Glacier after ninety days automatically?",
   "With a lifecycle rule on the bucket."),
]),

recap(["Buckets hold objects addressed by key",
       "IAM + bucket policies · Block Public Access on",
       "Storage classes + lifecycle rules cut cost",
       "Versioning · Object Lock · SSE-S3 / KMS",
       "Presigned URLs: direct, time-limited uploads",
       "Events → Lambda / SQS · multipart for big files"],
  "Let's recap. S3 stores objects in buckets, addressed by key. Control access with IAM and bucket policies, and keep public access blocked. Storage classes and lifecycle rules keep costs down. Versioning and object lock protect data, and encryption is on by default, with KMS for audited keys. Presigned URLs let clients upload directly for a limited time. And events trigger Lambda or queues, while multipart handles big files. Tomorrow: databases, caching and messaging."),
]
