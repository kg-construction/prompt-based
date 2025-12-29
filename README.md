# Prompt-based Knowledge Graph Construction API

Small Flask API that accepts text, pairs it with a few-shot prompt, and prepares it for downstream knowledge-graph extraction. The project ships with ready-to-use prompts and simple utilities to load them.

## Requirements
- Python >=3.10

## Setup

### 1. Install Python Dependencies

#### Linux / macOS (bash)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Windows (PowerShell)
```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

### 2. Install and Configure Ollama

#### Install Ollama:
- **Windows/Mac**: Download from [https://ollama.ai](https://ollama.ai)

#### Download model:
```bash
ollama pull llama3:8b
```

#### Run model
```
ollama run llama3:8b
```

#### Verify Ollama is running:
```bash
ollama serve
```

## Running the API
```bash
python -m src.app
```
The service listens on `http://127.0.0.1:5000`.

### Environment configuration
- `.env` is loaded automatically. 
- `DEFAULT_PROMPT_NAME` switches the default prompt template file (default: `prompts/knowledge_graph_prompt.txt`).
- `DEFAULT_SYSTEM_PROMPT_NAME` switches the system prompt file (default: `system/knowledge_graph_system.txt`).
- `OLLAMA_API_URL` points to the text-generation endpoint (default: `http://localhost:11434/api/generate` to satisfy the requested integration).
- `OLLAMA_MODEL` picks the model used in the payload (default: `llama3:8b` as requested).
- `OLLAMA_TIMEOUT_SECONDS` limits outbound requests (default: `30` to fail fast while allowing local inference time).
- `OLLAMA_CSV_PATH` stores model responses as CSV (default: `data/ollama_responses.csv` so outputs stay versioned outside `prompt/`).
- Requests set `stream: false` so the service receives a single JSON object instead of the default streaming token feed (avoids `Invalid JSON response` errors and keeps CSV logging simple).
- Generation options (all optional; blanks are ignored): `OLLAMA_SEED`, `OLLAMA_TEMPERATURE` (default `0.2` to bias toward deterministic graph output), `OLLAMA_TOP_K`, `OLLAMA_TOP_P`, `OLLAMA_MIN_P`, `OLLAMA_STOP`, `OLLAMA_NUM_CTX`, `OLLAMA_NUM_PREDICT`.

## Endpoints
- `POST /analyze`
  - Body: `{"text": "<your text>", "prompt_name": "prompts/knowledge_graph_prompt.txt", "system_prompt_name": "system/knowledge_graph_system.txt"}` (`prompt_name` and `system_prompt_name` optional; both default from `.env`).
  - Flow: loads the system prompt (from `prompt/system/`) and the prompt template (from `prompt/prompts/`), builds the message (few-shots + user text), calls `OLLAMA_API_URL` with `{model, system, prompt, options}` (`model` defaults to `llama3:8b`; `system` is the loaded system prompt file; `prompt` is the assembled message; `options` come from the `OLLAMA_*` variables), saves the returned payload to `OLLAMA_CSV_PATH`, and returns both the prompt metadata and the model response.
  - Response includes the resolved prompt text, the assembled `message_for_model`, and the raw generation payload returned by Ollama (see `/api/generate` response schema).

## Project Layout
- `src/` - Flask API following a simple DDD layering
- `prompt/system/` - System prompts (LLM behavior/constraints).
- `prompt/prompts/` - Few-shot prompt templates (include `${USER_TEXT}` placeholder).
- `tests/` - Pytest suite for services and controllers.

## Testing
```bash
python -m pytest 
```
Tests are organized by scope:
- `tests/unit/` for pure function/service tests.
- `tests/controllers/` for Flask blueprints using a test client with stubbed dependencies.
- `tests/infrastructure/` for the Ollama client + CSV logger.
- `tests/integration/` for end-to-end request flows through the app factory, including the mocked generation call and CSV write.
