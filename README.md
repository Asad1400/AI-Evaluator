# 🎓 Automated Evaluation of Descriptive Answers

A full-stack application for automated evaluation of student answers using Natural Language Processing (NLP) techniques. Built with FastAPI (backend) and React + Vite (frontend).

## 📋 Project Overview

This system assists teachers in grading subjective answers by providing data-driven evaluation signals through:
- **Rubric Matching**: LLM-based analysis of concept coverage
- **Semantic Similarity**: Measuring answer quality against model answers
- **Consistency Check**: Detecting contradictions using NLI models
- **Score Aggregation**: Weighted combination of all metrics

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────┐
│              Student Answer Input               │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │  Text Preprocessing │
        └──────────┬──────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼───┐    ┌────▼────┐    ┌───▼────┐
│Rubric │    │Semantic │    │  NLI   │
│Matcher│    │Analyzer │    │Analyzer│
│(FLAN) │    │(SentTr) │    │ (BART) │
└───┬───┘    └────┬────┘    └───┬────┘
    │             │              │
    └──────────┬──┴──────────────┘
               │
        ┌──────▼──────┐
        │ Aggregator  │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │Final Score  │
        │  Feedback   │
        └─────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the server:
```bash
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

**Note**: On first run, the system will download NLP models (~1GB). This is a one-time process.

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🎯 Usage

1. **Start both servers** (backend and frontend)
2. **Open browser** to `http://localhost:5173`
3. **Fill in the evaluation form**:
   - Question statement
   - Rubrics (comma-separated key points)
   - Model/correct answer
   - Student answer
   - Total marks
4. **Click "Evaluate Answer"**
5. **Review results** including:
   - Suggested grade
   - Score breakdown (rubric, semantic, NLI)
   - Rubric coverage analysis
   - Detailed feedback

### Sample Data

Click the **"Load Sample Data"** button to populate the form with example data.

## 🧠 NLP Models Used

| Component | Model | Purpose |
|-----------|-------|---------|
| Rubric Matching | `google/flan-t5-base` | Analyze concept coverage |
| Semantic Similarity | `sentence-transformers/all-MiniLM-L6-v2` | Measure answer quality |
| Contradiction Detection | `facebook/bart-large-mnli` | Detect inconsistencies |

## 📊 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Main Endpoint

**POST** `/evaluate`

**Request Body**:
```json
{
  "question": "Explain machine learning",
  "rubrics": ["Definition", "Types", "Applications"],
  "correct_answer": "Machine learning is...",
  "student_answer": "ML allows computers...",
  "total_marks": 10.0
}
```

**Response**:
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

## 🎨 Features

✅ **Multi-dimensional Evaluation**
- Rubric-based concept coverage
- Semantic understanding
- Contradiction detection

✅ **Modern UI/UX**
- Dark theme with glassmorphism
- Animated progress bars
- Responsive design
- Real-time backend status

✅ **Comprehensive Feedback**
- Detailed score breakdown
- Concept coverage analysis
- Actionable suggestions

## 📁 Project Structure

```
Data Science Project/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # Pydantic models
│   │   ├── services/
│   │   │   ├── rubric_matcher.py
│   │   │   ├── semantic_analyzer.py
│   │   │   ├── nli_analyzer.py
│   │   │   └── score_aggregator.py
│   │   └── utils/
│   │       └── text_preprocessing.py
│   ├── requirements.txt
│   └── README.md
└── frontend/
    ├── src/
    │   ├── components/
    │   │   ├── EvaluationForm.jsx
    │   │   └── ResultsDisplay.jsx
    │   ├── services/
    │   │   └── api.js
    │   ├── App.jsx
    │   └── App.css
    ├── package.json
    └── index.html
```

## 🔧 Configuration

Backend weights can be adjusted in `backend/app/main.py`:
```python
ScoreAggregator(
    rubric_weight=0.5,    # 50%
    semantic_weight=0.3,  # 30%
    nli_weight=0.2        # 20%
)
```

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.8+ is installed
- Check if port 8000 is available
- Verify all dependencies are installed

### Frontend shows "Backend Disconnected"
- Ensure backend is running on port 8000
- Check CORS configuration in `backend/app/main.py`

### Models downloading slowly
- First run downloads ~1GB of models
- Ensure stable internet connection
- Models are cached after first download

## 👥 Team

**DS-312 Application of Data Science**
- Ahmad Shahzad (221400077)
- Muhammad Asadullah (221400089)
- Zerlish Burhan (221400111)

## 📄 License

This project is created for educational purposes as part of DS-312 course.

## 🙏 Acknowledgments

- Hugging Face for NLP models
- FastAPI framework
- React and Vite teams
