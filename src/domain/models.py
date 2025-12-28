from dataclasses import dataclass


@dataclass(frozen=True)
class AnalyzeRequest:
    text: str
    prompt_name: str


@dataclass(frozen=True)
class AnalyzeResponse:
    prompt_name: str
    prompt: str
    input_text: str
    message_for_model: str

    def to_dict(self) -> dict:
        return {
            "prompt_name": self.prompt_name,
            "prompt": self.prompt,
            "input_text": self.input_text,
            "message_for_model": self.message_for_model,
        }
