# Raven #

***
***

## Preamble ##

This document makes the following assumptions:

  - developers have a working knowledge of:
  - Email processing and IMAP protocols
  - PDF parsing and OCR techniques
  - Double-entry bookkeeping principles
  - React and modern web development
  - RESTful API design and consumption

  - developers have a thorough knowledge of:
  - Python, Beancount, Fava, Pandas
  - Linux, bash
  - Web development (HTML, CSS, JavaScript)
  - Node.js, npm, and modern frontend tooling

## Introduction ##

Raven is a comprehensive, enterprise-grade receipt processing system that:

1. automatically processes email receipts by:
        1. Fetching emails with PDF attachments using IMAP
        1. Extracting transaction data using OCR and text parsing
        1. Storing transactions in Beancount format
        1. Providing real-time processing status and feedback

1. provides the following functionalities:
        1. Email receipt processing and parsing with time window filtering
        1. Bank statement comparison and reconciliation
        1. Modern React + Material-UI web interface
        1. Professional dashboard with analytics and charts
        1. Advanced ledger management with data grids
        1. Command-line tools for automation

These functionalities are served by a modular Python backend with a modern React frontend. Processing logic for different receipt types lives within the `src/processors/` directory.

## Configuration ##

### Environment Variables ###

### Environment Setup ###

The system supports multiple environments (dev, stg, prd). To configure an environment:

```bash
./tools/config.sh <environment>
```

For development, the environment type needs to be configured like so:

```bash
export PROJECT_ENV_TYPE='dev';
```

Otherwise if no `PROJECT_ENV_TYPE` is set, the environment will default to `prd`.

### Credentials ###

### Email Configuration ###

Obtain email credentials and configure the following settings:
   - IMAP server settings (Gmail, Outlook, etc.)
   - App password for secure authentication

The credentials must be added to `src/core/credentials.py` in order for the email
processing to work properly.

For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password instead of your regular password

### Frontend Configuration ###

The React frontend requires Node.js 16+ and npm. Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:5000
```

### Installation ###

#### Backend Dependencies

Ensure that Python 3.8 or greater is available in the environment. Also, if
virtual environments are in use, ensure that the correct one is active.

To install the required packages, do:

```bash
pip install -r cfg/<env>/requirements.txt
```

Additionally, install Tesseract OCR for PDF text extraction:

```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract
```

#### Frontend Dependencies

Install frontend dependencies:

```bash
cd frontend
npm install
```

## Workflow #

## Execution ##

### Running the main application ###

The Raven application provides both CLI and web interfaces. To run it, do:

```bash
# Start the complete application (backend + frontend)
./start.sh

# Process emails and launch web interface
./app.sh

# Process emails only
./app.sh process-emails

# Launch web interface only
./app.sh launch-fava

# Compare bank statement
./app.sh compare-bank data/sample_data/sample_bank_statement.csv

# Run comprehensive demo
./demo.sh
```

This will run the application in the configured environment.

### Frontend Development ###

For frontend development:

```bash
cd frontend
npm start
```

The frontend will be available at `http://localhost:3000`.

### Sending a bank statement for comparison ###

From another location, such as another terminal window, run a command of the structure:

```bash
python src/ui/bank_comparison.py <csv_file>
```

### Bank Statement Structure ###

The schema for bank statement CSV files is defined within the `src/processors/bank_processor.py`.

Sample CSV files are provided in the `data/sample_data/` directory.

### Sample Bank Statement CSV ###

```csv
Date,Description,Amount,Type
2024-01-15,WALMART SUPERCENTER,45.67,DEBIT
2024-01-16,STARBUCKS COFFEE,4.50,DEBIT
2024-01-17,AMAZON.COM,23.99,DEBIT
2024-01-18,SHELL GAS STATION,35.20,DEBIT
2024-01-19,NETFLIX SUBSCRIPTION,15.99,DEBIT
```

### Sample Comparison Output ###

```bash
Comparison Results:
  Matches: 3
  Ledger only: 2
  Bank only: 1

Matching transactions:
  2024-01-15 | WALMART SUPERCENTER | $45.67
  2024-01-16 | STARBUCKS COFFEE | $4.50
  2024-01-17 | AMAZON.COM | $23.99

Ledger-only transactions:
  2024-01-20 | LOCAL COFFEE SHOP | $15.99
  2024-01-21 | HARDWARE STORE | $89.15

Bank-only transactions:
  2024-01-18 | SHELL GAS STATION | $35.20
```

## Project Structure ##

```
raven/
├── app.sh                    # Main application launcher
├── start.sh                  # Complete application starter
├── demo.sh                   # Comprehensive demo runner
├── cfg/                      # Configuration files
│   ├── dev/                  # Development environment
│   │   └── requirements.txt
│   ├── stg/                  # Staging environment
│   │   └── requirements.txt
│   └── prd/                  # Production environment
│       ├── requirements.txt
│       └── env_example.txt
├── frontend/                 # React + Material-UI frontend
│   ├── public/              # Static assets
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API service layer
│   │   ├── App.js          # Main app component
│   │   └── index.js        # React entry point
│   └── package.json
├── src/                      # Backend source code
│   ├── core/                 # Core configuration and ledger
│   │   ├── config.py
│   │   ├── credentials.py    # Actual credentials (gitignored)
│   │   ├── credentials.py.skel # Credentials template
│   │   └── ledger.py
│   ├── processors/           # Data processing modules
│   │   ├── email_processor.py
│   │   ├── pdf_parser.py
│   │   ├── bank_processor.py
│   │   └── ledger_manager.py
│   ├── ui/                   # Legacy UI modules
│   │   ├── main.py
│   │   └── bank_comparison.py
│   └── utils/                # Utility functions
├── data/                     # Data directory
│   ├── ledger/               # Beancount ledger files
│   ├── attachments/          # Downloaded PDF attachments
│   ├── exports/              # Exported data
│   └── sample_data/          # Sample data for testing
│       ├── sample_bank_statement.csv
│       ├── alternative_bank_statement.csv
│       └── receipts/         # Sample PDF receipts
├── tests/                    # Test suite
│   ├── unit/                 # Unit tests
│   └── integration/          # Integration tests
├── docs/                     # Documentation
│   ├── api/                  # API documentation
│   └── user/                 # User documentation
├── scripts/                  # Utility scripts
├── tools/                    # Development tools
├── logs/                     # Application logs
└── README.md
```

## Features ##

### Email Processing ###
- Connects to IMAP email server
- Searches for unread emails with PDF attachments
- Downloads and processes receipt PDFs
- Extracts transaction data using OCR and text parsing
- Time window filtering for targeted processing
- Real-time processing status and feedback

### PDF Parsing ###
- Uses `pdfplumber` for text extraction
- Falls back to OCR for scanned receipts
- Extracts amount, date, and merchant information
- Handles various receipt formats
- Advanced OCR with OpenCV + Tesseract

### Transaction Comparison ###
- Normalizes transaction formats for comparison
- Matches transactions by amount and date
- Shows matching, ledger-only, and bank-only transactions
- Command-line output for easy review
- Drag-and-drop CSV upload interface
- Visual indicators for different transaction states

### Modern Web Interface ###
- React 18 with Material-UI 5 components
- Professional dashboard with analytics
- Interactive charts (pie charts, bar charts)
- Advanced data grid with sorting and filtering
- Real-time updates and status monitoring
- Responsive design for all devices
- Drag-and-drop file uploads
- Loading states and error handling

### Dashboard Analytics ###
- Transaction statistics and trends
- Category breakdown with pie charts
- Recent activity visualization
- System health monitoring
- Real-time data updates
- Export capabilities

### Ledger Management ###
- Professional data grid interface
- Complete transaction information
- Sorting, filtering, and pagination
- Statistical overview and metrics
- Export functionality for reports
- Mobile-responsive design

### API Integration ###
- RESTful API endpoints
- CORS support for frontend-backend communication
- Comprehensive error handling
- Health check endpoints
- Secure credential management

## Development ##

### Running Tests ###

```bash
# Run integration tests
python tests/integration/test_system.py

# Generate sample data
python scripts/generate_sample_pdfs.py

# Test bank statement comparison
python src/ui/bank_comparison.py data/sample_data/sample_bank_statement.csv
```

### Frontend Development ###

```bash
cd frontend
npm start          # Development server
npm run build     # Production build
npm test          # Run tests
```

### Sample Data ###

Generate sample PDF receipts for testing:

```bash
python scripts/generate_sample_pdfs.py
```

This creates 14 sample PDF receipts in `data/sample_data/receipts/` with realistic merchant names and amounts.

### Project Structure Benefits ###

- **Environment Separation**: Different configs for dev/stg/prd
- **Credential Security**: Sensitive data separated from code
- **Modular Design**: Clear separation of concerns
- **Testing Support**: Dedicated test structure
- **Documentation**: Organized docs structure
- **Modern Frontend**: React + Material-UI for professional UX
- **Scalable Architecture**: Ready for production deployment

## Technology Stack ##

### Backend (Python + Flask)
- **Flask**: Lightweight web framework with RESTful API
- **Beancount**: Double-entry bookkeeping system
- **IMAPClient**: Email processing and attachment handling
- **PDFPlumber**: PDF text extraction and parsing
- **Pandas**: Data processing and CSV handling
- **OpenCV + Tesseract**: OCR for scanned receipt processing

### Frontend (React + Material-UI)
- **React 18**: Modern React with hooks and functional components
- **Material-UI 5**: Professional UI component library
- **React Router**: Client-side routing
- **Axios**: HTTP client for API communication
- **Recharts**: Beautiful and interactive data visualization
- **MUI X Data Grid**: Advanced table component
- **Date-fns**: Modern date utility library

### Infrastructure
- **CORS Support**: Cross-origin resource sharing
- **Environment Configuration**: Multi-environment support
- **Error Handling**: Comprehensive error management
- **Security**: Secure credential management

## Security Notes ##

- Store email credentials securely in `src/core/credentials.py`
- Use App Passwords for Gmail
- Keep PDF attachments in secure location
- Regularly backup Beancount ledger file
- `credentials.py` is gitignored to prevent accidental commits
- Implement proper CORS configuration for production
- Use environment variables for sensitive configuration

## Future Enhancements ##

- Machine learning for better receipt parsing
- Support for more receipt formats
- Automatic categorization of transactions
- Integration with more bank APIs
- Mobile app integration
- Real-time sync with WebSocket connections
- Advanced analytics and predictive spending analysis
- Multi-currency support
- Cloud deployment with auto-scaling
- Database integration (PostgreSQL/MySQL)
- OAuth2 authentication and role-based access
- API versioning for backward compatibility