#  How to run

## Environment variables
Defaults from `.env`:
- `DEFAULT_PROMPT_NAME=prompts/few-shot.txt`
- `DEFAULT_SYSTEM_PROMPT_NAME=system/knowledge_graph.txt`
- `OLLAMA_API_URL=http://localhost:11434`
- `OLLAMA_MODEL=llama3:8b`
- `OLLAMA_CSV_PATH=data/ollama_responses.csv`
- Generation options (all optional; blanks ignored): `OLLAMA_SEED`, `OLLAMA_TEMPERATURE`, `OLLAMA_TOP_K`, `OLLAMA_TOP_P`, `OLLAMA_MIN_P`, `OLLAMA_STOP`, `OLLAMA_NUM_CTX`, `OLLAMA_NUM_PREDICT`.


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
