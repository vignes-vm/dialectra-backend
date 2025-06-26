# Dialectra Backend - AI-Powered Debate Simulator

This repository contains the backend for an AI-powered debate simulator that can generate debates between two AI agents on a given motion.

## Features

- Generate Prime Minister and Leader of Opposition speeches
- Get AI judge verdicts on debates
- Support for multiple LLM backends (OpenAI GPT-4 and Google Gemini)
- CLI and API interfaces

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - For OpenAI: `OPENAI_API_KEY`
   - For Google Gemini: `GOOGLE_API_KEY`

## Running the Application

### CLI Interface

Run the CLI interface with OpenAI:
```
python main.py
```

Run the CLI interface with Google Gemini:
```
python main.py --gemini
```

### FastAPI Server

Run the FastAPI server with default settings (OpenAI, host 0.0.0.0, port 8000):
```
python main.py --api
```

Run the FastAPI server with custom settings:
```
python main.py --api --gemini --host 127.0.0.1 --port 5000
```

## API Endpoints

Once the server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Available Endpoints

- `GET /motions` - Get a list of default debate motions
- `POST /debate` - Create a new debate session with a specified motion
- `GET /debate/{session_id}` - Get the current state of a debate session
- `POST /debate/{session_id}/pm_speech` - Generate the Prime Minister speech
- `POST /debate/{session_id}/lo_speech` - Generate the Leader of Opposition speech
- `POST /debate/{session_id}/judgment` - Generate the AI Judge verdict
- `POST /debate/{session_id}/save` - Save the debate to a file

## Example API Usage

### Create a new debate

```bash
curl -X POST "http://localhost:8000/debate" \
  -H "Content-Type: application/json" \
  -d '{"motion": "This House would ban private education", "llm_type": "openai"}'
```

### Generate a PM speech

```bash
curl -X POST "http://localhost:8000/debate/{session_id}/pm_speech"
```

### Generate an LO speech

```bash
curl -X POST "http://localhost:8000/debate/{session_id}/lo_speech"
```

### Generate a judgment

```bash
curl -X POST "http://localhost:8000/debate/{session_id}/judgment"
```

### Save the debate

```bash
curl -X POST "http://localhost:8000/debate/{session_id}/save"
```

## License

[MIT License](LICENSE)