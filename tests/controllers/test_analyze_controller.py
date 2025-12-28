import json
from pathlib import Path

import pytest

from src.controllers.analyze_controller import create_analyze_blueprint
from src.application.services import KnowledgeGraphService
from src.infrastructure.prompt_repository import PromptRepository


class StubPromptRepo(PromptRepository):
    def __init__(self, prompt_text: str):
        super().__init__(prompt_dir=Path("unused"))
        self.prompt_text = prompt_text

    def load_prompt(self, prompt_name: str) -> str:  # type: ignore[override]
        if prompt_name == "missing.txt":
            raise FileNotFoundError("not found")
        return self.prompt_text


@pytest.fixture()
def client():
    repo = StubPromptRepo(prompt_text="Prompt content")
    service = KnowledgeGraphService(repo, default_prompt="test_prompt.txt")

    from flask import Flask

    app = Flask(__name__)
    app.register_blueprint(create_analyze_blueprint(service))
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield client


def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


def test_analyze_happy_path(client):
    payload = {"text": "Some text", "prompt_name": "test_prompt.txt"}
    resp = client.post("/analyze", data=json.dumps(payload), content_type="application/json")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["prompt_name"] == "test_prompt.txt"
    assert data["prompt"] == "Prompt content"
    assert data["input_text"] == "Some text"
    assert "User: Some text" in data["message_for_model"]


def test_analyze_missing_text_returns_400(client):
    resp = client.post("/analyze", data=json.dumps({}), content_type="application/json")
    assert resp.status_code == 400
    assert "text" in resp.get_json()["error"]


def test_analyze_missing_prompt_returns_404(client):
    payload = {"text": "Other", "prompt_name": "missing.txt"}
    resp = client.post("/analyze", data=json.dumps(payload), content_type="application/json")

    assert resp.status_code == 404
    assert "not found" in resp.get_json()["error"]


def test_analyze_replaces_placeholder(client):
    repo = StubPromptRepo(prompt_text="Placeholder: ${USER_TEXT}")
    service = KnowledgeGraphService(repo, default_prompt="test_prompt.txt")

    from flask import Flask

    app = Flask(__name__)
    app.register_blueprint(create_analyze_blueprint(service))
    app.config.update({"TESTING": True})

    with app.test_client() as local_client:
        payload = {"text": "abc", "prompt_name": "test_prompt.txt"}
        resp = local_client.post("/analyze", data=json.dumps(payload), content_type="application/json")

        assert resp.status_code == 200
        assert resp.get_json()["message_for_model"] == "Placeholder: abc"
