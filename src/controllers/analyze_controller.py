from flask import Blueprint, jsonify, request

from ..application.services import KnowledgeGraphService
from ..domain.models import AnalyzeRequest


def create_analyze_blueprint(service: KnowledgeGraphService) -> Blueprint:
    blueprint = Blueprint("analyze", __name__)

    @blueprint.route("/health", methods=["GET"])
    def health() -> tuple:
        return jsonify({"status": "ok"}), 200

    @blueprint.route("/analyze", methods=["POST"])
    def analyze() -> tuple:
        data = request.get_json(silent=True) or {}
        text = data.get("text")
        if not text:
            return jsonify({"error": "Field 'text' is required."}), 400

        prompt_name = data.get("prompt_name") or service.get_default_prompt()

        try:
            response = service.analyze(AnalyzeRequest(text=text, prompt_name=prompt_name))
        except FileNotFoundError:
            return jsonify({"error": f"Prompt '{prompt_name}' not found."}), 404
        except ValueError as exc:
            return jsonify({"error": str(exc)}), 400

        return jsonify(response.to_dict()), 200

    return blueprint
