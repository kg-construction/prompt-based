from ..domain.models import AnalyzeRequest, AnalyzeResponse
from ..infrastructure.prompt_repository import PromptRepository


class KnowledgeGraphService:
    def __init__(self, prompt_repository: PromptRepository, default_prompt: str) -> None:
        self.prompt_repository = prompt_repository
        self.default_prompt = default_prompt

    def analyze(self, request: AnalyzeRequest) -> AnalyzeResponse:
        prompt_text = self.prompt_repository.load_prompt(request.prompt_name)
        # If prompt has a placeholder, fill it; otherwise append user text in a chat-style turn.
        if "${USER_TEXT}" in prompt_text:
            message = prompt_text.replace("${USER_TEXT}", request.text)
        else:
            message = f"{prompt_text}\n\nUser: {request.text}\nAssistant:"

        return AnalyzeResponse(
            prompt_name=request.prompt_name,
            prompt=prompt_text,
            input_text=request.text,
            message_for_model=message,
        )

    def get_default_prompt(self) -> str:
        return self.default_prompt
