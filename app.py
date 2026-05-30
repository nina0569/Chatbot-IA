from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def home():
    return "Chatbot IA funcionando correctamente 🚀"

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return jsonify({"ok": True}), 200

    try:
        data = request.get_json()
        mensaje_usuario = data.get("mensaje")

        if not mensaje_usuario:
            return jsonify({"respuesta": "No enviaste ningún mensaje"}), 400

        respuesta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un tutor de programación para estudiantes universitarios. Explica de forma clara y sencilla."},
                {"role": "user", "content": mensaje_usuario}
            ],
            max_tokens=300
        )

        texto = respuesta.choices[0].message.content
        return jsonify({"respuesta": texto})

    except Exception as e:
        return jsonify({"respuesta": "Error interno: " + str(e)}), 500

if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=puerto)