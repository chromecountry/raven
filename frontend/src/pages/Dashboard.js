import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Typography,
  Paper,
  CircularProgress,
  Alert,
} from '@mui/material';
import AnimatedCard from '../components/AnimatedCard';
import {
  Email as EmailIcon,
  Receipt as ReceiptIcon,
  AccountBalance as BankIcon,
  TrendingUp as TrendingIcon,
} from '@mui/icons-material';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { ledgerService, healthService } from '../services/api';

const COLORS = ['#7c3aed', '#8b5cf6', '#a855f7', '#c084fc', '#d8b4fe', '#e9d5ff'];

function Dashboard() {
  const [stats, setStats] = useState({
    totalTransactions: 0,
    totalAmount: 0,
    recentTransactions: [],
    health: 'unknown',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [ledgerResponse, healthResponse] = await Promise.all([
        ledgerService.getTransactions(),
        healthService.checkHealth(),
      ]);

      const transactions = ledgerResponse.transactions || [];
      const totalAmount = transactions.reduce((sum, tx) => sum + parseFloat(tx.amount || 0), 0);

      setStats({
        totalTransactions: transactions.length,
        totalAmount,
        recentTransactions: transactions.slice(-5),
        health: healthResponse.status,
      });
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryData = () => {
    const categories = {};
    stats.recentTransactions.forEach(tx => {
      const category = tx.payee || 'Unknown';
      categories[category] = (categories[category] || 0) + parseFloat(tx.amount || 0);
    });
    
    return Object.entries(categories).map(([name, value]) => ({ name, value }));
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Stats Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <AnimatedCard icon={<ReceiptIcon sx={{ fontSize: 32, color: '#ffffff' }} />}>
            <Typography color="textSecondary" gutterBottom>
              Total Transactions
            </Typography>
            <Typography variant="h4" sx={{ fontWeight: 700 }}>
              {stats.totalTransactions}
            </Typography>
          </AnimatedCard>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <AnimatedCard icon={<TrendingIcon sx={{ fontSize: 32, color: '#ffffff' }} />}>
            <Typography color="textSecondary" gutterBottom>
              Total Amount
            </Typography>
            <Typography variant="h4" sx={{ fontWeight: 700 }}>
              ${stats.totalAmount.toFixed(2)}
            </Typography>
          </AnimatedCard>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <AnimatedCard icon={<EmailIcon sx={{ fontSize: 32, color: '#ffffff' }} />}>
            <Typography color="textSecondary" gutterBottom>
              Email Processing
            </Typography>
            <Typography variant="h4" sx={{ fontWeight: 700 }}>
              Active
            </Typography>
          </AnimatedCard>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <AnimatedCard icon={<BankIcon sx={{ fontSize: 32, color: '#ffffff' }} />}>
            <Typography color="textSecondary" gutterBottom>
              System Status
            </Typography>
            <Typography variant="h4" sx={{ fontWeight: 700, color: stats.health === 'healthy' ? '#10b981' : '#ef4444' }}>
              {stats.health}
            </Typography>
          </AnimatedCard>
        </Grid>

        {/* Charts */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Transaction Categories
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={getCategoryData()}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {getCategoryData().map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: 400 }}>
            <Typography variant="h6" gutterBottom>
              Recent Transactions
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={stats.recentTransactions}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="payee" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    border: '1px solid #e2e8f0',
                    borderRadius: 8,
                    boxShadow: '0 4px 12px rgb(0 0 0 / 0.1)',
                  }}
                />
                <Bar dataKey="amount" fill="url(#purpleGradient)" />
                <defs>
                  <linearGradient id="purpleGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#7c3aed" />
                    <stop offset="100%" stopColor="#8b5cf6" />
                  </linearGradient>
                </defs>
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard; 