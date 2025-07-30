import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Configure axios to include credentials for session management
axios.defaults.withCredentials = true;

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

// Request interceptor to add auth headers if needed
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Don't redirect, let the App component handle auth state
      console.log('Authentication failed, will be handled by App component');
    }
    return Promise.reject(error);
  }
);

export const authService = {
  async login(credentials) {
    const response = await api.post('/api/login', credentials);
    return response.data;
  },

  async logout() {
    const response = await api.post('/api/logout');
    return response.data;
  },

  async checkAuthStatus() {
    const response = await api.get('/api/auth-status');
    return response.data;
  },

  async testSession() {
    const response = await api.get('/api/test-session');
    return response.data;
  },
};

export const emailService = {
  async processEmails(timeWindow = null) {
    const payload = {};
    if (timeWindow) {
      payload.start_date = timeWindow.startDate;
      payload.end_date = timeWindow.endDate;
    }
    const response = await api.post('/api/process-emails', payload);
    return response.data;
  },
};

export const bankService = {
  async uploadStatement(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/api/upload-bank-statement', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export const ledgerService = {
  async getTransactions() {
    const response = await api.get('/api/ledger');
    return response.data;
  },
};

export const healthService = {
  async checkHealth() {
    const response = await api.get('/api/health');
    return response.data;
  },
};

export default api; 