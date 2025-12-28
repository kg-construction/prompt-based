from pathlib import Path

import pytest

from src.application.services import KnowledgeGraphService
from src.domain.models import AnalyzeRequest
from src.infrastructure.prompt_repository import PromptRepository


class DummyPromptRepo(PromptRepository):
    def __init__(self, prompt_text: str):
        super().__init__(prompt_dir=Path("unused"))
        self.prompt_text = prompt_text

    def load_prompt(self, prompt_name: str) -> str:  # type: ignore[override]
        return self.prompt_text


def test_analyze_builds_payload():
    repo = DummyPromptRepo(prompt_text="Example Prompt")
    service = KnowledgeGraphService(repo, default_prompt="example.txt")
    request = AnalyzeRequest(text="Hello world", prompt_name="example.txt")

    response = service.analyze(request)

    assert response.prompt_name == "example.txt"
    assert response.prompt == "Example Prompt"
    assert response.input_text == "Hello world"
    assert "User: Hello world" in response.message_for_model
    assert response.message_for_model.startswith("Example Prompt")


def test_default_prompt_exposed():
    repo = DummyPromptRepo(prompt_text="Prompt")
    service = KnowledgeGraphService(repo, default_prompt="default.txt")

    assert service.get_default_prompt() == "default.txt"


def test_analyze_replaces_placeholder():
    repo = DummyPromptRepo(prompt_text="Prompt with ${USER_TEXT} inside")
    service = KnowledgeGraphService(repo, default_prompt="example.txt")
    request = AnalyzeRequest(text="Hello", prompt_name="example.txt")

    response = service.analyze(request)

    assert response.message_for_model == "Prompt with Hello inside"
