import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  CircularProgress,
  Alert,
  Chip,
  Divider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from '@mui/material';
import GradientButton from '../components/GradientButton';
import {
  CloudUpload as UploadIcon,
  AccountBalance as BankIcon,
  Receipt as ReceiptIcon,
  CheckCircle as MatchIcon,
  ExpandMore as ExpandIcon,
} from '@mui/icons-material';
import { bankService } from '../services/api';

function BankComparison() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [comparison, setComparison] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    if (selectedFile && selectedFile.type === 'text/csv') {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please select a valid CSV file');
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file first');
      return;
    }

    try {
      setUploading(true);
      setError(null);
      
      const response = await bankService.uploadStatement(file);
      setComparison(response.comparison);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload and compare bank statement');
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  const getComparisonSummary = () => {
    if (!comparison) return null;
    
    return [
      {
        title: 'Matching Transactions',
        count: comparison.matches,
        color: 'success',
        icon: <MatchIcon />,
      },
      {
        title: 'Ledger Only',
        count: comparison.ledger_only,
        color: 'warning',
        icon: <ReceiptIcon />,
      },
      {
        title: 'Bank Only',
        count: comparison.bank_only,
        color: 'info',
        icon: <BankIcon />,
      },
    ];
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Bank Statement Comparison
      </Typography>
      
      <Typography variant="body1" color="textSecondary" sx={{ mb: 3 }}>
        Upload a bank statement CSV and compare it with your ledger transactions
      </Typography>

      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Upload Bank Statement
          </Typography>
          
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={6}>
              <GradientButton
                variant="outlined"
                component="label"
                startIcon={<UploadIcon />}
                fullWidth
                sx={{ height: 56 }}
              >
                {file ? file.name : 'Choose CSV File'}
                <input
                  type="file"
                  hidden
                  accept=".csv"
                  onChange={handleFileChange}
                />
              </GradientButton>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <GradientButton
                variant="contained"
                size="large"
                onClick={handleUpload}
                disabled={!file || uploading}
                startIcon={uploading ? <CircularProgress size={20} /> : <BankIcon />}
                fullWidth
                sx={{ height: 56 }}
              >
                {uploading ? 'Processing...' : 'Compare Transactions'}
              </GradientButton>
            </Grid>
          </Grid>
          
          {file && (
            <Box sx={{ mt: 2 }}>
              <Chip
                icon={<BankIcon />}
                label={`Selected: ${file.name}`}
                color="primary"
                variant="outlined"
              />
            </Box>
          )}
        </CardContent>
      </Card>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {comparison && (
        <Paper sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Comparison Results
          </Typography>
          
          <Grid container spacing={2} sx={{ mb: 3 }}>
            {getComparisonSummary().map((item, index) => (
              <Grid item xs={12} sm={4} key={index}>
                <Card>
                  <CardContent>
                    <Box display="flex" alignItems="center" sx={{ mb: 1 }}>
                      {item.icon}
                      <Typography variant="h6" sx={{ ml: 1 }}>
                        {item.title}
                      </Typography>
                    </Box>
                    <Typography variant="h4" color={`${item.color}.main`}>
                      {item.count}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          <Divider sx={{ my: 3 }} />

          {/* Detailed Results */}
          <Box>
            <Accordion defaultExpanded>
              <AccordionSummary expandIcon={<ExpandIcon />}>
                <Typography variant="h6">
                  Matching Transactions ({comparison.matches})
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>Description</TableCell>
                        <TableCell>Amount</TableCell>
                        <TableCell>Status</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {comparison.details.matches.map((match, index) => (
                        <TableRow key={index}>
                          <TableCell>{match.bank.date}</TableCell>
                          <TableCell>{match.bank.description}</TableCell>
                          <TableCell>${match.bank.amount}</TableCell>
                          <TableCell>
                            <Chip
                              icon={<MatchIcon />}
                              label="Match"
                              color="success"
                              size="small"
                            />
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </AccordionDetails>
            </Accordion>

            <Accordion>
              <AccordionSummary expandIcon={<ExpandIcon />}>
                <Typography variant="h6">
                  Ledger Only Transactions ({comparison.ledger_only})
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>Description</TableCell>
                        <TableCell>Amount</TableCell>
                        <TableCell>Status</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {comparison.details.ledger_only.map((tx, index) => (
                        <TableRow key={index}>
                          <TableCell>{tx.date}</TableCell>
                          <TableCell>{tx.description}</TableCell>
                          <TableCell>${tx.amount}</TableCell>
                          <TableCell>
                            <Chip
                              icon={<ReceiptIcon />}
                              label="Ledger Only"
                              color="warning"
                              size="small"
                            />
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </AccordionDetails>
            </Accordion>

            <Accordion>
              <AccordionSummary expandIcon={<ExpandIcon />}>
                <Typography variant="h6">
                  Bank Only Transactions ({comparison.bank_only})
                </Typography>
              </AccordionSummary>
              <AccordionDetails>
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Date</TableCell>
                        <TableCell>Description</TableCell>
                        <TableCell>Amount</TableCell>
                        <TableCell>Status</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {comparison.details.bank_only.map((tx, index) => (
                        <TableRow key={index}>
                          <TableCell>{tx.date}</TableCell>
                          <TableCell>{tx.description}</TableCell>
                          <TableCell>${tx.amount}</TableCell>
                          <TableCell>
                            <Chip
                              icon={<BankIcon />}
                              label="Bank Only"
                              color="info"
                              size="small"
                            />
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </AccordionDetails>
            </Accordion>
          </Box>
        </Paper>
      )}
    </Box>
  );
}

export default BankComparison; 