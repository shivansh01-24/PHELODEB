"""
AI Philosophy Courtroom — Debate Logic Module
Handles AI opponent responses with domain restriction and philosopher personalities.
"""

import requests
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, AI_MODELS, MAX_OPPONENT_TOKENS


# ── Allowed Philosophy Topics ──────────────────────────────────
ALLOWED_TOPICS = {
    'free-will', 'ethics', 'consciousness', 'existentialism',
    'simulation', 'epistemology', 'justice', 'absurdism',
}

TOPIC_DESCRIPTIONS = {
    'free-will': 'Free Will vs Determinism',
    'ethics': 'Ethics and Morality',
    'consciousness': 'The Nature of Consciousness',
    'existentialism': 'Existentialism and Human Freedom',
    'simulation': 'Simulation Theory and Reality',
    'epistemology': 'Epistemology — The Limits of Knowledge',
    'justice': 'Justice, Fairness, and Social Contract',
    'absurdism': 'Absurdism and the Meaning of Life',
}

# ── Philosopher Personalities ──────────────────────────────────
PHILOSOPHER_STYLES = {
    'balanced': (
        "You argue in a balanced, analytical manner. "
        "Use clear logic, cite relevant philosophical concepts, and challenge assumptions."
    ),
    'socratic': (
        "You argue in the Socratic method. "
        "Primarily use probing questions to expose contradictions. "
        "Rarely make direct claims — instead, guide through questioning. "
        "Example: 'But if you claim X, does that not imply Y? And is Y not contradictory to Z?'"
    ),
    'nietzsche': (
        "You argue like Friedrich Nietzsche — bold, provocative, and unapologetic. "
        "Challenge moral assumptions, invoke the will to power, and question herd mentality. "
        "Use dramatic, aphoristic language."
    ),
    'stoic': (
        "You argue from a Stoic perspective — calm, rational, detached from emotion. "
        "Focus on what is within one's control, virtue ethics, and accepting nature's course. "
        "Reference Marcus Aurelius, Epictetus, or Seneca when relevant."
    ),
    'existentialist': (
        "You argue from an existentialist viewpoint — emphasize radical freedom, "
        "personal responsibility, absurdity, and authenticity. "
        "Reference Sartre, Camus, or Kierkegaard when relevant."
    ),
}

# ── Domain Restriction Keywords ────────────────────────────────
NON_PHILOSOPHY_KEYWORDS = [
    'code', 'program', 'python', 'javascript', 'html', 'css', 'sql',
    'math', 'calculate', 'equation', 'solve',
    'recipe', 'cook', 'food', 'weather', 'sports', 'game',
    'movie', 'music', 'celebrity', 'stock', 'crypto',
    'homework', 'assignment', 'exam',
    'hello', 'hi there', 'how are you', 'what is your name',
    'write me a', 'generate a', 'create a',
    'translate', 'summarize this article',
]

DOMAIN_REJECTION = (
    "I appreciate your curiosity, but I am designed exclusively for philosophical debate. "
    "I cannot assist with that query. Please present a philosophical argument related to our topic."
)


def is_philosophy_related(text: str) -> bool:
    """Check if the input is related to philosophy."""
    text_lower = text.lower().strip()
    
    # Short inputs might still be philosophical
    if len(text_lower) < 3:
        return False
    
    # Check for non-philosophy keywords
    for keyword in NON_PHILOSOPHY_KEYWORDS:
        if keyword in text_lower:
            # Some keywords might appear in philosophical context
            # e.g., "the game of life" or "calculate the moral weight"
            philosophy_terms = [
                'moral', 'ethic', 'logic', 'truth', 'reality', 'exist',
                'conscious', 'free will', 'determin', 'soul', 'mind',
                'philosophy', 'philosophical', 'argument', 'reason',
                'virtue', 'justice', 'meaning', 'absurd', 'simulat',
                'knowledge', 'belief', 'epistem', 'ontolog', 'metaphys',
            ]
            if any(term in text_lower for term in philosophy_terms):
                return True
            return False
    
    return True


def build_opponent_prompt(topic: str, philosopher: str, history: list, round_num: int) -> str:
    """Build the system prompt for the AI opponent."""
    topic_desc = TOPIC_DESCRIPTIONS.get(topic, topic)
    style = PHILOSOPHER_STYLES.get(philosopher, PHILOSOPHER_STYLES['balanced'])
    
    history_context = ""
    if history:
        recent = history[-3:]  # Last 3 exchanges for context
        for h in recent:
            history_context += f"\nUser (Round {h['round']}): {h['user']}\nYou (Round {h['round']}): {h['ai']}"
    
    return f"""You are a philosophical debate opponent in a courtroom setting.
DEBATE TOPIC: {topic_desc}
CURRENT ROUND: {round_num} of 5

STYLE: {style}

RULES — FOLLOW STRICTLY:
1. ONLY discuss philosophical topics. If the user's argument is not philosophical, respond: "{DOMAIN_REJECTION}"
2. Keep responses SHORT — maximum 3-4 sentences. Be concise and punchy.
3. Use logical argument structure: claim → reasoning → challenge.
4. Directly counter the user's specific argument. Do not repeat their points.
5. End with a pointed question or challenge when possible.
6. Do NOT use bullet points, numbered lists, or markdown formatting.
7. Do NOT be agreeable — you are the OPPONENT. Challenge everything.

{f'PREVIOUS EXCHANGES:{history_context}' if history_context else ''}

Respond as the prosecution opposing the user's argument. Be sharp, logical, and philosophically rigorous."""


def get_ai_response(argument: str, topic: str, philosopher: str, history: list, round_num: int) -> str:
    """Get AI opponent response from OpenRouter API with model fallback."""
    
    # Domain check
    if not is_philosophy_related(argument):
        return DOMAIN_REJECTION
    
    system_prompt = build_opponent_prompt(topic, philosopher, history, round_num)
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "AI Philosophy Courtroom",
    }
    
    # Try each model in order (primary → fallbacks)
    last_error = None
    for model in AI_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": argument},
            ],
            "max_tokens": MAX_OPPONENT_TOKENS,
            "temperature": 0.8,
            "top_p": 0.9,
        }
        
        try:
            print(f"[Debate] Trying model: {model}")
            response = requests.post(OPENROUTER_BASE_URL, json=payload, headers=headers, timeout=30)
            
            # If rate limited (429), try next model
            if response.status_code == 429:
                print(f"[Debate] Rate limited on {model}, trying fallback...")
                last_error = f"Rate limited on {model}"
                continue
            
            response.raise_for_status()
            data = response.json()
            
            content = data['choices'][0]['message']['content'].strip()
            
            # Clean up any markdown formatting
            content = content.replace('**', '').replace('*', '').replace('#', '')
            
            print(f"[Debate] Success with model: {model}")
            return content
            
        except requests.exceptions.Timeout:
            print(f"[Debate] Timeout on {model}, trying fallback...")
            last_error = f"Timeout on {model}"
            continue
        except requests.exceptions.RequestException as e:
            print(f"[Debate] API Error on {model}: {e}")
            last_error = str(e)
            continue
        except (KeyError, IndexError) as e:
            print(f"[Debate] Parse error on {model}: {e}")
            last_error = str(e)
            continue
    
    # All models failed
    print(f"[Debate] All models failed. Last error: {last_error}")
    return "A procedural error has occurred in the court. Please present your argument again."
