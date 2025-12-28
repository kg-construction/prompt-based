# Prompt-based Knowledge Graph Construction API

Small Flask API that accepts text, pairs it with a few-shot prompt, and prepares it for downstream knowledge-graph extraction. The project ships with ready-to-use prompts and simple utilities to load them.

## Requirements
- Python >=3.10

## Setup

### Linux / macOS (bash)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

## Running the API
```bash
python -m src.app
```
The service listens on `http://127.0.0.1:5000`.

### Environment configuration
- `.env` is loaded automatically. 
- Set `DEFAULT_PROMPT_NAME` to switch the default prompt without code changes (default: `knowledge_graph_prompt.txt`).

## Endpoints
- `POST /analyze`
  - Body: `{"text": "<your text>", "prompt_name": "knowledge_graph_prompt.txt"}` (`prompt_name` optional; defaults to the shipped prompt).
  - Response includes the resolved prompt text and a stub payload showing where model integration would occur.

## Project Layout
- `src/` - Flask API following a simple DDD layering
- `prompt/` - Few-shot prompts for knowledge-graph construction.
- `tests/` - Pytest suite for services and controllers.

## Testing
```bash
python -m pytest 
```
Tests are organized by scope:
- `tests/unit/` for pure function/service tests.
- `tests/controllers/` for Flask blueprints using a test client with stubbed dependencies.
- `tests/integration/` for end-to-end request flows through the app factory.
