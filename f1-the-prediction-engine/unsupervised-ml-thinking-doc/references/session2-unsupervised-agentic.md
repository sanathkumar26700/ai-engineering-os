# Session 2 — Unsupervised Learning, K-Means & Agentic AI Systems
**The Evolutionary Thinking Framework**
10 Thinking Frameworks | 5 AI Agent Moments | 2 Full Session Blocks
By Ayush Singh

---

## BLOCK A — Unsupervised Learning + K-Means

### Part 1: The Shift in Thinking — When Labels Disappear

In supervised learning, you are a student preparing for an exam where you have a textbook AND an answer key. In unsupervised learning, you have the textbook but no answer key. You have to find the patterns yourself.

**What changed from Session 1:**
In Session 1, we had a shopkeeper with a notebook. Every row had both input and answer. We always knew the correct output.

In unsupervised learning, the answer column is gone. The data exists. The structure might exist. But nobody told us what anything means. **Our job shifts from predicting to discovering.**

**Three questions that are naturally unsupervised:**

| Business Question | Why There Are No Labels | What We Are Looking For |
|------------------|------------------------|------------------------|
| "Who are our different types of customers?" | "Customer type" is not written anywhere | Natural groupings in behavior data |
| "Which transactions look suspicious?" | Most fraud has never been caught and labeled | Unusual patterns that stand out |
| "Which of our 500 features say the same thing?" | No one labeled which features are redundant | Patterns of similarity between features |

---

### THINKING FRAMEWORK #1 — Unsupervised vs Supervised: The Framing Shift

In supervised learning, you have a target (Y) and your job is to learn the function that maps X → Y.

In unsupervised learning, there is no Y. Your job is to find structure inside X itself.

This changes everything: how you evaluate success, how you measure quality, and what "correct" even means.

**Key question to ask:** "Do I have labels for what I'm trying to find, or am I discovering something the data hasn't told me yet?" If you have labels, think supervised. If not, think unsupervised.

---

### Part 2: K-Means Intuition — How Grouping Actually Works

K-Means was developed by Stuart Lloyd in 1957, originally to solve a signal compression problem for phone calls — not for customer segmentation or machine learning.

**The City Halls Analogy:**
A country has 1,000 families. The government wants to build exactly 3 community centers (K=3). Process:
1. Step 1 — Guess: Plant 3 flags randomly
2. Step 2 — Assign: Every family goes to the nearest flag
3. Step 3 — Improve: Move each flag to the geographic center of its group
4. Step 4 — Repeat: Reassign, move flags again
5. Step 5 — Stop: When flags stop moving, converged

The flags = centroids. The families = data points. The groups = clusters.

**Concrete example with numbers:**

| Student | Study Hours/Week | Test Score | Cluster |
|---------|-----------------|-----------|---------|
| Alice | 2 | 40 | Group 1 |
| Bob | 3 | 45 | Group 1 |
| Eve | 8 | 85 | Group 2 |
| Frank | 9 | 88 | Group 2 |

Group 1 centroid: avg study hours = 2.5, avg score = 43.25
Group 2 centroid: avg study hours = 8.75, avg score = 86.25

No one told it these groups existed. It found them.

**One critical thing K-Means assumes:** clusters are roughly round, compact, and similar in size. K-Means draws straight-line boundaries. If your data has crescent shapes, overlapping spirals, or very different densities, K-Means will give you the wrong answer with full confidence.

---

### THINKING FRAMEWORK #2 — Every Clustering Is a Hypothesis

Choosing K-Means is choosing a hypothesis: "my data comes in round, compact, similarly-sized blobs."

Just like choosing linear regression was a hypothesis about straight-line relationships, choosing K-Means is a hypothesis about the shape of your groups.

If the hypothesis is wrong: K-Means will produce clean-looking clusters that are completely meaningless. Always ask: "do I believe my data actually forms these kinds of round blobs?"

---

### Part 3: The Loss Function — What K-Means Optimizes

K-Means fits the same Hypothesis → Loss → Optimization framework:

| Step | Supervised Learning (Session 1) | K-Means (Today) |
|------|--------------------------------|-----------------|
| HYPOTHESIS | Data follows a straight line (y = wx + b) | Data comes in K round, compact clusters |
| LOSS | MSE — how wrong are the predictions? | WCSS / Inertia — how spread out are the clusters? |
| OPTIMIZATION | Gradient descent — walk downhill step by step | Coordinate descent — alternate assign → update |

**WCSS (Within-Cluster Sum of Squares):** For every data point, measure the distance from that point to its assigned centroid. Square that distance. Add them all up.

Lower WCSS = tighter clusters. Higher WCSS = loose, spread-out clusters. K-Means minimizes WCSS. Every step moves WCSS down or leaves it the same. It never goes up.

**Worked WCSS example:**

| Student | Score | Assigned Centroid | Distance | Distance Squared |
|---------|-------|-------------------|----------|-----------------|
| Alice | 40 | Centroid 1 (score=43) | 3 | 9 |
| Bob | 45 | Centroid 1 (score=43) | 2 | 4 |
| Eve | 85 | Centroid 2 (score=87) | 2 | 4 |
| Frank | 88 | Centroid 2 (score=87) | 1 | 1 |
| **TOTAL WCSS** | | | | **18** |

**Why squaring:** same reason as MSE — a point very far from its centroid gets punished much more than a point slightly off.

**The limitation — local optima:** K-Means is guaranteed to converge but not guaranteed to find the best answer. Bad starting positions → stuck in a local optimum. Fix: run K-Means many times with different starting positions (n_init parameter). Always check what default is being used.

---

### THINKING FRAMEWORK #3 — WCSS Minimization vs Business Value

K-Means minimizes WCSS. But "tight clusters" and "useful clusters" are not the same thing.

K=500 (one customer per cluster) gives WCSS=0. Mathematically perfect. Completely useless for any business purpose.

**The right question is not:** "is WCSS low?" **The right question is:** "are these groups meaningfully different from each other in ways my business can act on?"

Mathematical quality and business utility are not the same. Always validate clusters against domain knowledge.

---

### AI CODING AGENT MOMENT #1 — Setting Up K-Means

What the agent does automatically: runs K-Means with default settings, usually K=8, random initialization, 10 restarts.

What you need to specify:
```
"Run K-Means with K=3. Use K-Means++ initialization (not random).
Run 20 restarts (n_init=20) and keep the best result.
Scale all features to zero mean and unit variance BEFORE clustering.
Show me the final WCSS and a scatter plot of the clusters."
```

Why: without specifying scaling, a feature with range 0–1,000,000 will dominate the distance calculation and the feature with range 0–1 will be invisible. The agent will not warn you.

---

### Part 4: The Big Question — How Many Clusters?

There is no universal correct answer. There is only "useful given your purpose."

**Method 1: The Elbow Method**
Plot WCSS for K=1,2,3,...10. As K increases, WCSS always decreases but the rate slows. The curve bends at some point — that bend is the "elbow." It suggests a K where adding more clusters gives diminishing returns.

**Method 2: Business Logic**

| Situation | Business Constraint | K to Choose |
|-----------|--------------------|-----------:|
| Hospital grouping patients | Hospital has 3 care teams | 3 |
| School grouping students | School can run 4 support programs | 4 |
| Marketing campaigns | Budget for 2 campaign types | 2 |

If the math suggests K=7 but your operations team can only handle K=3 programs, choose K=3. A mathematically optimal clustering that cannot be acted on is worthless.

---

### THINKING FRAMEWORK #4 — K Is a Hyperparameter, Not a Parameter

In Session 1, the model learned its parameters (w and b) from data. You did not choose them.

K is different. **K is a hyperparameter. No algorithm learns K from data. You choose it before training starts.**

This means K requires judgment. Judgment requires knowing your domain and your operational context. The elbow method gives you a starting point. Business logic gives you the final answer.

**REALITY CHECK:**
- You pick K=10 because it gives the lowest WCSS. You get 10 customer segments. Your marketing team says: "We cannot run 10 different campaigns. Pick 3." You wasted the whole analysis.
- You pick K=2 because it is simple. The data has 5 natural groups. Two segments are so mixed they give you no useful targeting signal.

---

### Part 5: Now We Name Things

| What You Already Understood | The Official Name |
|-----------------------------|------------------|
| Finding structure in data without labels | Unsupervised learning |
| Grouping similar things together | Clustering |
| The number of groups you want | K (a hyperparameter) |
| The center of a group | Centroid |
| Assigning each point to the nearest centroid | Assignment step (E-step) |
| Moving centroids to the average of their group | Update step (M-step) |
| The "badness score" K-Means minimizes | WCSS — Within-Cluster Sum of Squares (also: Inertia) |
| How tightly each point fits its group | Silhouette score (0 to 1, higher is better) |
| Running K-Means many times to avoid bad starts | Multiple restarts (n_init parameter) |
| Smarter random starting positions | K-Means++ initialization |
| The "bend" in the WCSS vs K chart | Elbow point |
| Getting stuck in a non-optimal solution | Local optimum |

---

## BLOCK B — Agentic AI + Core ML Combined

### Part 6: Why ML Alone Is Incomplete

A healthcare company spends six months building a churn prediction model. 91% accuracy. The model runs in production. For one patient: churn probability = 0.91. The patient churns. The model was right. And it did not help at all.

**"A prediction without an action is just an expensive opinion."**

| What ML Courses Teach | What You Actually Need |
|----------------------|----------------------|
| How to build a model | How to connect the model to a decision |
| How to minimize loss | How to define what you actually care about |
| Accuracy on a test set | Whether the system improves real outcomes |
| Feature engineering | Encoding business context into decisions |
| Training pipeline | Prediction → decision → action → feedback loop |

---

### Part 7: The Decision Layer — The Missing Piece

Between "what will happen" and "make it happen" sits the decision layer. It converts the ML output into a specific, concrete action.

**ML Output → Decision Logic → Action**

| ML Output | Decision Logic | Action |
|-----------|---------------|--------|
| Churn probability = 0.91 | IF probability > 0.80 → intervene | Call the customer personally |
| Churn probability = 0.65 | IF 0.50 < probability < 0.80 | Send a discount offer by email |
| Churn probability = 0.30 | IF probability < 0.50 → ignore | Do nothing (save resources) |

**Where does the LLM fit?**

| Component | Role | Example |
|-----------|------|---------|
| ML Model | Generates the prediction or score | Churn probability = 0.91 |
| Decision Logic / Policy | Decides what action to take | Probability > 0.80 → call customer |
| LLM (optional) | Executes the action with language | Writes personalized message |
| Feedback System | Records outcome and updates model | Did customer respond? Did they stay? |

The LLM is the pen. The ML model + policy is the mind.

---

### AI CODING AGENT MOMENT #2 — Framing the System Before Writing Code

Most people ask the agent to "build a churn model." Wrong starting point.

```
"Before we write any code:
(1) Our ML model outputs churn probability 0–1.
(2) Our team can take three actions: personal call, email offer, or no action.
(3) A personal call costs $20 of staff time. An email costs $0.50.
(4) The customer lifetime value is $500.
Design the decision logic that maximizes expected profit per customer,
then build the model to feed it."
```

This gives the agent a complete system design problem. The agent builds the pieces. You designed the architecture.

---

### Part 8: Loss Function vs Agent Objective

**Loss function (ML):** how wrong is the prediction? (RMSE on delivery time estimates)
**Agent objective (Business):** what outcome do we care about? (Maximize on-time deliveries; minimize refund payouts)

A model can have near-zero RMSE and still fail to achieve the business objective. Example: model consistently underestimates delivery time by 2 minutes. RMSE looks fine. But every single delivery is late. Refund payouts are at record highs.

**"Loss function is what the model learns. Objective is what the agent cares about. Make sure they point in the same direction."**

---

### THINKING FRAMEWORK #5 — Align Loss and Objective Before Building

Before choosing a loss function, ask: "What is the business outcome I actually care about?"

Then ask: "Does minimizing this loss function lead to that outcome? Or could a model with low loss still fail at the objective?"

If misaligned: consider a custom loss function that encodes the real business cost structure.

---

### Part 9: Expected Value Thinking — The Decision Engine

Most systems use a threshold: IF probability > 0.5, take action. This is wrong in almost every real case.

Probability tells you how likely something is. It does not tell you how much it matters.

**Option A:** P(success) = 20%, Value if success = $100,000 → EV = $20,000
**Option B:** P(success) = 80%, Value if success = $10,000 → EV = $8,000

Probability alone says choose B. Expected value says choose A — it is worth 2.5x more.

**How to calculate:**
EV = Probability of success × Value if it happens
Net EV = (Probability × Value) − Cost of action

**Full example with costs:**

| Customer | P(stays if offered) | LTV | EV of Offer | Cost | Net EV | Decision |
|----------|--------------------|----|------------|------|--------|---------|
| Customer A | 0.6 | $200 | $120 | $5 | $115 | YES |
| Customer B | 0.05 | $200 | $10 | $5 | $5 | MAYBE |
| Customer C | 0.02 | $200 | $4 | $5 | -$1 | NO |

Customer C: naive probability-threshold system sends them an offer. Expected value says do not — you lose $1 per send. At scale, a disaster.

---

### THINKING FRAMEWORK #6 — Expected Value Converts ML Numbers Into Decisions

Probability tells you how likely. Expected value tells you what to do.

Every agent decision should pass through: **EV = P(outcome) × Value(outcome) − Cost(action)**

If Net EV > 0: act. If Net EV < 0: do not act. If uncertain: gather more information.

Business impact: this framework instantly improves prioritization, resource allocation, and ROI for any ML-powered system. It requires no new data. Just better decision logic.

---

### Part 10: Policy — The Agent's Decision Rulebook

A policy is a complete set of rules that maps every possible ML output to a specific action.

**Writing a policy — three components:**
1. Thresholds: the ML score ranges that trigger different actions
2. Actions: what specifically happens at each threshold
3. Costs and limits: how many actions can we afford?

**Complete example — school supporting struggling students:**

| Model Output (Risk Score) | Threshold Rule | Action | Why |
|--------------------------|---------------|--------|-----|
| 0.80 – 1.00 | High risk | Assign personal tutor immediately | Student likely to fail without intervention |
| 0.60 – 0.79 | Moderate risk | Weekly check-in with advisor | Student showing early warning signs |
| 0.40 – 0.59 | Low-moderate risk | Send study resources by email | Proactive support with low cost |
| 0.00 – 0.39 | Low risk | No action | Student likely to be fine |

---

### THINKING FRAMEWORK #7 — Policy Is the Bridge Between Prediction and Reality

Without a policy, the model's output dies in a spreadsheet. With a policy, it changes the world.

Good policies are transparent, auditable, and debatable. If your policy is a black box, nobody on your team can challenge it when it makes a mistake.

Start with simple threshold rules. Refine with expected value. Learn from outcomes over time.

---

### Part 11: The Feedback Loop — What Makes a System Agentic

| Stage | What Happens | Who Does It | Example |
|-------|-------------|-------------|---------|
| PREDICT | Model generates output | ML model | Churn probability = 0.91 |
| DECIDE | Policy maps output to action | Decision logic | IF > 0.80 → send offer |
| ACT | System executes the action | Application / LLM | Retention email is sent |
| OBSERVE | Record what actually happened | Logging system | Customer clicked: yes/no |
| UPDATE | New data re-trains or adjusts system | Retraining pipeline | Model gets smarter next month |

**"An agent is a system that closes the loop between prediction and reality."**

Why most systems are not agentic: most ML deployments miss the OBSERVE and UPDATE stages. The model is trained, deployed, and left running until someone notices it has become outdated.

Closing the loop is not technically complex. It is organizationally complex — it requires processes, ownership, and willingness to rebuild the model regularly. The engineering team built the model. The product team owns the action. Nobody owns the feedback.

---

### AI CODING AGENT MOMENT #3 — Building the Feedback Loop

```
"After each intervention (email sent, call made), log the following to a database:
customer_id, model_score_at_time, action_taken, date_of_action,
outcome_at_30_days (retained/churned), revenue_at_30_days."

Then: "Set up a monthly job that:
(1) joins action logs with outcome data,
(2) creates a labeled dataset from this (ML output + action taken + actual outcome),
(3) retrains the model on the last 12 months of data,
(4) compares new model vs old model on holdout set."
```

---

### Part 12: Full End-to-End Example — The Sales Agent

200 leads. Sales team has time for 60. Which ones to prioritize?

**Layer 2 — Prediction:**

| Lead | P(reply) | P(close\|reply) | Deal Size | Expected Value (EV) |
|------|---------|----------------|----------|-------------------|
| Lead A | 0.70 | 0.40 | $50,000 | $14,000 |
| Lead B | 0.30 | 0.60 | $80,000 | $14,400 |
| Lead C | 0.90 | 0.05 | $10,000 | $450 |
| Lead D | 0.20 | 0.50 | $5,000 | $500 |

EV = P(reply) × P(close|reply) × Deal Size. Lead C has 90% reply rate but EV of only $450. Lead B has 30% reply rate but EV of $14,400.

**Layer 3 — Decision (Policy):**

| EV Tier | Rule | Action |
|---------|------|--------|
| EV > $10,000 | Tier 1 — Priority | Personal call within 24 hours |
| $2,000 < EV < $10,000 | Tier 2 — Standard | Personalized email + follow-up call |
| $500 < EV < $2,000 | Tier 3 — Nurture | Automated email sequence |
| EV < $500 | Tier 4 — Deprioritize | Add to newsletter only |

**Layer 4 — Action:** LLM drafts personalized outreach for Tier 1 and Tier 2. The LLM is not deciding who to contact — the policy decided that. The LLM is writing the message.

**Layer 5 — Feedback:** Did they reply? Did they buy? What was the actual deal size? All logged. Every week, the model improves.

**REALITY CHECK:**
Lead C (90% reply, $450 EV) gets a personal call. Sales rep spends 40 minutes. No deal. Lead B ($14,400 EV) is buried in the queue. Gets an automated email 3 weeks later. By then, they bought from a competitor. The team worked just as hard. But they worked on the wrong things.

---

### AI CODING AGENT MOMENT #4 — Multi-Agent Architecture

```
"Build a pipeline with four components:
(1) Lead Scoring Model — outputs P(reply), P(close), and deal size estimate for each lead
(2) EV Calculator — computes EV and assigns tier based on the policy table
(3) Message Generator — given a lead's profile and tier, draft personalized outreach using LLM
(4) Outcome Logger — after 7 days, fetch CRM data to log reply/no-reply and deal status"
```

Each component is clean, testable, and replaceable. When the LLM improves, you swap it. When the model drifts, you retrain it.

---

### Part 13: The Intelligent System Stack

Every intelligent system you will ever build or evaluate can be understood through five layers:

| Layer | What It Does | What You Learned |
|-------|-------------|-----------------|
| Layer 1: Data | Raw observations and history | Data quality, feature engineering (Session 1) |
| Layer 2: Prediction | "What is likely to happen?" | Regression, supervised learning (Session 1); Clustering, unsupervised (Block A today) |
| Layer 3: Decision | "What should we do?" | Expected value, policy design (Block B today) |
| Layer 4: Action | "Make it happen" | Agent execution, LLM as action layer (Block B today) |
| Layer 5: Feedback | "What actually happened?" | Feedback loop, system retraining (Block B today) |

**"Agentic systems are pipelines of decisions, not single models."**

---

## Complete Thinking Framework Summary

| # | Framework | Core Insight |
|---|-----------|-------------|
| 1 | Unsupervised vs Supervised framing | When there is no Y, you discover structure. When there is a Y, you predict. |
| 2 | Every clustering is a hypothesis | K-Means assumes round, compact blobs. If wrong, results are wrong — confidently. |
| 3 | WCSS vs business value | Tight clusters ≠ useful clusters. Always validate against domain knowledge. |
| 4 | K is a hyperparameter | You choose K. The algorithm does not. Business constraints often decide. |
| 5 | Align loss and objective | Low loss ≠ good outcomes. Check that minimizing loss leads to your actual goal. |
| 6 | Expected value thinking | Act on EV = P × Value − Cost. Not on probability alone. |
| 7 | Policy bridges prediction and action | Without a policy, predictions die in a dashboard. Policy makes predictions useful. |
| 8 | Feedback loop = agentic | A system that predicts but never learns is not an agent. Close the loop. |
| 9 | Loss function ≠ agent objective | The model learns from loss. The agent cares about outcomes. Align them explicitly. |
| 10 | Agentic = pipeline of decisions | Not one model. Five layers. Data → Predict → Decide → Act → Feedback. |

---

## AI Coding Agent Moments Summary

| # | Stage | Your Strategic Value |
|---|-------|---------------------|
| 1 | K-Means setup | Specify K, initialization method, restarts, and feature scaling |
| 2 | System framing | Design the full system before writing any code |
| 3 | Feedback loop | Design the logging schema and retraining cadence |
| 4 | Multi-agent architecture | Decompose into clean, testable, replaceable components |
| 5 | (implied throughout) | Every agent moment: you design the architecture, agent builds the pieces |

---

## What You Can Build Now

With thinking from both sessions, you can now architect intelligent systems:

1. See a business problem: "Is this supervised (I have labels) or unsupervised (I need to discover structure)?"
2. Frame the prediction: What exactly does the model output?
3. Define the objective: What does the business actually care about? Is the loss function aligned with it?
4. Design the policy: Given the ML output, what are the rules for each action tier? What is the EV of each action?
5. Build the feedback loop: How do we log outcomes? How often do we retrain? Who owns each stage?

**"The agent will solve whatever problem you give it. Give it the right problem."**
