# Video-based Scenario & Test Case Generator

Automatically generate **test scenarios** and **test cases** from a video file using a multimodal LLM (OpenAI GPT-4o or Google Gemini).

## How it works

```
Video file
    │
    ▼
[VideoProcessor]  ──  samples N frames (configurable fps / max frames)
    │
    ▼
[ScenarioGenerator]  ──  sends frames to LLM → structured test scenarios
    │
    ▼
[TestCaseWriter]  ──  sends each scenario to LLM → detailed test cases
    │
    ▼
Output: Markdown report or JSON
```

## Project structure

```
.
├── src/
│   ├── main.py               # CLI entry point
│   ├── models.py             # Pydantic data models (Scenario, TestCase, …)
│   ├── video_processor.py    # Frame extraction with OpenCV
│   ├── llm_client.py         # Provider-agnostic LLM wrapper (OpenAI / Gemini)
│   ├── scenario_generator.py # Generate scenarios from video frames
│   ├── test_case_writer.py   # Generate test cases from scenarios
│   └── output_formatter.py   # Format results as Markdown or JSON
├── tests/                    # Pytest unit tests
├── requirements.txt
├── pyproject.toml
└── .env.example
```

## Setup

```bash
# 1. Clone and create a virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your LLM credentials
cp .env.example .env
# Edit .env and set OPENAI_API_KEY (or GOOGLE_API_KEY for Gemini)
```

## Usage

```bash
# Basic usage (OpenAI GPT-4o, Markdown output to stdout)
python -m src.main --video path/to/demo.mp4

# Use Gemini instead
python -m src.main --video demo.mp4 --provider gemini

# Add context to guide the LLM
python -m src.main --video demo.mp4 --context "E-commerce checkout flow demo"

# Save output to a file
python -m src.main --video demo.mp4 --output report.md

# Export as JSON
python -m src.main --video demo.mp4 --format json --output result.json

# Generate scenarios only (skip test case writing)
python -m src.main --video demo.mp4 --skip-test-cases

# Control frame sampling
python -m src.main --video demo.mp4 --fps 0.5 --max-frames 30
```

### All options

| Option | Default | Description |
|---|---|---|
| `--video` | *required* | Path to the input video file |
| `--context` | _(empty)_ | Free-text description to guide the LLM |
| `--provider` | `openai` | LLM provider: `openai` or `gemini` |
| `--model` | provider default | LLM model name |
| `--fps` | `1` | Frames per second to sample |
| `--max-frames` | `50` | Max frames sent to the LLM |
| `--output` | stdout | Output file path |
| `--format` | `markdown` | `markdown` or `json` |
| `--skip-test-cases` | false | Skip test case generation |

## Environment variables

All settings can also be controlled via environment variables (see `.env.example`):

| Variable | Description |
|---|---|
| `LLM_PROVIDER` | `openai` or `gemini` |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `OPENAI_MODEL` | OpenAI model name (default: `gpt-4o`) |
| `GOOGLE_API_KEY` | Your Google AI API key |
| `GEMINI_MODEL` | Gemini model name (default: `gemini-1.5-pro`) |
| `FRAMES_PER_SECOND` | Frames to sample per second (default: `1`) |
| `MAX_FRAMES` | Max frames to send to LLM (default: `50`) |
| `FRAME_WIDTH` | Frame resize width in pixels (default: `1280`) |

## Running tests

```bash
pytest tests/ -v
```

## Output example

```markdown
# Video Analysis Report

**Video:** `demo.mp4`
**Duration:** 45.0s
**Frames analysed:** 30

## Summary
Analysed 30 frames; identified 3 scenario(s).

---

## S-001: User Login

**Description:** A registered user logs in with valid credentials.

**Steps:**
1. Open the application
2. Enter username and password
3. Click the Login button

**Expected outcome:** User is redirected to the dashboard.

### Test Cases

#### TC-001: Login with valid credentials
- **Priority:** High
| Step | Action | Expected Result |
|------|--------|-----------------|
| 1 | Open the app | Login page is displayed |
| 2 | Enter valid credentials | Fields are populated |
| 3 | Click Login | Dashboard is shown |

**Expected outcome:** User is successfully logged in.
```
