import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const evaluateAnswer = async (evaluationData) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/evaluate`, evaluationData);
    return response.data;
  } catch (error) {
    if (error.response) {
      throw new Error(error.response.data.detail || 'Evaluation failed');
    } else if (error.request) {
      throw new Error('Cannot connect to server. Please ensure the backend is running.');
    } else {
      throw new Error('An unexpected error occurred');
    }
  }
};

export const checkHealth = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
  } catch (error) {
    throw new Error('Backend server is not responding');
  }
};
