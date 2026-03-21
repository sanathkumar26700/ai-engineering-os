---
name: supervised-ml-thinking-doc
description: >
  Generates a complete thinking document for any supervised ML algorithm in the
  exact style of the "Regression & Supervised Learning: The Evolutionary Thinking
  Framework" session document. Use this skill whenever a student wants to deeply
  understand a supervised ML algorithm — not just its mechanics but the full
  strategic thinking behind it: problem framing, hypothesis choice, loss function
  as a business decision, optimization failure modes, feature engineering,
  regularization, leakage, assumption diagnostics, and agent orchestration moments.
  Trigger this skill when the user says things like "help me understand [algorithm]
  the way we did regression", "build a thinking doc for [algorithm]", "apply the
  13 frameworks to [algorithm]", "walk me through [algorithm] like the session",
  or any request to deeply understand a supervised learning algorithm from first
  principles using the evolutionary thinking approach. This skill works for ANY
  supervised learning algorithm — logistic regression, decision trees, random
  forests, XGBoost, SVMs, naive bayes, KNN, neural networks, gradient boosting,
  and beyond.
---

# Supervised ML Thinking Doc Generator

## FIRST THING TO DO BEFORE ANYTHING ELSE

Read the reference file at: `references/regression-thinking-doc.md`

This is the complete Session 1 document — the gold standard for style, depth,
structure, and quality. Every document this skill generates must match it.
Specifically internalize before starting:
- The 13 thinking frameworks (exact names, numbers, and core insights)
- The 8 AI coding agent moment formats (structure, prompt style, reality check format)
- The narrative voice — plain language first, intuition before jargon, always
- The "REALITY CHECK — If you ignore this concept" format used after every major concept
- The 7-question algorithm interrogation template at the end
- The comparison table structure (hypothesis / loss / optimization / assumptions)

Do NOT start collecting inputs from the student until you have read this file.

---

## What this skill does

This skill generates a complete, deeply structured thinking document for any
supervised ML algorithm. The output mirrors the style, depth, and pedagogical
approach of the "Regression & Supervised Learning: The Evolutionary Thinking
Framework" document — which is the gold standard for how this program teaches
algorithms.

The document is NOT a tutorial. It is NOT a how-to guide. It contains NO code.
It is a thinking system — built around the 13 thinking frameworks and 8 agent
moments from the regression session — applied to a new algorithm so the student
can transfer their thinking, not just learn new facts.

The document is generated section by section with a pause after each one.
The student reads, absorbs, and types "continue" before the next section appears.

---

## STEP 0 — Before generating anything, collect three inputs

Ask the student these three questions in a single message. Wait for all three
answers before proceeding.

```
Before I build your thinking document, I need three things:

1. Which supervised ML algorithm do you want to explore?
   (any algorithm is fine — logistic regression, decision tree,
   XGBoost, SVM, KNN, naive bayes, neural network, or anything else)

2. What industry or domain do you work in or want to apply this to?
   (e.g. fintech, edtech, healthcare, e-commerce, SaaS, logistics —
   this anchors every business example in the document to your reality)

3. Have you read the Linear Regression Thinking Document from Session 1?
   (yes / no / partially — this changes how I connect concepts back
   to what you already know)
```

**If the student gives an unsupervised algorithm** (clustering, PCA, RL, etc.):
Redirect gently — "this skill is scoped to supervised learning algorithms
where we have labeled training data and a prediction target. [algorithm name]
is [unsupervised/RL] — want to pick a supervised algorithm instead, or shall
I explain the boundary?"

**Store the three answers internally.** Every section that follows uses them:
- Algorithm name → drives all technical content
- Domain → replaces every generic example with a domain-specific one
- Regression doc familiarity → if yes, explicitly connect back throughout;
  if no, add more foundational context in each section

---

## STEP 1 — The Human Story

Generate 3–4 paragraphs telling the story of where this algorithm came from.

**This is not a Wikipedia summary. This is a narrative.**

Cover:
- What real-world problem someone was actually trying to solve
- What tool or approach existed before this algorithm and why it was failing
- The specific moment or person where the algorithm emerged
- Why the algorithm was the inevitable answer to that specific frustration

**Quality bar:** After reading this section, the student should feel like
this algorithm was the only logical response to a specific human problem —
not like a mathematician invented it in the abstract.

End every section with this exact pause:

```
---
Take a moment to read this section.
When you're ready to continue, type: continue
---
```

---

## STEP 2 — The Intuition Build

Generate a plain-language explanation of the algorithm's core idea using an
example from the student's domain (from their answer to question 2).

**Rules for this section:**
- No technical jargon for the first 3 paragraphs minimum
- Start from something the student has experienced in their industry
- Show how the natural human behavior in that situation IS the algorithm
- The student should recognize their own intuition before they see the name

**Examples by domain (adapt, don't copy):**
- Fintech: a loan officer's gut check before they had a model
- Edtech: a mentor deciding which students need intervention
- Healthcare: a triage nurse sorting patients by urgency
- E-commerce: a buyer deciding whether a return is fraudulent
- SaaS: a sales rep deciding which leads to call first

After the intuition is established in plain language, introduce the
algorithm's name and formal identity — but only after the concept exists.

End with the standard pause block.

---

## STEP 3 — The Hypothesis

**This is where the mathematical structure is introduced — but intuitively first.**

Generate this section in three parts:

**Part A — Plain language hypothesis**
What shape does this algorithm assume the world has? A straight line, a
probability curve, a set of if-then rules, a distance boundary? Explain this
shape in one paragraph without any formula.

**Part B — The hypothesis table**
Always produce this exact table:

| What the hypothesis is | What it can capture | What it cannot capture | What you're betting on |
|------------------------|---------------------|------------------------|------------------------|
| [fill in]              | [fill in]           | [fill in]              | [fill in]              |

**Part C — The regression comparison**
Explicitly answer: how is this hypothesis different from linear regression's
hypothesis (y = wx + b), and what does that difference mean for when you
would choose one over the other?

This comparison must appear here AND in the final comparison section.
Don't save it all for the end.

End with the standard pause block.

---

## STEP 4 — The Loss Function

Generate this section in four parts:

**Part A — Plain language explanation**
What is the loss function for this algorithm? Explain it the way the regression
doc explained MSE — through a real situation where the wrong loss causes a
specific, painful business failure. Use the student's domain.

**Part B — Why this specific loss**
Why did this loss function win historically? What mathematical or practical
property made it the right choice for this algorithm's hypothesis? Connect
to the "Legendre and Gauss chose squaring for three reasons" style of
explanation from the regression doc.

**Part C — Thinking Framework #3 applied**
Produce a labeled box in this exact format:

```
THINKING FRAMEWORK #3 APPLIED TO [ALGORITHM NAME]:
The loss function is a business decision, not a technical one.

[2-3 paragraphs showing how this plays out differently than in regression.
What kinds of errors does this loss penalize? What business situations call
for a different loss? What would you tell the agent to change about the
default loss and why?]
```

**Part D — Reality Check**
Produce a labeled box in this exact format:

```
REALITY CHECK
If you ignore this concept:
- [specific failure scenario 1 in the student's domain]
- [specific failure scenario 2 in the student's domain]

[one sentence summary of the consequence]
```

End with the standard pause block.

---

## STEP 5 — The Optimization

Generate this section covering how the algorithm finds its best parameters.

**Rules:**
- Explain the optimization approach in plain language before any formula
- Explicitly compare to gradient descent from the regression document:
  - Is it the same engine? (e.g. logistic regression — yes, same GD)
  - Is it a variation? (e.g. neural networks — same but with backprop)
  - Is it completely different? (e.g. decision trees — greedy splitting,
    no gradient at all; KNN — no training phase whatsoever)
- The "completely different" cases are the most important — they force the
  student to re-examine what they assumed was universal

**For algorithms that use gradient descent:**
Apply Thinking Framework #5 explicitly — label it, show how the variant
choice (batch/SGD/mini-batch/Adam) plays out for this specific algorithm.

**For algorithms that do NOT use gradient descent:**
This is a major insight moment. Produce a callout:

```
THIS IS WHERE THE REAL LEARNING IS:
[Algorithm name] has no gradient descent. There are no weights being
nudged downhill. Instead: [explain the actual mechanism].

This means Thinking Framework #5 (gradient descent is the universal engine)
has an important qualifier: it's universal for *parametric* models that
optimize a continuous loss. [Algorithm name] is [explain the category].

What this teaches you about ML thinking: [the conceptual insight]
```

**Always include:** the failure modes specific to this algorithm's
optimization — what goes wrong in practice that gradient descent problems
don't produce.

End with the standard pause block.

---

## STEP 6 — All 13 Thinking Frameworks Applied

This is the centerpiece section. Go through all 13 frameworks one by one.

For each framework, produce:

```
THINKING FRAMEWORK #[N]: [Framework name]

[Core insight from the regression doc — one sentence]

Applied to [algorithm name]:
[2-3 paragraphs showing exactly how this framework plays out for this
specific algorithm. Use the student's domain for any examples.]

Compared to linear regression:
[ ] Identical — works exactly the same way
[ ] Similar — same principle, different execution
[ ] Fundamentally different — and here is why that matters:
[explanation of the difference and what it teaches]
```

**The 13 frameworks to cover:**

1. Problem framing is the highest-leverage skill
2. Every model is a hypothesis — know its limitations before you start
3. The loss function is a business decision, not a technical one
4. The universal ML architecture: Hypothesis → Loss → Optimization
5. Gradient descent is the universal engine, but its variants matter enormously
6. The feature vs complexity tradeoff defines senior ML engineers
7. Data leakage is the silent killer
8. How you split data matters as much as that you split it
9. Regularization is universal — but what kind of simplicity do you want?
10. Report business metrics, not just technical ones
11. The best features come from domain frameworks, not technical tricks
12. Violated assumptions give you confidently wrong answers
13. The pipeline is universal, but the gotchas at each stage are where projects die

**Pacing note:** This is the longest section. After frameworks 1–4, insert
a mid-section pause:

```
---
That covers the first four frameworks. Take a moment.
When you're ready for frameworks 5–13, type: continue
---
```

Then generate frameworks 5–13, then the standard end-of-section pause.

---

## STEP 7 — Agent Moments (minimum 3, maximum 5)

Generate at least 3 "AI Coding Agent Moment" sections in the exact format
used in the regression document.

**Format for each agent moment:**

```
AI CODING AGENT MOMENT #[N]: [Decision name]

Why the agent cannot do this alone:
[1 paragraph explaining the specific business or domain context the
agent is missing — not "it doesn't know your data" but the specific
strategic knowledge required]

What an expert tells the agent:
[Multi-line prompt template the student can paste directly.
Must be specific, not generic. Should include:
- The business context
- The specific asymmetry or constraint the agent doesn't know
- What to compare or produce
- What format the output should take]

REALITY CHECK
If you ignore this concept:
- [specific failure scenario]
- [specific failure scenario]

[one line summary]
```

**The agent moments must be specific to this algorithm.** Do not recycle
agent moments from the regression document. Each algorithm has its own
critical decision points. Examples:

- Logistic regression: threshold selection (default 0.5 is almost never right)
- Decision tree: depth selection and the cost of interpretability vs accuracy
- Random forest: feature importance vs actual causal importance
- XGBoost: early stopping and the difference between training loss and
  generalization
- SVM: kernel choice as a hypothesis decision
- KNN: distance metric as a domain knowledge decision

End with the standard pause block.

---

## STEP 8 — Real-World Framing Examples (3, domain-specific)

Generate 3 detailed business scenarios from the student's domain where
this algorithm is the right choice.

**Format for each scenario:**

```
Scenario [N]: [Scenario name in the student's domain]

The business question:
[What the stakeholder is actually asking]

The naive framing most people would use:
[What a junior engineer would build and why it's wrong or suboptimal]

The strategic framing:
[Why this algorithm specifically — not just "it works for classification"
but the specific property of this algorithm that matches this problem]

What success looks like in business terms:
[Not RMSE or AUC — the actual business outcome. Revenue protected,
decisions improved, cost reduced.]

The framing trap to avoid:
[The specific way this scenario tempts you into the wrong framing,
and the signal that you've fallen into it]
```

End with the standard pause block.

---

## STEP 9 — When It Breaks

Generate the specific, non-obvious failure modes of this algorithm.

**Rules:**
- No generic statements ("overfitting is bad" — every algorithm section says this)
- Only failure modes specific to this algorithm's structure
- Each failure mode must include: what it looks like when it's happening,
  why it's hard to detect, and what the consequence is in production

**Always cover:**
- What data characteristics cause this specific algorithm to fail silently
- What assumption violations are unique to this algorithm (not shared with regression)
- What the output looks like when the algorithm is failing but metrics look fine
- One real-world case study style example in the student's domain

**Produce a "failure signature" table:**

| Failure mode | What triggers it | What it looks like | Why it's invisible | Production consequence |
|--------------|-----------------|-------------------|-------------------|----------------------|
| [fill]       | [fill]          | [fill]            | [fill]            | [fill]               |

End with the standard pause block.

---

## STEP 10 — The Comparison Anchor

This section does not exist in the regression document. It exists here
because the student already has regression as their foundation, and this
section makes the transfer of thinking explicit.

Generate three parts:

**Part A — The comparison table**

| Dimension | Linear Regression | [Algorithm Name] | What the difference teaches |
|-----------|------------------|-------------------|----------------------------|
| Hypothesis | y = wx + b (line) | [hypothesis] | [insight] |
| Loss function | MSE | [loss] | [insight] |
| Optimization | Normal eq / GD | [method] | [insight] |
| Output | Continuous number | [output type] | [insight] |
| Key assumption | Linearity | [assumption] | [insight] |
| Regularization | Ridge / Lasso | [equivalent] | [insight] |
| When it breaks | Non-linearity, outliers | [specific breaks] | [insight] |
| Agent moment | Loss function choice | [key moment] | [insight] |

**Part B — What is identical**
2 paragraphs on what works exactly the same way as regression. The point:
when you encounter a new algorithm, you should immediately recognize the
parts you already understand.

**Part C — What is fundamentally different and why it matters**
2 paragraphs on the deepest conceptual difference. Not a surface difference
(different formula) but a structural difference (different category of
hypothesis, different optimization philosophy, different failure mode).
End with: "This difference matters because in production, it means..."

End with the standard pause block.

---

## STEP 11 — The 7-Question Interrogation (completed for this algorithm)

The regression document ends with a 7-question template the student can
use for any future algorithm. Complete it now for this algorithm.

```
THE 7-QUESTION ALGORITHM INTERROGATION: [Algorithm Name]

1. HUMAN PROBLEM: What real-world prediction/decision does this solve?
   [answer]

2. HYPOTHESIS: What mathematical structure does it assume?
   [answer]

3. LOSS FUNCTION: How does it measure badness? Is this right for YOUR problem?
   [answer + the question to ask yourself]

4. OPTIMIZATION: How does it find best parameters? What are the failure modes?
   [answer]

5. ASSUMPTIONS: What must be true about the data? How do you check?
   [answer + the diagnostic to run]

6. OVERFITTING: When does it overfit? What regularization works?
   [answer]

7. PRODUCTION GAPS: What breaks between notebook and production?
   (data drift, leakage, latency, explainability)
   [answer — specific to this algorithm]
```

After generating this, add:

```
Keep this completed interrogation. The next time you encounter a paper,
blog post, or colleague mentioning this algorithm, you now have a one-page
answer to every question a senior engineer will ask you about it.

When you're ready to build the thinking doc for your next algorithm,
run this skill again.
---
```

---

## CRITICAL STYLE RULES — enforce throughout every section

These are non-negotiable. Every section must follow them.

**1. Intuition before jargon — always**
Every technical term is introduced with a plain-language concept first.
The student understands the idea before they see the name. No exceptions.

**2. Domain specificity — always**
Every business example uses the student's domain from question 2.
"A company" is not acceptable. "A fintech startup doing SME lending in India"
is acceptable. Generic examples are a failure of this skill.

**3. Explicit framework labeling — always**
Every thinking framework section is labeled with its number and name in
the exact format: "THINKING FRAMEWORK #[N]: [Name]"
Frameworks are never embedded invisibly in prose.

**4. Pasteable agent prompts — always**
Agent moment prompts must be multi-line, specific, and pasteable directly
into Claude. "Tell the agent to check for overfitting" is not a prompt.
A prompt is a paragraph of specific instructions with context included.

**5. Reality checks — always**
Every major concept gets a reality check box. Not every section — every
concept. If you've introduced a concept that someone could ignore and
later regret, it gets a reality check.

**6. Comparison to regression — always**
The comparison appears in multiple sections, not just Section 10. Every
time a framework is applied or an optimization is explained, there is
an explicit note on how it compares to linear regression.

**7. No code — ever**
This document contains zero code. Not even pseudocode unless it is
genuinely the clearest way to express an idea. The regression document
has no code. This document has no code.

**8. Depth over speed**
This is not a summary. It is not a cheat sheet. It is a full thinking
document. Each section should be as long as it needs to be to reach
the quality bar. The regression document is 63 pages. This document
should be comparable in depth and density.

---

## Quality bars by section — how to know when a section is ready

| Section | Quality bar |
|---------|-------------|
| Human story | Student feels the algorithm was inevitable, not arbitrary |
| Intuition build | Non-technical colleague could follow first 3 paragraphs |
| Hypothesis | Student can explain the bet they're making before touching data |
| Loss function | Student can justify a non-default loss to a VP of Engineering |
| Optimization | Student can diagnose a training failure without help |
| 13 frameworks | Every framework has a "same/similar/different vs regression" judgment |
| Agent moments | Prompts are pasteable — no editing required before running |
| Framing examples | Examples are specific enough to be wrong in a specific way |
| When it breaks | Failure modes are specific to this algorithm, not generic ML advice |
| Comparison anchor | Student can answer "why not just use regression?" in 30 seconds |
| 7-question interrogation | Completed answers are specific, not generic — a senior engineer finds no gap |

---

## Handling edge cases

**If the student asks for a very simple algorithm (e.g. KNN, naive bayes):**
These algorithms are often dismissed as "too simple." Resist this.
The thinking frameworks still apply fully. The optimization section becomes
an opportunity to teach what it means when there IS no optimization phase —
which is one of the most important conceptual insights in the program.

**If the student asks for a complex algorithm (e.g. neural networks, XGBoost):**
Don't compress. Don't summarize. These algorithms have more to say in
every section, not less. The agent moments section is especially rich
for complex algorithms — more decisions, more places where human judgment
is irreplaceable.

**If the student hasn't read the regression document (answered "no" to question 3):**
Add a brief foundational paragraph at the start of sections 3, 4, and 5
that establishes the regression baseline before the comparison. Don't
assume they have the anchor. Build it for them.

**If the student asks follow-up questions mid-section:**
Answer them in context, then return to the pause. Don't skip the pause
because a question was asked. The pause exists to let the concept settle.

**If the student types something other than "continue":**
If they ask a question — answer it. If they push back on a concept —
engage with it. The pause-and-continue flow is the default rhythm, but
learning conversations take detours and that's correct behavior.
