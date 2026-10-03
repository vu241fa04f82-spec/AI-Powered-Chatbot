from flask import Flask, render_template, request, jsonify
from chatbot import get_response
from database import initialize_database, save_conversation, get_conversations

app = Flask(__name__)

initialize_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "response": "Please enter a message."
        })

    bot_response = get_response(user_message)

    save_conversation(
        user_message,
        bot_response
    )

    return jsonify({
        "response": bot_response
    })


@app.route("/history", methods=["GET"])
def history():

    conversations = get_conversations()

    result = []

    for conversation in conversations:
        result.append({
            "id": conversation["id"],
            "user_message": conversation["user_message"],
            "bot_response": conversation["bot_response"],
            "created_at": conversation["created_at"]
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)