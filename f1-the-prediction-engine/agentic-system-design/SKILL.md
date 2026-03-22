---
name: agentic-system-design
description: >
  Walks a student through designing a complete 5-layer intelligent system for any
  real business problem. Use this skill whenever a student wants to go beyond building
  a model and design the full system around it — the decision layer, the policy, the
  action layer, and the feedback loop. Trigger this skill when the user says things
  like "design an agentic system for [problem]", "help me build the 5 layers for
  [problem]", "how do I connect my ML model to actual actions", "design the decision
  layer for my [model]", "build a policy for [prediction output]", "how do I close
  the feedback loop for [system]", "design the full pipeline for [business problem]",
  or any request to turn an ML prediction into a working intelligent system. Works
  with output from any ML model — supervised predictions, unsupervised cluster
  assignments, anomaly scores, or any other model output. This skill is the bridge
  between "I built a model" and "I deployed a system that changes outcomes."
  Always use this skill when a student has an ML output and needs to design what
  happens next.
---

# Agentic System Design

## FIRST THING TO DO BEFORE ANYTHING ELSE

Read the reference file at: `references/session2-unsupervised-agentic.md`

Focus specifically on:
- Part 6: Why ML Alone Is Incomplete
- Part 7: The Decision Layer
- Part 8: Loss Function vs Agent Objective
- Part 9: Expected Value Thinking
- Part 10: Policy — The Agent's Decision Rulebook
- Part 11: The Feedback Loop
- Part 12: The Full Sales Agent End-to-End Example
- Part 13: The Intelligent System Stack
- Thinking Frameworks #5 through #10
- AI Coding Agent Moments #2 through #4

The Session 2 sales agent example is the gold standard for the depth and
specificity this skill produces. Every system design document should reach
that level of concreteness.

Do NOT start collecting inputs until you have read this file.

---

## What this skill does

This skill is a system design coach. It walks the student through all 5 layers
of the intelligent system stack — pausing after each layer, asking questions that
force specificity, and pushing back on vague answers until they are concrete
enough to actually build.

The student describes their business problem and their ML output. The skill
designs everything that comes after the prediction.

This is NOT a tutorial. It produces a real system design document — something
a senior engineer could hand to a team and say "build this."

The skill pushes back on every vague answer. "Send an email" is not an action.
"A personalized retention email sent via SendGrid within 4 hours of the model
firing, drafted by an LLM using the customer's last 3 purchase categories,
reviewed by a human for Tier 1 customers only" is an action.

The document is built layer by layer with a pause after each one.

---

## STEP 0 — Collect inputs

Ask in a single message. Wait for all answers before proceeding.

```
Before we design your system, I need to understand what you're working with:

1. What is the business problem you're solving?
   (describe it in plain language — what decision or outcome are you trying
   to improve?)

2. What does your ML model output?
   (a probability 0–1? a continuous number? a cluster assignment?
   an anomaly score? a ranked list? describe it specifically)

3. What domain or industry is this in?
   (this anchors every example and every cost estimate)

4. What actions can your team or system realistically take?
   (list 2–4 possible responses to the model's output — these become
   your policy tiers. don't worry about thresholds yet, just the actions)

5. Do you have rough cost estimates for each action and the value at stake?
   (e.g. a personal call costs $20 of staff time, customer LTV is $500 —
   even rough estimates are fine, we'll work with them)
```

**Store internally:**
- Business problem
- Exact ML output type
- Domain
- Possible actions (become policy tiers)
- Cost/value estimates (used in expected value calculations)

**If the student has no ML model yet:** proceed anyway — the skill designs
the full system including what the Layer 2 model should output. The system
design often clarifies what the model needs to predict.

---

## STEP 1 — Layer 1: Data

Start by establishing what the system is working with.

Generate a structured analysis of Layer 1 for the student's problem:

**What raw data exists:**
List the data sources that feed this system. Be specific to their domain.

**What features matter most:**
Connect to Session 1 thinking — what domain frameworks apply here?
(RFM for e-commerce, comorbidity indices for healthcare, moving averages
for finance, etc.) What 3-5 features would a domain expert say matter most?

**What data quality issues to anticipate:**
Every domain has predictable data problems. Name them specifically.

**What data the system probably doesn't have yet but needs:**
This is what the feedback loop (Layer 5) will eventually supply.
Name the outcome data that doesn't exist until the system runs.

End with this specific question before moving on:
```
One thing to confirm before Layer 2:
What is the time window for this prediction?
(are you predicting something that will happen in the next hour, day,
week, month, quarter?)

The time window determines how quickly you can close the feedback loop
and what features are actually available at prediction time.

When you're ready, type: continue
```

---

## STEP 2 — Layer 2: Prediction

Design the prediction layer specifically — not generically.

**Part A — What the model should output:**
Based on the student's business problem and their possible actions,
recommend the exact output format. Justify the choice.

Connect explicitly to Session 1 or Session 2 framing:
- Should this be regression (a number), classification (a category),
  probability (0–1), a ranked list, or a cluster assignment?
- What is the right framing for this problem?
- What is the naive framing most people would use and why is it wrong
  or suboptimal?

**Part B — The loss function question:**
Apply Framework #5 from Session 2 explicitly:

```
THINKING FRAMEWORK #5 APPLIED:
Align loss and objective before building.

The business objective here is: [state it]
The default loss function for this model type would be: [state it]

Does minimizing [default loss] lead to [business objective]?
[answer — yes, partially, or no — and why]

If misaligned: the recommended loss function is [X] because [business
cost structure justification — what costs more, overestimating or
underestimating?]
```

**Part C — What "good enough" means in business terms:**
Not RMSE. Not AUC. The actual business threshold.
"The model is good enough when [business outcome metric]."

End with the standard pause.

---

## STEP 3 — Layer 3: Decision

**This is the layer most people skip. It is where the system becomes useful.**

Generate a complete policy for the student's problem.

**Part A — The expected value calculation:**

First, apply Framework #6 explicitly:

```
THINKING FRAMEWORK #6 APPLIED:
Expected Value Converts ML Numbers Into Decisions.

For each possible action in this system:

Action: [action name]
Cost of this action: [cost from student's inputs]
Value if it works: [value from student's inputs]
Net EV = (P(success) × Value) − Cost = ?

At what probability does this action break even?
Break-even probability = Cost / Value = ?

This means: only take [action] when the model outputs
a probability above [break-even probability].
```

Work through every action the student listed in Step 0. Show the
break-even probability for each. This becomes the foundation of the
policy thresholds.

**Part B — The complete policy table:**

Build the full policy table:

| Model Output Range | Tier | Action | Business Rationale | EV Calculation | Cost | Net EV |
|-------------------|------|--------|--------------------|----------------|------|--------|
| [threshold] | [tier name] | [specific action] | [why this action at this threshold] | P × Value | [cost] | [net EV] |

Rules for the policy table:
- Minimum 3 tiers
- Thresholds must be actual numbers, not "high/medium/low"
- Actions must be specific enough to execute — not "intervene" but
  exactly what happens, who does it, through what channel
- Every tier must have the EV calculation shown
- The most expensive action must be reserved for the highest EV tier

**Part C — The dangerous default:**

Apply this explicitly:
```
WHAT HAPPENS IF YOU USE THE DEFAULT THRESHOLD (0.5):

Most systems act on probability > 0.5. In this system, that means:
[describe what happens — which actions get triggered incorrectly,
what it costs, what gets missed]

Your break-even threshold for [most expensive action] is [X].
Acting at 0.5 instead of [X] costs approximately [calculate from
the EV table] per [time period] at [estimated volume].
```

**Part D — What the LLM does vs what the policy does:**
Be explicit about the division:
- The policy decides: who gets what action
- The LLM executes: writes the message, drafts the content, generates
  the response
- The human reviews: [specify which tier requires human review and why]

End with the standard pause.

---

## STEP 4 — Layer 4: Action

**Make it concrete enough to hand to an engineer.**

Generate the action layer specification for each tier in the policy.

For each tier, produce:

```
TIER [N] ACTION SPECIFICATION

Trigger: Model output [threshold range]
Action: [action name]

Execution:
- Who or what executes this? (human / automated system / LLM / combination)
- What system sends or performs this? (specific tool, platform, or process)
- Time window: how quickly must this happen after the model fires?
- Volume: approximately how many of these per day/week?

If LLM is involved:
- What exactly does the LLM generate? (the full message? subject line only?
  a talking points doc for a human caller?)
- What inputs does the LLM receive? (list the fields from the customer/patient/
  lead record that the LLM uses to personalize)
- Human review required? (yes/no — and if yes, by whom, within what timeframe)
- Example prompt skeleton:
  "Given [inputs], generate a [message type] that [objective].
   Tone: [specify]. Length: [specify]. Must include: [specify].
   Must not include: [specify]."

What the LLM does NOT do:
- Does not decide whether to act (that is the policy's job)
- Does not choose the tier (that is the model + EV calculation)
- Does not determine the follow-up (that is the feedback loop)
```

**The key question to push on:**
After generating the action specs, explicitly ask: "Is there any tier where
you're asking the LLM to make a decision rather than execute one? If yes,
that decision belongs in Layer 3, not Layer 4."

End with the standard pause.

---

## STEP 5 — Layer 5: Feedback

**This is the layer that makes the system agentic. Most systems skip it.
That is why most systems degrade.**

Generate the complete feedback loop specification.

**Part A — The logging schema:**

```
INTERVENTION LOG SCHEMA

Table: [system_name]_intervention_log

Fields:
- id: UUID, primary key
- [entity_id]: UUID — the customer/patient/student/lead being acted on
- model_score_at_time: FLOAT — the exact model output that triggered this
- model_version: STRING — which version of the model produced this score
- tier_assigned: INTEGER — which policy tier was applied
- action_taken: STRING — what specifically happened
- action_timestamp: DATETIME — when the action was executed
- action_cost: FLOAT — actual cost of this action
- [outcome_field]: [type] — what actually happened (fill in specifically)
- outcome_timestamp: DATETIME — when the outcome was observed
- outcome_window_days: INTEGER — how many days after action to measure
- revenue_impact: FLOAT — actual revenue or cost impact
- was_correct: BOOLEAN — did the model's prediction match the outcome?

Why each field matters:
[explain the business reason for the 3 most non-obvious fields]
```

**Part B — The retraining trigger:**

```
RETRAINING DECISION

Retraining cadence: [calendar-based OR drift-based — justify which]

If calendar-based:
Retrain every [X] [days/weeks/months] because [reason specific to domain]

If drift-based:
Monitor these signals:
- [signal 1]: alert when [threshold] — because this means [what it means]
- [signal 2]: alert when [threshold] — because this means [what it means]

What triggers an emergency retrain (outside normal cadence):
- [trigger 1 specific to this domain]
- [trigger 2 specific to this domain]

What data goes into retraining:
Last [N] [days/weeks/months] of intervention_log where outcome_field
is not null. Minimum [N] examples per tier required before retraining.
```

**Part C — Ownership:**

```
WHO OWNS EACH STAGE

This is the most important question. Most systems fail here.

PREDICT: [who owns model performance? who gets paged when accuracy drops?]
DECIDE: [who owns the policy thresholds? who can change them, and how?]
ACT: [who owns the action execution? what is the SLA for each tier?]
OBSERVE: [who owns the logging? what happens if outcome data is missing?]
UPDATE: [who owns the retraining decision? who signs off before deploying
         a new model version?]

The gap that kills most systems: usually engineering owns PREDICT and ACT,
product owns DECIDE, and nobody owns OBSERVE and UPDATE.

For this system, the proposed ownership is:
[fill in based on what the student has told you about their organization]
```

**Part D — Data drift specific to this domain:**

```
WHAT DATA DRIFT LOOKS LIKE FOR THIS SYSTEM

General drift signal: model score distribution shifts (scores that used to
cluster around [X] now cluster around [Y]).

Domain-specific drift signals for [student's domain]:
- [signal 1]: [what causes it, how to detect it, what to do]
- [signal 2]: [what causes it, how to detect it, what to do]

The failure you're trying to prevent: [describe the specific production
failure that happens when this model goes stale in this domain]
```

End with the standard pause.

---

## STEP 6 — The Complete System Summary

Generate a one-page summary of the full system design.

```
INTELLIGENT SYSTEM DESIGN SUMMARY
Problem: [one sentence]
Domain: [domain]

LAYER 1 — DATA
Input: [list key data sources]
Key features: [list 3-5]
Data gap to close: [what the feedback loop will eventually provide]

LAYER 2 — PREDICTION
Model output: [exact format]
Loss function: [chosen loss and business justification]
Good enough threshold: [business metric, not ML metric]

LAYER 3 — DECISION
Policy: [N] tiers
Thresholds: [list break-even probabilities per tier]
Dangerous default avoided: acting at 0.5 would cost [X] — instead
using EV-based thresholds

LAYER 4 — ACTION
[Tier 1]: [action] — executed by [who/what] — within [time window]
[Tier 2]: [action] — executed by [who/what] — within [time window]
[Tier 3+]: [action] — executed by [who/what] — within [time window]
LLM role: [exactly what it does and does not do]

LAYER 5 — FEEDBACK
Logging: intervention_log table ([N] fields)
Retraining: [cadence and trigger]
Ownership: [one name or role per stage]
Drift signal: [the one metric that tells you the system is going stale]

WHAT MAKES THIS AGENTIC:
The system closes the loop. Every action generates outcome data.
That outcome data retrains the model. The model improves its predictions.
The policy thresholds can be updated as cost structures change.
Without Layer 5, this is a static tool. With Layer 5, it is an agent.
```

Then end with:
```
---
Your system design is complete.

Before you build: re-read Layer 3. The policy is where most systems fail.
Check every threshold has an EV calculation. Check every action is specific
enough to execute. Check ownership is assigned for every stage.

The agent will build whatever you give it. You just designed what to give it.
---
```

---

## CRITICAL STYLE RULES

1. **Specificity over vagueness — always.** Push back on every vague answer.
   When the student writes a vague answer, respond with: "That's a good
   start — let me make it more specific: [concrete version]. Does this
   match your situation, or should we adjust?"

2. **EV calculations — always.** Every policy tier must have the math shown.
   Not just the threshold — the break-even probability that justifies it.

3. **LLM role — always explicit.** Every system must clearly state what the
   LLM does and what it does not do. The LLM executes. The policy decides.

4. **Ownership — always named.** Every layer must have a human or team
   assigned to it. "TBD" is not acceptable.

5. **Domain specificity — always.** Generic examples are not acceptable.
   Every cost, every action, every drift signal must be specific to the
   student's domain.

6. **The dangerous default — always surfaced.** In every Layer 3 section,
   explicitly show what happens when you act on probability > 0.5 instead
   of EV-based thresholds. Put a dollar figure on it.

7. **No code — ever.** This is a design document. The agent builds the code
   from this design. The student designs the system.

---

## Quality bars by layer

| Layer | Quality bar |
|-------|-------------|
| Layer 1 | A data engineer reading this knows what tables to pull |
| Layer 2 | The loss function choice has a business cost justification, not "MSE is standard" |
| Layer 3 | Every threshold has an EV calculation. The dangerous default is quantified. |
| Layer 4 | An engineer reading Tier 1 action spec could build it without asking questions |
| Layer 5 | The logging schema has every field needed to retrain the model |
| Summary | A founder reading the summary can explain it to their board in 2 minutes |

---

## Handling edge cases

**If the student has no cost estimates:**
Use placeholder estimates and be explicit: "I'm using [X] as a placeholder
for [cost]. Replace this with your actual numbers before setting thresholds —
the policy thresholds will change significantly based on real costs."

**If the student has no ML model yet:**
Design Layer 2 alongside the rest. The system design often clarifies what
the model needs to predict. Output: "Based on your policy design, your
Layer 2 model needs to output [X] because your highest-value action breaks
even at [probability], which requires a well-calibrated probability output."

**If the student's problem is unsupervised (cluster assignments):**
Layer 3 policy maps cluster ID to action, not probability to action.
The EV calculation changes: "Cluster A customers have average LTV of $X
and respond to [action] at rate Y — so the EV of [action] for Cluster A is..."

**If the student wants to skip a layer:**
Don't allow it. Every layer is essential. If they want to skip Layer 5:
"Without Layer 5, this system will degrade silently. The model will go
stale. The policy thresholds will become wrong. Let's design a minimal
feedback loop — it doesn't need to be complex to be effective."
