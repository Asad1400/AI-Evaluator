import { useState } from 'react';
import EvaluationForm from './components/EvaluationForm';
import ResultsDisplay from './components/ResultsDisplay';
import { evaluateAnswer, checkHealth } from './services/api';
import './App.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState('checking');

  // Check backend health on mount
  useState(() => {
    checkHealth()
      .then(() => setBackendStatus('connected'))
      .catch(() => setBackendStatus('disconnected'));
  }, []);

  const handleEvaluate = async (evaluationData) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await evaluateAnswer(evaluationData);
      setResults(response);
      setBackendStatus('connected');
      
      // Scroll to results
      setTimeout(() => {
        document.getElementById('results-section')?.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        });
      }, 100);
    } catch (err) {
      setError(err.message);
      if (err.message.includes('connect')) {
        setBackendStatus('disconnected');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Background Elements */}
      <div className="bg-gradient-1"></div>
      <div className="bg-gradient-2"></div>
      <div className="bg-gradient-3"></div>

      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <h1>🎓 Automated Answer Evaluation System</h1>
          <p className="subtitle">AI-Powered Descriptive Answer Assessment using NLP</p>
          <div className="status-indicator">
            <span className={`status-dot ${backendStatus}`}></span>
            <span className="status-text">
              {backendStatus === 'connected' ? 'Backend Connected' : 
               backendStatus === 'disconnected' ? 'Backend Disconnected' : 
               'Checking...'}
            </span>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="app-main">
        <div className="container">
          {/* Backend Disconnected Warning */}
          {backendStatus === 'disconnected' && (
            <div className="alert alert-error">
              <span className="alert-icon">⚠️</span>
              <div>
                <strong>Backend Server Not Running</strong>
                <p>Please start the FastAPI backend server at http://localhost:8000</p>
              </div>
            </div>
          )}

          {/* Error Display */}
          {error && (
            <div className="alert alert-error">
              <span className="alert-icon">❌</span>
              <div>
                <strong>Evaluation Error</strong>
                <p>{error}</p>
              </div>
            </div>
          )}

          {/* Evaluation Form */}
          <section className="section">
            <EvaluationForm onSubmit={handleEvaluate} loading={loading} />
          </section>

          {/* Results Section */}
          {results && (
            <section className="section" id="results-section">
              <ResultsDisplay results={results} />
            </section>
          )}

          {/* Info Section */}
          {!results && !loading && (
            <section className="info-section">
              <div className="info-card">
                <h3>📋 How It Works</h3>
                <ol>
                  <li><strong>Rubric Matching:</strong> Analyzes concept coverage using LLM (FLAN-T5)</li>
                  <li><strong>Semantic Similarity:</strong> Measures answer quality using sentence transformers</li>
                  <li><strong>Consistency Check:</strong> Detects contradictions using NLI models</li>
                  <li><strong>Score Aggregation:</strong> Combines all metrics for final grade suggestion</li>
                </ol>
              </div>

              <div className="info-card">
                <h3>🎯 Features</h3>
                <ul>
                  <li>✓ Multi-dimensional answer evaluation</li>
                  <li>✓ Detailed rubric coverage analysis</li>
                  <li>✓ Semantic understanding of concepts</li>
                  <li>✓ Contradiction detection</li>
                  <li>✓ Comprehensive feedback generation</li>
                </ul>
              </div>
            </section>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <p>DS-312 Application of Data Science | Automated Evaluation System</p>
        <p className="team">Ahmad Shahzad • Muhammad Asadullah • Zerlish Burhan</p>
      </footer>
    </div>
  );
}

export default App;
