# AI Market Agent

This repository contains a simple autonomous market intelligence agent built
with FastAPI, LangGraph, and OpenAI. The agent performs a research–analysis–
writing workflow and can be triggered via an HTTP POST request.

## Setup

1. Create a Python virtual environment and activate it:
   ```powershell
   python -m venv venv
   & .\venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Copy the example env file and fill in your keys:
   ```powershell
   copy .env.example .env
   notepad .env  # or edit with your favorite editor
   ```

   - `OPENAI_API_KEY` **must** be a valid *secret* key from your OpenAI account
     (not a project/service key).
   - `TAVILY_API_KEY` and `PINECONE_API_KEY`/`PINECONE_INDEX` are optional;
     the agent will skip those services if they are not provided.

4. (Optional) run the helper script to generate `.env` interactively:
   ```powershell
   .\create_env.ps1
   ```

## Running the server

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API exposes a single endpoint:

```
POST /run-agent
Content-Type: application/json
{
  "query": "<your topic>"
}
```

Response:

```json
{ "report": "<generated text>" }
```

## Development notes

- The project uses `langgraph` to define a state graph. Nodes include
  `researcher`, `analyst`, and `writer`.
- LLM calls are wrapped with error handling; missing API keys result in
  informative messages rather than crashes.
- Environment variables are loaded with `python-dotenv` but do not override
  already-set variables (`override=False`).

## Security / Secrets

- **Never commit your `.env` file** or any API keys. The repository includes a
  `.gitignore` entry for `.env` and `.env.example` should be used for sharing
  configuration templates.
- If a key accidentally leaks, revoke it immediately in the provider's
  dashboard (OpenAI, Pinecone, Tavily).

## Optional enhancements

- Add unit tests using [pytest](https://pytest.org) to validate the graph
  nodes and API.
- Implement mock versions of external services for offline testing.


## Demo

Autonomous AI Research Agent generating intelligence reports.

![AI Agent Demo](demo/demo.gif)