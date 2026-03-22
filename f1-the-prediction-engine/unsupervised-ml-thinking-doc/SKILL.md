---
name: unsupervised-ml-thinking-doc
description: >
  Generates a complete thinking document for any unsupervised ML algorithm in the
  exact style and depth of the Session 2 "Unsupervised Learning + K-Means" teaching
  document. Use this skill whenever a student wants to deeply understand an unsupervised
  ML algorithm — not just its mechanics but the full strategic thinking behind it:
  the framing shift from supervised to unsupervised, hypothesis about data shape,
  loss equivalent and what it actually measures, optimization without gradient descent,
  evaluation without ground truth, and how to connect the algorithm's output to the
  5-layer agentic system stack. Trigger this skill when the user says things like
  "help me understand [algorithm] the way we did K-Means", "build a thinking doc
  for [unsupervised algorithm]", "apply the 10 frameworks to [algorithm]",
  "walk me through DBSCAN / PCA / hierarchical clustering / GMM / UMAP / isolation
  forest like session 2 taught K-Means", or any request to deeply understand an
  unsupervised learning algorithm from first principles. Works for ALL unsupervised
  algorithm families: clustering (DBSCAN, hierarchical, GMM, mean shift),
  dimensionality reduction (PCA, t-SNE, UMAP, autoencoders), and anomaly detection
  (isolation forest, one-class SVM, LOF). Always use this skill for unsupervised
  algorithms — never the supervised-ml-thinking-doc skill.
---

# Unsupervised ML Thinking Doc Generator

## FIRST THING TO DO BEFORE ANYTHING ELSE

Read the reference file at: `references/session2-unsupervised-agentic.md`

This is the complete Session 2 document — the gold standard for K-Means, all 10
thinking frameworks, the 5-layer agentic stack, and agent moments. Internalize
before starting:
- The 10 thinking frameworks (exact names, numbers, core insights)
- The K-Means anchor: hypothesis (round blobs) → loss (WCSS) → optimization
  (coordinate descent)
- The critical distinction: evaluation without ground truth
- WCSS vs business value (Framework #3) — mathematical quality ≠ business utility
- The 5-layer intelligent system stack (Data → Predict → Decide → Act → Feedback)
- The 5 AI coding agent moment formats

Do NOT start collecting inputs from the student until you have read this file.

---

## What this skill does

Generates a complete, deeply structured thinking document for any unsupervised ML
algorithm. The output mirrors the style, depth, and pedagogical approach of the
Session 2 K-Means teaching — which is the anchor document for all comparisons.

This is NOT a tutorial. NOT a how-to guide. Contains NO code. It is a thinking
system — built around the 10 frameworks from Session 2 — applied to a new
unsupervised algorithm so the student can transfer their thinking.

The document is generated section by section with a pause after each one. The
student reads, absorbs, and types "continue" before the next section appears.

---

## STEP 0 — Identify the algorithm family BEFORE collecting inputs

Three families exist. Each has a different purpose and the document handles them
differently. Identify which family the requested algorithm belongs to:

**FAMILY 1 — CLUSTERING**
Examples: DBSCAN, hierarchical/agglomerative, Gaussian Mixture Models (GMM),
mean shift, spectral clustering
Purpose: find natural groups in data
Loss equivalent: measures cluster quality (tightness, separation)
Closest to K-Means: yes — direct comparison works throughout

**FAMILY 2 — DIMENSIONALITY REDUCTION**
Examples: PCA, t-SNE, UMAP, autoencoders, LDA
Purpose: compress data while preserving structure
Loss equivalent: measures what is preserved vs lost during compression
Closest to K-Means: partial — hypothesis and optimization differ significantly
Key distinction to make explicit: the output is not groups, it is a new
representation of the data. "Correct" means something completely different.

**FAMILY 3 — ANOMALY DETECTION**
Examples: Isolation Forest, One-Class SVM, Local Outlier Factor (LOF),
autoencoders for anomaly detection
Purpose: find data points that don't fit the normal pattern
Loss equivalent: measures how well normal data is reconstructed or isolated
Closest to K-Means: partial — no clusters, but same "no ground truth" challenge
Key distinction: the output is a score per point, not a group assignment

**If the student gives a supervised algorithm:** redirect — "this skill is for
unsupervised learning algorithms where there are no labels. [algorithm] is
supervised — use the supervised-ml-thinking-doc skill instead."

**If unclear which family:** ask the student before proceeding.

---

## STEP 1 — Collect three inputs

Ask in a single message. Wait for all three answers.

```
Before I build your thinking document, I need three things:

1. Which unsupervised ML algorithm do you want to explore?
   (clustering, dimensionality reduction, or anomaly detection — all fine)

2. What industry or domain do you work in or want to apply this to?
   (e.g. fintech, edtech, healthcare, e-commerce, SaaS, logistics)

3. Have you read the K-Means section of Session 2?
   (yes / no / partially)
```

**Store internally:**
- Algorithm name + which family it belongs to
- Domain → used in every business example throughout
- K-Means familiarity → if yes, explicit comparisons; if no, more foundational
  context added in each section

---

## STEP 2 — The Human Story

Generate 3–4 paragraphs telling the story of where this algorithm came from.

**This is not a Wikipedia summary. This is a narrative.**

Cover:
- What real-world problem someone was actually trying to solve
- What tool or approach existed before and why it was failing
- The specific person/moment where the algorithm emerged
- Why the algorithm was the inevitable answer to that specific frustration
- One sentence on which family it belongs to and what gap it fills that
  K-Means cannot

**Quality bar:** After reading this, the student should feel like this algorithm
was the only logical response to a specific limitation — not like it was invented
in the abstract.

End with the standard pause:
```
---
Take a moment to read this section.
When you're ready to continue, type: continue
---
```

---

## STEP 3 — The Intuition Build

Generate a plain-language explanation using an example from the student's domain.

**Rules:**
- No technical jargon for the first 3 paragraphs minimum
- Start from something the student has experienced in their industry
- Crucially: show WHY supervised learning couldn't solve this problem.
  The absence of labels must be felt, not just stated.
- Show how the natural human behavior in that situation IS the algorithm

**Family-specific intuition anchors:**
- Clustering: "you already do this when you walk into a room and immediately
  sense the different types of people without anyone telling you the categories"
- Dimensionality reduction: "you already do this when you summarize a 3-hour
  meeting in 3 bullet points — compressing without losing what matters"
- Anomaly detection: "you already do this when you immediately notice the one
  person at a party who is acting differently from everyone else"

End with the standard pause.

---

## STEP 4 — The Hypothesis

**The central question for every unsupervised algorithm: what shape does it
assume the data has?**

Generate in three parts:

**Part A — Plain language hypothesis**
What shape does this algorithm assume the data has? No formula. One paragraph.

**Part B — The hypothesis table**

| What the hypothesis is | What shapes/structures it can find | What it cannot find | What you're betting on | How this differs from K-Means's hypothesis |
|------------------------|-----------------------------------|--------------------|-----------------------|-------------------------------------------|
| [fill] | [fill] | [fill] | [fill] | [fill] |

**Part C — The K-Means comparison**
Explicitly: how is this hypothesis different from K-Means's hypothesis (round,
compact, similarly-sized blobs)? What does that difference mean for when you
would choose one over the other?

End with the standard pause.

---

## STEP 5 — The Loss Function (or Equivalent)

**This section requires special handling by family.**

**For CLUSTERING algorithms:**
- What does the algorithm minimize or maximize?
- How is this similar to WCSS? How is it different?
- Apply Framework #3 explicitly: mathematical quality ≠ business utility.
  What is the K=500 equivalent failure for this algorithm?

**For DIMENSIONALITY REDUCTION algorithms:**
- What does the algorithm try to preserve? (variance? local neighborhoods?
  global structure?)
- How do you measure how much was lost in compression?
- This is NOT a loss function in the supervised sense — be explicit about that
- Apply Framework #3: a compression with low reconstruction error can still be
  useless for the downstream task

**For ANOMALY DETECTION algorithms:**
- What does "normal" look like mathematically?
- How is the anomaly score computed?
- There is no ground truth for "this is truly anomalous" — how do you know
  the algorithm is working?

**Always include:**
A reality check box in this format:
```
REALITY CHECK
If you ignore this concept:
- [specific failure scenario 1 in the student's domain]
- [specific failure scenario 2 in the student's domain]

[one sentence summary]
```

End with the standard pause.

---

## STEP 6 — The Optimization

How does this algorithm find its answer?

**Always compare explicitly to K-Means's coordinate descent:**
- Is it the same approach?
- Is it a variation?
- Is it completely different — no optimization at all?

**For algorithms with NO optimization step (e.g. DBSCAN scans directly,
LOF computes distances directly):**

Produce this callout:
```
THIS IS WHERE THE REAL LEARNING IS:
[Algorithm name] has no optimization loop. There is no loss being minimized
step by step. Instead: [explain the direct computation mechanism].

This means Framework #4 (K is a hyperparameter you choose) has a parallel
here: [what the equivalent human decision is for this algorithm].

What this teaches you about unsupervised learning: [the conceptual insight]
```

**Always include:** the failure modes specific to this algorithm's approach to
finding its answer — what goes wrong in practice that K-Means problems don't
produce.

End with the standard pause.

---

## STEP 7 — All 10 Thinking Frameworks Applied

The centerpiece section. Go through all 10 frameworks one by one.

For each framework produce:
```
THINKING FRAMEWORK #[N]: [Framework name]

[Core insight from Session 2 — one sentence]

Applied to [algorithm name]:
[2-3 paragraphs. Use the student's domain for any examples.]

Compared to K-Means:
[ ] Identical — works exactly the same way
[ ] Similar — same principle, different execution
[ ] Fundamentally different — and here is why that matters:
[explanation of the difference and what it teaches]
```

**The 10 frameworks to cover:**

1. Unsupervised vs Supervised framing shift
2. Every clustering is a hypothesis (adapt: "every unsupervised algorithm
   is a hypothesis about the shape of your data")
3. WCSS vs business value (adapt to this algorithm's equivalent metric)
4. K is a hyperparameter (adapt: what is the equivalent human decision
   for this algorithm?)
5. Align loss and objective
6. Expected value thinking (how does EV apply to decisions built on top
   of this algorithm's output?)
7. Policy bridges prediction and action (what policy would you build on
   top of this algorithm's output?)
8. Feedback loop = agentic
9. Loss function ≠ agent objective
10. Agentic = pipeline of decisions

**Pacing:** After frameworks 1–5, insert a mid-section pause:
```
---
That covers the first five frameworks. Take a moment.
When you're ready for frameworks 6–10, type: continue
---
```

Then generate 6–10, then the standard end-of-section pause.

---

## STEP 8 — Agent Moments (minimum 3)

Generate at least 3 agent moments in the exact format from Session 2.

```
AI CODING AGENT MOMENT #[N]: [Decision name]

Why the agent cannot do this alone:
[The specific business or domain context the agent is missing]

What an expert tells the agent:
[Multi-line prompt template — pasteable directly. Must include:
- The business context
- The specific constraint the agent doesn't know
- What to produce and in what format]

REALITY CHECK
If you ignore this concept:
- [specific failure]
- [specific failure]

[one line summary]
```

**Unsupervised agent moments have a specific character:**
The agent will always produce output — always give you clusters, dimensions,
or anomaly scores. The agent moment is always about making that output
meaningful and actionable, not just technically correct.

**Required agent moments by family:**
- Clustering: (1) feature scaling before clustering, (2) choosing K or
  equivalent parameter using business logic not just math, (3) validating
  clusters against domain knowledge before acting on them
- Dimensionality reduction: (1) choosing number of components based on
  downstream task not just variance explained, (2) interpreting what
  the components mean in business terms, (3) connecting reduced
  representation to a downstream prediction or decision
- Anomaly detection: (1) setting the anomaly threshold based on business
  cost of false positives vs false negatives, (2) validating flagged
  anomalies with domain experts before acting, (3) logging outcomes to
  retrain on confirmed anomalies

End with the standard pause.

---

## STEP 9 — Real-World Framing Examples (3, domain-specific)

Three business scenarios from the student's domain.

**Format for each:**
```
Scenario [N]: [Name in student's domain]

The business question:
[What the stakeholder is asking]

Why supervised learning couldn't solve this:
[The specific reason labels don't exist or can't be obtained]

Why this algorithm specifically:
[Not just "it works for this type" — the specific property of this
algorithm that matches this problem's shape]

What success looks like in business terms:
[Not a metric — the actual business outcome]

The trap to avoid:
[The specific way this scenario tempts you into the wrong approach,
and the signal that you've fallen into it]
```

End with the standard pause.

---

## STEP 10 — When It Breaks

The specific, non-obvious failure modes of this algorithm.

**Rules:**
- No generic statements ("it can overfit" — not acceptable without specifics)
- Only failure modes specific to this algorithm's structure
- Each failure mode: what triggers it, what it looks like, why it's hard
  to detect, what the production consequence is

**Always cover:**
- What data characteristics cause this algorithm to fail silently
- What the output looks like when failing but metrics look fine
- The unique failure mode that K-Means doesn't have
- One real-world scenario from the student's domain

**Produce a failure signature table:**
| Failure mode | What triggers it | What it looks like | Why it's invisible | Production consequence |
|--------------|-----------------|-------------------|-------------------|----------------------|

End with the standard pause.

---

## STEP 11 — The Comparison Anchor (K-Means vs This Algorithm)

This section makes the transfer of thinking explicit.

**Part A — Comparison table:**
| Dimension | K-Means | [Algorithm] | What the difference teaches |
|-----------|---------|-------------|---------------------------|
| Hypothesis | Round, compact, similar-sized blobs | [hypothesis] | [insight] |
| Loss equivalent | WCSS (within-cluster sum of squares) | [equivalent] | [insight] |
| Optimization | Coordinate descent (assign → update) | [method] | [insight] |
| Output | Cluster assignment per point | [output type] | [insight] |
| Key hyperparameter | K (number of clusters) | [equivalent] | [insight] |
| Evaluation without ground truth | Silhouette score, elbow method | [equivalent] | [insight] |
| When it breaks | Non-blob shapes, different densities | [specific breaks] | [insight] |
| Business validation required | Are K clusters actionable? | [equivalent question] | [insight] |

**Part B — What is identical to K-Means:**
2 paragraphs on what works exactly the same. The point: when you encounter
a new unsupervised algorithm, you should immediately recognize the parts
you already understand.

**Part C — What is fundamentally different and why it matters:**
2 paragraphs on the deepest conceptual difference. End with: "This
difference matters because in production, it means..."

End with the standard pause.

---

## STEP 12 — The "So What" — Connecting to the 5-Layer Stack

**This section does not exist in the K-Means teaching document. It is unique
to this skill and is mandatory for every algorithm.**

The student just built a deep understanding of an unsupervised algorithm.
But unsupervised learning has a unique failure mode: you can do everything
right mathematically and still have nothing actionable. You found 5 customer
segments. So what?

Force the student to connect their algorithm's output to the 5-layer
intelligent system stack from Session 2 Block B.

Generate this section in three parts:

**Part A — Where this algorithm lives in the stack:**
This algorithm is Layer 2 of the 5-layer stack. Its output feeds everything
above it. Explain specifically: what does this algorithm's output look like,
and what does Layer 3 (Decision) need to do with it?

**Part B — A complete policy built on this algorithm's output:**
Using the student's domain, design a simple but complete policy:
```
[Algorithm] output → Decision threshold → Action → Why

Example format:
Cluster assignment = "High Value" → Offer premium upsell → Expected LTV > $X
Anomaly score > 0.85 → Flag for human review → Cost of false negative > $Y
Component 1 score < -2 → Trigger intervention → [business reason]
```

**Part C — The feedback loop for this algorithm:**
How do you know, over time, if the clusters/components/anomalies are still
meaningful? What would data drift look like for this specific algorithm?
Who owns the retraining decision?

End with:
```
---
Your thinking document for [algorithm name] is complete.

Apply the 7-question interrogation to this algorithm now using your document:
1. Human problem: what does this solve?
2. Hypothesis: what shape does it assume?
3. Loss equivalent: what does it optimize?
4. Optimization: how does it find its answer?
5. Assumptions: what must be true about the data?
6. Overfitting equivalent: when does it produce meaningless output?
7. Production gaps: what breaks between notebook and production?

When you're ready to explore another algorithm, run this skill again.
---
```

---

## CRITICAL STYLE RULES — enforce throughout every section

1. **Intuition before jargon — always.** Every technical term introduced
   with plain-language concept first.

2. **Domain specificity — always.** Every business example uses the
   student's domain. "A company" is not acceptable.

3. **Explicit framework labeling — always.** Format:
   "THINKING FRAMEWORK #[N]: [Name]"

4. **Pasteable agent prompts — always.** Multi-line, specific, pasteable
   directly into Claude.

5. **Reality checks — always.** Every major concept gets a reality check box.

6. **K-Means comparison — always.** Appears in multiple sections, not just
   the comparison anchor.

7. **No code — ever.**

8. **"So what" enforced — always.** Never leave the student with an algorithm
   output that isn't connected to a decision or action.

9. **Family-appropriate language — always.** For dimensionality reduction,
   never call the loss equivalent a "loss function" without clarifying how
   it differs from supervised loss. For anomaly detection, never use
   "accuracy" without explaining why ground truth is unavailable.

---

## Quality bars by section

| Section | Quality bar |
|---------|-------------|
| Human story | Student feels the algorithm was inevitable, not arbitrary |
| Intuition build | Non-technical colleague could follow first 3 paragraphs |
| Hypothesis | Student can explain what shape they're betting their data has |
| Loss equivalent | Student can explain what "better" means without ground truth |
| Optimization | Student can explain what happens when there is no optimization loop |
| 10 frameworks | Every framework has a same/similar/different vs K-Means judgment |
| Agent moments | Prompts are pasteable — no editing required |
| Framing examples | Each explains why supervised learning couldn't solve it |
| When it breaks | Failure modes are specific — not generic unsupervised advice |
| Comparison anchor | Student can answer "why not just use K-Means?" in 30 seconds |
| So what | Student has a policy and a feedback loop sketched for their domain |

---

## Handling edge cases

**If the student asks for K-Means itself:**
Redirect — "K-Means is your anchor from Session 2. You already have the
complete thinking document from that session. Pick a new algorithm to explore."

**If the student asks for a supervised algorithm:**
Redirect to supervised-ml-thinking-doc skill.

**If the student asks for a semi-supervised or self-supervised algorithm:**
Handle it — explain at the start that this algorithm sits between supervised
and unsupervised, which family it's closest to, and proceed with that family's
approach while noting where the semi-supervised element changes things.

**If the student hasn't read Session 2 (answered "no" to step 1):**
Add foundational context at the start of sections 3, 4, and 5 establishing
what K-Means does before comparing. Don't assume the anchor exists — build it.

**If the student asks follow-up questions mid-section:**
Answer them, then return to the pause. Never skip the pause.
