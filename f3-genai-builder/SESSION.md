# F3 — The GenAI Builder
**Session:** GenAI Foundations
**Track:** AI Engineering Foundations
**Status:** Coming soon

---

## What this session is about

F1 and F2 were about learning patterns from data. F3 is about something different: models that already know almost everything, and your job is to direct them.

This session teaches you how LLMs actually work — not the marketing version, the engineering version. Tokens, embeddings, context windows, attention. Then it teaches you to build real things on top of them: prompt systems, RAG pipelines, API-powered tools.

The central question of this session: when do you use GenAI, and when do you use traditional ML?

---

## What you'll build

A functional GenAI tool via API — something a real user could interact with. With a proper prompt system, context management, and an understanding of where it will fail.

---

## Skills in this session (coming soon)

```
f3-genai-builder/
├── llm-intuition-skill/           ← What transformers actually do (no PhD required)
├── prompt-architecture-skill/     ← Zero-shot, few-shot, CoT — when to use which
├── rag-design-skill/              ← RAG: what it solves, when it fails, how to build it
├── api-engineering-skill/         ← Costs, rate limits, retries, latency — production reality
├── genai-vs-ml-skill/             ← Decision framework: GenAI vs traditional ML
└── genai-tool-skill/              ← Building and shipping a real GenAI tool
```

---

## The key questions this session answers

| Concept | The question |
|---|---|
| LLM intuition | What is the model actually doing when it generates a token? |
| Prompt engineering | Is this an art or an engineering discipline? (It's both.) |
| RAG | Why does a model that knows everything still need your documents? |
| API reality | What does it actually cost to run this in production? |
| GenAI vs ML | How do I decide which tool to reach for? |

---

## The single most important idea in this session

An LLM is a probability distribution over tokens, conditioned on everything that came before.

Everything else — prompting, RAG, fine-tuning, agents — is an attempt to condition that distribution more precisely toward what you actually want.

---

## Prerequisites

Complete F1 — The Prediction Engine before starting this session.
F2 — Cluster Thinking is helpful but not required.

**Previous:** F2 — Cluster Thinking
**Next:** F4 — Ship Ready
