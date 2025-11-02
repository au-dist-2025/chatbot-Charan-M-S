# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os, re
from random import choice

app = Flask(__name__)
CORS(app)

KB_FILE = "knowledge_base.json"
MEM_FILE = "user_memory.json"

def load_kb():
    with open(KB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_memory():
    if os.path.exists(MEM_FILE):
        try:
            with open(MEM_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (ValueError, json.JSONDecodeError):
            # empty or invalid JSON file - start with empty memory
            return {}
    return {}

def save_memory(mem):
    with open(MEM_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2)

kb = load_kb()

def detect_intent(text):
    t = text.lower()
    m = re.search(r"(?:my name is|i am|call me)\s+([a-zA-Z]+)", t)
    if m: return "name", m.group(1).capitalize()
    if any(w in t for w in ["hi","hello","hey"]): return "greet", None
    if "spaced repetition" in t or "spaced" in t: return "spaced", None
    if "note" in t: return "notes", None
    if "time" in t or "time management" in t: return "time", None
    if "exam" in t: return "exam", None
    if "resource" in t or "where to learn" in t: return "resources", None
    if "procrastin" in t: return "procrastination", None
    if "math" in t: return "math", None
    if "program" in t or "coding" in t: return "programming", None
    if "group study" in t or "group" in t: return "group", None
    if "active recall" in t or "recall" in t: return "recall", None
    if any(w in t for w in ["thanks","thank you"]): return "thanks", None
    if any(w in t for w in ["bye","exit","quit"]): return "bye", None
    return "unknown", None

def get_response(intent, ent, mem):
    if intent == "greet":
        name = mem.get("name")
        return f"Hello {name}! How can StudyBuddy help?" if name else "Hello! I'm StudyBuddy. How can I help you study today?"
    if intent == "name":
        mem["name"] = ent
        save_memory(mem)
        return f"Nice to meet you, {ent}. I'll remember your name."
    if intent == "spaced": return kb.get("what is spaced repetition")
    if intent == "notes": return kb.get("how to take notes")
    if intent == "time": return kb.get("time management tips")
    if intent == "exam": return kb.get("exam preparation")
    if intent == "resources": return kb.get("best study resources")
    if intent == "procrastination": return kb.get("how to avoid procrastination")
    if intent == "math": return kb.get("how to study math")
    if intent == "programming": return kb.get("how to study programming")
    if intent == "group": return kb.get("group study tips")
    if intent == "recall": return kb.get("what is active recall")
    if intent == "thanks": return "You're welcome! Good luck with your studies."
    if intent == "bye": return "Goodbye — study well!"
    return choice([
        "Sorry, I didn't get that. Could you rephrase or ask about study tips, time management, or notes?",
        "I don't know that yet. Try asking 'how to study math' or 'exam preparation'."
    ])

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json() or {}
        message = data.get("message", "")
        mem = load_memory()
        intent, ent = detect_intent(message)
        response = get_response(intent, ent, mem)
        return jsonify({"response": response})
    except Exception as e:
        # log the exception to server console for debugging
        import traceback
        traceback.print_exc()
        return jsonify({"error": "internal_server_error", "message": str(e)}), 500

@app.route("/")
def home():
    return "StudyBuddy API is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
