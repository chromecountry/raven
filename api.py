#!/usr/bin/env python3

"""
API endpoints for receipt processing system
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.processors.email_processor import EmailProcessor  # noqa: E402
from src.processors.pdf_parser import ReceiptParser  # noqa: E402
from src.processors.ledger_manager import LedgerManager  # noqa: E402
from src.processors.bank_processor import BankProcessor  # noqa: E402

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Ensure upload directory exists
UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)


@app.route('/api/process-emails', methods=['POST'])
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
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/upload-bank-statement', methods=['POST'])
def upload_bank_statement():
    """Upload and compare bank statement"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = UPLOAD_FOLDER / filename
            file.save(str(filepath))

            # Process the CSV
            ledger_manager = LedgerManager()
            bank_processor = BankProcessor(ledger_manager)

            bank_transactions = bank_processor.parse_csv(str(filepath))
            comparison = bank_processor.compare_transactions(bank_transactions)

            return jsonify({
                'success': True,
                'comparison': {
                    'matches': len(comparison['matches']),
                    'ledger_only': len(comparison['ledger_only']),
                    'bank_only': len(comparison['bank_only']),
                    'details': {
                        'matches': comparison['matches'][:10],
                        'ledger_only': comparison['ledger_only'][:10],
                        'bank_only': comparison['bank_only'][:10]
                    }
                }
            })

        return jsonify({'success': False, 'error': 'Invalid file type'}), 400

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/ledger')
def view_ledger():
    """View ledger transactions"""
    try:
        ledger_manager = LedgerManager()
        transactions = ledger_manager.get_transactions()
        return jsonify({
            'success': True,
            'transactions': transactions
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})


# For Vercel deployment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 