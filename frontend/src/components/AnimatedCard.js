import React from 'react';
import { Card, CardContent, Box } from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledCard = styled(Card)(({ theme }) => ({
  position: 'relative',
  overflow: 'hidden',
  background: 'linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)',
  border: '1px solid rgb(229 231 235)',
  borderRadius: 16,
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  cursor: 'pointer',
  
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '4px',
    background: 'linear-gradient(90deg, #7c3aed 0%, #8b5cf6 50%, #a855f7 100%)',
    transform: 'scaleX(0)',
    transition: 'transform 0.3s ease',
  },
  
  '&:hover': {
    transform: 'translateY(-8px)',
    boxShadow: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 10px 10px -5px rgb(0 0 0 / 0.04)',
    
    '&::before': {
      transform: 'scaleX(1)',
    },
  },
  
  '&:hover .card-icon': {
    transform: 'scale(1.1) rotate(5deg)',
  },
}));

const IconWrapper = styled(Box)(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  width: 64,
  height: 64,
  borderRadius: '50%',
  background: 'linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%)',
  marginBottom: theme.spacing(2),
  transition: 'all 0.3s ease',
  boxShadow: '0 4px 12px rgb(124 58 237 / 0.3)',
}));

const AnimatedCard = ({ icon, title, value, subtitle, color = 'primary', children, ...props }) => {
  return (
    <StyledCard {...props}>
      <CardContent sx={{ p: 3 }}>
        {icon && (
          <IconWrapper className="card-icon">
            {icon}
          </IconWrapper>
        )}
        {children}
      </CardContent>
    </StyledCard>
  );
};

export default AnimatedCard; 