#!/usr/bin/env python3

"""
Main script for receipt processing system with Fava integration
"""

import sys
import subprocess
from datetime import datetime
from src.processors.email_processor import EmailProcessor
from src.processors.pdf_parser import ReceiptParser
from src.processors.ledger_manager import LedgerManager
from src.core.config import FAVA_HOST, FAVA_PORT, BEANCOUNT_FILE


def process_emails(start_date: str = None, end_date: str = None) -> int:
    """Process emails and extract receipts with optional time window"""
    try:
        email_processor = EmailProcessor()
        receipt_parser = ReceiptParser()
        ledger_manager = LedgerManager()

        # Parse date parameters
        start_dt = None
        end_dt = None

        if start_date:
            try:
                start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
                print(f'Processing emails from {start_date}')
            except ValueError:
                print('Error: Invalid start_date format. Use YYYY-MM-DD')
                return 0

        if end_date:
            try:
                end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
                print(f'Processing emails until {end_date}')
            except ValueError:
                print('Error: Invalid end_date format. Use YYYY-MM-DD')
                return 0

        print('Fetching emails with PDF attachments...')
        attachments = email_processor.fetch_pdf_attachments(
            start_date=start_dt,
            end_date=end_dt
        )

        processed_count = 0
        for filename, file_path in attachments:
            print(f'Processing {filename}...')
            receipt_data = receipt_parser.parse_receipt(file_path)

            if receipt_data.get('amount'):
                ledger_manager.add_transaction(receipt_data)
                processed_count += 1
                merchant = receipt_data["merchant"]
                amount = receipt_data["amount"]
                print(f'Added transaction: {merchant} - ${amount}')
            else:
                print(f'Could not extract data from {filename}')

        email_processor.close()
        print(f'Processed {processed_count} receipts')
        return processed_count

    except Exception as e:
        print(f'Error processing emails: {e}')
        return 0


def launch_fava() -> None:
    """Launch Fava web interface"""
    if not BEANCOUNT_FILE.exists():
        print('No ledger file found. Creating empty ledger...')
        BEANCOUNT_FILE.parent.mkdir(exist_ok=True)
        BEANCOUNT_FILE.touch()

    print(f'Launching Fava on http://{FAVA_HOST}:{FAVA_PORT}')
    print(f'Ledger file: {BEANCOUNT_FILE}')
    print('Press Ctrl+C to stop')

    try:
        # Try default port first
        result = subprocess.run([
            'fava',
            '--host', FAVA_HOST,
            '--port', str(FAVA_PORT),
            str(BEANCOUNT_FILE)
        ], capture_output=True, text=True)

        if 'port 5000 is already in use' in result.stderr:
            # Try alternative port
            print('Port 5000 busy, trying port 5001...')
            subprocess.run([
                'fava',
                '--host', FAVA_HOST,
                '--port', '5001',
                str(BEANCOUNT_FILE)
            ])
        else:
            print(result.stdout)
            if result.stderr:
                print(result.stderr)

    except KeyboardInterrupt:
        print('\nShutting down...')
    except Exception as e:
        print(f'Error launching Fava: {e}')


def main() -> int:
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'process-emails':
            start_date = None
            end_date = None
            if len(sys.argv) > 2:
                start_date = sys.argv[2]
            if len(sys.argv) > 3:
                end_date = sys.argv[3]
            return process_emails(start_date=start_date, end_date=end_date)
        elif command == 'launch-fava':
            launch_fava()
            return 0
        elif command == 'help':
            print('Usage:')
            print('  python main.py process-emails [YYYY-MM-DD] [YYYY-MM-DD]')
            print('    # Process emails with optional date range')
            print('  python main.py launch-fava')
            print('    # Launch Fava')
            print('  python main.py')
            print('    # Process emails then launch Fava')
            return 0
        else:
            print(f'Unknown command: {command}')
            return 1

    # Default: process emails then launch Fava
    process_emails()
    launch_fava()
    return 0


if __name__ == '__main__':
    sys.exit(main())
