import React from 'react';
import { Button } from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledButton = styled(Button)(({ theme, variant = 'contained' }) => ({
  position: 'relative',
  overflow: 'hidden',
  textTransform: 'none',
  fontWeight: 600,
  borderRadius: 12,
  padding: '12px 32px',
  fontSize: '1rem',
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: '-100%',
    width: '100%',
    height: '100%',
    background: 'linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent)',
    transition: 'left 0.5s ease',
  },
  
  '&:hover::before': {
    left: '100%',
  },
  
  ...(variant === 'contained' && {
    background: 'linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%)',
    color: '#ffffff',
    fontWeight: 600,
    boxShadow: '0 4px 12px rgb(124 58 237 / 0.3)',
    
    '&:hover': {
      background: 'linear-gradient(135deg, #6d28d9 0%, #7c3aed 100%)',
      transform: 'translateY(-2px)',
      boxShadow: '0 8px 20px rgb(124 58 237 / 0.4)',
    },
    
    '&:active': {
      transform: 'translateY(0)',
    },
  }),
  
  ...(variant === 'outlined' && {
    border: '2px solid #7c3aed',
    color: '#7c3aed',
    background: 'transparent',
    fontWeight: 600,
    
    '&:hover': {
      background: 'linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%)',
      color: '#ffffff',
      borderColor: '#7c3aed',
      transform: 'translateY(-2px)',
      boxShadow: '0 8px 20px rgb(124 58 237 / 0.3)',
    },
  }),
  
  '&:disabled': {
    opacity: 0.6,
    transform: 'none',
    boxShadow: 'none',
    color: '#6b7280',
    background: '#f3f4f6',
    borderColor: '#d1d5db',
  },
}));

const GradientButton = ({ children, variant = 'contained', ...props }) => {
  return (
    <StyledButton variant={variant} {...props}>
      {children}
    </StyledButton>
  );
};

export default GradientButton; 