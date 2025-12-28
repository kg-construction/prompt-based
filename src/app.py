import os

from flask import Flask
from dotenv import load_dotenv

from .application.services import KnowledgeGraphService
from .controllers.analyze_controller import create_analyze_blueprint
from .infrastructure.prompt_repository import PromptRepository

DEFAULT_PROMPT = "knowledge_graph_prompt.txt"


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)

    env_default_prompt = os.getenv("prompt", DEFAULT_PROMPT)
    prompt_repository = PromptRepository()
    env_default_prompt = os.getenv("DEFAULT_PROMPT_NAME", DEFAULT_PROMPT)
    service = KnowledgeGraphService(prompt_repository, default_prompt=env_default_prompt)
    app.register_blueprint(create_analyze_blueprint(service))

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=True)
