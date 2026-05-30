@app.route("/chat", methods=["POST", "GET", "OPTIONS"])
def chat():
    if request.method == "GET":
        return jsonify({"respuesta": "Ruta /chat funcionando. Usa POST para conversar."})

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