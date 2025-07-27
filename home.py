from flask import Flask, render_template, request, jsonify
import sqlite3
import difflib
import re

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('chatbot.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def chatbot():
    return render_template("chatbot.html")

@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    data = request.get_json()
    user_msg = data.get('msg', '').strip().lower()

    wants_code = any(kw in user_msg for kw in ['code', 'program', 'implementation'])

    # 1. Try exact match
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM dsa WHERE LOWER(topic)=?", (user_msg.replace("code", "").strip(),)).fetchone()
    conn.close()

    if row:
        return format_response(row, wants_code)

    # 2. Try fuzzy match
    topic, score = find_best_topic(user_msg)
    if topic and score >= 0.6:
        conn = get_db_connection()
        row = conn.execute("SELECT * FROM dsa WHERE LOWER(topic)=?", (topic.lower(),)).fetchone()
        conn.close()
        if row:
            return format_response(row, wants_code)

    # 3. Not found
    return jsonify({
        "type": "text",
        "response": "Sorry, I don't have an answer for that yet."
    })


def format_response(row, wants_code=False):
    descriptions = [row["description1"], row["description2"]]
    descriptions = [d for d in descriptions if d]

    code_map = {
        "python": row["code"] or "",
        "cpp": row["code_cpp"] or "",
        "java": row["code_java"] or "",
        "c": row["code_c"] or ""
    }

    # Filter out empty code values
    code_map = {k: v for k, v in code_map.items() if v.strip()}

    # CASE: user only wants code
    if wants_code:
        return jsonify({
            "type": "multi-code",
            "topic": row["topic"],
            "descriptions": [],  # No descriptions
            "code": code_map
        })

    # CASE: user wants description (default)
    return jsonify({
        "type": "multi-code",
        "topic": row["topic"],
        "descriptions": descriptions,
        "code": {}  # No code unless explicitly asked
    })


def find_best_topic(user_input):
    conn = get_db_connection()
    rows = conn.execute("SELECT topic FROM dsa").fetchall()
    conn.close()

    all_topics = [row['topic'].lower().strip() for row in rows]
    input_keywords = re.findall(r'\b\w+\b', user_input.lower())

    # 1. Exact keyword match
    for topic in all_topics:
        topic_keywords = re.findall(r'\b\w+\b', topic)
        if any(word in input_keywords for word in topic_keywords):
            return topic, 1.0

    # 2. Fuzzy match using difflib
    match = difflib.get_close_matches(user_input, all_topics, n=1, cutoff=0.6)
    if match:
        return match[0], 0.7

    return None, 0

if __name__ == "__main__":
    app.run(debug=True)
