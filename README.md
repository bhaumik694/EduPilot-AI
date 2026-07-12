# EduPilot AI

A multi-agent LLM pipeline that generates grade-appropriate educational content — explanations and quizzes — then automatically reviews and refines it before it ever reaches a student.

Built around a **Generator → Reviewer → Refiner** architecture: one agent drafts the content, a second agent critiques it against educational standards, and if it doesn't pass, a third pass refines it using that feedback.

## How it works

```
   ┌────────────┐        ┌────────────┐        ┌────────────┐
   │  Generator  │ ─────▶ │  Reviewer   │ ─────▶ │  Refiner    │
   │   Agent     │        │   Agent     │  fail  │   Agent     │
   └────────────┘        └─────┬──────┘        └────────────┘
                                │ pass
                                ▼
                        Final content
```

1. **Generator agent** — takes a `topic` and `grade` level and produces a structured explanation plus a set of multiple-choice questions.
2. **Reviewer agent** — evaluates the generated content against grade-appropriateness and quality criteria, returning a `pass`/`fail` status with structured feedback.
3. **Refiner agent** — if the review fails, re-generates the content using the reviewer's feedback, producing an improved version.

All agent outputs are structured (JSON), not free text, so the pipeline can be consumed programmatically by any frontend.

## Features

- 🧠 **Multi-agent pipeline** — separate generation, review, and refinement stages instead of a single uncontrolled LLM call
- 🎯 **Grade-aware prompting** — content is tailored to a specific grade level (1–10)
- ✅ **Automated quality gate** — a reviewer agent checks the output before it's considered final
- 🔁 **Iterative refinement** — failed content is automatically improved, not just flagged
- 📋 **Structured outputs** — explanations and MCQs (with answers) returned as clean JSON via Pydantic models
- 🖥️ **FastAPI backend + Streamlit frontend** — a working demo UI out of the box

## Tech stack

| Layer       | Tech |
|-------------|------|
| Backend     | [FastAPI](https://fastapi.tiangolo.com/), [Pydantic](https://docs.pydantic.dev/) |
| LLM         | [Groq](https://groq.com/) (LLM inference API) |
| Frontend    | [Streamlit](https://streamlit.io/) |
| Config      | `python-dotenv` |
| HTTP client | `requests` |

## Project structure

```
EduPilot-AI/
├── backend/          # FastAPI app + agent pipeline (generator, reviewer, refiner)
├── frontend/          # Streamlit UI
├── tests/             # Test suite
├── groq_test.py        # Standalone script to sanity-check the Groq API connection
└── requirements.txt
```

## Getting started

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/keys)

### 1. Clone and install

```bash
git clone https://github.com/bhaumik694/EduPilot-AI.git
cd EduPilot-AI
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Run the backend

```bash
uvicorn backend.main:app --reload --port 8000
```

### 4. Run the frontend

In a separate terminal:

```bash
streamlit run frontend/app.py
```

The Streamlit app expects the backend to be running at `http://127.0.0.1:8000`.

## API

### `POST /generate`

Generates, reviews, and (if needed) refines educational content for a given topic and grade.

**Request body**

```json
{
  "grade": 5,
  "topic": "Photosynthesis"
}
```

**Response**

```json
{
  "initial_output": {
    "explanation": "...",
    "mcqs": [
      {
        "question": "What do plants need to make food?",
        "options": ["Sunlight, water, and CO2", "Only water", "Only sunlight", "Soil alone"],
        "answer": "Sunlight, water, and CO2"
      }
    ]
  },
  "review": {
    "status": "pass",
    "feedback": []
  },
  "refined_output": null
}
```

If `review.status` is `"fail"`, `review.feedback` contains the reviewer's notes and `refined_output` will contain the improved explanation and quiz, following the same shape as `initial_output`.

## Running tests

```bash
pytest tests/
```

## Roadmap ideas

- [ ] Support additional content types (worksheets, lesson plans, flashcards)
- [ ] Configurable review criteria per subject
- [ ] Persist generated content to a database
- [ ] Auth for multi-user / classroom use

## Contributing

Issues and pull requests are welcome. If you're adding a new agent stage or content type, please include a test under `tests/`.

## License

No license file is currently included in this repository — add one (MIT is a common default for projects like this) to clarify how others can use the code.
