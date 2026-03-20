# AI Engineering OS

Skills for AI engineers. One session at a time.

Each session is a folder. Each folder contains `SKILL.md` files — drop them into your project, tell your AI to read them, and it starts behaving like a senior engineer instead of a code generator.

---

## Sessions

| Session | Name | Topic | Status |
|---|---|---|---|
| F1 | **The Prediction Engine** | Regression & Supervised Learning | ✅ Ready |
| F2 | **Cluster Thinking** | K-Means & Unsupervised Learning | 🔜 Coming soon |
| F3 | **The GenAI Builder** | GenAI Foundations | 🔜 Coming soon |
| F4 | **Ship Ready** | EDA, Business Thinking & Sprint Readiness | 🔜 Coming soon |

---

## F1 — The Prediction Engine ✅

**9 skills. Full regression pipeline. From "what are we building?" to "here's the business impact."**

```
f1-the-prediction-engine/
├── SESSION.md                     ← Start here
├── problem-framing-skill/         ← Frame the right problem before touching data
├── model-hypothesis-skill/        ← Choose a hypothesis that matches your situation
├── loss-design-skill/             ← Design loss around business costs, not defaults
├── training-diagnostics-skill/    ← Debug training before trusting the output
├── feature-engineering-skill/     ← Domain knowledge beats polynomial noise
├── generalization-skill/          ← Overfitting, regularization, assumption checks
├── data-integrity-skill/          ← Catch leakage before it reaches production
├── evaluation-skill/              ← Report rupee impact, not just RMSE
└── ml-system-skill/               ← The full 7-stage pipeline, gate by gate
```

---

## F2 — Cluster Thinking 🔜

**K-Means & Unsupervised Learning — when you don't have labels**

```
f2-cluster-thinking/
└── SESSION.md                     ← Preview: what's coming
```

Skills planned: unsupervised framing, K-Means intuition, cluster failure modes,
validation (elbow + silhouette), segment-to-insight, full unsupervised pipeline.

---

## F3 — The GenAI Builder 🔜

**GenAI Foundations — LLMs, prompting, RAG, API engineering**

```
f3-genai-builder/
└── SESSION.md                     ← Preview: what's coming
```

Skills planned: LLM intuition, prompt architecture, RAG design, API engineering,
GenAI vs traditional ML decision framework, building a real tool.

---

## F4 — Ship Ready 🔜

**EDA, Business Thinking & Sprint Readiness — from model to delivered project**

```
f4-ship-ready/
└── SESSION.md                     ← Preview: what's coming
```

Skills planned: hypothesis-driven EDA, data quality assessment, insight-to-action,
production code habits, Git workflow, sprint tools.

---

## How to use any skill

1. Find the skill that matches where you are in your project
2. Copy that `SKILL.md` into your working folder
3. Tell your AI: `Read SKILL.md and follow it`
4. The AI asks the right questions instead of jumping to code

**In Cursor:** `@SKILL.md — read this and follow it`
**In Claude Code:** `Read SKILL.md and follow it for this project`
**In ChatGPT:** Paste the SKILL.md contents and say "follow these rules for our session"

---

## Research

`research/regression-supervised-learning.md` — the full conceptual foundation behind F1.
The 13 thinking frameworks and 8 AI coding agent moments that the F1 skills encode.

---

## The idea behind this repo

AI coding assistants are good at writing code. They are bad at judgment.

They default to binary classifiers when you need ranking. They use random splits on time-series data. They report RMSE to stakeholders who need rupee impact. They add polynomial features instead of asking a domain expert.

These skills don't make the AI write more code. They make it ask better questions. The SKILL.md files encode the judgment of a senior ML engineer — the questions they ask before writing a line, the checks they run after training, the translations they make before presenting results.

One session. One skill. Better engineering.
