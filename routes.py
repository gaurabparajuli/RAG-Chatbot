from flask import Blueprint, request, jsonify, render_template
from model import generate_response
from database import store_chat, connect_db

chat_bp = Blueprint('chat', __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    response, retrieved_docs = generate_response(query)
    store_chat("user", query)
    store_chat("system", response)
    
    return jsonify({"answer": response, "retrieved_chunks": retrieved_docs})

@chat_bp.route("/history", methods=["GET"])
def history():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chat ORDER BY timestamp DESC")
    history = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(history)

@chat_bp.route("/ask", methods=["POST"])
def ask():
    query = request.form.get("query")
    if not query:
        return render_template("index.html", error="Please enter a question.")
    response, _ = generate_response(query)
    store_chat("user",query)
    store_chat("system",response)
    return render_template("index.html",query=query,response=response)