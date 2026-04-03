# ⚖️ AI Philosophy Courtroom

<div align="center">

**A domain-specific Generative AI debate system that simulates philosophical debates in a courtroom format.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776ab?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-API-6366f1?style=for-the-badge)](https://openrouter.ai)
[![License](https://img.shields.io/badge/License-MIT-gold?style=for-the-badge)](LICENSE)

*Where minds clash and truth prevails*

</div>

---

## 📸 Screenshots

### Entry Screen
> Dark cinematic entry with golden typography, floating philosophical symbols, and animated scales of justice.
<img width="1465" height="787" alt="Screenshot 2026-04-03 104810" src="https://github.com/user-attachments/assets/fb7f3970-bbe5-4c5f-beb8-e27994090ad6" />

### Courtroom Interface
> Three-panel layout — Defense (You) | Judge (AI) | Prosecution (AI) — with glassmorphism panels, live scoring, and philosopher style selection.
<img width="1914" height="886" alt="Screenshot 2026-04-03 104729" src="https://github.com/user-attachments/assets/329d2cfa-8626-47c9-9591-cab226b8ce6b" />

<div align="center">



</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏛️ **Courtroom UI** | Premium dark theme with glassmorphism panels, gold accents, and smooth animations |
| 🤖 **AI Opponent** | Argues against you with sharp, logical counter-reasoning |
| 👨‍⚖️ **AI Judge** | Scores both arguments on logic, depth, and persuasiveness (0-10 scale) |
| 🎭 **Philosopher Styles** | Choose your debate personality — Socratic, Nietzschean, Stoic, Existentialist, or Balanced |
| ⚡ **Objection System** | Dramatic Ace Attorney-style objection overlay with screen flash |
| 📊 **5-Round Debates** | Progressive rounds with cumulative scoring and final verdict |
| 🔒 **Domain Restricted** | AI only responds to philosophy topics — rejects unrelated queries |
| 💎 **Token Optimized** | Short, punchy, argumentative responses — no essays |
| 🔮 **Floating Particles** | Greek/logic symbols (Φ, Ψ, Ω, ∀, ∃) floating in the background |
| ⌨️ **Typewriter Effect** | AI responses appear character-by-character |
| 🏆 **Final Verdict** | Grand finale overlay with cumulative scores and winner declaration |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | HTML5, CSS3, JavaScript | UI, animations, state management |
| **Backend** | Python (Flask) | API server, routing |
| **AI API** | OpenRouter | LLM-powered debate & judging |
| **Primary Model** | `meta-llama/llama-3.1-8b-instruct` | Main debate & judge model |
| **Fallback 1** | `mistralai/mistral-7b-instruct` | Used if primary is rate-limited |
| **Fallback 2** | `google/gemma-7b-it` | Final fallback option |
| **Styling** | Custom CSS with CSS Variables | Dark theme, glassmorphism, animations |
| **Typography** | Google Fonts (Cinzel, Inter, Playfair Display) | Premium courtroom aesthetic |

---

## 📁 Project Structure

```
Philosphy-Courtroom/
│
├── frontend/                  # Client-side code
│   ├── index.html             # Main HTML — courtroom layout
│   ├── style.css              # Premium dark theme + animations
│   └── app.js                 # Debate logic, API calls, DOM control
│
├── backend/                   # Server-side code
│   ├── app.py                 # Flask server — routes & API endpoints
│   ├── debate_logic.py        # AI opponent — prompts, domain check, fallbacks
│   └── judge.py               # AI judge — scoring, verdict, JSON parsing
│
├── config/                    # Configuration (⚠️ gitignored)
│   └── config.py              # API keys, model settings, token limits
│
├── tests/                     # Test suite
│   └── test_app.py            # Automated tests for all modules
│
├── .env                       # API key storage (⚠️ gitignored)
├── .gitignore                 # Security — excludes keys & config
├── requirements.txt           # Python dependencies
├── plan.md                    # Original project specification
└── README.md                  # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed
- **OpenRouter API key** — get one free at [openrouter.ai](https://openrouter.ai)

### Step 1: Clone the Repository

```bash
git clone https://github.com/shivansh01-24/PHELODEB.git
cd PHELODEB
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Key

Open the `.env` file and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=sk-or-v1-your_actual_key_here
```

> ⚠️ **Never commit your API key to GitHub!** The `.env` file is already in `.gitignore`.

### Step 4: Start the Server

```bash
cd backend
python app.py
```

You'll see:
```
⚖  AI Philosophy Courtroom — Server Starting...
   http://127.0.0.1:5000
```

### Step 5: Open in Browser

Navigate to **http://127.0.0.1:5000** and click **"Enter the Courtroom"** to begin.

---

## ☁️ Vercel Deployment

This project is pre-configured for serverless deployment on Vercel.

1. Create a GitHub repository and push this code to it.
2. Go to [Vercel](https://vercel.com/) and import your repository.
3. In the Vercel project settings, add your Environment Variables:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key.
4. Deploy! Vercel will automatically use `vercel.json` to configure the Python backend and static frontend.


---

## 🎮 How to Use

### Starting a Debate

1. **Select a Topic** — Use the dropdown in the header (e.g., "Free Will vs Determinism")
2. **Choose a Style** — Click a philosopher chip at the bottom (Socratic, Nietzschean, etc.)
3. **Type your argument** — Enter your philosophical stance in the input box
4. **Press Enter** or click the **➤ send button**
5. **Watch the AI respond** — The AI opponent will counter your argument with a typewriter effect
6. **Read the Judge's verdict** — The center panel shows scores for both sides

### Debate Flow

```
Round 1  →  You argue  →  AI counters  →  Judge scores both  →  Round 2 ...
                                                                    ↓
Round 5  →  Final verdict overlay  →  Winner declared  →  Start new case
```

### Objection System

- Click the red **⚡ OBJECTION!** button to dramatically challenge the AI's last argument
- A full-screen flash animation plays
- Your input is pre-filled with an objection opener — complete it with your counter-argument

### Philosopher Styles

| Style | Behavior |
|-------|----------|
| ⚖ **Balanced** | Analytical, logical, cites philosophical concepts |
| 🏛 **Socratic** | Uses probing questions to expose contradictions |
| ⚡ **Nietzschean** | Bold, provocative, challenges moral assumptions |
| 🗿 **Stoic** | Calm, rational, focuses on virtue and control |
| 🌀 **Existentialist** | Emphasizes freedom, responsibility, and absurdity |

### Available Topics

- Free Will vs Determinism
- Ethics & Morality
- Nature of Consciousness
- Existentialism
- Simulation Theory
- Epistemology — Limits of Knowledge
- Justice & Fairness
- Absurdism & Meaning of Life

---

## 🧪 Testing

A full test suite is provided to verify all components work correctly.

### Run All Tests

```bash
cd tests
python test_app.py
```

### What's Tested

| Test | What It Checks |
|------|---------------|
| `test_health_endpoint` | Server is running and responds correctly |
| `test_frontend_served` | HTML page loads from Flask |
| `test_domain_restriction` | Non-philosophy queries are rejected |
| `test_philosophy_detection` | Philosophy topics are correctly identified |
| `test_debate_endpoint` | AI opponent API returns valid responses |
| `test_judge_endpoint` | Judge API returns scores & feedback |
| `test_judge_json_parsing` | Judge handles malformed AI responses |
| `test_score_validation` | Scores are clamped to 0.0–10.0 range |
| `test_model_fallback_config` | All 3 models are configured correctly |
| `test_empty_argument_rejected` | Blank inputs are properly rejected |

### Expected Output

```
🧪 AI Philosophy Courtroom — Test Suite
============================================================

1. ✅ Health endpoint → Server is running
2. ✅ Frontend served → HTML loads correctly
3. ✅ Domain restriction → Non-philosophy rejected
4. ✅ Philosophy detection → Valid topics accepted
...

============================================================
Results: 10/10 passed
✅ All tests passed!
```

---

## 🔑 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the courtroom frontend |
| `GET` | `/api/health` | Health check — returns server status |
| `POST` | `/api/debate` | Submit argument, receive AI counter-argument |
| `POST` | `/api/judge` | Submit both arguments, receive verdict |

### POST `/api/debate`

**Request:**
```json
{
    "argument": "Free will exists because we experience choice",
    "topic": "free-will",
    "philosopher": "socratic",
    "history": [],
    "round": 1
}
```

**Response:**
```json
{
    "response": "But does the experience of choice prove its existence? Could not a determined system create the illusion of freedom?",
    "round": 1,
    "topic": "free-will"
}
```

### POST `/api/judge`

**Request:**
```json
{
    "user_argument": "Free will exists because...",
    "ai_argument": "But does the experience...",
    "topic": "free-will",
    "round": 1,
    "history": []
}
```

**Response:**
```json
{
    "user_score": 7.2,
    "ai_score": 7.8,
    "feedback": "User presents a valid experiential argument but AI effectively challenges the assumption."
}
```

---

## 🔒 Security

| Item | Status |
|------|--------|
| API keys in `.env` | ✅ Gitignored |
| `config/config.py` | ✅ Gitignored |
| No hardcoded secrets | ✅ Uses `python-dotenv` |
| Input length limit | ✅ Max 1000 characters |
| Domain restriction | ✅ Rejects non-philosophy queries |

---

## 🎨 Design Details

- **Color Palette**: Deep black (`#07070d`) + Gold accents (`#d4a853`) + Blue for user + Red for AI
- **Glass Effect**: `backdrop-filter: blur()` on all panels
- **Typography**: Cinzel (headings), Inter (body), Playfair Display (accents)
- **15+ Animations**: Entry fade, panel slides, gavel strike, score pop, typing dots, particle float, objection flash, verdict reveal
- **Responsive**: Adapts to tablet and mobile with stacked panels

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with 🧠 philosophy and ⚡ code**

*"The unexamined life is not worth living." — Socrates*

</div>
