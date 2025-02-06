from flask import Flask, jsonify, session, render_template, request
from flask_cors import CORS
from gemini import GeminiModel

app = Flask(__name__)
CORS(app)

bot = GeminiModel()

@app.route("/genai/<prompt>")
def test(prompt):
    reply = bot.send_message(prompt)
    return jsonify(eval(reply))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)