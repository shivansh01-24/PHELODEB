"""
AI Philosophy Courtroom — Judge Module
Evaluates debate arguments and provides scoring and verdicts.
"""

import requests
import json
import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, AI_MODELS, MAX_JUDGE_TOKENS


def build_judge_prompt(topic: str, round_num: int, history: list) -> str:
    """Build the system prompt for the AI judge."""

    history_summary = ""
    if history and len(history) > 1:
        recent = history[-3:]
        for h in recent:
            history_summary += f"\n  Round {h['round']} — User: \"{h['user'][:80]}...\" | AI: \"{h['ai'][:80]}...\""

    return f"""You are an impartial philosophical judge in a courtroom debate.
TOPIC: {topic}
ROUND: {round_num} of 5

YOUR TASK:
Evaluate both arguments and return a JSON verdict.

SCORING CRITERIA (0.0 to 10.0):
- Logical coherence: Is the argument internally consistent?
- Philosophical depth: Does it engage meaningfully with philosophical concepts?
- Persuasiveness: How compelling is the argument?
- Counter-argument strength: Does it effectively address the opponent's points?
- Use of evidence/examples: Are claims supported?

RESPONSE FORMAT — You MUST respond with ONLY valid JSON, nothing else:
{{
  "user_score": <number 0.0-10.0>,
  "ai_score": <number 0.0-10.0>,
  "feedback": "<one sentence explaining key strength/weakness>"
}}

RULES:
- Be fair and impartial. Do not always favor one side.
- Score based purely on argument quality, not topic position.
- Keep feedback to ONE concise sentence.
- The scores should reflect genuine quality differences.
- Do NOT add any text outside the JSON object.
{f'CONTEXT FROM EARLIER ROUNDS:{history_summary}' if history_summary else ''}"""


def parse_judge_response(content: str) -> dict:
    """Parse judge response, handling potential formatting issues."""

    # Try direct JSON parse
    try:
        result = json.loads(content.strip())
        return validate_verdict(result)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON from text
    json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
    if json_match:
        try:
            result = json.loads(json_match.group())
            return validate_verdict(result)
        except json.JSONDecodeError:
            pass

    # Try extracting scores from text
    user_match = re.search(r'user[_\s]*score["\s:]*(\d+\.?\d*)', content, re.IGNORECASE)
    ai_match = re.search(r'ai[_\s]*score["\s:]*(\d+\.?\d*)', content, re.IGNORECASE)

    if user_match and ai_match:
        return {
            "user_score": min(float(user_match.group(1)), 10.0),
            "ai_score": min(float(ai_match.group(1)), 10.0),
            "feedback": "The judge has evaluated both arguments on their logical merits."
        }

    # Fallback — balanced scores
    return {
        "user_score": 6.5,
        "ai_score": 7.0,
        "feedback": "Both arguments presented valid philosophical perspectives."
    }


def validate_verdict(result: dict) -> dict:
    """Ensure verdict has all required fields with valid values."""
    user_score = float(result.get('user_score', 6.0))
    ai_score = float(result.get('ai_score', 6.5))

    # Clamp scores
    user_score = max(0.0, min(10.0, user_score))
    ai_score = max(0.0, min(10.0, ai_score))

    return {
        "user_score": round(user_score, 1),
        "ai_score": round(ai_score, 1),
        "feedback": result.get('feedback', 'The judge has noted the arguments of both parties.')
    }


def get_judge_verdict(user_argument: str, ai_argument: str, topic: str, round_num: int, history: list) -> dict:
    """Get judge verdict from OpenRouter API with model fallback."""

    system_prompt = build_judge_prompt(topic, round_num, history)

    user_content = (
        f"DEFENSE (User) argues:\n\"{user_argument}\"\n\n"
        f"PROSECUTION (AI) argues:\n\"{ai_argument}\"\n\n"
        f"Evaluate both arguments and return your verdict as JSON."
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "AI Philosophy Courtroom — Judge",
    }

    # Try each model in order (primary → fallbacks)
    last_error = None
    for model in AI_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "max_tokens": MAX_JUDGE_TOKENS,
            "temperature": 0.4,
            "top_p": 0.85,
        }

        try:
            print(f"[Judge] Trying model: {model}")
            response = requests.post(OPENROUTER_BASE_URL, json=payload, headers=headers, timeout=30)

            # If rate limited (429), try next model
            if response.status_code == 429:
                print(f"[Judge] Rate limited on {model}, trying fallback...")
                last_error = f"Rate limited on {model}"
                continue

            response.raise_for_status()
            data = response.json()

            content = data['choices'][0]['message']['content'].strip()
            print(f"[Judge] Success with model: {model}")
            return parse_judge_response(content)

        except requests.exceptions.Timeout:
            print(f"[Judge] Timeout on {model}, trying fallback...")
            last_error = f"Timeout on {model}"
            continue
        except requests.exceptions.RequestException as e:
            print(f"[Judge] API Error on {model}: {e}")
            last_error = str(e)
            continue
        except (KeyError, IndexError) as e:
            print(f"[Judge] Parse error on {model}: {e}")
            last_error = str(e)
            continue

    # All models failed — return balanced fallback
    print(f"[Judge] All models failed. Last error: {last_error}")
    return {
        "user_score": 6.0,
        "ai_score": 6.5,
        "feedback": "A procedural matter delayed the judge's evaluation."
    }
