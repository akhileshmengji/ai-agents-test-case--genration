# <Your Product Name> Product Knowledge

Purpose: Permanent product knowledge for <Your Product Name>. This is the
single source of truth the AI agent reads before analysing any user story -
it is what lets the agent spot gaps ("this contradicts rule X") instead of
just rephrasing the acceptance criteria back at you.

Replace every `<placeholder>` below with real facts about your product.
Keep entries short, factual, and testable ("OTP expires after 10 minutes",
not "OTP should expire reasonably quickly"). See `examples/acme-lms/PRODUCT_KNOWLEDGE.md`
for a fully filled-in reference.

## 1. Product Overview
- Product Name: <name>
- One-paragraph description of what the product does and who uses it.
- Platforms: <Web / Android / iOS / API / ...>

## 2. User Roles
- <Role 1> (e.g. Admin)
- <Role 2> (e.g. Customer)
- <Role 3> (e.g. Agent)

## 3. Core Modules
List the top-level modules/features that matter for QA (e.g. Auth, Checkout,
Search, Notifications, Billing, Reporting). This is the vocabulary story
files will use in `meta.module`.

## 4. Role Capabilities
For each role from Section 2, list what it CAN and explicitly CANNOT do.
Explicit "cannot" statements are often the most valuable gap-detection fuel -
a story that lets a restricted role perform a forbidden action is an
immediate, high-confidence gap.

## 5. Authentication & Session Rules
- Login method(s):
- Token/OTP/session expiry rules:
- Retry / resend / lockout rules:
- Session lifetime and renewal behaviour:

## 6. Domain-Specific Business Rules
Add one numbered section per module as you learn its rules from real
stories. Examples of the kind of fact that belongs here:
- Uniqueness constraints ("a mobile number can exist only once within the
  same batch")
- Irreversible actions ("a batch cannot be deleted")
- State-machine rules ("an invite becomes invalid after successful use")
- Timing/expiry rules ("invite link valid for 30 days")
- Cross-entity rules ("teacher may invite the same number to different
  batches, but not twice to the same batch")

## 7. Non-Functional Baselines
- Performance SLAs (P95 latency targets per critical flow)
- Accessibility standard (e.g. WCAG 2.1 AA)
- Supported browsers / OS versions / device classes

---

## How this file grows

Whenever a new story JSON is processed, the agent should:
1. Cross-reference the story's acceptance criteria against everything in
   this file to find contradictions and gaps.
2. Append any *newly confirmed* fact (only what the story's AC/BR text
   actually states - never inferred or guessed) under the most relevant
   section above, or create a new numbered section if none fits.
3. Never delete or silently overwrite existing facts unless a story
   explicitly and unambiguously contradicts them.

This turns the file into a living spec that gets more precise with every
story you run through the pipeline - which is also what makes later gap
analysis sharper (new stories get checked against everything learned from
earlier ones, not just their own text).
