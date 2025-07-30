import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';
import Layout from './components/Layout';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import EmailProcessing from './pages/EmailProcessing';
import BankComparison from './pages/BankComparison';
import LedgerView from './pages/LedgerView';
import { authService } from './services/api';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await authService.checkAuthStatus();
      setAuthenticated(response.authenticated);
    } catch (error) {
      console.log('Auth check failed:', error);
      setAuthenticated(false);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = () => {
    setAuthenticated(true);
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setAuthenticated(false);
    }
  };

  // Handle authentication failures from API calls
  const handleAuthFailure = () => {
    setAuthenticated(false);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <div>Loading...</div>
      </Box>
    );
  }

  if (!authenticated) {
    return <Login onLogin={handleLogin} />;
  }

  return (
    <Box sx={{ display: 'flex' }}>
      <Layout onLogout={handleLogout}>
        <Routes>
          <Route path="/" element={<Dashboard onAuthFailure={handleAuthFailure} />} />
          <Route path="/emails" element={<EmailProcessing onAuthFailure={handleAuthFailure} />} />
          <Route path="/bank-comparison" element={<BankComparison onAuthFailure={handleAuthFailure} />} />
          <Route path="/ledger" element={<LedgerView onAuthFailure={handleAuthFailure} />} />
          <Route path="/login" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Box>
  );
}

export default App; 