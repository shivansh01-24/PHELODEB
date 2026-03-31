"""
AI Philosophy Courtroom - Flask Backend Server
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import traceback

# Add parent directory to path for config imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from debate_logic import get_ai_response, is_philosophy_related, DOMAIN_REJECTION
from judge import get_judge_verdict

# -- Flask App --
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)


# -- Serve Frontend --
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)


# -- API: Debate Endpoint --
@app.route('/api/debate', methods=['POST'])
def handle_debate():
    """Handle user argument and return AI opponent response."""
    try:
        data = request.get_json(force=True, silent=True)

        if not data:
            return jsonify({"error": "No data provided"}), 400

        argument = data.get('argument', '').strip()
        topic = data.get('topic', 'free-will')
        philosopher = data.get('philosopher', 'balanced')
        history = data.get('history', [])
        round_num = data.get('round', 1)

        if not argument:
            return jsonify({"error": "No argument provided"}), 400

        if len(argument) > 1000:
            return jsonify({"error": "Argument too long. Keep it under 1000 characters."}), 400

        # Get AI response
        response_text = get_ai_response(argument, topic, philosopher, history, round_num)

        return jsonify({
            "response": response_text,
            "round": round_num,
            "topic": topic,
        })

    except Exception as e:
        print(f"[ERROR] Debate endpoint: {e}")
        traceback.print_exc()
        return jsonify({
            "error": "Internal server error",
            "response": "A procedural error has occurred in the court. Please try again."
        }), 200  # Return 200 so frontend can display the message


# -- API: Judge Endpoint --
@app.route('/api/judge', methods=['POST'])
def handle_judge():
    """Evaluate both arguments and return judge verdict."""
    try:
        data = request.get_json(force=True, silent=True)

        if not data:
            return jsonify({"error": "No data provided"}), 400

        user_argument = data.get('user_argument', '').strip()
        ai_argument = data.get('ai_argument', '').strip()
        topic = data.get('topic', 'free-will')
        round_num = data.get('round', 1)
        history = data.get('history', [])

        if not user_argument or not ai_argument:
            return jsonify({"error": "Both arguments required for judgment"}), 400

        # Get verdict
        verdict = get_judge_verdict(user_argument, ai_argument, topic, round_num, history)

        return jsonify(verdict)

    except Exception as e:
        print(f"[ERROR] Judge endpoint: {e}")
        traceback.print_exc()
        # Return a valid verdict so frontend doesn't crash
        return jsonify({
            "user_score": 6.0,
            "ai_score": 6.5,
            "feedback": "The judge encountered a procedural delay. Scores are provisional."
        })


# -- API: Health Check --
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "The court is in session."})


# -- Run --
if __name__ == '__main__':
    print("\nAI Philosophy Courtroom - Server Starting...")
    print("   http://127.0.0.1:5000\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
