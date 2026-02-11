# Automated Evaluation System - Backend

FastAPI backend for automated evaluation of descriptive answers using NLP.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### POST /evaluate
Evaluate a student answer

**Request Body:**
```json
{
  "question": "Explain machine learning",
  "rubrics": ["Definition", "Types", "Applications"],
  "correct_answer": "Machine learning is...",
  "student_answer": "ML allows computers to learn...",
  "total_marks": 10.0
}
```

**Response:**
```json
{
  "scores": {
    "rubric_score": 0.75,
    "semantic_score": 0.82,
    "nli_score": 0.90,
    "final_score": 0.80
  },
  "suggested_grade": 8.0,
  "total_marks": 10.0,
  "percentage": 80.0,
  "feedback": "...",
  "rubric_analysis": {...}
}
```

## Models Used

- **Rubric Matching**: google/flan-t5-base
- **Semantic Similarity**: sentence-transformers/all-MiniLM-L6-v2
- **NLI/Contradiction**: facebook/bart-large-mnli

Models will download automatically on first run (~1GB total).
