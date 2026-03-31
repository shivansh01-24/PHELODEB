"""
AI Philosophy Courtroom - Test Suite
Tests all backend modules: server, debate logic, judge, domain restriction, config.

Usage:
    cd tests
    python test_app.py
"""

import sys
import os
import json
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# -- Test Counter --
passed = 0
failed = 0
total = 0


def test(name, condition, detail=""):
    global passed, failed, total
    total += 1
    if condition:
        passed += 1
        print(f"  {total:>2}. [PASS] {name}")
    else:
        failed += 1
        print(f"  {total:>2}. [FAIL] {name} -- {detail}")


# ==============================================================
print("\n[TEST] AI Philosophy Courtroom - Test Suite")
print("=" * 60)


# -- 1. Config Tests -------------------------------------------
print("\n[CONFIG] Config & Models")
print("-" * 40)

try:
    from config.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, AI_MODELS, MAX_OPPONENT_TOKENS, MAX_JUDGE_TOKENS

    test("Config loads", True)
    test("API key is set", OPENROUTER_API_KEY and OPENROUTER_API_KEY != "your_openrouter_api_key_here",
         "API key not configured in .env")
    test("Base URL is correct", "openrouter.ai" in OPENROUTER_BASE_URL,
         f"Got: {OPENROUTER_BASE_URL}")
    test("3 models configured", len(AI_MODELS) == 3,
         f"Expected 3 models, got {len(AI_MODELS)}")
    test("Primary model is llama-3.1-8b", "llama-3.1-8b-instruct" in AI_MODELS[0],
         f"Got: {AI_MODELS[0]}")
    test("Fallback 1 is mistral-7b", "mistral-7b" in AI_MODELS[1],
         f"Got: {AI_MODELS[1]}")
    test("Fallback 2 is gemma-7b", "gemma-7b" in AI_MODELS[2],
         f"Got: {AI_MODELS[2]}")
    test("Opponent token limit set", MAX_OPPONENT_TOKENS > 0,
         f"Got: {MAX_OPPONENT_TOKENS}")
    test("Judge token limit set", MAX_JUDGE_TOKENS > 0,
         f"Got: {MAX_JUDGE_TOKENS}")
except Exception as e:
    test("Config loads", False, str(e))


# -- 2. Domain Restriction Tests --------------------------------
print("\n[DOMAIN] Domain Restriction")
print("-" * 40)

try:
    from debate_logic import is_philosophy_related, DOMAIN_REJECTION

    # Should PASS (philosophy topics)
    test("'Free will is an illusion' -> accepted",
         is_philosophy_related("Free will is an illusion"))
    test("'Consciousness requires experience' -> accepted",
         is_philosophy_related("Consciousness requires subjective experience"))
    test("'Morality is relative' -> accepted",
         is_philosophy_related("Morality is relative to culture"))
    test("'I think therefore I am' -> accepted",
         is_philosophy_related("I think therefore I am"))
    test("'Existence precedes essence' -> accepted",
         is_philosophy_related("Existence precedes essence according to Sartre"))

    # Should FAIL (non-philosophy topics)
    test("'Write me python code' -> rejected",
         not is_philosophy_related("Write me python code"))
    test("'What is the weather' -> rejected",
         not is_philosophy_related("What is the weather today"))
    test("'Calculate 2+2' -> rejected",
         not is_philosophy_related("Calculate 2+2"))
    test("'Hello how are you' -> rejected",
         not is_philosophy_related("Hello how are you"))

    # Edge case: philosophy term + non-philosophy keyword
    test("'The game of moral philosophy' -> accepted (edge case)",
         is_philosophy_related("The game of moral philosophy is complex"))

    # Very short input
    test("Short input 'hi' -> rejected",
         not is_philosophy_related("hi"))

    # Domain rejection message exists
    test("Rejection message is defined",
         len(DOMAIN_REJECTION) > 20,
         "Rejection message too short")

except Exception as e:
    test("Domain restriction module loads", False, str(e))


# -- 3. Judge JSON Parsing Tests --------------------------------
print("\n[JUDGE] Judge Response Parsing")
print("-" * 40)

try:
    from judge import parse_judge_response, validate_verdict

    # Perfect JSON
    result = parse_judge_response('{"user_score": 7.5, "ai_score": 8.2, "feedback": "Good debate"}')
    test("Parses clean JSON",
         result["user_score"] == 7.5 and result["ai_score"] == 8.2)

    # JSON with surrounding text
    result = parse_judge_response('Here is my verdict: {"user_score": 6.0, "ai_score": 7.0, "feedback": "test"} end')
    test("Extracts JSON from text",
         result["user_score"] == 6.0 and result["ai_score"] == 7.0)

    # Malformed -- should fallback gracefully
    result = parse_judge_response("This is not JSON at all")
    test("Handles non-JSON gracefully",
         "user_score" in result and "ai_score" in result)

    # Score clamping
    result = validate_verdict({"user_score": 15.0, "ai_score": -3.0})
    test("Clamps scores to 0-10 range",
         result["user_score"] == 10.0 and result["ai_score"] == 0.0)

    # Missing fields
    result = validate_verdict({"user_score": 5.0})
    test("Handles missing fields",
         result["ai_score"] == 6.5 and result["feedback"] != "")

    # Score rounding
    result = validate_verdict({"user_score": 7.777, "ai_score": 3.333})
    test("Rounds scores to 1 decimal",
         result["user_score"] == 7.8 and result["ai_score"] == 3.3)

except Exception as e:
    test("Judge parsing module loads", False, str(e))


# -- 4. Flask Server Tests --------------------------------------
print("\n[SERVER] Flask Server Endpoints")
print("-" * 40)

try:
    from app import app as flask_app

    client = flask_app.test_client()

    # Health endpoint
    res = client.get('/api/health')
    test("GET /api/health -> 200",
         res.status_code == 200)
    data = json.loads(res.data)
    test("Health returns status 'ok'",
         data.get("status") == "ok")

    # Frontend serving
    res = client.get('/')
    test("GET / -> serves HTML",
         res.status_code == 200 and b"<!DOCTYPE html>" in res.data)
    test("HTML contains courtroom title",
         b"Philosophy Courtroom" in res.data)

    # CSS serving
    res = client.get('/style.css')
    test("GET /style.css -> 200",
         res.status_code == 200)

    # JS serving
    res = client.get('/app.js')
    test("GET /app.js -> 200",
         res.status_code == 200)

    # Debate endpoint -- empty argument
    res = client.post('/api/debate',
                      data=json.dumps({"argument": "", "topic": "ethics"}),
                      content_type='application/json')
    test("POST /api/debate empty -> 400",
         res.status_code == 400)

    # Debate endpoint -- no data
    res = client.post('/api/debate',
                      data="not json",
                      content_type='text/plain')
    test("POST /api/debate no JSON -> 400",
         res.status_code == 400)

    # Debate endpoint -- argument too long
    res = client.post('/api/debate',
                      data=json.dumps({"argument": "x" * 1500, "topic": "ethics"}),
                      content_type='application/json')
    test("POST /api/debate too long -> 400",
         res.status_code == 400)

    # Judge endpoint -- missing arguments
    res = client.post('/api/judge',
                      data=json.dumps({"user_argument": "test"}),
                      content_type='application/json')
    test("POST /api/judge missing fields -> 400",
         res.status_code == 400)

except Exception as e:
    test("Flask server loads", False, str(e))


# -- 5. Live API Tests (requires API key) -----------------------
print("\n[API] Live API Tests (requires valid API key)")
print("-" * 40)

try:
    from config.config import OPENROUTER_API_KEY as key_check

    if key_check and key_check != "your_openrouter_api_key_here":
        client = flask_app.test_client()

        # Debate -- valid philosophy argument
        print("  ...calling OpenRouter API (may take 10-20 seconds)...")
        res = client.post('/api/debate',
                          data=json.dumps({
                              "argument": "Free will is an illusion created by consciousness",
                              "topic": "free-will",
                              "philosopher": "balanced",
                              "history": [],
                              "round": 1
                          }),
                          content_type='application/json')
        test("Debate API returns 200",
             res.status_code == 200,
             f"Got status {res.status_code}")

        if res.status_code == 200:
            data = json.loads(res.data)
            test("Debate response has content",
                 len(data.get("response", "")) > 10,
                 "Response too short or empty")
            print(f"       AI said: \"{data.get('response', '')[:100]}...\"")

            # Judge -- evaluate the exchange
            print("  ...calling Judge API...")
            res2 = client.post('/api/judge',
                               data=json.dumps({
                                   "user_argument": "Free will is an illusion",
                                   "ai_argument": data["response"],
                                   "topic": "free-will",
                                   "round": 1,
                                   "history": []
                               }),
                               content_type='application/json')
            test("Judge API returns 200",
                 res2.status_code == 200,
                 f"Got status {res2.status_code}")

            if res2.status_code == 200:
                verdict = json.loads(res2.data)
                test("Judge returns user_score",
                     "user_score" in verdict)
                test("Judge returns ai_score",
                     "ai_score" in verdict)
                test("Judge returns feedback",
                     "feedback" in verdict and len(verdict["feedback"]) > 5)
                test("Scores are in valid range",
                     0 <= verdict["user_score"] <= 10 and 0 <= verdict["ai_score"] <= 10,
                     f"user={verdict['user_score']}, ai={verdict['ai_score']}")
                print(f"       Scores: You={verdict['user_score']}, AI={verdict['ai_score']}")
                print(f"       Feedback: \"{verdict['feedback'][:100]}\"")

        # Domain restriction -- live test
        res = client.post('/api/debate',
                          data=json.dumps({
                              "argument": "Write me python code for sorting",
                              "topic": "ethics",
                              "philosopher": "balanced",
                              "history": [],
                              "round": 1
                          }),
                          content_type='application/json')
        if res.status_code == 200:
            data = json.loads(res.data)
            test("Domain restriction works live",
                 "philosophical" in data["response"].lower() or "debate" in data["response"].lower() or "cannot" in data["response"].lower(),
                 f"Response: {data['response'][:80]}")
    else:
        print("  [SKIP] No API key configured in .env")
        print("         Add your key to .env and re-run to test API integration.")

except Exception as e:
    test("Live API tests", False, str(e))


# ==============================================================
print("\n" + "=" * 60)
print(f"Results: {passed}/{total} passed", end="")
if failed > 0:
    print(f", {failed} failed")
    print("[FAIL] Some tests failed -- check the output above.")
else:
    print()
    print("[PASS] All tests passed!")
print("=" * 60 + "\n")

sys.exit(0 if failed == 0 else 1)
