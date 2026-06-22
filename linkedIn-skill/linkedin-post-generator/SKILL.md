---
name: linkedin-post-generator
description: >
  Generate high-quality, human-sounding LinkedIn posts by combining a viral signal from Reddit or Twitter/X with the student's personal voice from their master doc. Use this skill whenever someone wants to write a LinkedIn post, says "help me write a post", "turn this Reddit thread into a post", "I found this tweet — make it a LinkedIn post", or pastes any Reddit/Twitter content and asks what to do with it. Also trigger when someone shares a topic they want to post about and asks how to frame it for LinkedIn. This skill asks clarifying questions before writing — it does not generate a post without understanding the person's angle and voice.
---

# LinkedIn Post Generator

## Core Philosophy

A LinkedIn post is not news. It's not a summary. It's not a tutorial.

It's an **opinionated take from a specific person** — triggered by something that's already proven to resonate with an audience.

The formula: **Viral Signal (from Reddit/Twitter) + Your Personal Story/Opinion (from master doc) = Post that feels human and gets engagement.**

Never write the post before you understand both inputs.

---

## Step 1: Understand the Source Material

When a student shares a Reddit post, Twitter/X thread, or just a topic — first understand what they've given you.

**Ask yourself:**
- Is this a Reddit post? A tweet? A comment? A news headline?
- What's the viral signal here — is it a controversial opinion, a surprising stat, a relatable frustration, a bold prediction?
- How many upvotes/likes/comments? (Validation of virality)
- What's the emotion the original content triggered — curiosity, disagreement, surprise, recognition?

If the student shares a link or screenshot but not enough context, ask:
> "Can you tell me what specifically stood out to you about this? What was your gut reaction when you saw it?"

---

## Step 2: Ask These Questions (Always, Before Writing)

Don't skip this. A post written without these answers will sound generic.

### Required Questions (ask all of these):

**1. What's your gut reaction to this content?**
> Do you agree, disagree, want to add nuance, or does it remind you of something you've personally experienced?

**2. Have you ever experienced something related to this — personally or in your work?**
> Even a small connection is enough. "This reminded me of when I was debugging a model for 3 days and realized..." is better than a generic opinion.

**3. What do you want people to take away from your post?**
> Should they feel validated? Should they think differently? Should they be curious about your work?

**4. Who are you talking to?**
> Recruiters? Fellow engineers? Founders? Just your niche AI/ML audience? (This changes the tone and depth.)

**5. Do you have a master doc?** (the personal writing sample / voice experiment from Week 1)
> If yes, paste the relevant part or the whole thing. If no, ask them to share 3-4 sentences in their own words about their background or experience.

### Conditional Questions (ask if needed):

**If they want to disagree with the source:**
> "What specifically do you think is wrong or incomplete? And what's your alternative take?"

**If they're not sure what their angle is:**
> "Let me suggest 3 angles — tell me which one feels most like you." Then generate the angles, don't write the post yet.

**If they want to add a personal story:**
> "Walk me through what happened, even roughly. The messier the better — I'll clean it up."

---

## Step 3: Suggest an Angle Before Writing

Once you have the source + their answers, don't jump to the post. First, present 2-3 possible angles:

**Format:**
```
Angle 1 — [Label]: [One sentence describing the approach]
Angle 2 — [Label]: [One sentence describing the approach]
Angle 3 — [Label]: [One sentence describing the approach]

Which feels most like you — or should we mix elements?
```

**Common angle types:**
- **Contrarian** — you disagree with the popular take in the source
- **Personal validation** — the source mirrors something you've lived through, and you add your story
- **Layer of nuance** — you agree but want to add what the source missed
- **Future prediction** — you use the source as a jumping-off point for where this is heading
- **Builder's perspective** — you've actually built something related, here's what you found

---

## Step 4: Write the Post

Once the angle is confirmed, write the post following these rules:

### Structure
Read `references/post-structure.md` for detailed formatting. Short version:

1. **Hook (Line 1)** — Single sentence. Bold claim, surprising stat, or punchy question. This is what shows in the feed before "see more." Everything depends on this line.
2. **Setup (Lines 2-4)** — Brief context. What happened, what you saw, what triggered this.
3. **The turn** — Your opinion, story, or insight. This is the value.
4. **Takeaway** — What should the reader do, think, or feel differently?
5. **Soft close** — Optional: a question to invite comments, or a one-liner that lands the point.

### Voice Rules (non-negotiable)
- Short paragraphs. Max 2 sentences per paragraph. White space is your friend on LinkedIn.
- No bullet points unless genuinely listing things (max 3-4 items, not as a crutch)
- Don't start with "I" — LinkedIn algorithm and readers both respond better to a hook that starts with the point
- No "In today's world...", "It's no secret that...", "I'm excited to share..."
- Write like you're texting a smart friend, not presenting at a conference
- One intentional small imperfection — a fragmented sentence, a conversational aside, a "tbh" or "ngl" where it fits naturally. This signals human.

### AI Detection Rules
Read `references/ai-slop-removal.md` before finalizing. Hard bans:
- "delve", "landscape", "tapestry", "pivotal", "testament to", "underscores the importance of"
- "In conclusion", "In summary", "Let's explore"
- Three-item parallel lists with the same structure (Rule of Three AI tell)
- Ending any paragraph with a clause about significance or importance

### Length
- LinkedIn posts: 150–300 words is the sweet spot. Under 150 feels lazy. Over 400 starts to lose people.
- Hook + blank line + content + blank line between each paragraph.

---

## Step 5: Output Format

Deliver in this order:

```
POST (ready to copy-paste):
[Full post text]

---

HOOK VARIANT:
[Alternative first line if they want to test a different opener]

---

NOTES:
[1-2 sentences on what angle you used and any suggested tweaks they can make]
```

---

## Step 6: Offer to Iterate

After delivering, always say:

> "Want me to make it more contrarian / more personal / shorter / add a specific story? Just tell me what to tweak."

Don't rewrite from scratch unless they ask. Make targeted edits.

---

## References

- `references/post-structure.md` — detailed hook formulas and post formats
- `references/ai-slop-removal.md` — full banned word list and AI detection patterns to avoid
