# AI Philosophy Courtroom — Project Specification

## Project Overview

AI Philosophy Courtroom is a **domain-specific Generative AI debate system** designed to simulate philosophical debates in a courtroom format.
The system must only operate within **philosophy debate domain** and refuse unrelated queries.

The application will include:

* Courtroom debate UI
* AI opponent
* AI judge evaluation
* Domain-restricted responses
* Smooth animations
* Token-efficient responses
* Secure API handling
* GitHub-safe structure

---

# Core Requirements

## 1. Domain Restriction (IMPORTANT)

The AI must ONLY respond to philosophy debate topics.

If user asks anything unrelated, it must reply:

```
Sorry, I am trained only for philosophical debate topics. I cannot answer this query.
```

Allowed Topics:

* Free will vs determinism
* Ethics
* Consciousness
* Existentialism
* Simulation theory
* Moral philosophy
* Logic arguments
* Epistemology

Not Allowed:

* coding help
* math
* general chat
* personal advice
* random questions

---

# UI Concept — Philosophy Courtroom

Layout Structure

Top:

* Case Title
* Topic selector
* Reset debate

Center:

* Left: User Lawyer
* Right: AI Lawyer
* Middle: AI Judge Verdict

Bottom:

* Small input box
* Send argument button

---

# Animation Requirements

## Entry Animation (Very Important)

On app start:

1. Dark screen fade in
2. Title appears with glow effect
3. Courtroom UI slides upward
4. Judge panel fades in
5. Input box appears last

Animation must be:

* smooth
* fast
* modern
* no lag

---

# Smooth Animation Requirements

Every interaction must animate:

* message slide up
* judge verdict fade
* score counter animate
* typing indicator
* button hover glow
* panel transitions

All animations must be:

* smooth
* subtle
* not heavy
* performance optimized

---

# Stack Requirement

Frontend:

* HTML
* CSS
* JavaScript

Backend:

* Python (Flask)

AI API:

* OpenRouter API

Styling:

* Tailwind CSS

Animation:

* Framer Motion (if React)
  OR
* CSS animations (if pure HTML)

---

# Token Optimization (IMPORTANT)

Responses must be:

* short
* logical
* argument style
* not long paragraphs

Example output:

```
Your claim assumes free causation.
However determinism argues all actions have prior causes.
Can you justify causality independence?
```

Avoid:

* long essays
* storytelling
* unnecessary explanation

Goal:
Save output tokens.

---

# AI Behavior

System Prompt must enforce:

* philosophical debate mode
* argument format
* short responses
* judge evaluation
* domain restriction

Judge must evaluate:

* logic strength
* fallacies
* clarity
* winner

---

# Project File Structure

```
Philosphy-Courtroom/
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── app.js
│
├── backend/
│   ├── app.py
│   ├── debate_logic.py
│   ├── judge.py
│
├── config/
│   └── config.py        ← API KEY FILE (NOT PUSHED)
│
├── .env                 ← API KEY (NOT PUSHED)
├── .gitignore
├── README.md
```

---

# API Key Security (VERY IMPORTANT)

API key must NEVER be uploaded to GitHub.

Use:

config/config.py

Example:

```
OPENROUTER_API_KEY = "your_key_here"
```

Add to `.gitignore`:

```
.env
config/config.py
```

Do NOT upload:

* api key
* .env
* config files
* test keys
* debug logs

---

# GitHub Repository

Project must be continuously updated in:

https://github.com/shivansh01-24/Philosphy-Courtroom.git

Update rules:

Only push:

* frontend code
* backend code
* animations
* UI improvements
* prompt logic
* judge system

Do NOT push:

* API keys
* personal data
* test junk
* AI generation logs
* irrelevant files

---

# AI Training Behavior

AI must behave as:

Role:
Philosophical Debate Opponent

Style:
Logical
Short
Argumentative
Counter questioning

Reject non-domain queries.

---

# Input Box Requirement

Input must be:

* small
* minimal
* single line
* expandable
* centered

Example:

```
[ Enter your argument... ]
```

No big chat textarea.

---

# Judge Output Format

```
Judge Verdict:

User Logic: 7.5
AI Logic: 8.2

Winner: AI

Weakness:
User argument lacked causal justification
```

---

# Features List

Required:

* debate UI
* AI opponent
* AI judge
* topic selector
* animations
* token optimized output
* domain restriction
* secure API

Optional:

* score history
* debate rounds
* philosopher personalities
* typing animation
* sound effects

---

# Final Goal

Build a:

Domain-specific
Generative AI
Philosophy Debate Courtroom
with smooth animations
secure API
token efficient responses
and strict topic control

This project must be:

* visually astonishing
* technically correct
* secure
* domain constrained
* presentation ready

---
