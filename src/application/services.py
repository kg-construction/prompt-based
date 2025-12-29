from typing import Optional

from ..domain.models import AnalyzeRequest, AnalyzeResponse
from ..infrastructure.ollama_client import OllamaClient
from ..infrastructure.prompt_repository import PromptRepository


class KnowledgeGraphService:
    def __init__(
        self,
        prompt_repository: PromptRepository,
        default_prompt: str,
        default_system_prompt: str,
        ollama_client: Optional[OllamaClient] = None,
    ) -> None:
        self.prompt_repository = prompt_repository
        self.default_prompt = default_prompt
        self.default_system_prompt = default_system_prompt
        self.ollama_client = ollama_client

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        prompt_name = request.prompt_name or self.default_prompt
        system_prompt_name = request.system_prompt_name or self.default_system_prompt

        system_prompt_text = self.prompt_repository.load_prompt(system_prompt_name)
        prompt_text = self.prompt_repository.load_prompt(prompt_name)

        # If prompt has a placeholder, fill it; otherwise append user text in a chat-style turn.
        if "${USER_TEXT}" in prompt_text:
            message = prompt_text.replace("${USER_TEXT}", request.text)
        else:
            message = f"{prompt_text}\n\nUser: {request.text}\nAssistant:"

        generation_response = None
        if self.ollama_client:
            generation_response = self.ollama_client.generate(
                system_prompt=system_prompt_text,
                prompt=message,
                prompt_name=prompt_name,
                input_text=request.text,
            )

        return AnalyzeResponse(
            prompt_name=prompt_name,
            system_prompt_name=system_prompt_name,
            prompt=prompt_text,
            input_text=request.text,
            message_for_model=message,
            generation=generation_response,
        )

    def get_default_prompt(self) -> str:
        return self.default_prompt

    def get_default_system_prompt(self) -> str:
        return self.default_system_prompt
