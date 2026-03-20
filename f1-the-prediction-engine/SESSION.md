# F1 — The Prediction Engine
**Session:** Regression & Supervised Learning
**Track:** AI Engineering Foundations

---

## What this session is about

Before you touch a library, before you write a line of code, you need to understand one thing: what does it mean for a machine to *learn*?

This session answers that question from the ground up. Not just the math — the thinking. Why regression exists, what a loss function really is, why gradient descent works, and most importantly: why most students build the right model for the wrong problem.

By the end, you won't just know linear regression. You'll have a framework for thinking about every ML algorithm you'll ever encounter.

---

## What you'll build

A complete regression pipeline on a real dataset — from raw data to a result you can explain to a non-technical stakeholder. Every step follows the 9 skills in this folder.

---

## The 9 skills in this session

Each skill is a `SKILL.md` file you drop into your project. Your AI reads it and behaves like a senior engineer, not a code monkey.

```
f1-the-prediction-engine/
├── problem-framing-skill/       ← Stage 1: Frame the right problem first
├── model-hypothesis-skill/      ← Stage 2: Choose your hypothesis wisely
├── loss-design-skill/           ← Stage 3: Design loss around business costs
├── training-diagnostics-skill/  ← Stage 4: Debug training before trusting results
├── feature-engineering-skill/   ← Stage 5: Domain knowledge beats polynomial tricks
├── generalization-skill/        ← Stage 6: Detect and fix overfitting + assumptions
├── data-integrity-skill/        ← Stage 7: Catch leakage before it catches you
├── evaluation-skill/            ← Stage 8: Report impact, not just RMSE
└── ml-system-skill/             ← Stage 9: The full pipeline, gate by gate
```

---

## How to use these skills

### Option A — One skill at a time (recommended for beginners)

Pick the skill that matches where you are in the project. Copy that `SKILL.md` into your working folder. Tell your AI to read it.

```
Week 1 — Starting out:
  problem-framing-skill → model-hypothesis-skill

Week 2 — Working with data:
  data-integrity-skill → feature-engineering-skill

Week 3 — Training:
  loss-design-skill → training-diagnostics-skill

Week 4 — Evaluating:
  generalization-skill → evaluation-skill

Submission:
  ml-system-skill (final gate check)
```

### Option B — Full pipeline (recommended for projects)

Copy all 9 skills into your project folder. Use `ml-system-skill` as your guide — it references the others at the right stages.

Tell your AI:
```
Read all SKILL.md files in this folder.
Follow ml-system-skill as the pipeline controller.
Use the other skills when their stage comes up.
```

---

## The session map

| Concept | Skill | The key question it answers |
|---|---|---|
| Why does regression exist? | `problem-framing-skill` | What decision are we actually making? |
| What is a model? | `model-hypothesis-skill` | What are we assuming about the world? |
| What is a cost function? | `loss-design-skill` | What does "wrong" cost the business? |
| How does the model learn? | `training-diagnostics-skill` | Why is training failing / slow / diverging? |
| What makes a good feature? | `feature-engineering-skill` | What does a domain expert already know? |
| What is overfitting really? | `generalization-skill` | Will this work on data the model hasn't seen? |
| What is data leakage? | `data-integrity-skill` | Would I actually have this info at prediction time? |
| How do I measure success? | `evaluation-skill` | What does the stakeholder actually care about? |
| How do I run a real pipeline? | `ml-system-skill` | What are the gotchas at each stage? |

---

## The single most important idea in this session

```
HYPOTHESIS → LOSS → OPTIMIZATION
```

Every ML algorithm ever invented follows this three-step architecture.
Linear regression (1805). GPT-4 (2023). Everything in between.

If you understand these three for any algorithm, you understand that algorithm at its core.
If you can't state all three, you don't understand it yet.

---

## Recommended reading

`../research/regression-supervised-learning.md`

This is the full conceptual foundation behind all 9 skills — the history, the math, the 13 thinking frameworks, and the 8 moments where human judgment beats AI automation.

---

## What comes next

Once you've completed this session:
- You can frame any supervised learning problem correctly
- You can audit any dataset for leakage before modeling
- You can translate technical results into business impact
- You have a pipeline template you'll reuse for the rest of your career

**Next session:** F2 — Cluster Thinking *(K-Means & Unsupervised Learning)*
