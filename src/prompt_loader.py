from pathlib import Path

# Base directory = repository root (src/..)
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_DIR = BASE_DIR / "prompt"


def load_prompt(prompt_name: str) -> str:
    """
    Read a prompt file from the prompt directory, preventing path traversal.
    """
    prompt_path = (PROMPT_DIR / prompt_name).resolve()
    if PROMPT_DIR not in prompt_path.parents:
        raise ValueError(f"Prompt path {prompt_name!r} is outside the prompt directory.")

    if not prompt_path.is_file():
        raise FileNotFoundError(f"Prompt {prompt_name!r} not found at {prompt_path}.")

    return prompt_path.read_text(encoding="utf-8").strip()
