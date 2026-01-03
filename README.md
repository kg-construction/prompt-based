# Prompt-based Knowledge Graph Construction API

Small Flask API that accepts text, pairs it with a few-shot prompt, and prepares it for downstream knowledge-graph extraction. The project ships with ready-to-use prompts and simple utilities to load them.

## Project Layout
- `src/` - Flask API following a simple DDD layering
- `prompt/system/` - System prompts (LLM behavior/constraints).
- `prompt/prompts/` - Few-shot prompt templates (include `${USER_TEXT}` placeholder).
- `tests/` - Pytest suite for services and controllers.
