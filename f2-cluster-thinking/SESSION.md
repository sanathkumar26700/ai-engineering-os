# F2 — Cluster Thinking
**Session:** K-Means & Unsupervised Learning
**Track:** AI Engineering Foundations
**Status:** Coming soon

---

## What this session is about

In F1 you had labels. Someone told you the answer — "this customer churned, this one didn't." The model's job was to learn the pattern.

In F2, nobody gives you the answer. You have data. No labels. No target column. The question becomes: *what structure is hiding in this data?*

This session teaches you to find it — and more importantly, to know when the structure you found is real versus something the algorithm invented.

---

## What you'll build

A customer segmentation system on real e-commerce data — from raw behavioral data to actionable business segments with distinct retention strategies per cluster.

---

## Skills in this session (coming soon)

```
f2-cluster-thinking/
├── unsupervised-framing-skill/    ← When you don't have labels — what are you even doing?
├── kmeans-intuition-skill/        ← K-Means from scratch, step-by-step
├── cluster-failure-skill/         ← Wrong K, scaling failures, non-spherical traps
├── cluster-validation-skill/      ← Elbow method, silhouette score, business sense-check
├── segment-insight-skill/         ← Turning cluster numbers into business recommendations
└── unsupervised-pipeline-skill/   ← Full pipeline: data → clusters → decisions
```

---

## The key questions this session answers

| Concept | The question |
|---|---|
| Unsupervised framing | Without a label, what does "correct" even mean? |
| K-Means mechanics | What is the algorithm actually doing at each step? |
| Failure modes | Why does K-Means fail, and how do you catch it? |
| Choosing K | Is there a right answer, or is it always a judgment call? |
| Business translation | What do you *do* with the clusters once you have them? |

---

## The single most important idea in this session

Clustering algorithms always find clusters. Even in random noise.

The hard part is not running the algorithm — it's knowing whether what it found is real, stable, and actionable. That judgment cannot be automated.

---

## Prerequisites

Complete F1 — The Prediction Engine before starting this session.

**Previous:** F1 — The Prediction Engine
**Next:** F3 — The GenAI Builder
