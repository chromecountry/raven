#!/usr/bin/env python3

"""
API endpoints for receipt processing system
"""

import os
import sys
import logging
from datetime import datetime
from pathlib import Path
from functools import wraps
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.processors.email_processor import EmailProcessor  # noqa: E402
from src.processors.pdf_parser import ReceiptParser  # noqa: E402
from src.processors.ledger_manager import LedgerManager  # noqa: E402
from src.processors.bank_processor import BankProcessor  # noqa: E402

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Configure session for cross-origin requests
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS required for cross-origin
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Required for cross-origin
app.config['SESSION_COOKIE_DOMAIN'] = None
app.config['SESSION_COOKIE_PATH'] = '/'

# Configure CORS with specific origins
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS(app, origins=allowed_origins, supports_credentials=True)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Ensure upload directory exists
UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)

# File upload configuration
ALLOWED_EXTENSIONS = {'csv'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Simple user credentials (in production, use proper user management)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')

# Check if credentials are configured
if not ADMIN_USERNAME or not ADMIN_PASSWORD:
    logger.warning("ADMIN_USERNAME and ADMIN_PASSWORD must be set as environment variables")
    logger.warning("Using default credentials for development only")
    ADMIN_USERNAME = ADMIN_USERNAME or 'admin'
    ADMIN_PASSWORD = ADMIN_PASSWORD or 'password123'


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Debug session state
        logger.info(f"Session data: {dict(session)}")
        logger.info(f"Authenticated: {session.get('authenticated')}")
        
        if not session.get('authenticated'):
            logger.warning("Authentication failed - session not authenticated")
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/test-session')
def test_session():
    """Test endpoint to check session state"""
    logger.info(f"Test session - Session data: {dict(session)}")
    return jsonify({
        'session_data': dict(session),
        'authenticated': session.get('authenticated', False),
        'username': session.get('username')
    })


@app.route('/api/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    """Login endpoint"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Debug output
        logger.info(f"Login attempt - Username: {username}")
        logger.info(f"Expected username: {ADMIN_USERNAME}")
        logger.info(f"Password match: {password == ADMIN_PASSWORD}")
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['authenticated'] = True
            session['username'] = username
            
            # Debug session after setting
            logger.info(f"Session set - authenticated: {session.get('authenticated')}")
            logger.info(f"Session data: {dict(session)}")
            
            return jsonify({
                'success': True,
                'message': 'Login successful'
            })
        else:
            logger.warning("Login failed - invalid credentials")
            return jsonify({
                'success': False,
                'error': 'Invalid credentials'
            }), 401
    except Exception as e:
        logger.error(f"Login error: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout endpoint"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logout successful'
    })


@app.route('/api/auth-status')
def auth_status():
    """Check authentication status"""
    return jsonify({
        'authenticated': session.get('authenticated', False),
        'username': session.get('username')
    })


@app.route('/api/debug-env')
def debug_env():
    """Debug endpoint to check environment variables (remove in production)"""
    return jsonify({
        'admin_username_set': bool(ADMIN_USERNAME),
        'admin_password_set': bool(ADMIN_PASSWORD),
        'admin_username_length': len(ADMIN_USERNAME) if ADMIN_USERNAME else 0,
        'admin_password_length': len(ADMIN_PASSWORD) if ADMIN_PASSWORD else 0,
        'secret_key_set': bool(os.environ.get('SECRET_KEY')),
        'allowed_origins': allowed_origins
    })


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/process-emails', methods=['POST'])
@require_auth
@limiter.limit("10 per hour")
def process_emails():
    """Process emails endpoint with optional time window"""
    try:
        # Parse optional date parameters
        start_date_str = None
        end_date_str = None
        if request.is_json:
            start_date_str = request.json.get('start_date')
            end_date_str = request.json.get('end_date')

        start_date = None
        end_date = None

        if start_date_str:
            try:
                start_date = datetime.strptime(
                    start_date_str, '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid start_date format. Use YYYY-MM-DD'
                }), 400

        if end_date_str:
            try:
                end_date = datetime.strptime(
                    end_date_str, '%Y-%m-%d'
                ).date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid end_date format. Use YYYY-MM-DD'
                }), 400

        email_processor = EmailProcessor()
        receipt_parser = ReceiptParser()
        ledger_manager = LedgerManager()

        attachments = email_processor.fetch_pdf_attachments(
            start_date=start_date,
            end_date=end_date
        )
        processed_count = 0
        results = []

        for filename, file_path in attachments:
            receipt_data = receipt_parser.parse_receipt(file_path)
            if receipt_data.get('amount'):
                ledger_manager.add_transaction(receipt_data)
                processed_count += 1
                results.append({
                    'filename': filename,
                    'merchant': receipt_data.get('merchant', 'Unknown'),
                    'amount': receipt_data.get('amount', 'Unknown'),
                    'date': receipt_data.get('date', 'Unknown')
                })

        email_processor.close()

        return jsonify({
            'success': True,
            'processed_count': processed_count,
            'results': results,
            'time_window': {
                'start_date': start_date_str,
                'end_date': end_date_str
            }
        })

    except Exception as e:
        logger.error(f"Error processing emails: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/upload-bank-statement', methods=['POST'])
@require_auth
@limiter.limit("20 per hour")
def upload_bank_statement():
    """Upload and compare bank statement"""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        # Security checks
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Only CSV files allowed'
            }), 400

        # Check file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > MAX_FILE_SIZE:
            return jsonify({
                'success': False,
                'error': 'File too large. Maximum 10MB allowed'
            }), 400

        # Secure filename
        filename = secure_filename(file.filename)
        file_path = UPLOAD_FOLDER / filename
        
        # Save file
        file.save(file_path)
        
        # Process file
        bank_processor = BankProcessor(LedgerManager())
        bank_transactions = bank_processor.parse_csv(str(file_path))
        comparison = bank_processor.compare_transactions(bank_transactions)
        
        # Clean up uploaded file
        file_path.unlink(missing_ok=True)
        
        return jsonify({
            'success': True,
            'comparison': {
                'matches': len(comparison['matches']),
                'ledger_only': len(comparison['ledger_only']),
                'bank_only': len(comparison['bank_only']),
                'details': comparison
            }
        })

    except Exception as e:
        logger.error(f"Error uploading bank statement: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/ledger')
@require_auth
@limiter.limit("100 per hour")
def view_ledger():
    """Get ledger transactions"""
    try:
        ledger_manager = LedgerManager()
        transactions = ledger_manager.get_transactions()
        
        return jsonify({
            'success': True,
            'transactions': transactions
        })
    except Exception as e:
        logger.error(f"Error viewing ledger: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 