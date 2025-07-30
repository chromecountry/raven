import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Grid,
  Paper,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  CircularProgress,
  Alert,
  Chip,
  Divider,
} from '@mui/material';
import GradientButton from '../components/GradientButton';
import {
  Email as EmailIcon,
  Receipt as ReceiptIcon,
  CalendarToday as CalendarIcon,
  CheckCircle as CheckIcon,
} from '@mui/icons-material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { emailService } from '../services/api';

function EmailProcessing() {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);

  const handleProcessEmails = async () => {
    try {
      setProcessing(true);
      setError(null);
      
      const response = await emailService.processEmails(
        startDate ? startDate.toISOString().split('T')[0] : null,
        endDate ? endDate.toISOString().split('T')[0] : null
      );
      
      setResults(response);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to process emails');
      console.error('Email processing error:', err);
    } finally {
      setProcessing(false);
    }
  };

  const getTimeWindowText = () => {
    if (!startDate && !endDate) return 'All unread emails';
    if (startDate && endDate) return `${startDate.toLocaleDateString()} - ${endDate.toLocaleDateString()}`;
    if (startDate) return `From ${startDate.toLocaleDateString()}`;
    if (endDate) return `Until ${endDate.toLocaleDateString()}`;
    return 'All unread emails';
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Email Processing
      </Typography>
      
      <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
        Process incoming emails and extract receipt data from PDF attachments
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Processing Configuration
          </Typography>
          
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={4}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DatePicker
                  label="Start Date (Optional)"
                  value={startDate}
                  onChange={setStartDate}
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </LocalizationProvider>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DatePicker
                  label="End Date (Optional)"
                  value={endDate}
                  onChange={setEndDate}
                  renderInput={(params) => <TextField {...params} fullWidth />}
                />
              </LocalizationProvider>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <GradientButton
                variant="contained"
                size="large"
                onClick={handleProcessEmails}
                disabled={processing}
                startIcon={processing ? <CircularProgress size={20} /> : <EmailIcon />}
                fullWidth
              >
                {processing ? 'Processing...' : 'Process Emails'}
              </GradientButton>
            </Grid>
          </Grid>
          
          <Box sx={{ mt: 2 }}>
            <Chip
              icon={<CalendarIcon />}
              label={getTimeWindowText()}
              color="primary"
              variant="outlined"
            />
          </Box>
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {results && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Processing Results
          </Typography>
          
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={4}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Processed Receipts
                  </Typography>
                  <Typography variant="h4" color="primary">
                    {results.processed_count}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} sm={4}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Time Window
                  </Typography>
                  <Typography variant="body2">
                    {results.time_window.start_date || 'All'} - {results.time_window.end_date || 'All'}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} sm={4}>
              <Card>
                <CardContent>
                  <Typography color="textSecondary" gutterBottom>
                    Status
                  </Typography>
                  <Chip
                    icon={<CheckIcon />}
                    label="Success"
                    color="success"
                    size="small"
                  />
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {results.results && results.results.length > 0 && (
            <>
              <Typography variant="h6" gutterBottom>
                Processed Receipts
              </Typography>
              
              <List>
                {results.results.map((receipt, index) => (
                  <React.Fragment key={index}>
                    <ListItem>
                      <ListItemIcon>
                        <ReceiptIcon color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary={receipt.merchant}
                        secondary={`${receipt.filename} - ${receipt.date}`}
                      />
                      <Typography variant="h6" color="primary">
                        ${receipt.amount}
                      </Typography>
                    </ListItem>
                    {index < results.results.length - 1 && <Divider />}
                  </React.Fragment>
                ))}
              </List>
            </>
          )}
        </Paper>
      )}
    </Box>
  );
}

export default EmailProcessing; 