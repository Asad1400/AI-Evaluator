import './ResultsDisplay.css';

const ResultsDisplay = ({ results }) => {
  if (!results) return null;

  const { scores, suggested_grade, total_marks, percentage, feedback, rubric_analysis } = results;

  const getGradeColor = (percentage) => {
    if (percentage >= 85) return '#4ade80';
    if (percentage >= 70) return '#60a5fa';
    if (percentage >= 55) return '#fbbf24';
    if (percentage >= 40) return '#fb923c';
    return '#f87171';
  };

  const getScoreLabel = (score) => {
    if (score >= 0.85) return 'Excellent';
    if (score >= 0.70) return 'Good';
    if (score >= 0.55) return 'Satisfactory';
    if (score >= 0.40) return 'Fair';
    return 'Needs Improvement';
  };

  return (
    <div className="results-display">
      <div className="results-header">
        <h2>📊 Evaluation Results</h2>
      </div>

      {/* Main Grade Display */}
      <div className="grade-card" style={{ borderColor: getGradeColor(percentage) }}>
        <div className="grade-label">Suggested Grade</div>
        <div className="grade-value" style={{ color: getGradeColor(percentage) }}>
          {suggested_grade.toFixed(2)} / {total_marks}
        </div>
        <div className="percentage">{percentage.toFixed(1)}%</div>
      </div>

      {/* Score Breakdown */}
      <div className="scores-section">
        <h3>Score Breakdown</h3>
        
        <div className="score-item">
          <div className="score-header">
            <span className="score-name">📋 Rubric Coverage</span>
            <span className="score-value">{(scores.rubric_score * 100).toFixed(1)}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill rubric"
              style={{ width: `${scores.rubric_score * 100}%` }}
            ></div>
          </div>
          <div className="score-label-text">{getScoreLabel(scores.rubric_score)}</div>
        </div>

        <div className="score-item">
          <div className="score-header">
            <span className="score-name">🎯 Semantic Similarity</span>
            <span className="score-value">{(scores.semantic_score * 100).toFixed(1)}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill semantic"
              style={{ width: `${scores.semantic_score * 100}%` }}
            ></div>
          </div>
          <div className="score-label-text">{getScoreLabel(scores.semantic_score)}</div>
        </div>

        <div className="score-item">
          <div className="score-header">
            <span className="score-name">✓ Consistency Check</span>
            <span className="score-value">{(scores.nli_score * 100).toFixed(1)}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill nli"
              style={{ width: `${scores.nli_score * 100}%` }}
            ></div>
          </div>
          <div className="score-label-text">{getScoreLabel(scores.nli_score)}</div>
        </div>

        <div className="score-item final">
          <div className="score-header">
            <span className="score-name">⭐ Final Score</span>
            <span className="score-value">{(scores.final_score * 100).toFixed(1)}%</span>
          </div>
          <div className="progress-bar">
            <div 
              className="progress-fill final"
              style={{ width: `${scores.final_score * 100}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Rubric Analysis */}
      <div className="rubric-analysis">
        <h3>Rubric Analysis</h3>
        
        {rubric_analysis.covered_concepts.length > 0 && (
          <div className="concept-group covered">
            <div className="concept-header">✅ Covered Concepts ({rubric_analysis.covered_concepts.length})</div>
            <div className="concept-list">
              {rubric_analysis.covered_concepts.map((concept, idx) => (
                <span key={idx} className="concept-tag">{concept}</span>
              ))}
            </div>
          </div>
        )}

        {rubric_analysis.partial_concepts && rubric_analysis.partial_concepts.length > 0 && (
          <div className="concept-group partial">
            <div className="concept-header">⚠️ Partially Covered ({rubric_analysis.partial_concepts.length})</div>
            <div className="concept-list">
              {rubric_analysis.partial_concepts.map((concept, idx) => (
                <span key={idx} className="concept-tag">{concept}</span>
              ))}
            </div>
          </div>
        )}

        {rubric_analysis.missing_concepts.length > 0 && (
          <div className="concept-group missing">
            <div className="concept-header">❌ Missing Concepts ({rubric_analysis.missing_concepts.length})</div>
            <div className="concept-list">
              {rubric_analysis.missing_concepts.map((concept, idx) => (
                <span key={idx} className="concept-tag">{concept}</span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Detailed Feedback */}
      <div className="feedback-section">
        <h3>Detailed Feedback</h3>
        <div className="feedback-content">
          {feedback.split('\n').map((line, idx) => (
            <p key={idx}>{line}</p>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;
