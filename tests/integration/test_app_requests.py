import json
from pathlib import Path

import pytest

from src.app import create_app
from src.infrastructure import prompt_repository


@pytest.fixture()
def client(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    prompt_dir = tmp_path / "prompt"
    prompt_dir.mkdir()
    (prompt_dir / "test_prompt.txt").write_text("Prompt content", encoding="utf-8")

    original_init = prompt_repository.PromptRepository.__init__

    def _init(self, prompt_dir=None, _default_dir=prompt_dir):
        chosen_dir = _default_dir if prompt_dir is None else prompt_dir
        original_init(self, prompt_dir=chosen_dir)

    monkeypatch.setattr(prompt_repository.PromptRepository, "__init__", _init)

    app = create_app()
    app.config.update({"TESTING": True})

    with app.test_client() as client:
        yield client


def test_analyze_request_flow(client):
    payload = {"text": "Integration text", "prompt_name": "test_prompt.txt"}
    resp = client.post("/analyze", data=json.dumps(payload), content_type="application/json")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["prompt_name"] == "test_prompt.txt"
    assert data["prompt"] == "Prompt content"
    assert data["input_text"] == "Integration text"
    assert "User: Integration text" in data["message_for_model"]


def test_analyze_placeholder_is_replaced(client, monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    prompt_dir = tmp_path / "prompt2"
    prompt_dir.mkdir()
    (prompt_dir / "test_prompt.txt").write_text("Placeholder ${USER_TEXT}", encoding="utf-8")

    original_init = prompt_repository.PromptRepository.__init__

    def _init(self, prompt_dir=None, _default_dir=prompt_dir):
        chosen_dir = _default_dir if prompt_dir is None else prompt_dir
        original_init(self, prompt_dir=chosen_dir)

    monkeypatch.setattr(prompt_repository.PromptRepository, "__init__", _init)

    app = create_app()
    app.config.update({"TESTING": True})
    with app.test_client() as client2:
        payload = {"text": "XYZ", "prompt_name": "test_prompt.txt"}
        resp = client2.post("/analyze", data=json.dumps(payload), content_type="application/json")

        assert resp.status_code == 200
        assert resp.get_json()["message_for_model"] == "Placeholder XYZ"
