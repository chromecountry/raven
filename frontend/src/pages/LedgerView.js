import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  CircularProgress,
  Alert,
  Card,
  CardContent,
  Grid,
} from '@mui/material';
import {
  Receipt as ReceiptIcon,
  TrendingUp as TrendingIcon,
  CalendarToday as CalendarIcon,
} from '@mui/icons-material';
import { DataGrid } from '@mui/x-data-grid';
import { ledgerService } from '../services/api';

const columns = [
  {
    field: 'date',
    headerName: 'Date',
    width: 120,
    valueFormatter: (params) => {
      if (!params.value) return '';
      return new Date(params.value).toLocaleDateString();
    },
  },
  {
    field: 'payee',
    headerName: 'Merchant',
    width: 200,
    flex: 1,
  },
  {
    field: 'amount',
    headerName: 'Amount',
    width: 120,
    type: 'number',
    valueFormatter: (params) => {
      if (!params.value) return '';
      return `$${parseFloat(params.value).toFixed(2)}`;
    },
  },
  {
    field: 'currency',
    headerName: 'Currency',
    width: 100,
  },
];

function LedgerView() {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    totalTransactions: 0,
    totalAmount: 0,
    averageAmount: 0,
  });

  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const response = await ledgerService.getTransactions();
      
      const txData = response.transactions || [];
      const rows = txData.map((tx, index) => ({
        id: index,
        ...tx,
      }));
      
      setTransactions(rows);
      
      // Calculate stats
      const totalAmount = txData.reduce((sum, tx) => sum + parseFloat(tx.amount || 0), 0);
      const averageAmount = txData.length > 0 ? totalAmount / txData.length : 0;
      
      setStats({
        totalTransactions: txData.length,
        totalAmount,
        averageAmount,
      });
    } catch (err) {
      setError('Failed to load ledger transactions');
      console.error('Ledger error:', err);
    } finally {
      setLoading(false);
    }
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
        Ledger View
      </Typography>
      
      <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
        View all processed transactions from email receipts
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Stats Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <ReceiptIcon color="primary" sx={{ mr: 2, fontSize: 40 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Transactions
                  </Typography>
                  <Typography variant="h4">
                    {stats.totalTransactions}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <TrendingIcon color="secondary" sx={{ mr: 2, fontSize: 40 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Total Amount
                  </Typography>
                  <Typography variant="h4">
                    ${stats.totalAmount.toFixed(2)}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <CalendarIcon color="success" sx={{ mr: 2, fontSize: 40 }} />
                <Box>
                  <Typography color="textSecondary" gutterBottom>
                    Average Amount
                  </Typography>
                  <Typography variant="h4">
                    ${stats.averageAmount.toFixed(2)}
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Transactions Table */}
      <Paper sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={transactions}
          columns={columns}
          pageSize={10}
          rowsPerPageOptions={[10, 25, 50]}
          disableSelectionOnClick
          loading={loading}
          sx={{
            '& .MuiDataGrid-cell': {
              borderBottom: '1px solid #e0e0e0',
            },
            '& .MuiDataGrid-columnHeaders': {
              backgroundColor: '#f5f5f5',
              borderBottom: '2px solid #e0e0e0',
            },
          }}
        />
      </Paper>
    </Box>
  );
}

export default LedgerView; 