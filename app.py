import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import anthropic
from dotenv import load_dotenv
from knowledge_base import ISCP_SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)
CORS(app)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

ESCALATION_KEYWORDS = [
    "complaint", "appeal", "safeguarding", "bullying", "harassment",
    "speak to someone", "talk to a person", "human", "real person",
    "urgent", "emergency", "arcp tomorrow", "arcp today",
    "locked out", "account disabled", "data missing", "records lost",
]

def should_escalate(message: str) -> bool:
    lower = message.lower()
    return any(kw in lower for kw in ESCALATION_KEYWORDS)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "messages" not in data:
        return jsonify({"error": "Invalid request"}), 400

    user_messages = data["messages"]  # list of {"role": "user"/"assistant", "content": "..."}

    # Check latest user message for hard escalation triggers
    latest_user_msg = ""
    for m in reversed(user_messages):
        if m["role"] == "user":
            latest_user_msg = m["content"]
            break

    immediate_escalate = should_escalate(latest_user_msg)

    if immediate_escalate:
        escalation_note = (
            "\n\n---\n"
            "**This sounds like something our helpdesk team should handle directly.** "
            "Please contact them:\n\n"
            "- **Email:** helpdesk@iscp.ac.uk\n"
            "- **Phone:** 020 7869 6299\n"
            "- **Hours:** Monday–Friday, 9am–5pm\n\n"
            "They aim to respond to emails within 24 hours."
        )
    else:
        escalation_note = ""

    try:
        response = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=1024,
            system=ISCP_SYSTEM_PROMPT,
            messages=user_messages,
        )

        reply = response.content[0].text

        # Append escalation details if triggered
        if escalation_note:
            reply += escalation_note

        return jsonify({
            "reply": reply,
            "escalated": immediate_escalate,
        })

    except anthropic.AuthenticationError:
        return jsonify({"error": "Invalid API key. Please check your .env file."}), 401
    except anthropic.APIError as e:
        return jsonify({"error": f"API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("WARNING: ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key.")
    app.run(debug=True, port=5050)
