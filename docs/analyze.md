
# Analyze 

## Endpoints
- `POST /analyze`
  - Body: `{ "text": "<required>", "prompt_name": "<optional>", "system_prompt_name": "<optional>" }`
  - Behavior: loads system + prompt files (overrides if provided), builds the message (replaces `${USER_TEXT}` or appends a chat-style turn), calls Ollama `/api/generate` with `stream:false`, logs response to CSV, and returns prompt metadata + generation payload.
  - Example request:
    ```bash
    curl -X POST http://127.0.0.1:5000/analyze \
      -H "Content-Type: application/json" \
      -d '{"text":"Alice knows Bob."}'
    ```
  - Example response (shape):
    ```json
    {
      "text": "Alice knows Bob.",
      "rdf": "rdf.."
    }
    ```
