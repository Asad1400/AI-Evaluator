import { useState } from 'react';
import './EvaluationForm.css';

const EvaluationForm = ({ onSubmit, loading }) => {
  const [formData, setFormData] = useState({
    question: '',
    rubrics: '',
    correct_answer: '',
    student_answer: '',
    total_marks: 10
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'total_marks' ? parseFloat(value) || 0 : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Convert rubrics from comma-separated string to array
    const rubricsArray = formData.rubrics
      .split(',')
      .map(r => r.trim())
      .filter(r => r.length > 0);
    
    if (rubricsArray.length === 0) {
      alert('Please enter at least one rubric point');
      return;
    }
    
    const evaluationData = {
      ...formData,
      rubrics: rubricsArray
    };
    
    onSubmit(evaluationData);
  };

  const loadSampleData = () => {
    setFormData({
      question: 'Explain the concept of machine learning and its applications.',
      rubrics: 'Definition of machine learning, Types of machine learning, Real-world applications, Examples',
      correct_answer: 'Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. There are three main types: supervised learning (learning from labeled data), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through trial and error). Machine learning is used in various real-world applications such as recommendation systems (Netflix, Spotify), image recognition (face detection, medical imaging), natural language processing (chatbots, translation), and autonomous vehicles.',
      student_answer: 'Machine learning allows computers to learn from data without being programmed. It includes supervised and unsupervised learning. Examples include Netflix recommendations and face recognition in smartphones.',
      total_marks: 10
    });
  };

  return (
    <div className="evaluation-form">
      <div className="form-header">
        <h2>📝 Answer Evaluation</h2>
        <button 
          type="button" 
          onClick={loadSampleData}
          className="sample-btn"
          disabled={loading}
        >
          Load Sample Data
        </button>
      </div>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="question">Question Statement *</label>
          <textarea
            id="question"
            name="question"
            value={formData.question}
            onChange={handleChange}
            required
            rows="3"
            placeholder="Enter the question..."
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="rubrics">Rubrics / Key Points * <span className="hint">(comma-separated)</span></label>
          <textarea
            id="rubrics"
            name="rubrics"
            value={formData.rubrics}
            onChange={handleChange}
            required
            rows="3"
            placeholder="e.g., Definition, Types, Applications, Examples"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="correct_answer">Model / Correct Answer *</label>
          <textarea
            id="correct_answer"
            name="correct_answer"
            value={formData.correct_answer}
            onChange={handleChange}
            required
            rows="5"
            placeholder="Enter the model answer..."
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="student_answer">Student Answer *</label>
          <textarea
            id="student_answer"
            name="student_answer"
            value={formData.student_answer}
            onChange={handleChange}
            required
            rows="5"
            placeholder="Enter the student's response..."
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="total_marks">Total Marks *</label>
          <input
            type="number"
            id="total_marks"
            name="total_marks"
            value={formData.total_marks}
            onChange={handleChange}
            required
            min="0"
            step="0.5"
            disabled={loading}
          />
        </div>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? (
            <>
              <span className="spinner"></span>
              Evaluating...
            </>
          ) : (
            <>
              <span>🚀</span>
              Evaluate Answer
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default EvaluationForm;
