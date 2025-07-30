import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? `${window.location.origin}/api` 
    : 'http://localhost:5000');

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const emailService = {
  processEmails: async (startDate = null, endDate = null) => {
    const payload = {};
    if (startDate) payload.start_date = startDate;
    if (endDate) payload.end_date = endDate;
    
    const response = await api.post('/api/process-emails', payload);
    return response.data;
  },
};

export const bankService = {
  uploadStatement: async (file) => {
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
  getTransactions: async () => {
    const response = await api.get('/api/ledger');
    return response.data;
  },
};

export const healthService = {
  checkHealth: async () => {
    const response = await api.get('/api/health');
    return response.data;
  },
};

export default api; 