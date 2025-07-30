# Raven Frontend

A modern React + Material-UI frontend for the Raven Intelligent Receipt Processing System.

## Features

### 🎯 Core Functionality
- **Email Processing**: Process incoming emails with PDF receipt attachments
- **Time Window Filtering**: Filter emails by date range for targeted processing
- **PDF Receipt Parsing**: Extract transaction data from receipt PDFs
- **Bank Statement Comparison**: Upload CSV bank statements and compare with ledger
- **Transaction Matching**: Clear visualization of matching, ledger-only, and bank-only transactions
- **Ledger Management**: Professional data grid view of all transactions

### 🎨 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Material-UI Components**: Professional, accessible, and beautiful interface
- **Real-time Updates**: Live data updates and processing status
- **Interactive Charts**: Pie charts and bar charts for data visualization
- **Data Grid**: Advanced table with sorting, filtering, and pagination
- **Loading States**: Smooth loading indicators and progress feedback
- **Error Handling**: Comprehensive error messages and recovery

### 📊 Dashboard Analytics
- **Transaction Statistics**: Total transactions, amounts, and averages
- **Category Breakdown**: Pie chart showing transaction categories
- **Recent Activity**: Bar chart of recent transactions
- **System Health**: Real-time system status monitoring

## Technology Stack

- **React 18**: Modern React with hooks and functional components
- **Material-UI 5**: Professional UI component library
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **Recharts**: Beautiful and composable charts
- **MUI X Data Grid**: Advanced data table component
- **Date-fns**: Modern date utility library

## Getting Started

### Prerequisites
- Node.js 16+ and npm
- Backend API running on port 5000

### Installation

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**:
   ```bash
   npm start
   ```

3. **Build for production**:
   ```bash
   npm run build
   ```

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:5000
```

## Application Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable UI components
│   │   └── Layout.js      # Main layout with navigation
│   ├── pages/             # Page components
│   │   ├── Dashboard.js   # Main dashboard with charts
│   │   ├── EmailProcessing.js  # Email processing interface
│   │   ├── BankComparison.js   # Bank statement comparison
│   │   └── LedgerView.js  # Transaction ledger view
│   ├── services/          # API service layer
│   │   └── api.js         # HTTP client and API calls
│   ├── App.js             # Main app component
│   └── index.js           # React entry point
└── package.json
```

## Pages Overview

### 🏠 Dashboard
- **Overview Cards**: Key metrics and system status
- **Transaction Charts**: Pie chart for categories, bar chart for recent activity
- **Real-time Stats**: Live updates of transaction counts and amounts
- **System Health**: API connectivity and service status

### 📧 Email Processing
- **Time Window Selection**: Date pickers for filtering email processing
- **Processing Controls**: Start/stop processing with real-time feedback
- **Results Display**: Detailed list of processed receipts
- **Status Indicators**: Success/error states with clear messaging

### 🏦 Bank Comparison
- **File Upload**: Drag-and-drop CSV file upload
- **Comparison Results**: Summary cards showing match statistics
- **Detailed Tables**: Expandable sections for each transaction type
- **Visual Indicators**: Color-coded chips for different transaction states

### 📋 Ledger View
- **Data Grid**: Advanced table with sorting and pagination
- **Transaction Details**: Complete transaction information
- **Statistics Cards**: Summary metrics for the ledger
- **Export Ready**: Data formatted for easy export

## API Integration

The frontend communicates with the backend through RESTful APIs:

### Email Processing
```javascript
POST /api/process-emails
{
  "start_date": "2024-01-01",  // Optional
  "end_date": "2024-01-31"     // Optional
}
```

### Bank Statement Upload
```javascript
POST /api/upload-bank-statement
Content-Type: multipart/form-data
file: CSV file
```

### Ledger Data
```javascript
GET /api/ledger
```

### Health Check
```javascript
GET /api/health
```

## Development

### Code Style
- ESLint configuration for consistent code style
- Prettier for automatic code formatting
- Material-UI best practices for component design

### State Management
- React hooks for local state management
- Context API for global state (if needed)
- Axios interceptors for error handling

### Performance
- Lazy loading for route-based code splitting
- Memoization for expensive calculations
- Optimized re-renders with React.memo

## Deployment

### Production Build
```bash
npm run build
```

### Static Hosting
The build output can be deployed to any static hosting service:
- Netlify
- Vercel
- AWS S3
- GitHub Pages

### Docker Deployment
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## Contributing

1. Follow the existing code style and patterns
2. Add appropriate error handling and loading states
3. Test on different screen sizes for responsiveness
4. Update documentation for new features

## Troubleshooting

### Common Issues

**API Connection Errors**
- Ensure backend is running on port 5000
- Check CORS configuration in backend
- Verify API endpoints are accessible

**Build Errors**
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check for version conflicts in package.json
- Ensure all dependencies are compatible

**Performance Issues**
- Use React DevTools to identify unnecessary re-renders
- Implement React.memo for expensive components
- Consider code splitting for large components

## License

This project is part of the Raven Intelligent Receipt Processing System. 