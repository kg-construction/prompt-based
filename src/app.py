from flask import Flask, jsonify, request

from .prompt_loader import load_prompt

app = Flask(__name__)

DEFAULT_PROMPT = "knowledge_graph_prompt.txt"


@app.route("/health", methods=["GET"])
def health() -> tuple:
    return jsonify({"status": "ok"}), 200


@app.route("/analyze", methods=["POST"])
def analyze() -> tuple:
    data = request.get_json(silent=True) or {}
    text = data.get("text")
    if not text:
        return jsonify({"error": "Field 'text' is required."}), 400

    prompt_name = data.get("prompt_name", DEFAULT_PROMPT)

    try:
        prompt_text = load_prompt(prompt_name)
    except FileNotFoundError:
        return jsonify({"error": f"Prompt '{prompt_name}' not found."}), 404
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    # This is where you would call your LLM client. For now we echo the payload.
    payload_for_model = f"{prompt_text}\n\nUser: {text}\nAssistant:"

    return (
        jsonify(
            {
                "prompt_name": prompt_name,
                "prompt": prompt_text,
                "input_text": text,
                "message_for_model": payload_for_model,
            }
        ),
        200,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
