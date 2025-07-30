import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import EmailProcessing from './pages/EmailProcessing';
import BankComparison from './pages/BankComparison';
import LedgerView from './pages/LedgerView';

function App() {
  return (
    <Box sx={{ display: 'flex' }}>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/emails" element={<EmailProcessing />} />
          <Route path="/bank-comparison" element={<BankComparison />} />
          <Route path="/ledger" element={<LedgerView />} />
        </Routes>
      </Layout>
    </Box>
  );
}

export default App; 